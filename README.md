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
## Create a Blog feature to share my knowledge
This will be a great place to share the knowledge I learn. I can update it daily, weekly, monthly or whenever I want. This will add to what recruiters get to learn about me.

This section will be about how to use the Django Admin interface, which is where I'll create, update and delete posts and categories as necessary.
- This blog app will allow the following functions:
    1. Create, update, and delete blog posts.
    2. Display posts to the users as either an index view or a detail view
    3. Assign categories to posts
    4. Allow users to comment on posts

- Also, this is where the Django Admin interface will be learned and utilized. I will be able to create, update, and delete posts and categories as necessary.

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

### Blog App: Models
the `models.py` file in this app is much more complicated than it was for the projects app.

# WHERE I LEFT OFF:
The spot right above, I never got to start creating the models.

##### link to project tutorial:
https://realpython.com/get-started-with-django-1/#why-you-should-learn-django

switch to **blog-main** branch in github, that is where the blog app was created. It hasn't been merged yet.
- For this app I will need three seperate DB tables for the blog:
  1. Post
  2. Category
  3. Comment

These tables need to be related to one another. This is made easier because Django models come with the fields specifically for this purpose.

###### First: I will create the `Categopry` and `Post` models

The code should look like this:

```sh
from django.db import models

class Category(models.Model): # Very Simple, Just Store Name of Category
    name = models.CharField(max_length=20) # Give CharField a max length of 20

class Post(models.Model):
    title = models.CharField(max_length=255) # Only limit title so it isn't too long
    body = models.TextField() # Body shouldn't be limited for a blog post
    created_on = models.DateTimeField(auto_now_add=True) #Django's own datetime fields
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')
```

- Django's date time field allows you to store the date and time of when something was created or modified very simply.
  - `auto_now_add=True` assigns the current date and time to this field anytime an instance of the class is **created**
  - `auto_now=True` assigns the current date and time to this field whenever an instance of this class is saved. This means whenever I edit an instance of this class, the `date_modified` will be updated.

> The most interesting field on the post model is the final field, `categories`. We want to link our models for categories and posts in such a way that many `categories` can be assigned to many `posts`. Django makes this super easy with the `ManyToManyField`. This field links the `Post` and `Category` models and allows us to create a relationship between the two tables.
> The `ManyToManyField` takes two arguments. The first is the model with which the relationship is, in this case its `Category`. The second allows us to access the relationship from a `Category` object, even though we haven’t added a field there. By adding a `related_name` of `posts`, we can access `category.posts` to give us a list of `posts` with that `category`.

- The Third aand final model I need is comments. I need a Comment class that uses a relationshipo field similar to ManyToManyField that relates, `Post` and `Category`. However, I only want the relationship to go one way. *Basically* **one post should have many comments**

Defining the `Comment` class:
```sh
class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    # created the one to many relationship
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
```

The first three models are normal. But the last line, `post` is not something that has been used.

- `post` is another **Relational Field** called the `ForeignKey` field. It is similar to many to many, but instead it is a Many To One relationship.
  - the reasoning for this in this instance, is that you can have many comments associated with one post, but you cant have a comment associated with many posts.

`ForeignKey` takes in TWO args.
1. the other model in the relationship (in this case `Post`)
2. tells Django what to do when a post is deleted.
   - If a post is deleted then we don't want the comments related to it hanging around. So we delete them as well by adding the `on_delete=models.CASCADE`

##### Now that the models are created, create the migration files.

`$ python manage.py makemigrations blog`

- remember to migrate the tables. This time, don't add the app-specific flag. Later on I will need the `User` model that Django creates for you:

`$ python manage.py migrate`

# BLOG APP: Django Admin

Since I am the only one who will be writing blog posts, there is no need to create a user interface to do so. I can just use Django's Admin tool which is really easy and convenient.

To access Admin I have to add myself as a superuser. The reason is because I applied migrations project-wide instead of just for the blog app. Django has a built in user models and a user management system that lets me login to Admin.

