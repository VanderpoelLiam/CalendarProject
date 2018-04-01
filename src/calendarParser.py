import httplib2
import datetime
import dateutil.parser

from googleapiclient import discovery
from googleParser import Parser
from datetime import datetime, timedelta


class Calendar:
    def __init__(self, now):
        self.events = []
        self.now = now

    def __iter__(self):
        return iter(self.events)

    def __contains__(self, event):
        return self.events.__contains__(event)

    def addEvent(self, event):
        if event.startTime == None or event.endTime == None:
            raise TimesNotInitialized("Start and End Times for the Event must"
                + " be set before adding it to the calendar")
        self.events.append(event)
        self.events = sorted(self.events)

    def removeEvent(self, event):
        self.events.remove(event)

    def getNumEvents(self):
        return len(self.events)

    def clear(self):
        self.events.clear()

    def getNextEvent(self, timeMin = None):
        if timeMin == None:
            timeMin = self.now

        for event in self:
            if event.startTime >= timeMin:
                return event
        raise NoEventsException("There are no events after %s"
            % timeMin.strftime("%H:%M %a %d %b %Y"))

    def updateCalendar(self):
        pass


class Event:
    def __init__(self, name, startTime, endTime):
        self.name = name
        self.startTime = startTime
        self.endTime = endTime

    def __lt__(self, other):
        if isinstance(other, Event):
            return self.startTime < other.startTime
        else:
            return AttributeError


class CalendarParser(Parser):
    now = datetime.now()
    twoWks = now + timedelta(days = 14)

    def parseCalendar(self, timeMin = now, timeMax = twoWks):
        """Produces a Calendar object that is an aggregation of Event objects
        from now until timeMax.
        Inputs:
            now: datetime.datetime
                Current datetime
            timeMax: datetime.datetime
                Until when to check for events
        Returns:
            calendar: Calendar
                Aggregation of Event objects
        """
        calGoogle = self.__getCalendar()
        cal = Calendar(CalendarParser.now)

        timeMinGF = self.__toGoogleFormat(timeMin)
        timeMaxGF = self.__toGoogleFormat(timeMax)
        # info on format eventsResult: https://developers.google.com/google-apps/calendar/v3/reference/events/list#response
        eventsResult = calGoogle.events().list(
            calendarId='primary', timeMin=timeMinGF, timeMax=timeMaxGF, singleEvents=True,
            orderBy='startTime').execute()
        # list of events in format: https://developers.google.com/google-apps/calendar/v3/reference/events#resource
        events = eventsResult.get('items', [])
        for event in events:
            name = event.get('summary')
            try:
                startTime = self.__fromGoogleFormat(event['start'].get('dateTime'))
                endTime   = self.__fromGoogleFormat(event['end'].get('dateTime'))
                event = Event(name, startTime, endTime)
                cal.addEvent(event)
            except Exception as e:
                pass
        return cal

    def __getCalendar(self):
        """Returns:
            calendar: Authorized Calendar API service instance.
                A way for me to access my calendar"""
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/calendar-python-event-schedueler.json
        credentials = super().getCredentials(
            'calendar-python-event-schedueler.json',
             'Google Calendar Event Parser',
              'https://www.googleapis.com/auth/calendar')
        http = credentials.authorize(httplib2.Http())
        calendar = discovery.build('calendar', 'v3', http=http)

        return calendar

    def __toGoogleFormat(self, dt):
        """Converts a datetime.datetime to required format for timeMax or timeMin
        methods of events list function: RFC3339 timestamp with mandatory time zone
        offset, e.g., 2011-06-03T10:00:00-07:00
        """
        fromZone = dateutil.tz.tzlocal()
        toZone = dateutil.tz.tzutc()
        # tell datetime it is in local time
        localDatetime = dt.replace(tzinfo = fromZone)
        # convert to UTC time
        utcDatetime = localDatetime.astimezone(toZone)
        googleFormat = utcDatetime.isoformat() # convert to string RFC3339 timestamp

        return googleFormat

    def __fromGoogleFormat(self, dt):
        """Converts RFC3339 timestamp with mandatory time zone offset to date as a
        tuple in ('hh:mm', 'dd/mm/yy') format. See toGoogleFormat() for more details
        on RFC3339 format.
        """
        # fromZone = dateutil.tz.tzutc()
        # toZone = dateutil.tz.tzlocal()
        #
        # # converts string RFC3339 timestamp to datetime with no timezone info
        # datetime = dateutil.parser.parse(dt)
        # # tell datetime it is in UTC time
        # utcDatetime = datetime.replace(tzinfo = fromZone)
        # # convert to local time
        # localDatetime = utcDatetime.astimezone(toZone)
        # # removes timezone awareness of datetime
        # localDatetime = localDatetime.replace(tzinfo = None)
        datetime = dateutil.parser.parse(dt).replace(tzinfo = None)

        return datetime


class NoEventsException(Exception):
    pass


class TimesNotInitialized(Exception):
    pass
