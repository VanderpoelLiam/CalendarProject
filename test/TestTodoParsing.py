import unittest
import itertools
import parsedatetime as pdt
import shelve

from datetime import datetime, timedelta
from todoParser import *
from calendarParser import Event, Calendar


# class TodoTests(unittest.TestCase):
#     def setUp(self):
#         twoHrs = timedelta(hours = 2)
#
#         self.todo = Todo("hunt shrimp", datetime(2016, 6, 10),
#             twoHrs)
#         self.todoDiffName = Todo("smell cheese", datetime(2016, 6, 10),
#             twoHrs)
#         self.todoDiffTimespan = Todo("hunt shrimp", datetime(2016, 6, 10),
#             timedelta(hours = 6))
#         self.todoDiffDeadline = Todo("hunt shrimp", datetime(2011, 1, 1),
#             twoHrs)
#
#         self.filename = 'testTodoData'
#
#         self.largeTodo = Todo("large todo", datetime(2015, 1, 2, 15, 30),
#             twoHrs)
#         self.middleTodo = Todo("middle todo", datetime(2014, 1, 2, 15, 30),
#             twoHrs)
#         self.smallsTodo = Todo("small todo", datetime(2013, 1, 2, 15, 30),
#             twoHrs)
#
#     def tearDown(self):
#         TaskManager().clearTasks()
#         shelfFile = shelve.open(self.filename)
#         shelfFile.clear()
#         shelfFile.close()
#
#     def testEquals(self):
#         self.assertEqual(self.todo, Todo("hunt shrimp", datetime(2016, 6, 10),
#             timedelta(hours = 2)))
#         self.assertNotEqual(self.todo, self.todoDiffName)
#         self.assertNotEqual(self.todo, self.todoDiffTimespan)
#         self.assertNotEqual(self.todo, self.todoDiffDeadline)
#
#     def testCreateTask(self):
#         self.todo.createTask()
#         self.assertEqual(TaskManager().getNumTasks(), 1)
#         task = TaskManager().getTasks()[0]
#
#         self.assertIsNone(task.startTime)
#         self.assertIsNone(task.endTime)
#         self.assertEqual(task.name, self.todo.name)
#         self.assertEqual(task.deadline, self.todo.deadline)
#         self.assertEqual(task.timespan, self.todo.timespan)
#
#     def testBreakUpTodoTimespan80Min(self):
#         setattr(self.todo, "timespan", timedelta(minutes = 80))
#         self.todo.breakUpTodo()
#         self.assertEqual(TaskManager().getNumTasks(), 2)
#         for task in TaskManager().getTasks():
#             self.assertEqual(task.timespan, timedelta(minutes = 40))
#
#     def testBreakUpTodoTimespan100Min(self):
#         setattr(self.todo, "timespan", timedelta(minutes = 100))
#         self.todo.breakUpTodo()
#         self.assertEqual(TaskManager().getNumTasks(), 2)
#         for task in TaskManager().getTasks():
#             self.assertEqual(task.timespan, timedelta(minutes = 50))
#
#     def testBreakUpTodoTimespan220Min(self):
#         setattr(self.todo, "timespan", timedelta(minutes = 220))
#         self.todo.breakUpTodo()
#         self.assertEqual(TaskManager().getNumTasks(), 5)
#
#         for i, task in enumerate(TaskManager().getTasks()):
#             if i < 3:
#                 self.assertEqual(task.timespan, timedelta(minutes = 50))
#             else:
#                 self.assertEqual(task.timespan, timedelta(minutes = 35))
#
#     def testStoreTodo(self):
#         self.todo.storeTodo(self.filename)
#         shelfFile = shelve.open(self.filename)
#         storedTodos = list(shelfFile.values())
#         shelfFile.close()
#
#         self.assertEqual(len(storedTodos), 1)
#         self.assertEqual(storedTodos[0], self.todo)
#
#     def testLessThan(self):
#         self.assertLess(self.middleTodo, self.largeTodo)
#         self.assertLess(self.smallsTodo, self.middleTodo)
#         self.assertLess(self.smallsTodo, self.largeTodo)
#
#     def testSortingList(self):
#         todosOrdered = [self.smallsTodo, self.middleTodo, self.largeTodo]
#         permutCorrectOrder = itertools.permutations(todosOrdered)
#         for i in permutCorrectOrder:
#             todoList = [i[0], i[1], i[2]]
#             self.assertEqual(sorted(todoList), todosOrdered)
#
#
# class TodoManagerTests(unittest.TestCase):
#     def setUp(self):
#         now = datetime.now()
#         oneWkDate = now + timedelta(days = 7)
#         twoWkDate = now + timedelta(days = 14)
#         threeWkDate = now + timedelta(days = 21)
#         oneHr = timedelta(hours = 1)
#         threeHrs = timedelta(hours = 3)
#
#         self.t1Wk = Todo("todo 1wk", oneWkDate, oneHr)
#         self.t4Days = Todo("todo 4 days", now + timedelta(days = 4), oneHr)
#         self.t1WkAgo = Todo("todo 1wk ago", now - timedelta(days = 7), threeHrs)
#         self.t4DaysAgo = Todo("todo 4 days ago", now - timedelta(days = 4), threeHrs)
#         self.t2Wk = Todo("todo 2wks", twoWkDate, threeHrs)
#         self.t3Wk = Todo("todo 3wks", threeWkDate, threeHrs)
#
#         self.filename = 'testTodoData'
#
#     def tearDown(self):
#         TodoManager().clearTodos()
#
#         shelfFile = shelve.open(self.filename)
#         shelfFile.clear()
#         shelfFile.close()
#
#     def testAddTodo(self):
#         self.addThreeTodos()
#
#         self.assertIn(self.t1Wk, TodoManager())
#         self.assertIn(self.t2Wk, TodoManager())
#         self.assertIn(self.t3Wk, TodoManager())
#         self.assertEqual(3, TodoManager().getNumTodos())
#
#     def testRemoveTodo(self):
#         self.addThreeTodos()
#         TodoManager().removeTodo(self.t2Wk)
#
#         self.assertIn(self.t1Wk, TodoManager())
#         self.assertNotIn(self.t2Wk, TodoManager())
#         self.assertIn(self.t3Wk, TodoManager())
#         self.assertEqual(2, TodoManager().getNumTodos())
#
#     def testGetTodos(self):
#         self.addThreeTodos()
#         todos = TodoManager().getTodos()
#
#         self.assertIn(self.t1Wk, todos)
#         self.assertIn(self.t2Wk, todos)
#         self.assertIn(self.t3Wk, todos)
#         self.assertEqual(3, len(todos))
#
#     def testClearTodos(self):
#         self.addThreeTodos()
#         self.assertEqual(3, TodoManager().getNumTodos())
#
#         TodoManager().clearTodos()
#         self.assertEqual(0, TodoManager().getNumTodos())
#
#     def addThreeTodos(self):
#         TodoManager().addTodo(self.t1Wk)
#         TodoManager().addTodo(self.t2Wk)
#         TodoManager().addTodo(self.t3Wk)
#
#     def storeThreeTodos(self, filename):
#         self.t1Wk.storeTodo(filename)
#         self.t2Wk.storeTodo(filename)
#         self.t3Wk.storeTodo(filename)
#
#     def testUpdateTodoManagerAddsToTodoManager(self):
#         self.storeThreeTodos(self.filename)
#         self.t4Days.storeTodo(self.filename)
#
#         TodoManager().updateTodoManager(self.filename)
#         self.assertEqual(TodoManager().getNumTodos(), 2)
#
#         todos = TodoManager().getTodos()
#         self.assertIn(self.t1Wk, todos)
#         self.assertIn(self.t4Days, todos)
#
#     def testUpdateTodoManagerRemovesStoredTodos(self):
#         self.t1WkAgo.storeTodo(self.filename)
#         self.t4DaysAgo.storeTodo(self.filename)
#         self.storeThreeTodos(self.filename)
#
#         TodoManager().updateTodoManager(self.filename)
#         self.assertEqual(TodoManager().getNumStoredTodos(self.filename), 2)
#
#         storedTodos = TodoManager().getStoredTodos(self.filename)
#         self.assertNotIn(self.t1Wk, storedTodos)
#         self.assertNotIn(self.t1WkAgo, storedTodos)
#         self.assertNotIn(self.t4DaysAgo, storedTodos)
#
#     def testUpdateTodoManagerLeavesFutureTodosUnchanged(self):
#         self.storeThreeTodos(self.filename)
#
#         TodoManager().updateTodoManager(self.filename)
#         self.assertEqual(TodoManager().getNumStoredTodos(self.filename), 2)
#
#         storedTodos = TodoManager().getStoredTodos(self.filename)
#         self.assertIn(self.t2Wk, storedTodos)
#         self.assertIn(self.t3Wk, storedTodos)


