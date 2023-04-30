from PIL import Image
from pillow_heif import register_heif_opener
import shutil
import concurrent.futures


register_heif_opener()
import os


input_directory = "source_folder_path"
output_directory = "target_folder_path"


# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def convert_file(filename):
    # Check if file is HEIC
    if filename.endswith(".heic") or filename.endswith(".HEIC"):
        # Open HEIC file
        heic_path = os.path.join(input_directory, filename)
        image = Image.open(heic_path)
        
        # Copy EXIF data
        exif_data = image.getexif()
        
        # Convert to JPEG
        output_filename = os.path.splitext(filename)[0] + ".jpg"
        output_path = os.path.join(output_directory, output_filename)
        image.save(output_path, "JPEG", quality=90, exif=exif_data)
        
        # Print confirmation message
        print(f"Converted {filename} to {output_filename}")
    # Check if file is already a JPEG
    
        
        # Print confirmation message
        print(f"Copied {filename} to {output_directory}")

# Get list of files in input directory
files = os.listdir(input_directory)

# Create thread pool with 10 workers
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    # Submit file conversion jobs to thread pool
    future_to_filename = {executor.submit(convert_file, filename): filename for filename in files}
    
    # Wait for all jobs to finish
    for future in concurrent.futures.as_completed(future_to_filename):
        filename = future_to_filename[future]
        try:
            _ = future.result()
        except Exception as e:
            print(f"{filename} generated an exception: {e}")