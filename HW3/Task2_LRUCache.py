from collections import OrderedDict


class LRUCache():
    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self._cache = OrderedDict()

    def get(self, key: str) -> str:
        if key in self._cache:
            return self._cache[key]
        else:
            return ''

    def set(self, key: str, value: str) -> None:

        if key in self._cache:
            self._cache[key] = value
            self._cache.move_to_end(key)
        else:
            if len(self._cache) < self.capacity:
                self._cache[key] = value
                self._cache.move_to_end(key)
            else:
                self._cache.popitem(last=False)
                self._cache[key] = value
                self._cache.move_to_end(key)

    def DEL(self, key: str) -> None:
        if key in self._cache:
            self._cache.pop(key)

    def __str__(self):
        return str(self._cache)


cache = LRUCache(4)
cache.set(1, 1)
print(cache)
cache.set(2, 2)
cache.set(3, 3)
cache.set(4, 4)
print(cache)
cache.set(5, 5)
print(cache)
cache.DEL(5)
print(cache)
cache.set(2, 22)
print(cache)
print(cache.get(4))
print(cache.get(1))
