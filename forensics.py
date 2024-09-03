import os
from PIL import Image
import exifread

def load_image(image_path):
    try:
        img = Image.open(image_path)
        img.verify()  # Verify that this is an image
        return img
    except Exception as e:
        print(f"Failed to load image: {e}")
        return None

def extract_metadata(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            tags = exifread.process_file(img_file)
            return tags
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None

def display_metadata(tags):
    print("\nExtracted Metadata:")
    if not tags:
        print("No metadata found.")
    else:
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                print(f"{tag}: {tags[tag]}")

def main():
    image_path = input("Enter the path to the image file: ").strip()

    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return

    img = load_image(image_path)
    if img is None:
        print("Could not open the image. Please check the file.")
        return

    tags = extract_metadata(image_path)
    display_metadata(tags)

if __name__ == "__main__":
    main()
