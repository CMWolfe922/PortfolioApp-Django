from django.shortcuts import render
from projects.models import Project

# Create your views here.


def project_index(request):
    projects = Project.all()  # query all objs in projects table in database
    # contxts sends information to template. every view func needs one
    context = {
        'projects': projects,
    }

    return render(request, 'project_index.html', context)

# Now I need to create the project_detail() func


def project_detail(request, pk):
    # perform query for object in projects table with primary key
    project = Project.objects.get(pk=pk)
    # assign project with primary key to context to
    # pass information to views template
    context = {
        'project': project
    }

    return render(request, 'project_detail.html', context)
