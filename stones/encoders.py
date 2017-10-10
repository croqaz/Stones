
try:
    import ujson as json
except ModuleNotFoundError:
    try:
        import simplejson as json
    except ModuleNotFoundError:
        print('For better performance using JSON, install either UJSON or simplejson')
        import json

try:
    import cbor2
except ModuleNotFoundError:
    print('CBOR can be installed at PyPi.python.org/pypi/cbor2')

try:
    import msgpack
except ModuleNotFoundError:
    print('MessagePack can be installed at PyPi.python.org/pypi/msgpack-python')


def encode_json(data):
    return json.dumps(data).encode('utf8')

def decode_json(data):
    return json.loads(data)


def encode_cbor(data):
    return cbor2.dumps(data)

def decode_cbor(data):
    return cbor2.loads(data)


def encode_msgpack(data):
    return msgpack.packb(data, use_bin_type=True)

def decode_msgpack(data):
    return msgpack.unpackb(data)


encoders = {
    'json': {
        'encode': encode_json,
        'decode': decode_json
    },
    'cbor': {
        'encode': encode_cbor,
        'decode': decode_cbor
    },
    'msgpack': {
        'encode': encode_msgpack,
        'decode': decode_msgpack
    }
}
