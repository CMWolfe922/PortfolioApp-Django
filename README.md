# PortfolioApp-Django

Creating an app to host my porfolio using django and heroku

## Instructions For Managing Django Project

__Project App: Models__
- To store data to display on a website I need a database
- Django comes with an ORM built-in so I don't need to worry about SQL
  - an ORM is a program that allows **classes to create tables** and **class attributes that correspond to columns** in that table and the **class instances are the rows**
- When using an ORM the **classes built** representing the database tables **are called models**
  - In Django, these live in the **models.py** module inside each app created.

*Inside my projects app I will only need one table to store different projects that I can display to users.*
##### Which means just one model in models.py
I will create a **Projects** model with these fields:
- **title** short string field to hold the name of the project
- **description** larger string field describing project scope
- **technology** String field limited to a select number of choices
- **image** image field that holds the path to where the image is stored.

###### Example:
```sh
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=20)
    image = models.FilePathField(path="/img")
```
--> Side note, Django comes with many more built in field types. These are just 3 of the basics. CharField needs a max_length, TextField doesn't require a max and the FilePath requires a path to a file name.
--> Also, By default Django uses SQLite3 but I can add PostgreSQL and or MySQL to this project. But to start the process of creating the Database, I need to create a migration.

__Managing the Migration__

- Process of creating the database:
  - Create a __Migration__
  - This is a file with a migration class
  - It gives Django rules on how and what changes to make to the database.

_In order to do this, I need to type the following into the command prompt/bash shell_

```sh
$ python manage.py makemigrations projects
```

Now that the migration file has been created, I need to apply it. this creates the db by using the migrate command.

`python manage.py migrate projects'


### Use Shell to Create Project Instances:

To create instances of our Project class, we’re going to have to use the Django shell. The Django shell is similar to the Python shell but allows you to access the database and create entries. To access the Django shell, we use another Django management command:

`python manage.py shell`

- Next import my models
`>>> from projects.models import Project`

*Now I can create a new project with the following attributes:*
- name: My First Project
- description: A Web development project
- technology: Django
- image: img/prject1.png

**Now in order to do this, I have to use the shell to create an instance of the project using Django's shell**
```sh
>> p1 = Project(
    title='My First Project',
    description='A Web development project',
    technology='Django',
    image='img/project1.png'
)
>> p1.save()
```

that creates an entry into my projects table and saves it to the database which now allows me to display on my portfolio site.

I am goign to add two more fake projects just for now.
```sh
>> p2 = Project(
    title='My second Project',
    description='Another web development project',
    technology='Flask',
    image='img/project2.png'
)
>> p2.save()
>> p3 = Project(
    title='My third Project',
    description='My third and final development project fake entry',
    technology='Django',
    image='img/project3.png'
)
```

#### END OF THIS SECTION
Now I know how to create apps, models, migrate those models, and add entrys to the database using Django's shell.

==============
==============

## Left off at Project App: Views
