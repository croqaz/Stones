
#- rev: v4 -
#- hash: EAKY6Z -

import pickle

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
    from cbor2.types import CBORTag
except ModuleNotFoundError:
    print('CBOR can be installed at PyPi.python.org/pypi/cbor2')

try:
    import msgpack
except ModuleNotFoundError:
    print('MessagePack can be installed at PyPi.python.org/pypi/msgpack-python')


TUP_FLAG = b'__(,)__'
SET_FLAG = b'__{,}__'


def noop(data):
    return data


def encode_pickle(data):
    return pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL, fix_imports=False)


def decode_pickle(data):
    return pickle.loads(data, fix_imports=False)


def encode_json(data):
    if isinstance(data, tuple):
        data = [TUP_FLAG] + list(data)
    elif isinstance(data, set):
        data = [SET_FLAG] + list(data)
    return json.dumps(data).encode('utf8')


def decode_json(data):
    data = json.loads(data)
    tup_flag = TUP_FLAG.decode('utf8')
    set_flag = SET_FLAG.decode('utf8')
    if isinstance(data, str):
        return data.encode('utf')
    if isinstance(data, list) and data[0] == tup_flag:
        return tuple(d.encode('utf') for d in data[1:])
    if isinstance(data, list) and data[0] == set_flag:
        return set(d.encode('utf') for d in data[1:])
    if isinstance(data, list):
        return [d.encode('utf') for d in data]


def _cbor_encoder(encoder, value):
    encoder.encode(CBORTag(38, sorted(value)))


def _cbor_decoder(decoder, tag, fp):
    return set(tag.value)


def encode_cbor(data):
    return cbor2.dumps(data, default=_cbor_encoder)


def decode_cbor(data):
    return cbor2.loads(data, tag_hook=_cbor_decoder)


def _msgpack_encoder(data):
    if isinstance(data, tuple):
        data = [TUP_FLAG] + list(data)
    elif isinstance(data, set):
        data = [SET_FLAG] + list(data)
    return data


def _msgpack_decoder(data):
    if data[0] == TUP_FLAG:
        data = tuple(data[1:])
    elif data[0] == SET_FLAG:
        data = set(data[1:])
    return data


def encode_msgpack(data):
    return msgpack.dumps(data, use_bin_type=True, strict_types=True, default=_msgpack_encoder)


def decode_msgpack(data):
    return msgpack.loads(data, list_hook=_msgpack_decoder)


encoders = {
    'noop': {
        'encode': noop,
        'decode': noop
    },
    'pickle': {
        'encode': encode_pickle,
        'decode': decode_pickle
    },
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
