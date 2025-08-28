import os
import argparse
from PIL import Image
from pathlib import Path

def optimize_image(source_path, output_path, format, quality, max_width):
    """
    Optimizes a single image by resizing, compressing, and converting it.
    """
    try:
        with Image.open(source_path) as img:

            if img.width > max_width:
                width_percent = (max_width / float(img.width))
                new_height = int((float(img.height) * float(width_percent)))
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"    - Resized to {max_width}px width")


            if format.lower() == 'jpeg' and img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
                print(f"    - Converted to RGB for JPEG compatibility")

            print(f"    - Saving as {format.upper()} with quality {quality}%")
            img.save(output_path, format=format, quality=quality, optimize=True)
            return True
    except Exception as e:
        print(f"    - ERROR: Could not process {source_path}. Reason: {e}")
        return False

def main():
    """
    Main function to parse arguments and process the images.
    """
    parser = argparse.ArgumentParser(description="Batch optimize images for web use.")
    parser.add_argument('--input', required=True, type=str, help="Directory containing original images.")
    parser.add_argument('--output', required=True, type=str, help="Directory to save optimized images.")
    parser.add_argument('--format', type=str, default='JPEG', choices=['JPEG', 'WEBP', 'PNG'], help="Output image format.")
    parser.add_argument('--quality', type=int, default=75, help="Compression quality (1-100).")
    parser.add_argument('--width', type=int, default=1920, help="Maximum width for resizing images.")

    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.is_dir():
        print(f"Error: Input directory '{input_dir}' not found.")
        return
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("==========================================")
    print("      STARTING BATCH IMAGE OPTIMIZER      ")
    print("==========================================")
    print(f"Input Directory: {input_dir}")
    print(f"Output Directory: {output_dir}")
    print(f"Target Format: {args.format.upper()}")
    print(f"Quality: {args.quality}%")
    print(f"Max Width: {args.width}px")
    print("------------------------------------------")

    processed_count = 0
    error_count = 0
    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    for item in input_dir.iterdir():
        if item.is_file() and item.suffix.lower() in supported_extensions:
            print(f"Processing '{item.name}'...")
            output_filename = f"{item.stem}.{args.format.lower()}"
            output_path = output_dir / output_filename
            
            if optimize_image(item, output_path, args.format, args.quality, args.width):
                processed_count += 1
            else:
                error_count += 1
    
    print("------------------------------------------")
    print("               PROCESS COMPLETE               ")
    print(f"Successfully processed: {processed_count} images")
    print(f"Failed to process: {error_count} images")
    print("==========================================")

if __name__ == "__main__":
    main()