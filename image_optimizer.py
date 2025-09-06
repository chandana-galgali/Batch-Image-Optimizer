import argparse
from PIL import Image
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT_DIR = SCRIPT_DIR / 'images' / 'input'
OUTPUT_DIR = SCRIPT_DIR / 'images' / 'output'
DEFAULT_FORMAT = 'JPEG'

def optimize_image(source_path, max_width, max_height, quality):
    """
    Optimizes a single image by resizing it to fit a bounding box,
    then determines a descriptive filename and saves it.
    """
    try:
        with Image.open(source_path) as img:
            original_size = img.size
            
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            final_size = img.size
            
            if final_size == original_size:
                print(f"    - Image is already within bounds. No resize needed.")
            else:
                 print(f"    - Resized from {original_size[0]}x{original_size[1]} to {final_size[0]}x{final_size[1]}px")

            base_filename = f"{source_path.stem}_{final_size[0]}x{final_size[1]}"
            output_filename = f"{base_filename}.{DEFAULT_FORMAT.lower()}"
            output_path = OUTPUT_DIR / output_filename
            
            counter = 1
            while output_path.exists():
                output_filename = f"{base_filename}_{counter}.{DEFAULT_FORMAT.lower()}"
                output_path = OUTPUT_DIR / output_filename
                counter += 1
            
            if counter > 1:
                print(f"    - WARNING: File exists. Saving as '{output_path.name}' to avoid overwrite.")

            if DEFAULT_FORMAT.lower() == 'jpeg' and img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
                print(f"    - Converted to RGB for JPEG compatibility")

            print(f"    - Saving as '{output_path.name}' with quality {quality}%")
            img.save(output_path, format=DEFAULT_FORMAT, quality=quality, optimize=True)
            return True
    except Exception as e:
        print(f"    - ERROR: Could not process {source_path}. Reason: {e}")
        return False

def main():
    """
    Main function to parse arguments and process images.
    """
    parser = argparse.ArgumentParser(
        description="Batch compress and resize images to fit within a bounding box. Looks for images in './images/input' and saves them to './images/output'."
    )
    parser.add_argument(
        '--max-width',
        required=True,
        type=int,
        help="The maximum width for the output images in pixels."
    )
    parser.add_argument(
        '--max-height',
        required=True,
        type=int,
        help="The maximum height for the output images in pixels."
    )
    parser.add_argument(
        '--quality',
        type=int,
        default=75,
        help="Compression quality for the output JPEG images (1-100). Default is 75."
    )
    args = parser.parse_args()

    if not INPUT_DIR.is_dir():
        print(f"Error: Input directory '{INPUT_DIR}' not found. Please create it.")
        return
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("==========================================")
    print("      STARTING BATCH IMAGE OPTIMIZER      ")
    print("==========================================")
    print(f"Input Directory: {INPUT_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Bounding Box: {args.max_width}w x {args.max_height}h px")
    print(f"Output Quality: {args.quality}%")
    print("------------------------------------------")

    processed_count = 0
    error_count = 0
    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    for item in INPUT_DIR.iterdir():
        if item.is_file() and item.suffix.lower() in supported_extensions:
            print(f"Processing '{item.name}'...")
            
            if optimize_image(item, args.max_width, args.max_height, args.quality):
                processed_count += 1
            else:
                error_count += 1
    
    print("------------------------------------------")
    print("               PROCESS COMPLETE               ")
    print(f"Successfully processed: {processed_count} images")
    print("==========================================")

if __name__ == "__main__":
    main()