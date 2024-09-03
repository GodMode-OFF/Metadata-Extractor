from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
import exifread

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def extract_metadata(image_path):
    metadata = {}
    try:
        # Open the image file in binary mode
        with open(image_path, 'rb') as img_file:
            # Extract EXIF tags
            tags = exifread.process_file(img_file)

            # Filter out any tags with empty values
            metadata = {tag: str(value) for tag, value in tags.items() if value}
    except Exception as e:
        print(f"Error extracting metadata: {e}")
    
    return metadata

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file part"
        
        file = request.files['image']
        if file.filename == '':
            return "No selected file"
        
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            metadata = extract_metadata(file_path)
            if metadata:
                return render_template('index.html', metadata=metadata, image_path=file.filename)
            else:
                return render_template('index.html', error="No metadata found or the image has no EXIF data.", image_path=file.filename)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
