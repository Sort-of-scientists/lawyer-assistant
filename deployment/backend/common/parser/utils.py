import io
import docx

from typing import Any
from tika import parser

TIKA_ENDPOINT = "http://tika:9998/tika"


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


def parse_document(document_as_bytes: Any) -> str:
    return parser.from_buffer(document_as_bytes, TIKA_ENDPOINT)["content"]