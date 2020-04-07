from collections import OrderedDict


class LRUCache(OrderedDict):
    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self._cache = OrderedDict()

    def GET(self, key: str) -> str:
        return self._cache[key]

    def SET(self, key: str, value: str) -> None:

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