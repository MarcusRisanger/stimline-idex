"""Some helper utils relevant across modules."""

from urllib.parse import quote


def url_encode_id(id: str) -> str:
    """
    Encode a non-UUID ID for use in a URL.

    >>> id = "1/3-K-1"
    >>> assert url_encode_id(id) == "1%2F3-K-1"
    """
    return quote(id, safe="")
