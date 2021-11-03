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

## Project App: Views
Now that I created the projects to display on my portfolio site. I need to create view functions to send the data from the database to the html templates.

- In the projects app, I am going to create two different views:
1. An index view that shows a snippet of information about each project
2. a detail view that shows more information on a particular topic.

First, I will start with the index view because the logic is simpler.
- to do that I need to import the `Project` class from models.py and create a function `project_index()` that renders a template called `project_index.html`
- inside of the the body of the function, you'll make a Django ORM query to select all objects in the Project table:

```sh
from django.shortcuts import render
from projects.models import Project

def project_index(request):
    projects = Project.all()
    context = {
    'projects': projects
    }
    return render(request, 'project_index.html', context)
```

--- Inside that block of code there is a lot that is happening:
1. Line 5: creates a query for all objects in projects table. With a query you can use simple commands that allows you to create, retrieve, update, or delete objects (or rows) in your database.
   - a database query returns a collection of all objects that match the query, known as a Queryset. In this case I needed all the objects in the table so it will return a collection of all projects.
2. Line 6: defines a dictionary `context`, this is used to send the queryset containg all project data. The context variable is used to send information to our template.
- **EVERY VIEW FUNCTION NEEDS TO HAVE A CONTEXT DICTIONARY**

**Now we create project_detail func:**
```sh
def project_detail(request, pk):

    project = Project.objects.get(pk=pk)

    context = {

        'project': project

    }

    return render(request, 'project_detail.html', context)
```
#### I NEED TO ADD NOTES ABOVE ABOUT PROJECT DETAIL FUNC FOR FUTURE REFERENCE.
I am rushing, so I am only going to put minimum notes from here, just on what happens next or copy and paste code examples.
**==============================================================**

- **Now we hook up the view functions to URLs**
1. create a urls.py file in the projects directory
```sh
from django.urls import path

from . import views


urlpatterns = [

    path("", views.project_index, name="project_index"),

    path("<int:pk>/", views.project_detail, name="project_detail"),

]
```
#### Now I need to hook these up to the urls.py file in main folder

- add the following line of code in the main urls file:
  - `path('projects/', include("projects.urls"))`
- That line of code goes under `urlpatterns` in the main directory.
The file should look like this when complete:
```sh
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("projects/", include("projects.urls")),
]
```

This line of code includes all the URLs in the projects app but means they are accessed when prefixed by projects/. There are now two full URLs that can be accessed with our project:


    localhost:8000/projects: The project index page
    localhost:8000/projects/3: The detail view for the project with pk=3


## FINAL STEP: create two templates
### Projects App: Templates
1. The `project_index` template
2. the `proect_detail` template

As we’ve added Bootstrap styles to our application, we can use some pre-styled components to make the views look nice. Let’s start with the project_index template.

For the project_index template, you’ll create a grid of Bootstrap cards, with each card displaying details of the project. Of course, we don’t know how many projects there are going to be. In theory, there could be hundreds to display.

We don’t want to have to create 100 different Bootstrap cards and hard-code in all the information to each project. Instead, we’re going to use a feature of the Django template engine: for loops.

Using this feature, you’ll be able to loop through all the projects and create a card for each one. The for loop syntax in the Django template engine is as follows:

```sh
{% for project in projects %}
{# Do something... #}
{% endfor %}

```

Now that you know how for loops work, you can add the following code to a file named `projects/templates/project_index.html`:

```sh
{% extends "base.html" %}

{% load static %}

{% block page_content %}

<h1>Projects</h1>

<div class="row">

{% for project in projects %}

    <div class="col-md-4">

        <div class="card mb-2">

            <img class="card-img-top" src="{% static project.image %}">

            <div class="card-body">

                <h5 class="card-title">{{ project.title }}</h5>

                <p class="card-text">{{ project.description }}</p>

                <a href="{% url 'project_detail' project.pk %}"

                   class="btn btn-primary">

                    Read More

                </a>

            </div>

        </div>

    </div>

    {% endfor %}

</div>

{% endblock %}
```


There’s a lot of Bootstrap HTML here, which is not the focus of this tutorial. Feel free to copy and paste and take a look at the Bootstrap docs if you’re interested in learning more. Instead of focusing on the Bootstrap, there are a few things to highlight in this code block.

In line 1, we extend base.html as we did in the Hello, World! app tutorial. I’ve added some more styling to this file to include a navigation bar and so that all the content is contained in a Bootstrap container. The changes to base.html can be seen in the source code on GitHub.

On line 2, we include a {% load static %} tag to include static files such as images. Remember back in the section on Django models, when you created the Project model. One of its attributes was a filepath. That filepath is where we’re going to store the actual images for each project.

Django automatically registers static files stored in a directory named static/ in each application. Our image file path names were of the structure: img/<photo_name>.png.

When loading static files, Django looks in the static/ directory for files matching a given filepath within static/. So, we need to create a directory named static/ with another directory named img/ inside. Inside img/, you can copy over the images from the source code on GitHub.

On line 6, we begin the for loop, looping over all projects passed in by the context dictionary.

Inside this for loop, we can access each individual project. To access the project’s attributes, you can use dot notation inside double curly brackets. For example, to access the project’s title, you use {{ project.title }}. The same notation can be used to access any of the project’s attributes.

On line 9, we include our project image. Inside the src attribute, we add the code {% static project.image %}. This tells Django to look inside the static files to find a file matching project.image.

The final point that we need to highlight is the link on line 13. This is the link to our project_detail page. Accessing URLs in Django is similar to accessing static files. The code for the URL has the following form:

```sh
{% url '<url path name>' <view_function_arguments> %}
```

In this case, we are accessing a URL path named project_detail, which takes integer arguments corresponding to the pk number of the project.

With all that in place, if you start the Django server and visit localhost:8000/projects, then you should see something like this:
![image of how our projects portfolio should look](https://files.realpython.com/media/Screenshot_2018-12-16_at_16.46.36.a71c744f096a.png)


#### With the project_index.html template in place, it’s time to create the project_detail.html template. The code for this template is below:

```sh
{% extends "base.html" %}
{% load static %}

{% block page_content %}
<h1>{{ project.title }}</h1>
<div class="row">
    <div class="col-md-8">
        <img src="{% static project.image %}" alt="" width="100%">
    </div>
    <div class="col-md-4">
        <h5>About the project:</h5>
        <p>{{ project.description }}</p>
        <br>
        <h5>Technology used:</h5>
        <p>{{ project.technology }}</p>
    </div>
</div>
{% endblock %}
```


The code in this template has the same functionality as each project card in the project_index.html template. The only difference is the introduction of some Bootstrap columns.

If you visit localhost:8000/projects/1, you should see the detail page for that first project you created:

In this section, you learned how to use models, views, and templates to create a fully functioning app for your personal portfolio project. Check out the source code for this section on GitHub.

**=============================================================**
# New Section:
## Create a Blog
- posts can be created, updated, deleted and shared
- Display posts ti the user as either an index view or a detail view.
- assign categories to posts
- allow users to comment on posts.

This section will be about how to use the Django Admin interface, which is where I'll create, update and delete posts and categories as necessary.

- Before I can start bbuilding out this portion of the site. I need to create another django app inside the my_portfolio_app directory.
- **To do this go to command line/bash shell and type**
  - `python manage.py startapp blog`
*make sure when adding an app, to be in the main project directory*

**now just like before, I need to add the blog app to `INSTALLED_APPS` in `settings.py`**

```sh
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "projects",
    "blog",
]
```
