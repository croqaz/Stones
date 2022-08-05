
def ensure_bytes(text):
    if isinstance(text, bytes):
        return text
    if isinstance(text, str):
        return text.encode('utf8')
    raise TypeError('Cannot convert {} type into bytes'.format(type(text)))
