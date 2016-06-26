# Project Attendance using Outside in TDD and Django

This project try to save the attendance of a group of students registered in courses.
This action is done by a professor.

To explore the functionalities you have to create a admin user,
log in as admin (/login/admin) and create an user, courses, students.

Sometimes I had to break the rules but I tried to go in this order of implementation:
- functional test (using page objects)
- templates
- urls
- test views
- views
- test models
- models

# Run in development

To run this project you need to create a virtualenv with python 3 and have bower installed.
This project use sqlite as database if you want change it to mysql or postgresql specially if
you want to use in production.

```
$ pip install -r requirements.txt
$ bower install
```

# License

MIT
