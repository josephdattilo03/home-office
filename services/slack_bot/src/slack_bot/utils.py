from pydantic import HttpUrl, TypeAdapter, ValidationError


_http_url = TypeAdapter(HttpUrl)


def is_link(message, **kwargs) -> bool:
    print("got to link")
    text = message.get("text", "").strip()
    print("text: " + text)
    if not (text.startswith("<") and text.endswith(">")):
        print("returned not seeing <>")
        return False
    url = text[1:-1].split("|", 1)[0]  # <url|label> -> url - slack wraps data like this
    try:
        _http_url.validate_python(url)
        return True
    except ValidationError:
        print("returning url validation")
        return False
