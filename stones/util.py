
# def ensure_string(text):
#     if isinstance(text, str):
#         return text
#     if isinstance(text, bytes):
#         return text.decode('utf')
#     raise TypeError('Cannot convert {} type into string'.format(type(text)))


def ensure_bytes(text):
    if isinstance(text, bytes):
        return text
    if isinstance(text, str):
        return text.encode('utf')
    raise TypeError('Cannot convert {} type into bytes'.format(type(text)))
