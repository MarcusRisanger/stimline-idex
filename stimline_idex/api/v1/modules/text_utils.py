"""Some helper utils relevant across modules."""

from urllib.parse import quote


def url_encode_id(id: str) -> str:
    return quote(id, safe="")
