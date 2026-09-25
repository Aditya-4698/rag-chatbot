import pymupdf


def extract_pdf_pages(file):
    """
    Extract text from a PDF page by page.

    Returns:
        [
            {
                "page_number": 1,
                "text": "..."
            },
            ...
        ]
    """

    file.seek(0)

    pdf_bytes = file.read()

    pages = []

    with pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf",
    ) as pdf:

        for page_number, page in enumerate(pdf, start=1):

            text = page.get_text("text")

            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

    return pages