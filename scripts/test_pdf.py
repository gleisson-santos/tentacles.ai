
import os
from pathlib import Path

def test_ww2_pdf_exists():
    pdf_path = Path("outputs/pdfs/ww2_vibrant_history.pdf")
    assert pdf_path.exists(), "PDF was not generated"
    assert pdf_path.stat().st_size > 1000, "PDF is too small (might be empty or corrupted)"
    print("Test passed: PDF exists and has valid size.")

if __name__ == "__main__":
    try:
        test_ww2_pdf_exists()
    except AssertionError as e:
        print(f"Test failed: {e}")
        exit(1)
