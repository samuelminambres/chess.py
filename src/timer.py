import time

class Timer:

    def __init__(self, time_limit: float, increment: float):
        self.time_left = time_limit
        self.increment = increment
        self.last_start_time = None
        self.is_running = False

    @property
    def time_left(self):
        return self._time_left
    
    @time_left.setter
    def time_left(self, value):
        if not isinstance(value, float):
            raise TypeError("Time left must be float")
        self._time_left = value

    @property
    def increment(self):
        return self._increment
    
    @increment.setter
    def increment(self, value):
        if not isinstance(value, float):
            raise TypeError("Increment must be float")
        self._increment = value

    @property
    def last_start_time(self):
        return self._last_start_time
    
    @last_start_time.setter
    def last_start_time(self, value):
        if not isinstance(value, float) and value is not None:
            raise TypeError("Last start time must be float or None")
        self._last_start_time = value

    @property
    def is_running(self):
        return self._is_running
    
    @is_running.setter
    def is_running(self, value):
        if not isinstance(value, bool):
            raise TypeError("Is running flag must be bool")
        self._is_running = value

    def __str__(self):
        self.update()
        minutes = int(self.time_left // 60)
        seconds = int(self.time_left % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def start(self):
        if not self.is_running:
            self.last_start_time = time.time()
            self.is_running = True

    def stop(self):
        if self.is_running:
            self.update()
            self.time_left += self.increment
            self.is_running = False

    def update(self):
        if self.is_running:
            current_time = time.time()
            self.time_left -= current_time - self.last_start_time
            self.last_start_time = current_time
            if self.time_left < 0:
                self.time_left = 0

    def is_timeout(self):
        self.update()
        return self.time_left <= 0