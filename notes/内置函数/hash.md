# hash

🔨 hash(*object*)



Return the hash value of the object (if it has one). Hash values are integers. They are used to quickly compare dictionary keys during a dictionary lookup. Numeric values that compare equal have the same hash value (even if they are of different types, as is the case for 1 and 1.0).

Note

For objects with custom [`__hash__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__hash__) methods, note that [`hash()`](https://docs.python.org/3.7/library/functions.html#hash) truncates the return value based on the bit width of the host machine. See [`__hash__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__hash__) for details.