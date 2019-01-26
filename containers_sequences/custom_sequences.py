"""
Book: Clean code in python.
Chapter: Creating your own sequences, p28.

Sequence is an object that implements __getitem__ and __len__. (i.e Lists, Tuples, Strings)
"""
import collections


# 1st Option: By creating a wrapper around a built-in type
class CustomSequenceWrapper:
    def __init__(self, *values):
        # Delegate the behavior to the underlying object as much as possible
        self._values = list(values)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, item):
        prefix = "modified_"
        return f"{prefix}{self._values.__getitem__(item)}"

my_seq = CustomSequenceWrapper(1,3,4,5)

for item in my_seq:
    print(item)

print(my_seq[0:2])

for i in range(1, 3):
    print(my_seq[i])

print(",".join(my_seq))


# 2nd Option: By extending a built-in type using the collections module.
# NOTE:
#   You should never try to extend a built-in type directly. Use the
#   collections module instead. For explanation see:
#   Chapter: Extending built-in types, p51.
class CustomSequenceExtention(collections.UserList):
    def __getitem__(self, index):
        value = super().__getitem__(index)
        prefix = "remodified_"
        return f"{prefix}{value}"

my_seq = CustomSequenceExtention([1,3,4,5])

for item in my_seq:
    print(item)

print(my_seq[0:2])

for i in range(1, 3):
    print(my_seq[i])

print(",".join(my_seq))
