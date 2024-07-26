import time
from collections import defaultdict, Counter


class RateLimiter:
    def __init__(self, rate_per_second):
        self.rate_per_second = rate_per_second
        self.last_sent_time = defaultdict(lambda: time.time())
        self.count = defaultdict(int)
        self.direction_counts = defaultdict(Counter)
        self.current_direction = defaultdict(str)

    def update_direction(self, key, direction):
        self.direction_counts[key][direction] += 1
        self.current_direction[key] = direction

    def should_send(self, key):
        current_time = time.time()
        if current_time - self.last_sent_time[key] >= 1:
            self.last_sent_time[key] = current_time
            self.count[key] = 0
            self.direction_counts[key] = Counter()
        if self.count[key] < self.rate_per_second:
            self.count[key] += 1
            return True
        return False

    def send(self, key, action):
        if self.should_send(key):
            most_common_direction = self.direction_counts[key].most_common(1)
            if most_common_direction:
                direction = most_common_direction[0][0]
                action(direction)
            self.direction_counts[key] = Counter()  # Reset counts after sending
