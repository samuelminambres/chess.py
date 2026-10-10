import time

class Timer:
    """Manages game clock countdown and per-move increments for a player.

    Attributes:
        time_left (float): Remaining time in seconds.
        increment (float): Time increment in seconds added when stopped.
        last_start_time (float or None): Epoch timestamp of the last clock start.
        is_running (bool): Whether the timer is actively counting down.
    """

    def __init__(self, time_limit: float, increment: float):
        """Initializes the timer with a time limit and increment.

        Args:
            time_limit (float): Initial time limit in seconds.
            increment (float): Time increment in seconds added when stopped.
        """
        self.time_left = time_limit
        self.increment = increment
        self.last_start_time = None
        self.is_running = False

    @property
    def time_left(self):
        """Gets the remaining time.

        Returns:
            float: The remaining time in seconds.
        """
        return self._time_left
    
    @time_left.setter
    def time_left(self, value):
        """Sets the remaining time.

        Args:
            value (float): The remaining time in seconds.

        Raises:
            TypeError: If value is not a float.
        """
        if not isinstance(value, float):
            raise TypeError("Time left must be float")
        self._time_left = value

    @property
    def increment(self):
        """Gets the time increment added per move.

        Returns:
            float: The increment time in seconds.
        """
        return self._increment
    
    @increment.setter
    def increment(self, value):
        """Sets the time increment added per move.

        Args:
            value (float): The increment time in seconds.

        Raises:
            TypeError: If value is not a float.
        """
        if not isinstance(value, float):
            raise TypeError("Increment must be float")
        self._increment = value

    @property
    def last_start_time(self):
        """Gets the timestamp of the last timer start.

        Returns:
            float or None: Epoch timestamp of the last start, or None.
        """
        return self._last_start_time
    
    @last_start_time.setter
    def last_start_time(self, value):
        """Sets the timestamp of the last timer start.

        Args:
            value (float or None): Epoch timestamp of the timer start, or None.

        Raises:
            TypeError: If value is not a float and not None.
        """
        if not isinstance(value, float) and value is not None:
            raise TypeError("Last start time must be float or None")
        self._last_start_time = value

    @property
    def is_running(self):
        """Gets whether the timer is currently running.

        Returns:
            bool: True if the timer is running, False otherwise.
        """
        return self._is_running
    
    @is_running.setter
    def is_running(self, value):
        """Sets the running state of the timer.

        Args:
            value (bool): True if running, False otherwise.

        Raises:
            TypeError: If value is not a bool.
        """
        if not isinstance(value, bool):
            raise TypeError("Is running flag must be bool")
        self._is_running = value

    def __str__(self):
        """Returns the formatted remaining time as MM:SS.

        Returns:
            str: The remaining time formatted as 'MM:SS'.
        """
        self.update()
        minutes = int(self.time_left // 60)
        seconds = int(self.time_left % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def start(self):
        """Starts the timer if it is not already running."""
        if not self.is_running:
            self.last_start_time = time.time()
            self.is_running = True

    def stop(self):
        """Stops the timer and adds the increment to the remaining time."""
        if self.is_running:
            self.update()
            self.time_left += self.increment
            self.is_running = False

    def update(self):
        """Updates the remaining time based on the elapsed time since last start."""
        if self.is_running:
            current_time = time.time()
            self.time_left -= current_time - self.last_start_time
            self.last_start_time = current_time
            if self.time_left < 0:
                self.time_left = 0

    def is_timeout(self):
        """Checks if the timer has expired.

        Returns:
            bool: True if remaining time is less than or equal to 0, False otherwise.
        """
        self.update()
        return self.time_left <= 0