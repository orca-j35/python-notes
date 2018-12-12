# slice

🔨 *class* slice(*stop*)

🔨 *class* slice(*start*, *stop*[, *step*])

Return a [slice](https://docs.python.org/3.7/glossary.html#term-slice) object representing the set of indices specified by `range(start, stop,step)`. The *start* and *step* arguments default to `None`. Slice objects have read-only data attributes `start`, `stop` and `step` which merely return the argument values (or their default). They have no other explicit functionality; however they are used by Numerical Python and other third party extensions. Slice objects are also generated when extended indexing syntax is used. For example: `a[start:stop:step]` or `a[start:stop, i]`. See[`itertools.islice()`](https://docs.python.org/3.7/library/itertools.html#itertools.islice) for an alternate version that returns an iterator.