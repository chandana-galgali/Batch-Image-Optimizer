/* No third-party libraries. All image bytes stay in this browser. */
const $ = id => document.getElementById(id);
let selected = [];
let processed = [];
const dropzone = $('dropzone');
const fileInput = $('fileInput');
const accept = files => {
  const allowed = ['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/bmp'];
  const incoming = Array.from(files).filter(file => allowed.includes(file.type));
  selected = selected.concat(incoming);
  processed = [];
  $('download').disabled = true;
  $('optimize').disabled = !selected.length;
  $('clear').disabled = !selected.length;
  $('summary').textContent = `${selected.length} image${selected.length === 1 ? '' : 's'} ready to optimize`;
  renderRows(selected.map(f => ({name:f.name, text:formatBytes(f.size)})));
};
dropzone.addEventListener('click', () => fileInput.click());
dropzone.addEventListener('keydown', event => {if (event.key === 'Enter' || event.key === ' ') {event.preventDefault();fileInput.click();}});
fileInput.addEventListener('change', event => {accept(event.target.files);fileInput.value='';});
for (const evt of ['dragenter','dragover']) dropzone.addEventListener(evt, e => {e.preventDefault();dropzone.classList.add('dragover');});
for (const evt of ['dragleave','drop']) dropzone.addEventListener(evt, e => {e.preventDefault();dropzone.classList.remove('dragover');});
dropzone.addEventListener('drop', e => accept(e.dataTransfer.files));
$('quality').addEventListener('input', () => $('qvalue').textContent = `${$('quality').value}%`);
$('format').addEventListener('change', () => $('quality').disabled = $('format').value === 'image/png');
$('clear').addEventListener('click', () => {selected=[];processed=[];renderRows([]);$('summary').textContent='Add images to get started.';$('optimize').disabled=$('clear').disabled=$('download').disabled=true;});
function formatBytes(bytes){return bytes>=1048576?`${(bytes/1048576).toFixed(2)} MB`:`${(bytes/1024).toFixed(1)} KB`;}
function renderRows(rows){const root=$('results');root.replaceChildren();for(const row of rows){const el=document.createElement('div');el.className='result';const name=document.createElement('span');name.className='file-name';name.textContent=row.name;const stats=document.createElement('span');stats.className=`stats ${row.error?'error':''}`;stats.textContent=row.text;el.append(name,stats);root.append(el);}}
function loadImage(file){return new Promise((resolve,reject)=>{const url=URL.createObjectURL(file);const img=new Image();img.onload=()=>{URL.revokeObjectURL(url);resolve(img);};img.onerror=()=>{URL.revokeObjectURL(url);reject(new Error('Cannot decode this image'));};img.src=url;});}
function canvasBlob(canvas,type,quality){return new Promise((resolve,reject)=>canvas.toBlob(blob=>blob?resolve(blob):reject(new Error('Browser cannot encode this format')),type,quality));}
async function convert(file,index,opts){const image=await loadImage(file);const scale=Math.min(1,opts.width/image.naturalWidth,opts.height/image.naturalHeight);const width=Math.max(1,Math.round(image.naturalWidth*scale));const height=Math.max(1,Math.round(image.naturalHeight*scale));const canvas=document.createElement('canvas');canvas.width=width;canvas.height=height;const ctx=canvas.getContext('2d');if(!ctx)throw new Error('Canvas not available');if(opts.type==='image/jpeg'){ctx.fillStyle='#ffffff';ctx.fillRect(0,0,width,height);}ctx.drawImage(image,0,0,width,height);const blob=await canvasBlob(canvas,opts.type,opts.quality);const ext={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}[opts.type];const safe=file.name.replace(/\.[^.]+$/,'').replace(/[^\w\-. ]/g,'_');return {name:`${safe}_${width}x${height}_${index+1}.${ext}`,blob,original:file.size};}
$('optimize').addEventListener('click',async()=>{const width=Number($('width').value),height=Number($('height').value);if(!Number.isSafeInteger(width)||!Number.isSafeInteger(height)||width<1||height<1||width>20000||height>20000){$('summary').textContent='Enter width and height from 1 to 20,000 pixels.';return;}const opts={width,height,type:$('format').value,quality:Number($('quality').value)/100};$('optimize').disabled=true;$('download').disabled=true;processed=[];const rows=[];for(let i=0;i<selected.length;i++){const file=selected[i];$('summary').textContent=`Optimizing ${i+1} of ${selected.length}…`;try{const item=await convert(file,i,opts);processed.push(item);const change=100*(1-item.blob.size/item.original);rows.push({name:item.name,text:`${formatBytes(item.original)} → ${formatBytes(item.blob.size)} · ${change.toFixed(1)}% smaller`});}catch(err){rows.push({name:file.name,text:err.message,error:true});}renderRows(rows);await new Promise(resolve=>setTimeout(resolve,0));}const before=processed.reduce((n,x)=>n+x.original,0),after=processed.reduce((n,x)=>n+x.blob.size,0);$('summary').textContent=`${processed.length}/${selected.length} completed · ${before?((1-after/before)*100).toFixed(1):0}% total size reduction`;$('download').disabled=!processed.length;$('optimize').disabled=false;});
/* Minimal uncompressed ZIP writer. PNG/JPEG/WebP already compressed; STORE avoids redundant work. */
const u16=n=>[n&255,n>>>8&255],u32=n=>[n&255,n>>>8&255,n>>>16&255,n>>>24&255];
const table=Array.from({length:256},(_,n)=>{for(let i=0;i<8;i++)n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0;});
function crc32(bytes){let crc=0xffffffff;for(const b of bytes)crc=table[(crc^b)&255]^(crc>>>8);return (crc^0xffffffff)>>>0;}
async function makeZip(items){const enc=new TextEncoder();const parts=[],central=[];let offset=0;for(const item of items){const data=new Uint8Array(await item.blob.arrayBuffer()),name=enc.encode(item.name),crc=crc32(data);const local=new Uint8Array([80,75,3,4,20,0,0,0,0,0,0,0,0,0,...u32(crc),...u32(data.length),...u32(data.length),...u16(name.length),0,0,...name]);parts.push(local,data);const cd=new Uint8Array([80,75,1,2,20,0,20,0,0,0,0,0,0,0,0,0,...u32(crc),...u32(data.length),...u32(data.length),...u16(name.length),0,0,0,0,0,0,0,0,0,0,0,0,...u32(offset),...name]);central.push(cd);offset+=local.length+data.length;}const centerSize=central.reduce((sum,x)=>sum+x.length,0);const footer=new Uint8Array([80,75,5,6,0,0,0,0,...u16(items.length),...u16(items.length),...u32(centerSize),...u32(offset),0,0]);return new Blob([...parts,...central,footer],{type:'application/zip'});}
$('download').addEventListener('click',async()=>{if(!processed.length)return;const button=$('download');button.disabled=true;button.textContent='Preparing ZIP…';try{const blob=await makeZip(processed);const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='pixelbatch-optimized.zip';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);}catch(err){$('summary').textContent=`ZIP creation failed: ${err.message}`;}finally{button.disabled=false;button.textContent='Download ZIP ↓';}});