class TodoParserTests(unittest.TestCase):
    def setUp(self):
        self.testTodoParser = TodoParser()
        self.todoDataMissingSemicolon = ["eat cabbage", "3 hours tomorrow"]
        self.todoDataNoDeadline = ["eat cabbage", "20 min", "asdfasf"]
        self.todoDataNoTimespan = ["eat cabbage", "slasdf", "tomorrow"]
        self.todoDataCorrectOrder = ["feed on souls of living", "3 hours",
            "next monday"]

        cal = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)
        now = datetime.now()
        self.timespan = timedelta(hours = 3)
        self.deadline = cal.parseDT("next monday", now)[0]

        self.todoFromTodoData = Todo("feed on souls of living",
            self.timespan, self.deadline)

    def testRaisesMissingSemiColonException(self):
        self.assertRaises(MissingSemiColonException,
            self.testTodoParser.parseTodoData, self.todoDataMissingSemicolon)

    def testRaisesDatetimeConversionException(self):
        self.assertRaises(DatetimeConversionException,
            self.testTodoParser.parseTodoData, self.todoDataNoDeadline)

    def testRaisesTimedeltaConversionException(self):
        self.assertRaises(TimedeltaConversionException,
            self.testTodoParser.parseTodoData, self.todoDataNoTimespan)

    # def testParsingAllRearragementsOfCorrectOrder(self):
    #     # permutCorrectOrder = itertools.permutations(self.todoDataCorrectOrder)
    #     # for i in permutCorrectOrder:
    #     #     todoData = [i[0], i[1], i[2]]
    #     #     testTodo = self.testTodoParser.parseTodoData(todoData)
    #     #     self.assertEqual(testTodo, self.todoFromTodoData)
    #
    # def testParseTimespan(self):
    #     timespan, timespanIndex = self.testTodoParser.parseTimespan(
    #         self.todoDataCorrectOrder, 0)
    #     self.assertEqual(timespan, self.timespan)
    #     self.assertEqual(timespanIndex, 1)
    #
    # def testParseDeadline(self):
    #     deadline, deadlineIndex = self.testTodoParser.parseDeadline(
    #         self.todoDataCorrectOrder, 0)
    #     self.assertEqual(deadline, self.deadline)
    #     self.assertEqual(deadlineIndex, 2)


