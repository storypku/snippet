from time import time
from llist import sllist
from collections import namedtuple
Event = namedtuple("Event", ("count", "time"));
class MinuteHourCounter:
    """Class to keep track of events (e.g.how many bytes a web server has
    transferred) over the past minute and over the past hour.
    """

    def __init__(self):
        self.minute_events = sllist()
        # only contains elements NOT in minute_events
        self.hour_events = sllist()
        self.minute_count = 0
        # counts ALL events over past hour, including past minute
        self.hour_count = 0

    def add(self, count=0):
        """Add a new data point (count >= 0).
        For the next minute, minuteCount will be larger by +count.
        For the next hour, hourCount will be larger by +count.
        """
        now_secs = time()
        self._shiftOldEvents(now_secs)
        # Feed into the minute list (not into the hour list -- that will
        # happen later
        self.minute_events.append(Event(count, now_secs))
        self.minute_count += count
        self.hour_count += count

    def minuteCount(self):
        """Return the accumulated count over the past 60 seconds."""
        self._shiftOldEvents(time())
        return self.minute_count

    def hourCount(self):
        """Return the accumulated count over the past 3600 seconds."""
        self._shiftOldEvents(time())
        return self.hour_count


    def _shiftOldEvents(self, now_secs):
        """Find and delete old events, and decrease hour_count and
        minute_count accordingly."""
        minute_ago = now_secs - 60
        hour_ago = now_secs - 3600
        # Move events more than one minute old from "minute_events" into
        # "hour_events" (Events older than one hour will e removed in the
        # second loop.)
        while self.minute_events.size != 0 and\
                self.minute_events.first().time <= minute_ago:
            self.hour_events.append(self.minute_events.first())
            self.minute_count -= self.minute_events.first().count
            self.minute_events.popleft()
        # Remove events more than one hour old from "hour_events"
        while self.hour_events.size != 0 and\
                self.hour_events.first().time <= hour_ago:
            self.hour_count -= self.hour_events.first().count
            self.hour_events.popleft()

