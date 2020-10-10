from django.urls import path
from .views import rooms_view, SeeRoomsView

app_name = "rooms"

urlpatterns = [path("", rooms_view),
               path("<int:pk>", SeeRoomsView.as_view())
               ]
