# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path
from .views import test
from .api.project import ProjectList
from django.conf.urls import url

urlpatterns = [
    # path('^api/projects', include(projectsUrls)),
    path('/', test),
    url('/project/', ProjectList.as_view())
]
