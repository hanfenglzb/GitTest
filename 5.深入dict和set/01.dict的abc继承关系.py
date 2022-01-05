from collections.abc import Mapping

a = {}
default_value = a.setdefault("1", 1)
print(default_value, a)
default_value = a.setdefault("1", 2)
print(default_value, a)
