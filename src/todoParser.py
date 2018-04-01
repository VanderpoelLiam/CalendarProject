import httplib2
import dateutil.parser
import base64
import parsedatetime as pdt
import email
import shelve

from datetime import datetime, timedelta
from googleapiclient import discovery, errors
from googleParser import Parser
from calendarParser import Event, NoEventsException


class Todo:
    fiftyMin = timedelta(minutes = 50)
    hundrdMin =  timedelta(minutes = 100)
    def __init__(self, name, deadline, timespan):
        """
        name: string
            name of todo.
        deadline: datetime.datetime
            when todo must be completed.
        timespan: datetime.timedelta
            approximately how long todo will take to complete.
        """
        self.name = name
        self.deadline = deadline
        self.timespan = timespan

    def __eq__(self, other):
        if not isinstance(other, Todo):
            return False
        return self.name == other.name and \
            self.deadline == other.deadline and \
            self.timespan == other.timespan

    def __hash__(self):
        return 3 * hash(self.name) + 5 * hash(self.deadline) + \
            7 * hash(self.timespan)

    def __lt__(self, other):
        if isinstance(other, Todo):
            return self.deadline < other.deadline
        else:
            return AttributeError

    def key(self):
        """Key used to access Todo in shelve file
        """
        return self.name + " " + self.getDeadline()

    def breakUpTodo(self):
        """Requires Todo.timespan greater 50 min
        """
        newTimespan = self.timespan

        while newTimespan > Todo.hundrdMin:
            newTimespan -= Todo.fiftyMin
            TaskManager().addTask(
                Task(self.name, None, None, Todo.fiftyMin, self.deadline))

        if newTimespan <=  Todo.hundrdMin:
            task = Task(self.name, None, None, newTimespan / 2, self.deadline)
            TaskManager().addTask(task)
            TaskManager().addTask(task)

    def getDeadline(self):
        """Returns deadline as formatted string:
            'Hour:Minute Weekday Day Month Year'
        """
        return self.deadline.strftime("%H:%M %a %d %b %Y")

    def storeTodo(self, filename = 'storedTodoData'):
        shelfFile = shelve.open(filename)
        shelfFile[self.key()] = self
        shelfFile.close()

    def createTask(self):
        """Requires Todo.deadline less twoWks from now and
            Todo.timespan less/equal 50 min
        """
        TaskManager().addTask(Task(self.name, None, None, self.timespan,
            self.deadline))


class TodoManager:
    __instance = None
    __todos = []
    now = datetime.now()
    twoWks = now + timedelta(days = 14)

    def __new__(cls):
        # enforces sigleton design pattern
        if TodoManager.__instance is None:
            TodoManager.__instance = object.__new__(cls)
        return TodoManager.__instance

    def __contains__(self, todo):
        return TodoManager.__todos.__contains__(todo)

    def addTodo(self, todo):
        TodoManager.__todos.append(todo)

    def removeTodo(self, todo):
        TodoManager.__todos.remove(todo)

    def getTodos(self):
        return TodoManager.__todos

    def clearTodos(self):
        TodoManager.__todos.clear()

    def getNumTodos(self):
        return len(TodoManager.__todos)

    def updateTodoManager(self, filename = 'storedTodoData'):
        """Adds stored Todo with Todo.deadline less than twoWks to TodoManager,
        removes all moved Todo and those with Todo.deadline less/equal to
        TodoManager.now
        """

        toRemove = []
        for todo in self.getStoredTodos(filename):
            if todo.deadline < TodoManager.twoWks:
                TodoManager().addTodo(todo)
                toRemove.append(todo)
                continue
            if todo.deadline <= TodoManager.now:
                toRemove.append(todo)

        shelfFile = shelve.open(filename)
        for todo in toRemove:
            del shelfFile[todo.key()]
        shelfFile.close()

    def getStoredTodos(self, filename = 'storedTodoData'):
        storedTodos = []
        shelfFile = shelve.open(filename)
        for key in shelfFile:
            storedTodos.append(shelfFile[key])
        shelfFile.close()

        return storedTodos

    def getNumStoredTodos(self, filename = 'storedTodoData'):
        return len(self.getStoredTodos(filename))

    def createTasks(self):
        """Creates one or more Task objects for each Todo in TodoManager that
        need to be assigned startTime/endTime by TaskManager
        """
        self.updateTodoManager()
        for todo in self.getTodos():
            if todo.deadline >= TodoManager.twoWks:
                todo.storeTodo()
            if todo.timespan > Todo.fiftyMin:
                todo.breakUpTodo()
            else:
                todo.createTask()


