from django.urls import path

from homepage import views

app_name = "homepage"


urlpatterns = [
    path("", views.upload, name="upload"),
    path("datatable/", views.tableview, name="tableview"),
]
