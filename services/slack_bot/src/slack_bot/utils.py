from pydantic import HttpUrl, TypeAdapter, ValidationError


_http_url = TypeAdapter(HttpUrl)


def is_link(message, **kwargs) -> bool:
    text = message.get("text", "").strip()
    if not (text.startswith("<") and text.endswith(">")):
        return False
    url = text[1:-1].split("|", 1)[0]  # <url|label> -> url - slack wraps data like this
    try:
        _http_url.validate_python(url)
        return True
    except ValidationError:
        return False
