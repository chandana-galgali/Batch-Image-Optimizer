## Batch-Image-Optimizer
A powerful and simple command-line utility to optimize a folder of images. This tool proportionally resizes images to fit within a bounding box, compresses them, and saves them with descriptive filenames based on their final dimensions.

# Features
- **Simplified Workflow**: Just drop your images into the _images/input_ folder and run the script.
- **Bounding Box Resizing**: Shrinks large images to fit within a maximum width AND maximum height, perfectly preserving the original aspect ratio without cropping.
- **Descriptive Filenames**: Automatically renames output files to include their final dimensions (e.g., __photo_1280x720.jpeg__).
- **Conflict Handling**: Prevents overwriting files by automatically adding a number to the filename if it already exists (e.g., __photo_1280x720_1.jpeg__).
- **Quality Control**: Adjust the JPEG compression quality to balance file size and visual fidelity.

# Installation
1. Clone the repository:
```bash
git clone https://github.com/chandana-galgali/Batch-Image-Optimizer.git
cd Batch-Image-Optimizer
```

2. Create the necessary folders:
The script expects a specific folder structure. This command creates the _images_ folder and the _input_ sub-folder.
```bash
mkdir -p images/input
```

3. Install dependencies:
It's recommended to use a virtual environment.
```bash
# Create and activate a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the required library
pip install -r requirements.txt
```

# Usage
The script is run from the command line. It automatically uses the _./images/input_ folder and saves results to _./images/output_, so you only need to provide the dimensions and quality.

**Basic Example**
To process all images to fit within a 1920x1080 bounding box using the default 75% quality:
```bash
python image_optimizer.py --max-width 1920 --max-height 1080
```

**Advanced Example**
To process all images to fit within a 1000x1000 bounding box and set the compression quality to a higher 85%:
```bash
python image_optimizer.py --max-width 1000 --max-height 1000 --quality 85
```
