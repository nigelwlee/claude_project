from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Extract text content from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text as a string
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text.strip()

    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")
