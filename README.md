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
