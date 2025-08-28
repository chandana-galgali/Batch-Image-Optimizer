## Batch-Image-Optimizer
A powerful and simple command-line utility to optimize a folder of images for web use. This tool can resize, compress, and convert images in bulk, making it perfect for preparing website assets, blog post images, or photo galleries.

# Features
- **Batch Processing**: Optimize an entire folder of images at once.
- **Resizing**: Set a maximum width to automatically resize large images while preserving the aspect ratio.
- **Compression**: Control the image quality to find the perfect balance between file size and visual fidelity.
- **Format Conversion**: Convert images to modern, web-friendly formats like JPEG, PNG, or WEBP.
- **Easy to Use**: Simple command-line interface that can be easily scripted or integrated into other workflows.

# Installation
1. Clone the repository:
```bash
git clone https://github.com/chandana-galgali/Batch-Image-Optimizer.git
cd Batch-Image-Optimizer
```

2. Install dependencies:
It's recommended to use a virtual environment.
```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the required library
pip install -r requirements.txt
```

# Usage
The script is run from the command line and accepts several arguments to control the optimization process.

**Basic Example**
To process a folder named originals and save the optimized images into a folder named optimized:
```bash
python image_optimizer.py --input originals --output optimized
```

**Advanced Example**
To process the same folders, but convert the images to WEBP format, set the quality to 85%, and resize them to a maximum width of 1024 pixels:
```bash
python image_optimizer.py --input originals --output optimized --format WEBP --quality 85 --width 1024
```