class TodoParser(Parser):
    def parseTodos(self):
        """Parses todos from email and adds them to the TodoManager
        """
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/gmail-python-get-todos.json
        credentials = super().getCredentials('gmail-python-get-todos',
            'Gmail Get Todos',
            'https://www.googleapis.com/auth/gmail.modify')
        http = credentials.authorize(httplib2.Http())
        gmail = discovery.build('gmail', 'v1', http=http)

        emails = self.__listMessagesMatchingQuery(gmail, 'me',
            'from:me;subject:todo;is:unread')

        for email in emails:
            msg_id = email['id']
            rawMessage = self.__getMimeMessage(gmail, 'me', msg_id)
            body = self.__getEmailBody(rawMessage)
            todoData = self.__getTodoData(body)
            self.parseTodoData(todoData)
            self.__markEmailsAsRead(gmail, 'me', msg_id)

    def __listMessagesMatchingQuery(self, service, user_id, query=''):
      """List all Messages of the user's mailbox matching the query.
      Inputs:
        service: Authorized Gmail API service instance.
        user_id: string.
            User's email address. The special value "me" can be used to indicate
            the authenticated user.
        query: string.
            Search operators to filter messages returned,
            see 'https://support.google.com/mail/answer/7190?hl=en' for details.

      Outputs:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
      """
      try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
          messages.extend(response['messages'])

        while 'nextPageToken' in response: # go through all messages
          page_token = response['nextPageToken']
          response = service.users().messages().list(userId=user_id, q=query,
                                             pageToken=page_token).execute()
          messages.extend(response['messages'])

        return (messages)
      except errors.HttpError as error:
        print ('An error occurred: %s' % error)

    def __markEmailsAsRead(self, service, user_id, msg_id):
        """Marks email with id msg_id as read
        Inputs:
          service: Authorized Gmail API service instance.
          user_id: string.
              User's email address. The special value "me" can be used to indicate
              the authenticated user.
          msg_id: string.
              The ID of the Message required.
        No outputs."""
        try:
            msg_labels = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
            message = service.users().messages().modify(userId=user_id, id=msg_id,
                                                        body=msg_labels).execute()

        except errors.HttpError as error:
            print ('An error occurred: %s' % error)

    def __getMimeMessage(self, service, user_id, msg_id):
      """Get a Message and use it to create a MIME Message.
      Inputs:
        service: Authorized Gmail API service instance.
        user_id: string.
            User's email address. The special value "me" can be used to indicate
            the authenticated user.
        msg_id: string.
            The ID of the Message required.
      Returns:
        A MIME Message, consisting of data from Message.
      """
      try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='raw').execute()

        msg_str = base64.urlsafe_b64decode(message['raw'].replace('-_', '+/').encode('ASCII'))

        mime_msg = email.message_from_bytes(msg_str)

        return mime_msg
      except errors.HttpError as error:
        print ('An error occurred: %s' % error)

    def parseTodoData(self, todoData):
        """Produces a list of todos from the raw email message
        Inputs:
            todoData: list
                cleaned up strings of todo data
        """
        cal = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)
        now = datetime.now()
        numDataParts = len(todoData)

        if numDataParts % 3 != 0:
            raise MissingSemiColonException("Include a ';' after each section")

        index = 0
        while(index < numDataParts):
            name = todoData[index]

            timespan = cal.parseDT(
                todoData[index + 1], sourceTime=datetime.min)[0] - datetime.min

            if timespan == timedelta():
                raise TimedeltaConversionException(
                    "Timespan cannot be converted to timedelta object")

            deadline = cal.parseDT(todoData[index + 2], now)[0]

            if deadline <= now:
                raise DatetimeConversionException(
                    "Deadline cannot be converted to datetime object")

            TodoManager().addTodo(Todo(name, deadline, timespan))
            index += 3

    # def parseTimespan(self, todoData, index):
    #     """
    #     Inputs:
    #         todoData: list
    #             cleaned up strings of todo data
    #         index: integer
    #             current index in todoData list
    #
    #     Outputs:
    #         timespanData: tuple
    #             timespan: datetime.timedelta
    #                 approximate timespan for todo
    #             timespanIndex: integer
    #                 index of timespan data in todoData relative to index
    #
    #         raises TimedeltaConversionException if cannot find a timespan
    #     """
    #     cal = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)
    #
    #     for i in range(3):
    #         timespan = cal.parseDT(
    #             todoData[index + i],
    #             sourceTime=datetime.min)[0] - datetime.min
    #
    #         if timespan != timedelta():
    #             timespanIndex = i
    #             break
    #
    #     if timespan == timedelta():
    #         raise TimedeltaConversionException(
    #             "Timespan cannot be converted to timedelta object")
    #
    #     return (timespan, timespanIndex)
    #
    # def parseDeadline(self, todoData, index):
    #     """
    #     Inputs:
    #         todoData: list
    #             cleaned up strings of todo data
    #         index: integer
    #             current index in todoData list
    #
    #     Outputs:
    #         deadlineData: tuple
    #             deadline: datetime.datetime
    #                 deadline for todo
    #             deadlineIndex: integer
    #                 index of deadline data in todoData relative to index
    #
    #         raises DatetimeConversionException if cannot find a datetime
    #     """
    #     cal = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)
    #     now = datetime.now()
    #
    #     for i in range(3):
    #         deadline = cal.parseDT(todoData[index + i], now)[0]
    #         print(deadline)
    #
    #         if deadline > now:
    #             deadlineIndex = i
    #             break
    #
    #     if not(deadline > now):
    #         raise DatetimeConversionException(
    #             "Deadline cannot be converted to datetime object")
    #
    #     return (deadline, deadlineIndex)

    def __getEmailBody(self, rawMessage):
        """Gets email body as a string from raw email message
        """
        for i, part in enumerate(rawMessage.walk()):
            if part.get_content_type() == 'text/plain':
                # gets email body as string
                body = part.get_payload(decode=True).decode("utf-8")
                return(body)

    def __getTodoData(self, body):
        """
        Removes'\r\n' from the email body, and splits up body by ';'

        Inputs:
            body: string
                email body

        Outputs:
            todoData: list
                cleaned up strings of todo data
        """
        splitBody = body.split(';')
        todoData = []
        for sec in splitBody:
            sec = sec.strip("\r\n")
            if len(sec) > 0:
                todoData.append(sec)

        return todoData