to get started type in the shell:
`$ python manage.py createsuperuser`

- Now I will have to create a username, email, and password. Once those are entered it will tell me te superuser was created. (even if I make a mistake I can just startover)

## Create Username, email and password for superuser (check black book)

#### Register Models in Admin site:
Once you login to admin the only "models" that are there will be groups and users. none of the models I created are there. I have to register my models in the Admin Interface.

- So inside the `blog` directory, open up admin.py and add the following code:

```sh
from django.contrib import admin
from blog.models import Post, Category

class PostAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

# Add Comment if I need to monitor them

# class CommentAdmin(admin.ModelAdmin):
#   pass
# admin.site.register(Comment, CommentAdmin)

# Now register them
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
```

*That is how to register your models for the Admin site.*

I didn't add the comments because usually I wouldn't have a reason to write or edit comments myself. But if i need to add a feature to monitor and moderate comments then it would be done exactly the same way.


# BLOG APP: Views

I am going to create three view functions in the `view.py` file in the `blog` directory.
1. `blog_index` This will be a list of all my posts
2. `blog_detail` This will display the full post along with all the comments and a form to allow users to create new comments.
3. `blog_category` this is close to what `blog_index` is but it will only display posts of a specific category that the user can choose.

- So the easiest view function to create will be the index view, just like in the Project app. All I need to do is query all the post objects from my database.

```sh
from django.shortcuts import render
from blog.models import Post, Comment

# create the view function
def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {
        "posts": posts,
    }
    return render(request, "blog_index.html", context)
```

On line 2, you import the `Post` and the `Comment` models, and on line 5 inside the view function, you obtain a Queryset containing all the posts in the database. `order_by()` orders the Queryset according to the argument given. The minus sign tells Django to start with the largest value rather than the smallest. We use this, as we want the posts to be ordered with the most recent post first.
After that you define the `context` dictionary and render the template. (I will create the templates after the view functions are created)

- Remember that each view func needs to have a context dictionary!

--> Now create the `blog_category()` view. This view func will need to take a category as an argument and query the Post database

```sh
def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by('-created_on')
    context = {
        "category": category,
        "posts": posts
        }
    return render(request, "blog_category.html", context)
```

On line 14, you’ve used a Django Queryset filter. The argument of the filter tells Django what conditions need to be met for an object to be retrieved. In this case, we only want posts whose categories contain the category with the name corresponding to that given in the argument of the view function. Again, you’re using order_by() to order posts starting with the most recent.

We then add these posts and the category to the context dictionary, and render our template.

The last view function to add is blog_detail(). This is more complicated as we are going to include a form. Before you add the form, just set up the view function to show a specific post with a comment associated with it. This function will be almost equivalent to the project_detail() view function in the projects app:

```sh
def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
    }

    return render(request, "blog_detail.html", context)
```

The view function takes a pk value as an argument and, on line 22, retrieves the object with the given pk.

On line 23, we retrieve all the comments assigned to the given post using Django filters again.

Lastly, add both post and comments to the context dictionary and render the template.

#### Creating Forms In Django:
- To add a form to the page, you’ll need to create another file in the blog directory named forms.py.
    - Django forms are very similar to models. **A form consists of a class where the class attributes are form fields.**
    - Django comes with some built-in form fields that you can use to quickly create the form you need.

- Fields I will use to create my Django form:
  - author --> CharField
  - body --> CharField
  - add a DateTime field for when the form is submitted.

__NOTE__: *if the CharField of my form corresponds to a model CharField, make sure both have the same max_length value*

```sh
from django import forms

class CommentForm(forms.Form):
    author = forms.CharField(max_length=60, widget=forms.TextInput(
        attrs={
            "class":"form-control",
            "placeholder":"Your Name"
        }
    ))
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class":"form-control",
            "placeholder":"Leave a Comment!"
        }
    ))
```

