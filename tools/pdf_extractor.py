import io
import pdfplumber


def extract_pdf_text(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            try:
                page_text = page.extract_text()
            except Exception:
                page_text = None
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)
