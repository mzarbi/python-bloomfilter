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
# Initialize BloomFilter with expected number of records as 10000
bloom = UniversalBloomFilter(expected_num_records=10000)

# Inserting a single integer
bloom.insert(42)
assert 42 in bloom

# Inserting a single float
bloom.insert(3.14159)
assert 3.14159 in bloom

# Inserting multiple integers
bloom.insert([1, 2, 3, 4, 5])
assert all(i in bloom for i in [1, 2, 3, 4, 5])

# Inserting multiple floats
bloom.insert([0.1, 0.2, 0.3])
assert all(f in bloom for f in [0.1, 0.2, 0.3])

# Inserting a range of integers
bloom.insert((10, 20))
assert all(i in bloom for i in range(10, 21))

# Inserting datetime objects
from datetime import datetime, timedelta
now = datetime.now()
bloom.insert(now)
assert now in bloom

# Inserting a range of datetime objects
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 1, 5)
bloom.insert((start_date, end_date))
assert all((start_date + timedelta(days=i)) in bloom for i in range(5))

# Inserting strings
bloom.insert("Hello, World!")
assert "Hello, World!" in bloom

# Inserting a range of strings (Note: Ranges aren't really meaningful for strings, but this is how it'd work)
bloom.insert(("a", "d"))
assert all(char in bloom for char in ["a", "b", "c", "d"])

# Inserting other types by converting to string
custom_obj = {"name": "Alice", "age": 30}
bloom.insert(custom_obj)
assert custom_obj in bloom

# Using the save and load functionality
bloom.save("bloom_filter.pkl")
loaded_bloom = UniversalBloomFilter.load("bloom_filter.pkl")
assert 42 in loaded_bloom

# Print BloomFilter representation
    print(bloom)
```