# Project overview

**PixelBatch: a privacy-first batch image optimizer.** Resize and compress entire image batches directly in the browser, or automate the same workflow with a Python CLI.

**Problem:** Optimizing images by hand is repetitive, and most web compressors require uploading your files to a server.

**Solution:** One tool with two interfaces: a browser-based drag-and-drop workspace and a scriptable command-line utility. Both process files locally.

**Engineering highlights:**
- Aspect-ratio-preserving bounding-box resize, with no upscaling
- EXIF orientation handling in the CLI
- Alpha-safe conversion when exporting transparent images to JPEG
- Non-destructive naming when output files would collide
- Per-file error isolation, so one bad image doesn't stop the batch
- Native Canvas encoding and an in-browser ZIP export
- Unit tests and CI on every push

**Pipeline:** file selection → decode → resize → encode → local export (download or ZIP).

**Design decision:** PixelBatch ships as a static website rather than a browser extension. A static site gives a live, zero-maintenance demo, while an extension would add permissions and distribution overhead without solving a clear additional need.

**GitHub topics:** `image-optimization`, `python`, `pillow`, `javascript`, `webp`, `batch-processing`, `privacy-first`.
