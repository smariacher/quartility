import os
import zipfile

def compress_to_zip(folder_path, output_dir = './_projects'):
    """
    Compresses the given folder into a ZIP archive and saves it to ./projects
    with the same name as the folder.

    Parameters:
        folder_path (str): Path to the folder to compress.
        output_dir (str): Directory to save the zip file. Relative paths are resolved from the current working directory.
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"{folder_path} is not a valid folder")

    # Ensure output folder exists
    os.makedirs(output_dir, exist_ok=True)

    # Name of the output zip file
    folder_name = os.path.basename(os.path.normpath(folder_path))
    zip_path = os.path.join(output_dir, f"{folder_name}.zip")

    # Compress folder recursively
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Preserve folder structure inside the zip
                zipf.write(file_path, os.path.relpath(file_path, folder_path))