# Portfolio presentation

**Title:** PixelBatch — A Privacy-First Batch Image Optimizer

**One-line pitch:** Resize and compress entire image batches directly in your browser, or automate the same workflow with a Python CLI.

**Problem:** Optimizing images manually is repetitive, and web compressors often require uploading files.

**Solution:** A lightweight two-interface tool: a browser-first drag-and-drop workspace and a repeatable command-line utility.

**Engineering highlights:** Aspect-ratio-preserving bounding boxes; EXIF orientation handling in CLI; alpha-safe JPEG conversion; non-destructive conflict naming; batch error isolation; native Canvas conversion and ZIP export in-browser; unit tests and automated CI.

**Suggested portfolio cards:**
1. Screenshot of the browser workspace after processing 3 sample images.
2. Two-column "Browser vs CLI" section emphasizing a different usage situation for each.
3. Mini architecture: file selection → decode → resize → encode → local export.
4. A short screen recording of import → adjust → compress → ZIP download.

**Suggested repository description:** Privacy-first batch image optimizer with a responsive browser UI and Python CLI. Resize, convert, compress, and export locally.

**Suggested GitHub topics:** `image-optimization`, `python`, `pillow`, `javascript`, `webp`, `batch-processing`, `privacy-first`.

**Release strategy:** Static site first, not an extension. A live URL and screenshot provide a useful demo with almost zero maintenance. An extension would add permissions and distribution complexity without solving a clear additional need.
