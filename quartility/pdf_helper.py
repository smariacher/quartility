import os
import tempfile
import uuid
from PyPDF2 import PdfReader, PdfWriter
from IPython.display import display, IFrame
import hashlib
import json
from .core import convert_to_project_path

def file_hash(filepath, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def displayPages(pdf_path, page_numbers, save_folder = "_freeze/pdf/"):
    """
    Extracts specified pages from a PDF file, saves them as a new PDF with a unique name, 
    and displays the result in an embedded viewer.

    This function:
      1. Resolves the absolute path to the source PDF (relative paths are resolved against the project path).
      2. Validates that the source PDF exists.
      3. Uses PyPDF2 to extract only the pages listed in `page_numbers`.
      4. Generates a unique filename for the new PDF based on the selected pages.
      5. Saves the resulting PDF to the `_freeze/pdf` directory in the Quarto project if not specified otherwise.
      6. Displays the saved PDF inline using an HTML iframe (works in Jupyter/Quarto).

    Args:
        pdf_path (str): Path to the source PDF file. Can be absolute or relative to the project root.
        page_numbers (list[int]): A list of 1-based page numbers to extract. 
                                   Pages outside the valid range are skipped with a warning.
        save_folder (str, optional): Output save folder to store the generated PDF file. 

    Raises:
        FileNotFoundError: If the specified PDF file does not exist.
    
    Side Effects:
        - Creates (if necessary) and writes the output PDF to `_freeze/pdf/` if not specified otherwise.
        - Prints warnings for any page numbers outside the source PDF range.
        - Displays the generated PDF inline.

    Example:
        >>> displayPages("docs/sample.pdf", [1, 3, 5])
        # Creates `_freeze/pdf/selected_pages_<hash>.pdf` containing pages 1, 3, and 5,
        # then displays it inline.
    """
    # Resolve absolute path to source PDF
    if not os.path.isabs(pdf_path):
        pdf_path = convert_to_project_path(pdf_path)
    pdf_path = os.path.normpath(pdf_path)
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for p in page_numbers:
        if 1 <= p <= len(reader.pages):
            writer.add_page(reader.pages[p - 1])
        else:
            print(f"Warning: page {p} out of range.")

    pages_str = json.dumps(page_numbers)  # serialize list to string
    unique_id = hashlib.sha256(pages_str.encode('utf-8')).hexdigest()

    unique_filename = f"selected_pages_{unique_id}.pdf"

    # Save in a public folder inside the Quarto project (_freeze/pdf)
    pdf_dir = os.path.join(save_folder, "pdf")
    os.makedirs(pdf_dir, exist_ok=True)
    output_pdf_path = os.path.join(pdf_dir, unique_filename)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    display(IFrame(src=output_pdf_path, width=700, height=600))
