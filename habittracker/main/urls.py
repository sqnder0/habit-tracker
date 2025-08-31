from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("update_day/", views.update_day, name="update_day"),
    path("settings/", views.settings, name="settings"),
    path("day/<int:year>/<int:month>/<int:day>", views.render_day, name="day"),
    path("update_habit/", views.update_habit, name="update_habit"),
    path("delete_habit/", views.delete_habit, name="update_habit"),
    path("create_habit/", views.create_habit, name="create_habit")
]