You’ll also notice an argument `widget` has been passed to both the fields. The **author field** has the `forms.TextInput` widget. This tells Django to load this field as an HTML text input element in the templates. The body field uses a `forms.TextArea` widget instead, so that the field is rendered as an HTML text area element.

**These widgets also take an argument** `attrs`, which is a dictionary and allows us to specify some CSS classes, which will help with formatting the template for this view later. It also allows us to add some placeholder text.

When a form is posted, a `POST` request is sent to the server. So, in the view function, we need to check if a `POST` request has been received. We can then create a comment from the form fields. Django comes with a handy `is_valid()` on its forms, so we can check that all the fields have been entered correctly.

Once you’ve created the comment from the form, you’ll need to save it using `save()` and then query the database for all the comments assigned to the given post.

- In order to make this work, I will have to update my view function.
> Add this to the `blog_detail` function
> ```sh
> form = CommentForm()
> if request.method == 'POST':
>   form=CommentForm(request.POST)
>   if form.is_valid():
>       comment = Comment(
>           author=form.cleaned_data["author"],
>           body=form.cleaned_data["body"]
>           post=post
>       )
>       comment.save()
> ```
- then inside the context dictionary add `"form":form`

ALSO, MAKE SURE TO IMPORT THE FORM AT THE BEGINNING OF THE VIEWS FILE
`from .forms import CommentForm`

- Next we check if a `POST` request was received. If it is then create a new instance of the form, populated with the data entered into the form.
- the form is then validated using `is_valid()` If the form is valid, then a new instance of `Comment` is created. **I can access the data from the form using `form.cleaned_data`, which is a dictionary**
- *The keys of the dictionary correspond to the form fields. This way I can access the fields in the form by using their name. Like the `author` I can just use `form.cleaned_data['author']`* **Don't forget to add the current post to the comment when you create it!**

**The Life Cycle of submitting a Form:**
>1. When a user visits a page containing a form, they send a GET request to the server. In this case, there’s no data entered in the form, so we just want to render the form and display it.
>2. When a user enters information and clicks the Submit button, a POST request, containing the data submitted with the form, is sent to the server. At this point, the data must be processed, and two things can happen:
>   - The form is valid, and the user is redirected to the next page.
>   - The form is invalid, and empty form is once again displayed. The user is back at step 1, and the process repeats.