class TaskTests(unittest.TestCase):
    def setUp(self):
        twoHrs = timedelta(hours = 2)
        self.largeTask = Task("large deadline and startTime",
            datetime(2015, 1, 2, 15, 30), datetime(2015, 1, 2, 16),
            twoHrs, datetime(2015, 3, 2, 15, 30))
        self.middleTask = Task("middle deadline and startTime",
            datetime(2014, 1, 2, 15, 30), datetime(2014, 1, 2, 16),
            twoHrs, datetime(2014, 3, 2, 15, 30))
        self.smallTask = Task("small deadline and startTime",
            datetime(2013, 1, 2, 15, 30), datetime(2013, 1, 2, 16),
            twoHrs, datetime(2013, 3, 2, 15, 30))

        self.largeEvent = Event("large event", datetime(2015, 1, 2, 15, 30),
            datetime(2015, 1, 2, 16))
        self.middleEvent = Event("middle event", datetime(2014, 1, 2, 15, 30),
            datetime(2014, 1, 2, 16))
        self.smallEvent = Event("small event", datetime(2013, 1, 2, 15, 30),
            datetime(2013, 1, 2, 16))

        self.testCalendar = Calendar(datetime(2016, 1, 1, 6))

        self.testTM = TaskManager()
        now = datetime.now()
        self.cal = Calendar(now)
        twoHrs = timedelta(hours = 2)
        twoDays = timedelta(days = 2)
        self.task1 = Task("task 1", None, None, twoHrs, now + twoDays)

    def tearDown(self):
        self.testTM.clearTasks()
        self.testTM.setCalendar(None)

    def testLessThanOtherTask(self):
        self.assertLess(self.middleTask, self.largeTask)
        self.assertLess(self.smallTask, self.middleTask)
        self.assertLess(self.smallTask, self.largeTask)

    def testSortingListOtherTasks(self):
        todosOrdered = [self.smallTask, self.middleTask, self.largeTask]
        permutCorrectOrder = itertools.permutations(todosOrdered)
        for i in permutCorrectOrder:
            todoList = [i[0], i[1], i[2]]
            self.assertEqual(sorted(todoList), todosOrdered)

    def testLessThanOtherEvent(self):
        self.assertLess(self.middleEvent, self.largeTask)
        self.assertLess(self.smallTask, self.middleEvent)
        self.assertLess(self.middleTask, self.largeEvent)
        self.assertLess(self.smallEvent, self.middleTask)

    def testSortingListOtherEvent(self):
        eventAndTasksOrdered = [self.smallTask, self.middleEvent,
            self.largeTask]
        taskAndEventOrdered = [self.smallEvent, self.middleTask,
            self.largeEvent]

        permutCorrectOrder1 = itertools.permutations(eventAndTasksOrdered)
        permutCorrectOrder2 = itertools.permutations(taskAndEventOrdered)
        for i in permutCorrectOrder1:
            eventList = [i[0], i[1], i[2]]
            self.assertEqual(sorted(eventList), eventAndTasksOrdered)
        for i in permutCorrectOrder2:
            eventList = [i[0], i[1], i[2]]
            self.assertEqual(sorted(eventList), taskAndEventOrdered)

    def testSetTimesStartTooEarly(self):
        task = Task("task 1", None, None, timedelta(minutes = 50),
            datetime(2016, 1, 2))
        startTime = datetime(2016, 1, 1, 6)

        self.assertRaises(StartTooEarlyException, task.setTimes, startTime,
            self.testCalendar)

        task = Task("task 1", None, None, timedelta(minutes = 50),
            datetime(2122, 1, 2))
        startTime = datetime(2122, 1, 1, 6)

        self.assertRaises(StartTooEarlyException, task.setTimes, startTime,
            self.testCalendar)

        task = Task("task 1", None, None, timedelta(minutes = 50),
            datetime(1995, 1, 2))
        startTime = datetime(1995, 1, 1, 6)

        self.assertRaises(StartTooEarlyException, task.setTimes, startTime,
            self.testCalendar)

    def testSetTimesEndTooLate(self):
        timespan = timedelta(minutes = 50)
        tenPM = datetime(2016, 1, 1, 22)
        startTime = tenPM - timespan / 2
        task = Task("task 1", None, None, timespan,
            datetime(2016, 1, 2))

        self.assertRaises(EndTooLateException, task.setTimes, startTime,
            self.testCalendar)

        tenPM = datetime(2122, 1, 1, 22)
        startTime = tenPM - timespan / 2
        task = Task("task 1", None, None, timespan,
            datetime(2122, 1, 2))

        self.assertRaises(EndTooLateException, task.setTimes, startTime,
            self.testCalendar)

        tenPM = datetime(1995, 1, 1, 22)
        startTime = tenPM - timespan / 2
        task = Task("task 1", None, None, timespan,
            datetime(1995, 1, 2))

        self.assertRaises(EndTooLateException, task.setTimes, startTime,
            self.testCalendar)

    def testSetTimesOverlapingEvents(self):
        timespan = timedelta(minutes = 50)
        task = Task("task 1", None, None, timespan,
            datetime(2016, 1, 2))
        startTime = datetime(2016, 1, 1, 10)
        endTime = startTime + timespan

        overlappingEvent1 = Event("event 1", endTime, endTime + timespan)
        self.testCalendar.addEvent(overlappingEvent1)

        self.assertRaises(OverlapingEventsException, task.setTimes, startTime,
            self.testCalendar)

        task = Task("task 1", None, None, timespan,
            datetime(1995, 1, 2))
        startTime = datetime(1995, 1, 1, 10)
        endTime = startTime + timespan

        overlappingEvent1 = Event("event 1", endTime, endTime + timespan)
        self.testCalendar.addEvent(overlappingEvent1)

        self.assertRaises(OverlapingEventsException, task.setTimes, startTime,
            self.testCalendar)

        task = Task("task 1", None, None, timespan,
            datetime(2122, 1, 2))
        startTime = datetime(2122, 1, 1, 10)
        endTime = startTime + timespan

        overlappingEvent1 = Event("event 1", endTime, endTime + timespan)
        self.testCalendar.addEvent(overlappingEvent1)

        self.assertRaises(OverlapingEventsException, task.setTimes, startTime,
            self.testCalendar)

        fourMin = timedelta(minutes = 4)
        newStartime = endTime + fourMin
        overlappingEvent2 = Event("event 1", newStartime, newStartime + timespan)
        self.testCalendar.clear()
        self.testCalendar.addEvent(overlappingEvent1)

        self.assertRaises(OverlapingEventsException, task.setTimes, startTime,
            self.testCalendar)

    def testSetTimesSetsStartAndEndTimes(self):
        timespan = timedelta(minutes = 50)
        task = Task("task 1", None, None, timespan,
            datetime(2016, 1, 2))
        startTime = datetime(2016, 1, 1, 10)
        endTime = startTime + timespan

        task.setTimes(startTime, self.testCalendar)
        self.assertEqual(startTime, task.startTime)
        self.assertEqual(endTime, task.endTime)

    def testScheduleTask(self):
        self.testTM.setCalendar(self.cal)
        self.testTM.addTask(self.task1)
        self.task1.schedueleTask()

        cal = self.testTM.getCalendar()
        self.assertEqual(1, cal.getNumEvents())
        self.assertIn(self.task1, cal)

    def testFindTimesCatchesStartTooEarlyException(self):
        task = Task("task 1", None, None, timedelta(minutes = 50),
            datetime(1995, 1, 2))
        self.testCalendar.now = datetime(1995, 1, 1, 6)

        task.findTimes(self.testCalendar)
        self.assertEqual(task.startTime, datetime(1995, 1, 1, 9))

    def testFindTimesCatchesEndTooLateException(self):
        timespan = timedelta(minutes = 50)
        tenPM = datetime(1991, 1, 1, 22)
        self.testCalendar.now = tenPM - timespan / 2
        task = Task("task 1", None, None, timespan,
            datetime(1991, 1, 3))

        task.findTimes(self.testCalendar)
        self.assertEqual(task.startTime, datetime(1991, 1, 2, 9))

    def testFindTimesCatchesOverlapingEventsException(self):
        timespan = timedelta(minutes = 50)
        fiveMin = timedelta(minutes = 5)
        task = Task("task 1", None, None, timespan,
            datetime(1999, 1, 2))
        self.testCalendar.now = datetime(1999, 1, 1, 9, 30)
        eventStart = self.testCalendar.now + timespan
        eventEnd = eventStart + timespan

        overlappingEvent1 = Event("event 1", eventStart, eventEnd)
        self.testCalendar.addEvent(overlappingEvent1)

        task.findTimes(self.testCalendar)
        self.assertEqual(task.startTime, overlappingEvent1.endTime + fiveMin)


        startTime = overlappingEvent1.endTime + fiveMin
        endTime = startTime + timespan
        overlappingEvent2 = Event("event 2", startTime, endTime)
        self.testCalendar.addEvent(overlappingEvent2)

        task.findTimes(self.testCalendar)
        self.assertEqual(task.startTime, overlappingEvent2.endTime + fiveMin)

    def testFindTimesCannotFindTimes(self):
        timespan = timedelta(minutes = 50)
        fiveMin = timedelta(minutes = 5)
        task = Task("task 1", None, None, timespan,
            datetime(2022, 1, 2, 3))

        self.testCalendar.now = datetime(2022, 1, 2, 1)

        eventStart = datetime(2022, 1, 2, 1, 30)
        eventEnd = eventStart + timespan
        event = Event("event 1", eventStart, eventEnd)

        self.assertRaises(InsufficientTimeException, task.findTimes,
            self.testCalendar)


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.testTM = TaskManager()
        now = datetime.now()
        self.cal = Calendar(now)
        twoHrs = timedelta(hours = 2)
        twoDays = timedelta(days = 2)

        self.task1 = Task("task 1", None, None, twoHrs, now + twoDays)
        self.task2 = Task("task 2", None, None, twoHrs, now + twoDays)
        self.task3 = Task("task 3", None, None, twoHrs, now + twoDays)

    def tearDown(self):
        self.testTM.clearTasks()
        self.testTM.setCalendar(None)

    def testSetGetCalendar(self):
        self.assertIsNone(self.testTM.getCalendar())
        self.testTM.setCalendar(self.cal)
        self.assertEqual(self.testTM.getCalendar(), self.cal)

    def testScheduleTasks(self):
        self.testTM.addTask(self.task1)
        self.testTM.addTask(self.task2)
        self.testTM.addTask(self.task3)

        self.assertRaises(NoCalendarInstanceException,
            self.testTM.schedueleTasks)

        self.testTM.setCalendar(self.cal)
        self.testTM.schedueleTasks()
        for task in self.testTM.getTasks():
            self.assertIsNotNone(task.startTime)
            self.assertIsNotNone(task.endTime)


if __name__ == '__main__':
    unittest.main()
