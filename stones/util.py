
#- rev: v1 -
#- hash: 2PIP7P -

def ensure_bytes(text):
    if isinstance(text, bytes):
        return text
    if isinstance(text, str):
        return text.encode('utf')
    raise TypeError('Cannot convert {} type into bytes'.format(type(text)))
