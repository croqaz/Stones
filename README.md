
# 🗿Stones

[![Build Status](https://travis-ci.org/ShinyTrinkets/Stones.svg?branch=master)](https://travis-ci.org/ShinyTrinkets/Stones) [![Codecov](https://codecov.io/gh/ShinyTrinkets/Stones/branch/master/graph/badge.svg)](https://codecov.io/gh/ShinyTrinkets/Stones) ![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)

> Base library for persistent key-value stores, 100% compatible with Python dict.

![Stones image](https://raw.githubusercontent.com/ShinyTrinkets/stones/master/images/stones-image.jpg)

The idea behind this project is to have a common interface for a multitude of persistent key-value stores, easy to use and extend, with some extra built-in features as bonus. Inspired from [Datastore](https://github.com/datastore/datastore) and [MemDown](https://github.com/level/memdown).


## Features and Limitations

- the same API that you already know from [Python dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
- thread safe updates
- excellent test coverage (>90%)
- only the Memory Store is available by default, to be used as an example. Other Stores _will be available soon_ ™ (LevelDB, LMDB, DBM, Redis, etc).
- 1st limitation: the keys can only be bytes. This is actually more of a feature.
- 2nd limitation: the values are actually also bytes, but a serializer (default is Pickle) converts the data structure into bytes
- there are several serializers available: Pickle, JSON and optional: cbor2, msgpack. You can easily add your own serializer, please check the documentation below.
- 3rd limitation: after the data was serialized, you have to continue using the same serializer. If for some reason, you want to switch the serializer, you can create a new Store with your new serializer and copy all the data from the old Store.


## Install

This project uses [Python 3.5+](https://www.python.org/) and [pip](https://pip.pypa.io/). A [virtual environment](https://virtualenv.pypa.io/) is strongly encouraged.

```sh
$ pip install git+https://github.com/ShinyTrinkets/Stones
```


## Usage

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


## More or less similar projects

Python:

* [TinyDB](https://github.com/msiemens/tinydb) - awesome lightweight document oriented database
* [Lukedeo/Cupboard](https://github.com/lukedeo/Cupboard) - store things in a variety of NoSQL KV stores
* [Lcrees/Shove](https://bitbucket.org/lcrees/shove) - unmaintained (2 years)
* [ShuhaoWu/Kvkit](https://github.com/shuhaowu/kvkit) - unmaintained (4 years)
* [Datastore](https://github.com/datastore/datastore) - unmaintained since 2014
* [Persistent dict ActiveState recipe](https://code.activestate.com/recipes/576642) - from 2009

Node.js:

* [MemDown](https://github.com/level/memdown) - abstract LevelDown store for Node.js and browsers
* [NeDB](https://github.com/louischatriot/nedb) - embedded database for Node.js, nw.js, Electron and browsers
* [FortuneJS](https://github.com/fortunejs/fortune) - database abstraction layer with a common interface for databases
* [PouchDB](https://github.com/pouchdb/pouchdb) - pocket-sized database


## License

[MIT](LICENSE) © 2017 Cristi Constantin.
