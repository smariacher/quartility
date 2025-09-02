import pytest
import os
import tempfile
from quartility import convert_to_project_path, displayPages, compress_to_zip

PDF_PATH = "./some.pdf"

def test_convert_to_project_path():
    path = convert_to_project_path(PDF_PATH, "setup.cfg")
    assert isinstance(path, str)
    assert PDF_PATH.split("/")[-1] in path

def test_displayPages():
    if not os.path.exists(PDF_PATH):
        # skip test if PDF not present
        pytest.skip("PDF not found")
    try:
        displayPages(PDF_PATH, [1, 2, 3])
    except Exception as e:
        pytest.fail(f"displayPages raised an exception: {e}")

def test_compress_to_zip():
    with tempfile.TemporaryDirectory() as tmpdir:
        f1 = os.path.join(tmpdir, "file1.txt")
        f2 = os.path.join(tmpdir, "file2.txt")
        open(f1, "w").write("hello")
        open(f2, "w").write("world")
        
        try:
            compress_to_zip(tmpdir)
            zip_path = os.path.join(".", "_projects", os.path.basename(tmpdir) + ".zip")  # manually compute
            print(zip_path)
            assert os.path.exists(zip_path)
            assert zip_path.endswith(".zip")
        except Exception as e:
            pytest.fail(f"compress_to_zip raised an exception: {e}")

