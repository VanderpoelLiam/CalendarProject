from calendarParser import CalendarParser, Calendar, Event
from todoParser import TodoParser, TodoManager, Todo, Task, TaskManager
from datetime import datetime


cal = CalendarParser().parseCalendar()

TodoParser().parseTodos()

TodoManager().createTasks()

TaskManager().setCalendar(cal)
TaskManager().schedueleTasks()

for event in cal:
    print("Name: %s" % event.name)
    print("Start: %s" % event.startTime)
    print("End: %s\n" % event.endTime)

# TaskManager().updateCalendar()

# cal.updateCalendar(TaskManager())
def createCalEvent(calendar, name, times):
    """Create a new event in my google calendar
    Inputs:
        todo: tuple
            Parameters of my event
        calendar: Authorized Calendar API service instance.
            A way for me to access my calendar
        times: tuple OR False
            Start and end datetimes of event, or False if event cannot be
            schedueled
    Outputs:
        Directly creates the event in google calendar, or returns the name(s)
        of the event that cannot be created with given parameters
    """
    logging.debug("Running createCalEvent()")

    if times:
        # can scheduele event
        startTime, endTime = times
        start = toReadable(startTime)
        print("Schedueling event: %s at %s" % (name, start))
        startTime = toGoogleFormat(startTime)
        endTime = toGoogleFormat(endTime)

        event = {'summary': name,
                'start': {'dateTime': startTime},
                'end': {'dateTime': endTime}
                }
        #creates event in calendar
        calEvent = calendar.events().insert(calendarId='primary',
                   sendNotifications=True, body=event).execute()
    else:
        # if no availible times
        print("Unable to scheduele event %s" % name)
