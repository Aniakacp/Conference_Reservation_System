"""conference_rooms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from conference_reservation.views import ConferenceMainView, ConferenceRoomList, AddConferenceRoom, ConferenceRoomDetails, ConferenceRoomEdit, ConferenceRoomDelete, ConferenceRoomReserve, ConferenceRoomSearch #ConferenceRoomSearch_2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('conference-rooms/', ConferenceMainView.as_view(), name='main'),
    path('room/new/', AddConferenceRoom.as_view(), name='add_conference'),
    path('conference-list/', ConferenceRoomList.as_view(), name='conference_list'),
    path('room/<int:id>/', ConferenceRoomDetails.as_view(), name='conference_details'),
    path('room/modify/<int:id>/', ConferenceRoomEdit.as_view(), name='conference_edit'),
    path('room/delete/<int:id>/', ConferenceRoomDelete.as_view(), name='conference_delete'),
    path('room/reserve/<int:id>/', ConferenceRoomReserve.as_view(), name='conference_reserve'),
    path('room/search/', ConferenceRoomSearch.as_view(), name='conference_search'),
  #  path('room/search-2/', ConferenceRoomSearch_2.as_view(), name='conference_search_2'),
]
