"""
Functions that serialize Python objects.
Pickle and JSON are builtin libraries.
CBOR2 and MsgPack are available with PIP.
Other than the normal objects, available in all languages,
the `tuple`, `set` and `frozenset` are also supported.
"""

import pickle
from io import BytesIO
from .util import ensure_bytes

try:
    # Ultra fast JSON encoder and decoder
    import ujson as json
except ModuleNotFoundError:
    try:
        # Second fast JSON encoder and decoder
        import simplejson as json
    except ModuleNotFoundError:
        # print('For better performance using JSON, install either UJSON or simplejson')
        import json

try:
    import cbor2
    from cbor2.types import CBORTag
except ModuleNotFoundError:
    cbor2 = None
    # print('CBOR can be installed at PyPi.python.org/pypi/cbor2')

try:
    import msgpack
except ModuleNotFoundError:
    msgpack = None
    # print('MessagePack can be installed at PyPi.python.org/pypi/msgpack')

TUP_FLAG = b'__(,)__'
SET_FLAG = b'__{,}__'
F_SET_FLAG = b'__f{}__'  # frozenset

TUP_CBOR = 38


def noop(data):
    """
    No-op "encoder" returns the object exactly as it is.
    """
    return data


def encode_pickle(data):
    """
    Serialize an object using Pickle's highest protocol.
    Pickle doesn't need any help dealing with custom Python structures.
    """
    return pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL, fix_imports=False)


def decode_pickle(data):
    """
    Restore original object using Pickle.
    """
    return pickle.loads(data, fix_imports=False)


def _convert_python_obj(data):
    """
    Convert tuple, set and frozenset into list
    and insert a special flag in the first position,
    to recognize how the list should be converted back.
    Used by JSON and MsgPack.
    """
    if isinstance(data, tuple):
        return [TUP_FLAG] + list(data)
    if isinstance(data, set):
        return [SET_FLAG] + list(data)
    if isinstance(data, frozenset):
        return [F_SET_FLAG] + list(data)
    return data


def _restore_python_obj(data):
    """
    Convert flagged list back to a Python object.
    Used by JSON and MsgPack.
    """
    if isinstance(data, (bytes, str)):
        return ensure_bytes(data)
    if isinstance(data, list):
        if data[0] == TUP_FLAG:
            return tuple(data[1:])
        if data[0] == SET_FLAG:
            return set(data[1:])
        if data[0] == F_SET_FLAG:
            return frozenset(data[1:])
    return data


def encode_json(data):
    """
    Serialize an object using JSON.
    Convert special Python iterable into list.
    """
    data = _convert_python_obj(data)
    return ensure_bytes(json.dumps(data))


def decode_json(data):
    """
    Restore original object using JSON.
    JSON doesn't know how to deal with bytes and it needs help.
    """
    data = json.loads(data)
    if isinstance(data, (bool, int, float)):
        return data
    if isinstance(data, (bytes, str)):
        return ensure_bytes(data)
    if isinstance(data, dict):
        return {_restore_python_obj(k): _restore_python_obj(v) for k, v in data.items()}
    return _restore_python_obj([_restore_python_obj(e) for e in data])


def _cbor_encoder(encoder, data):
    """
    Hook to convert tuples and sets into lists.
    The list of CBOR tags:
    http://cbor2.readthedocs.io/en/latest/usage.html#tag-support
    """
    if isinstance(data, tuple):
        encoder.encode(CBORTag(TUP_CBOR, list(data)))


def _cbor_decoder(decoder, tag, _):
    """
    Hook to convert lists into their original objects.
    """
    if tag.tag == TUP_CBOR:
        return tuple(tag.value)


def encode_cbor(data):
    """
    Serialize an object using CBOR.
    The CBOR Encoder is needed to revert the default
    behaviour of treating tuples like normal lists.
    """
    mem_file = BytesIO()
    encoder = cbor2.CBOREncoder(mem_file, default=_cbor_encoder)
    del encoder._encoders[tuple]  # Enable the default callback
    encoder.encode(data)
    return mem_file.getvalue()


def decode_cbor(data):
    """
    Restore original object using CBOR.
    """
    return cbor2.loads(data, tag_hook=_cbor_decoder)


def encode_msgpack(data):
    """
    Serialize an object using MsgPack.
    """
    return msgpack.dumps(data, use_bin_type=True, strict_types=True, default=_convert_python_obj)


def decode_msgpack(data):
    """
    Restore original object using MsgPack.
    """
    return msgpack.loads(data, list_hook=_restore_python_obj)


serializers = {
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
    }
}

if cbor2:
    serializers['cbor'] = {'encode': encode_cbor, 'decode': decode_cbor}

if msgpack:
    serializers['msgpack'] = {'encode': encode_msgpack, 'decode': decode_msgpack}
