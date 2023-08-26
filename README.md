pybloom
=======

`pybloom` is a Python module offering Bloom Filter data structures, including the classic Bloom Filter and an implementation of Scalable Bloom Filters. Additionally, it introduces the `UniversalBloomFilter` to support a broader range of data types.

Bloom filters are incredibly efficient when you know the size of your data set in advance. In contrast, Scalable Bloom Filters dynamically grow in size based on the false positive probability and the data set's size.

## Features:
* Standard Bloom Filter
* Scalable Bloom Filter
* Universal Bloom Filter

### Universal Bloom Filter
A new addition that allows for a more flexible handling of multiple data types like integers, floats, strings, and datetime objects.

## Examples:

### Classic Bloom Filter

```python
from pybloom import BloomFilter
f = BloomFilter(capacity=1000, error_rate=0.001)
[f.add(x) for x in range(10)]
assert all([(x in f) for x in range(10)])
assert 10 not in f
assert 5 in f
```
### Scalable Bloom Filter
```python
from pybloom import ScalableBloomFilter
sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
count = 10000
for i in range(0, count):
    sbf.add(i)
assert (1.0 - (len(sbf) / float(count))) <= sbf.error_rate + 2e-18
```
### Universal Bloom Filter
```python
from pybloom_live import UniversalBloomFilter
ubf = UniversalBloomFilter()

# Inserting and checking various data types:
ubf.insert(42)
assert 42 in ubf
ubf.insert(3.14159)
assert 3.14159 in ubf
ubf.insert("Hello, World!")
assert "Hello, World!" in ubf

from datetime import datetime
now = datetime.now()
ubf.insert(now)
assert now in ubf
```