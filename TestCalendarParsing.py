import unittest
import itertools

from datetime import datetime, timedelta
from calendarParser import Calendar, Event, CalendarParser, NoEventsException,\
    TimesNotInitialized


class CalendarTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now()
        self.cal = Calendar(self.now)
        self.e1 = Event("Event 1", self.now, self.now)
        self.e2 = Event("Event 2", self.now, self.now)

        self.earlyEvent = Event("Event early", datetime(2011, 1, 1),
            datetime(2011, 1, 1))
        self.earlyMidEvent = Event("Event early mid", datetime(2012, 1, 1),
            datetime(2012, 1, 1))
        self.lateMidEvent = Event("Event late mid", datetime(2013, 1, 1),
            datetime(2013, 1, 1))
        self.lateEvent = Event("Event late", datetime(2014, 1, 1),
            datetime(2014, 1, 1))

    def testAddEvent(self):
        self.cal.addEvent(self.e1)
        self.cal.addEvent(self.e2)

        self.assertIn(self.e1, self.cal)
        self.assertIn(self.e2, self.cal)
        self.assertEqual(2, self.cal.getNumEvents())

    def testAddEventNoneStartEndTimes(self):
        e1 = Event("event no start/end times", None, None)
        e2 = Event("event no start time", None, datetime(2011, 4, 1))
        e3 = Event("event no end time", datetime(2015, 2, 1), None)

        self.assertRaises(TimesNotInitialized, self.cal.addEvent, e1)
        self.assertRaises(TimesNotInitialized, self.cal.addEvent, e2)
        self.assertRaises(TimesNotInitialized, self.cal.addEvent, e3)

    def testEventsAreSorted(self):
        self.cal.addEvent(self.earlyMidEvent)
        self.cal.addEvent(self.earlyEvent)
        self.cal.addEvent(self.lateEvent)
        self.cal.addEvent(self.lateMidEvent)
        orderAdded = [self.earlyMidEvent, self.earlyEvent,
            self.lateEvent, self.lateMidEvent]
        events = []
        for event in self.cal:
            events.append(event)
        self.assertEqual(events, sorted(orderAdded))

        self.cal.clear()
        self.cal.addEvent(self.lateEvent)
        self.cal.addEvent(self.lateMidEvent)
        self.cal.addEvent(self.earlyEvent)
        self.cal.addEvent(self.earlyMidEvent)
        orderAdded = [self.lateEvent, self.lateMidEvent,
            self.earlyEvent, self.earlyMidEvent]
        events = []
        for event in self.cal:
            events.append(event)
        self.assertEqual(events, sorted(orderAdded))

    def testRemoveEvent(self):
        self.cal.addEvent(self.e1)
        self.cal.addEvent(self.e2)

        self.cal.removeEvent(self.e1)
        self.assertNotIn(self.e1, self.cal)
        self.assertEqual(1, self.cal.getNumEvents())

    def testClear(self):
        self.cal.addEvent(self.e1)
        self.cal.addEvent(self.e2)

        self.cal.clear()
        self.assertNotIn(self.e1, self.cal)
        self.assertNotIn(self.e2, self.cal)
        self.assertEqual(0, self.cal.getNumEvents())

    def testGetNextEvent(self):
        fiveMin = timedelta(minutes = 5)
        tenMin = timedelta(minutes = 10)
        farFromNow1 = self.now + timedelta(hours = 10)
        farFromNow2 = self.now + timedelta(hours = 28)
        farFromNow3 = self.now + timedelta(hours = 39)

        nextEventStartTime = self.now + fiveMin
        nextEventEndTime = self.now + tenMin
        nextEvent = Event("Next Event", nextEventStartTime, nextEventEndTime)

        farEvent1 = Event("Event Far Away 1", farFromNow1, farFromNow1 + tenMin)
        farEvent2 = Event("Event Far Away 2", farFromNow2, farFromNow2 + tenMin)
        farEvent3 = Event("Event Far Away 3", farFromNow3, farFromNow3 + tenMin)

        self.cal.addEvent(nextEvent)
        self.cal.addEvent(farEvent1)
        self.cal.addEvent(farEvent2)
        self.cal.addEvent(farEvent3)

        self.assertEqual(self.cal.getNextEvent(), nextEvent)
        self.assertEqual(self.cal.getNextEvent(nextEventStartTime), nextEvent)
        self.assertEqual(self.cal.getNextEvent(nextEventEndTime), farEvent1)

    def testGetNextEventSameStartimeAsNextEvent(self):
        tenMin = timedelta(minutes = 10)
        nextEvent = Event("Next Event", self.now, self.now + tenMin)
        self.cal.addEvent(nextEvent)
        self.assertEqual(self.cal.getNextEvent(), nextEvent)

    def testGetNextEventRaisesNoEventsException(self):
        self.assertRaises(NoEventsException, self.cal.getNextEvent)

        fiveMin = timedelta(minutes = 5)
        tenMin = timedelta(minutes = 10)

        prevEventStartTime = self.now - tenMin
        prevEventEndTime = prevEventStartTime + fiveMin
        prevEvent = Event("Previous Event", prevEventStartTime,
            prevEventEndTime)
        self.cal.addEvent(prevEvent)
        self.assertRaises(NoEventsException, self.cal.getNextEvent)

    def testUpdateCalendar(self):
        pass


class EventTests(unittest.TestCase):
    def setUp(self):
        self.largeEvent = Event("large event", datetime(2015, 1, 2, 15, 30),
            datetime(2015, 1, 2, 16))
        self.middleEvent = Event("middle event", datetime(2014, 1, 2, 15, 30),
            datetime(2014, 1, 2, 16))
        self.smallEvent = Event("small event", datetime(2013, 1, 2, 15, 30),
            datetime(2013, 1, 2, 16))

    def testLessThan(self):
        self.assertLess(self.middleEvent, self.largeEvent)
        self.assertLess(self.smallEvent, self.middleEvent)
        self.assertLess(self.smallEvent, self.largeEvent)

    def testSortingList(self):
        eventsOrdered = [self.smallEvent, self.middleEvent, self.largeEvent]
        permutCorrectOrder = itertools.permutations(eventsOrdered)
        for i in permutCorrectOrder:
            eventList = [i[0], i[1], i[2]]
            self.assertEqual(sorted(eventList), eventsOrdered)


class CalendarParserTests(unittest.TestCase):
    def setUp(self):
        pass

    def testXXXX(self):
        pass


if __name__ == '__main__':
    unittest.main()