##### HEADS UP:
The Django forms module will show some errors that can be displayed to the user. So when building more complex applications I will need to use this feature. [Click Here For More Information](https://docs.djangoproject.com/en/2.1/topics/forms/#rendering-form-error-messages)

Notice also, that I use the `comment.save()` to save the comment and then we add the form to the context dictionary so that the form can be accessed in the HTML template.

*Now before I can create the templates to see the app up and running, I have to hook up the URLs.*
**To do this I have to create a `urls.py` file inside the `blog` directory, and then add the URLs for the three views**

###### `urls.py` inside `blog` directory
```sh
from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("<category>/", views.blog_category, name="blog_category")
]
```

- Once the URLs are created, I add them to the main projects urls.py file using the `include()` function
```sh
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("projects/", include("projects.urls")),
    path("blog/", include("blog.urls")),
]
```
With this set up, all the blog URLs will be prefixed with blog/, and you’ll have the following URL paths:
  - **localhost:8000/blog:** Blog index
  - **localhost:8000/blog/1:** Blog detail view of blog with `pk=1`
  - **localhost:8000/blog/python**: Blog index view of all posts with category python

---> Now to make these urls work, I have to create the templates for them. In this section, you created all the views for your blog application. You learned how to use filters when making queries and how to create Django forms. It won’t be long now until you can see your blog app in action!

======
**NEW SECTION**
======
#### Blog App: Templates

The final piece of our blog app is the templates. By the end of this section, you’ll have created a fully functioning blog.

**You’ll notice there are some bootstrap elements included in the templates to make the interface prettier**. These aren’t the focus of the tutorial so I’ve glossed over what they do but do check out the [Bootstrap docs](https://getbootstrap.com/docs/4.1/getting-started/introduction/) to find out more.

*The first template you’ll create is for the blog index in a new file blog/templates/blog_index.html. This will be very similar to the projects index view.*

You’ll **use a for loop to loop over all the posts**. For **each post**, you’ll **display the title and a snippet of the body**. *As always, you’ll extend the base template personal_porfolio/templates/base.html, which contains our navigation bar and some extra formatting*:

```sh
{% extends "base.html" %}
{% block page_content %}
<div class="col-md-8 offset-md-2">
    <h1>Blog Index</h1>
    <hr>
    {% for post in posts %}
    <!-- Show the post title using a hyperlink which is a Django hyperlink pointing to the
    URL named blog_detail. It will take an integer as its argument and should correspond to
    the pk value of the post -->
    <h2><a href="{% url 'blog_detail' post.pk%}">{{ post.title }}</a></h2>
    <small>
        <!-- Now show the created_on attribute of the post and its category. The for loop
        is to loop over all the categories assigned to the post -->
        {{ post.created_on.date }} |&nbsp;
        Categories:&nbsp;
        {% for category in post.categories.all %}
        <a href="{% url 'blog_category' category.name %}">
            {{ category.name }}
        </a>&nbsp;
        {% endfor %}
    </small>
    <!-- use a template filter slice that cuts the body of the post off at 400 characters
    which will make the blog index more readable -->
    <p>{{ post.body | slice:":400" }}...</p>
    {% endfor %}
</div>
{% endblock %}
```

- First, we have the post title, which is a hyperlink. The link is a Django link where we are pointing to the URL named blog_detail, which takes an integer as its argument and should correspond to the pk value of the post.

- Underneath the title, we’ll display the created_on attribute of the post as well as its categories. On line 11, we use another for loop to loop over all the categories assigned to the post.

- then we use a template filter slice to cut off the post body at 400 characters so that the blog index is more readable.

Once that’s in place, you should be able to access this page by visiting **`localhost:8000/blog`:**

###### Create blog_category.html
This will display the blog posts that correspond to a given category.
It is Identical to the blog_index.html file except for a few changes. Like the category name inside the h1 tag instead of Blog index
```sh
{% extends "base.html" %}
{% block page_content %}
<div class="col-md-8 offset-md-2">
    <!-- Use Django template filter "title". This applies titlecase to the string and
    makes words start with an uppercase character -->
    <h1>{{ category | title }}</h1>
    <hr>
    <!-- Use for loop to grab each post and dsplay them on the page -->
    {% for post in posts %}
        <h2><a href="{% url 'blog_detail' post.pk%}">{{ post.title }}</a></h2>
        <small>
            {{ post.created_on.date }} |&nbsp;
            Categories:&nbsp;
            {% for category in post.categories.all %}
            <a href="{% url 'blog_category' category.name %}">
                {{ category.name }}
            </a>&nbsp;
            {% endfor %}
        </small>
        <p>{{ post.body | slice:":400" }}...</p>
        {% endfor %}
</div>
{% endblock %}
```
Most of this template is identical to the previous template. The only difference is on line 4, where we use another Django template filter [title](https://docs.djangoproject.com/en/2.1/ref/templates/builtins/#title). This applies titlecase to the string and makes words start with an uppercase character.

With that template finished, you’ll be able to access your category view. If you defined a category named python, you should be able to visit localhost:8000/blog/python and see all the posts with that category:
![Example of what this page should look like](https://robocrop.realpython.net/?url=https%3A//files.realpython.com/media/Screenshot_2018-12-17_at_23.50.51.08dadaa185fc.png&w=696&sig=ba04bfb8c05fe5f7aed0aad6708a93b23286ccc7)


The last template to create is the blog_detail template. In this template, you’ll display the title and full body of a post.

Between the title and the body of the post, you’ll display the date the post was created and any categories. Underneath that, you’ll include a comments form so users can add a new comment. Under this, there will be a list of comments that have already been left:
