# CalendarProject

This project is the backend for a optimized task scheduler. It uses the [google calendar api](https://developers.google.com/calendar/) to get my current commitments, then parses the list of tasks that I email to myself using the [gmail api](https://developers.google.com/gmail/api/). These tasks are broken up into time slots of 50 minutes or less, then scheduled such that they can be completed as early as possible before the due date. My calendar is then updated with my new schedule. 
