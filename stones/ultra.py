
class UltraStore:

    def _encode(self, value):
        ...

    def _decode(self, value):
        ...


    def set_add(self, key, value):
        """
        Add a value in the set found at key
        """
        encoded = self.get(key)
        kset = set(self._decode(encoded)) if encoded else set()
        kset.add(value)
        self[key] = self._encode(kset)

    def set_remove(self, key, value):
        """
        Remove a value from the set found at key
        """
        encoded = self.get(key)
        kset = set(self._decode(encoded)) if encoded else set()
        kset.discard(value)
        self[key] = self._encode(kset)


    def list_append(self, key, value):
        """
        Add a value in the list found at key
        """
        encoded = self.get(key)
        klist = list(self._decode(encoded))
        klist.append(value)
        self[key] = self._encode(klist)

    def list_remove(self, key, value):
        """
        Remove a value from the list found at key
        """
        encoded = self.get(key)
        klist = list(self._decode(encoded))
        klist.remove(value)
        self[key] = self._encode(klist)
