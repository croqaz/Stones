
# Stones
[![Build Status](https://travis-ci.org/ShinyTrinkets/Stones.svg?branch=master)](https://travis-ci.org/ShinyTrinkets/Stones) [![Codecov](https://codecov.io/gh/ShinyTrinkets/Stones/branch/master/graph/badge.svg)](https://codecov.io/gh/ShinyTrinkets/Stones) ![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Persistent key-value containers, compatible with Python dict.

![Stones image](https://raw.githubusercontent.com/ShinyTrinkets/stones/master/images/stones-image.jpg)


### Features and limitations

- the stores have exactly the same methods as a Python dict (get, set, delete, update, keys, values, items, contains, length, clear)
- limitation: the keys can only be bytes
- the values are actually also bytes, but an encoder converts your data structure into bytes
- there are several encoders available: pickle, JSON and optional: cbor2, msgpack
- you can easily add your own encoder
- only the memory store available by default (not persistent, a wrapper for Python dict)
- after the data was saved on HDD, when re-opening the store, you must use the same encoder (makes sense, right?)


### Usage

```python
from stones import stone

# Create a new persistent dictionary, backed by LevelDB
stor = stone('my-db', persistence='level', encoder='pickle')

# You can use it just like a normal Python dict,
# with the limitation that keys are bytes,
# and the values must be serializable
stor[b's'] = b'whatever'
stor[b'li'] = [True, False, None, -1]
stor[b'tu'] = ('Yes', 'No', 3)

b's' in stor
# True
len(stor)
# 3
stor.keys()
# [b'li', b's', b'tu']
stor.values()
# [[True, False, None, -1], b'whatever', ('Yes', 'No', 3)]

# The data is decoded in place
-1 in stor[b'li']
# True
3 in stor[b'tu']
# True

del stor[b'li']
stor.get(b'li', False)
# False

# The data is persisted
del stor
# Re-create the store, using the same encoder
stor = stone('my-db', persistence='level', encoder='pickle')

len(stor)
# 2
stor.keys()
# [b's', b'tu']
```


### Similar projects

* [Lukedeo/Cupboard](https://github.com/lukedeo/Cupboard) - awesome
* [Lcrees/Shove](https://bitbucket.org/lcrees/shove) - unmaintained (2 years)
* [Datastore](https://github.com/datastore/datastore) - unmaintained (4 years)
* [ShuhaoWu/Kvkit](https://github.com/shuhaowu/kvkit) - unmaintained (4 years)
* [Persistent dict ActiveState recipe](https://code.activestate.com/recipes/576642) - from 2009
