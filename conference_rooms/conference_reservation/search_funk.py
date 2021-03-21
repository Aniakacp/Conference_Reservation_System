# TO DELETE
# class ConferenceRoomSearch_2(View):
#     return render(request, 'conference_search.html')
#     def get(self, request):
#         return render(request, 'conference_search.html')
#     def post(self, request):
#         conference_rooms = ConferenceRoom.objects.all()
#         conference_rooms_list = []
#         info=''
#         for room in conference_rooms:
#             conference_rooms_list.append(room.name)
#         room_name = request.POST.get('room_name')
#         min_capacity = request.POST.get('capacity')
#         projector = request.POST.get('projector')
#         reservation_date = request.POST.get('reservation_date')
#         if not projector:
#             projector="False"
#         if room_name:
#             if room_name in conference_rooms_list:
#                 searched_room= ConferenceRoom.objects.get(name= room_name)
#                 id= searched_room.id
#                 return redirect(f'/room/{id}/')
#             else:
#                 info='No such room'
#                 return render(request, 'conference_search.html', {'info': info})
#         if projector=='on':
#             searched_room = ConferenceRoom.objects.filter(projector='True')
#             return render(request, 'conference_searched_rooms.html', {'searched_room': searched_room})
#         if reservation_date:
#             now = datetime.now().strftime("%Y-%m-%d")
#             free_rooms = []
#             booked_rooms =[]
#             if now < str(reservation_date):
#                 reservations = Reservation.objects.filter(date = reservation_date)
#                 all_rooms= ConferenceRoom.objects.all()
#                 for reservation in reservations:
#                     if reservation.conference_room not in booked_rooms:
#                         booked_rooms.append(reservation.conference_room)
#                 for room in all_rooms:
#                     if room not in booked_rooms:
#                         free_rooms.append(room)
#                 if reservations == Reservation.objects.none():
#                     free_rooms= all_rooms
#                 return render(request, 'conference_searched_rooms.html', {'free_rooms': free_rooms, 'reservation_date': reservation_date})
#             else:
#                 info= "Incorrect date!!!"
#                 return render(request, 'conference_search.html', {'info': info})
#         if min_capacity:
#             searched_room= ConferenceRoom.objects.filter(capacity__gte= min_capacity)
#             if searched_room:
#                 return render(request, 'conference_searched_rooms.html', {'searched_room':searched_room})
#             else:
#                 info = 'No such room'
#                 return render(request, 'conference_search.html', {'info': info})
#         info="Incorrect input"
#         return render(request, 'conference_search.html', {'info': info})
