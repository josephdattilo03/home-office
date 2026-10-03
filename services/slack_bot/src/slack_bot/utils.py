from pydantic import HttpUrl, TypeAdapter, ValidationError


_http_url = TypeAdapter(HttpUrl)


def is_link(message, **kwargs) -> bool:
    try:
        _http_url.validate_python(message)
        return True
    except ValidationError:
        return False
