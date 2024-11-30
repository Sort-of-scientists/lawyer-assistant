import io
import docx


def text_to_docx_bytes(text: str) -> bytes:
    """
    Return .docx file in bytes.

    Parameters
    ----------
    text : str
        Content of document.

    Returns
    -------
    bytes
        Bytes of document.
    """

    doc = docx.Document()
    
    doc.add_paragraph(text)
    
    byte_stream = io.BytesIO()
    
    doc.save(byte_stream)
    
    byte_stream.seek(0)
    return byte_stream.getvalue()