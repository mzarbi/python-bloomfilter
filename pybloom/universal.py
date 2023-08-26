import pickle
import hashlib
from pybloom_live import BloomFilter
from datetime import datetime
from typing import Union, List, Tuple, Any


class UniversalBloomFilter:
    VALID_GRANULARITIES = {'year', 'month', 'day', 'hour', 'minute'}

    def __init__(self, date_granularity: str = 'day', step: int = 1, precision: int = 2,
                 expected_num_records: int = 1000, error_rate: float = 0.1):
        if date_granularity not in self.VALID_GRANULARITIES:
            raise ValueError(f"Unsupported date granularity: {date_granularity}")
        self.date_granularity = date_granularity
        self.step = step
        self.precision = precision
        self.bloom_filter = BloomFilter(capacity=expected_num_records, error_rate=error_rate)

    def _normalize_value(self, val: Any) -> int:
        if isinstance(val, (int, float)):
            return int(val * (10 ** self.precision)) if isinstance(val, float) else val
        if isinstance(val, datetime):
            return self._handle_datetime(val)
        return self._handle_string(str(val))

    def _handle_datetime(self, val: datetime) -> int:
        handlers = {
            'year': lambda d: d.year,
            'month': lambda d: d.year * 12 + d.month,
            'day': lambda d: (d - datetime(1970, 1, 1)).days,
            'hour': lambda d: int((d - datetime(1970, 1, 1)).total_seconds() / 3600),
            'minute': lambda d: int((d - datetime(1970, 1, 1)).total_seconds() / 60)
        }
        return handlers[self.date_granularity](val)

    def _handle_string(self, val: str) -> int:
        return int(hashlib.sha256(val.encode()).hexdigest(), 16)

    def insert_single(self, data: Any):
        self.bloom_filter.add(self._normalize_value(data))

    def insert_range(self, data_range: Tuple[Any, Any]):
        start_norm, end_norm = map(self._normalize_value, data_range)
        for val in range(start_norm, end_norm + 1, self.step):
            self.bloom_filter.add(val)

    def insert(self, data: Union[Any, List[Any], Tuple[Any, Any]]):
        if isinstance(data, list):
            for item in data:
                self.insert_single(item)
        elif isinstance(data, tuple) and len(data) == 2:
            self.insert_range(data)
        else:
            self.insert_single(data)

    def check_single(self, data: Any) -> bool:
        return self._normalize_value(data) in self.bloom_filter

    def check_range(self, data_range: Tuple[Any, Any]) -> bool:
        start_norm, end_norm = map(self._normalize_value, data_range)
        return all(val in self.bloom_filter for val in range(start_norm, end_norm + 1, self.step))

    def check(self, data: Union[Any, List[Any], Tuple[Any, Any]]) -> bool:
        if isinstance(data, list):
            return all(self.check_single(item) for item in data)
        elif isinstance(data, tuple) and len(data) == 2:
            return self.check_range(data)
        return self.check_single(data)

    def save(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename: str) -> 'UniversalBloomFilter':
        with open(filename, 'rb') as f:
            return pickle.load(f)

    # Magic methods
    def __contains__(self, data: Union[Any, List[Any], Tuple[Any, Any]]) -> bool:
        return self.check(data)

    def __len__(self) -> int:
        # Note: This isn't precise because Bloom filters don't inherently store counts
        return len(self.bloom_filter)

    def __repr__(self) -> str:
        return (f"<UniversalBloomFilter(granularity={self.date_granularity}, step={self.step}, "
                f"precision={self.precision}, expected_num_records={self.bloom_filter.capacity}, "
                f"error_rate={self.bloom_filter.error_rate})>")
