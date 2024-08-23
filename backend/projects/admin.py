from django.contrib import admin

# import the model Projects
from .models import Project, Task

# create a class for the admin-model integration
class ProjectAdmin(admin.ModelAdmin):

    # add the fields of the model here
    list_display = ("name","description","start_date", "end_date")

class TaskAdmin(admin.ModelAdmin):

    # add the fields of the model here
    list_display = ("title","description","status", "project", "assigned_to", "due_date")

# we will need to register the
# model class and the Admin model class
# using the register() method
# of admin.site class
admin.site.register(Project,ProjectAdmin)
admin.site.register(Task,TaskAdmin)
