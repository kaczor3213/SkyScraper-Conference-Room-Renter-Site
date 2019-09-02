from django.urls import path, re_path
from .views import *

urlpatterns = [
    #obsługa daty z re patha
    path('', RoomMenu.as_view(), name='menu'),
    path('create/', RoomCreate.as_view(), name='create'),
    path('reserve/', RoomPicker.as_view(), name='picker'),
    path('<int:room_id>/', RoomDetails.as_view(), name='details'),
    path('modify/<int:room_id>/', RoomModify.as_view(), name='modify'),
    re_path(r'^reserve/(?P<room_id>\d*)/(?P<reservation_date>\d{4}-\d{2}-\d{2})/$', RoomReserve.as_view(), name='reserve'),
    path('delete/<int:room_id>/', RoomDelete.as_view(), name='delete'),
]