class Task(Event, Todo):
    def __init__(self, name, startTime, endTime, timespan, deadline):
        Event.__init__(self, name, startTime, endTime)
        self.timespan = timespan
        self.deadline = deadline

    def __lt__(self, other):
        if isinstance(other, Task):
            return Todo.__lt__(self, other)
        if isinstance(other, Event):
            return Event.__lt__(self, other)
        else:
            return AttributeError

    def schedueleTask(self):
        cal = TaskManager().getCalendar()
        self.findTimes(cal)
        cal.addEvent(self)
        TaskManager().setCalendar(cal)

    def findTimes(self, calendar):
        startTime = calendar.now
        while startTime + self.timespan < self.deadline:
            try:
                self.setTimes(startTime, calendar)
            except StartTooEarlyException:
                startTime = datetime(startTime.year, startTime.month,
                    startTime.day, 9)
            except EndTooLateException:
                nextDay = startTime + timedelta(days = 1)
                startTime = datetime(nextDay.year, nextDay.month,
                    nextDay.day, 9)
            except OverlapingEventsException:
                nextEvent = calendar.getNextEvent(startTime)
                eventEndTime = nextEvent.endTime
                fiveMin = timedelta(minutes = 5)
                startTime = eventEndTime + fiveMin
            else:
                break


        if self.startTime is None:
            raise InsufficientTimeException("Unable to scheduele task before" +
                "the deadline")

    def setTimes(self, startTime, calendar):
        """Checks if Task can be schedueled at startTime. Raises appropriate
        exceptions if startTime violates any invariants. Else sets
        self.startTime to startTime, and self.endTime to startTime +
        self.timespan.
        """
        nineAM = datetime(startTime.year, startTime.month, startTime.day, 9)
        if startTime < nineAM:
            raise StartTooEarlyException("Cannot find time before 9:00")

        endTime = startTime + self.timespan
        tenPM = datetime(startTime.year, startTime.month, startTime.day, 22)
        if endTime > tenPM:
            raise EndTooLateException("Cannot find time after 22:00")

        try:
            eventStartime = calendar.getNextEvent(startTime).startTime
            fiveMin = timedelta(minutes = 5)
            if endTime > eventStartime - fiveMin:
                raise OverlapingEventsException("Cannot find time less than " +
                    "5 min before next event")
        except NoEventsException:
            pass

        self.startTime = startTime
        self.endTime = self.startTime + self.timespan


class TaskManager:
    __instance = None
    __calendar = None
    __tasks = []
    def __new__(cls):
        # enforces sigleton design pattern
        if TaskManager.__instance is None:
            TaskManager.__instance = object.__new__(cls)
        return TaskManager.__instance

    def __contains__(self, task):
        return TaskManager.__tasks.__contains__(task)

    def addTask(self, task):
        TaskManager.__tasks.append(task)

    def removeTask(self, task):
        TaskManager.__tasks.remove(task)

    def getTasks(self):
        return TaskManager.__tasks

    def clearTasks(self):
        TaskManager.__tasks.clear()

    def getNumTasks(self):
        return len(TaskManager.__tasks)

    def setCalendar(self, calendar):
        TaskManager.__calendar = calendar

    def getCalendar(self):
        return TaskManager.__calendar

    def schedueleTasks(self):
        if self.getCalendar() is None:
            raise NoCalendarInstanceException("Set associated Calendar " +
                "object in order to scheduele Tasks")

        for task in sorted(self.getTasks()):
            task.schedueleTask()


class MissingSemiColonException(Exception):
    pass


class DatetimeConversionException(Exception):
    pass


class TimedeltaConversionException(Exception):
    pass


class StartTooEarlyException(Exception):
    pass


class EndTooLateException(Exception):
    pass


class OverlapingEventsException(Exception):
    pass


class NoCalendarInstanceException(Exception):
    pass


class InsufficientTimeException(Exception):
    pass
