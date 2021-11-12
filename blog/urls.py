
# hookup the URLs created in the views file
# first import the proper information
from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("<category>/", views.blog_category, name="blog_category")
]
# Now that the URLs are created and ready, add them to the project
# URL configuration using include()
