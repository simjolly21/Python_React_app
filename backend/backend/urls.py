# backend/urls.py

from django.contrib import admin
from django.urls import path, include
# import views from projects
from projects import views

# import routers from the REST framework
# it is necessary for routing
from rest_framework import routers
from projects.views import ProjectViewSet, TaskViewSet

# create a router object
router = routers.DefaultRouter()

# register the router
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('projects/', include(router.urls))
]

