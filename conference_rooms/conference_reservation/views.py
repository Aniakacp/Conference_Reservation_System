from django.shortcuts import render, redirect
from django.views import View
from conference_reservation.models import ConferenceRoom, Reservation
from datetime import datetime

class ConferenceMainView(View):
    def get(self, request):
        return render(request,'main.html')

class ConferenceRoomList(View):
    def get(self, request):
        conference_rooms= ConferenceRoom.objects.all()
        reservations = Reservation.objects.all()
        now = datetime.now().strftime("%Y-%m-%d")
        today_booked_rooms=[]
        for reservation in reservations:
            if str(reservation.date) == now:
                today_booked_rooms.append(reservation.conference_room.name)
        return render(request, 'conference_list.html', {'conference_rooms': conference_rooms, 'reservations': reservations, 'today_booked_rooms':today_booked_rooms})

class AddConferenceRoom(View):
    def get(self, request):
        return render(request, 'conference_add.html')
    def post(self, request):
        conference_rooms = ConferenceRoom.objects.all()
        conference_rooms_list=[]
        for room in conference_rooms:
            conference_rooms_list.append(room.name)
        room_name= request.POST.get('room_name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        if not projector:
            projector="False"
        if room_name and capacity:
            if room_name not in conference_rooms_list and int(capacity)>0:
                if projector=='on':
                    ConferenceRoom.objects.create(name= room_name, capacity=capacity, projector='True')
                else:
                    ConferenceRoom.objects.create(name=room_name, capacity=capacity, projector='False')
                return redirect('main')
            else:
                info = "Input data incorrect"
        else:
            info= "Input data incorrect"
        return render(request, 'conference_add.html', {'info': info})

class ConferenceRoomDetails(View):
    def get(self, request, id):
        now = datetime.now().strftime("%Y-%m-%d")
        reservation = Reservation.objects.filter(conference_room=id).order_by('date')
        conference_room = ConferenceRoom.objects.get(pk=id)
        reservation_dates=[]
        for room in reservation:
            if now < str(room.date):
                reservation_dates.append(room)
        return render(request, 'conference_details.html', {'conference_room':conference_room, 'reservation_dates':reservation_dates})

class ConferenceRoomEdit(View):
    def get(self, request, id):
        conference_room = ConferenceRoom.objects.get(pk=id)
        return render(request, 'conference_edit.html', {'conference_room': conference_room})
    def post(self, request, id):
        conference_room = ConferenceRoom.objects.filter(pk=id)
        conference_rooms = ConferenceRoom.objects.all()
        conference_rooms_list = []
        for room in conference_rooms:
            conference_rooms_list.append(room.name)
        room_name = request.POST.get('room_name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        info=''
        if not projector:
            projector = "False"
        if room_name and capacity:
            if room_name not in conference_rooms_list and int(capacity) > 0:
                if projector == 'on':
                    conference_room.update(name=room_name, capacity=capacity, projector='True')
                else:
                    conference_room.update(name=room_name, capacity=capacity, projector='False')
                return redirect('conference_list')
            else:
                info = "Input data incorrect"
        else:
            info = "Input data incorrect"
        return render(request, 'conference_edit.html', {'conference_room': conference_room, 'info': info})

class ConferenceRoomDelete(View):
    def get(self, request, id):
        conference_room = ConferenceRoom.objects.get(pk=id)
        if conference_room:
            conference_room.delete()
            return redirect('conference_list')
        return render(request)

class ConferenceRoomReserve(View): # datetime(2020, 6, 15)
    def get(self, request, id):
        reservation= Reservation.objects.filter(conference_room=id)
        conference_room = ConferenceRoom.objects.get(pk=id)
        return render(request, 'conference_reservation.html', {'reservation': reservation, 'conference_room': conference_room})
    def post(self, request, id):
        info= ''
        reservation = Reservation.objects.filter(conference_room=id)
        conference_room = ConferenceRoom.objects.get(pk=id)
        comment= request.POST.get('comment')
        new_reservation_date= request.POST.get('reservation_date')
        now= datetime.now().strftime("%Y-%m-%d")
        for date in reservation:
            if new_reservation_date == str(date.date):
                info= 'Conference Room not available on this date.'
                return render(request, 'conference_reservation.html', {'reservation': reservation, 'info': info})
        if new_reservation_date < now:
            info= 'Date incorrect'
        else:
            Reservation.objects.create(date= new_reservation_date, conference_room= conference_room, comment= comment)
            return redirect('conference_list')
        return render(request, 'conference_reservation.html', {'reservation':reservation, 'info': info})

class ConferenceRoomSearch(View):
    def get(self, request):
        return render(request, 'conference_search.html')

    def post(self, request):
        room_name = request.POST.get('room_name')
        min_capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        reservation_date = request.POST.get('reservation_date')
        info = ''
        if not projector:
            projector = "False"

        #------------------------------ROOM NAME --------------------------------------------------
        conference_rooms = ConferenceRoom.objects.all()
        conference_rooms_list = []
        for room in conference_rooms:
            conference_rooms_list.append(room.name)
        if room_name:
            if room_name in conference_rooms_list:
                searched_room = ConferenceRoom.objects.get(name=room_name)
                id = searched_room.id
                return redirect(f'/room/{id}/')
            else:
                info = 'No such room'
                return render(request, 'conference_search.html', {'info': info})

        # ------------------------------DATE & CAPACITY & PROJECTOR-----------------------------------------------------

        if reservation_date and min_capacity and projector == 'on':
            projector_on= ConferenceRoom.objects.filter(projector='True')
            searched_room = ConferenceRoom.objects.filter(capacity__gte=min_capacity)
            now = datetime.now().strftime("%Y-%m-%d")
            free_rooms = []
            booked_rooms = []
            if now < str(reservation_date) and searched_room and projector_on:
                reservations = Reservation.objects.filter(date=reservation_date)
                for reservation in reservations:
                    if reservation.conference_room not in booked_rooms:
                        booked_rooms.append(reservation.conference_room)
                all_rooms = ConferenceRoom.objects.all()
                for room in all_rooms:
                    if room not in booked_rooms: #pokoje danego dnia
                        for capacity in searched_room: #pojemnosc sali
                            if capacity == room:
                                for projektor_elm in projector_on:
                                    if projektor_elm == room:
                                        free_rooms.append(room)
                if reservations == Reservation.objects.none():
                    free_rooms = all_rooms
                if free_rooms:
                    return render(request, 'conference_searched_rooms.html',
                              {'free_rooms': free_rooms, 'reservation_date': reservation_date})
                else:
                    info = 'No such room'
                    return render(request, 'conference_search.html', {'info': info})
            else:
                info = 'No such room'
                return render(request, 'conference_search.html', {'info': info})

        # ------------------------------DATE & PROJEKTOR -----------------------------------------------------
        if reservation_date and projector == 'on':
            projektor_on = ConferenceRoom.objects.filter(projector='True')
            now = datetime.now().strftime("%Y-%m-%d")
            free_rooms = []
            booked_rooms = []
            if now < str(reservation_date) and projektor_on:
                reservations = Reservation.objects.filter(date=reservation_date)
                for reservation in reservations:
                    if reservation.conference_room not in booked_rooms:
                        booked_rooms.append(reservation.conference_room)
                all_rooms = ConferenceRoom.objects.all()
                for room in all_rooms:
                    if room not in booked_rooms:
                        for projector_elm in projektor_on:
                            if projector_elm == room:
                                free_rooms.append(room)
                if reservations == Reservation.objects.none():
                    free_rooms = all_rooms
                if free_rooms:
                    return render(request, 'conference_searched_rooms.html',
                              {'free_rooms': free_rooms, 'reservation_date': reservation_date})
                else:
                    info = 'No such room'
                    return render(request, 'conference_search.html', {'info': info})
            else:
                info = 'No such room'
                return render(request, 'conference_search.html', {'info': info})

        # ------------------------------DATE & CAPACITY-----------------------------------------------------
        if reservation_date and min_capacity:
            searched_room = ConferenceRoom.objects.filter(capacity__gte=min_capacity)
            now = datetime.now().strftime("%Y-%m-%d")
            free_rooms = []
            booked_rooms = []
            if now < str(reservation_date) and searched_room:
                reservations = Reservation.objects.filter(date=reservation_date)
                for reservation in reservations:
                    if reservation.conference_room not in booked_rooms:
                        booked_rooms.append(reservation.conference_room)
                all_rooms = ConferenceRoom.objects.all()
                for room in all_rooms:
                    if room not in booked_rooms:
                        for capacity in searched_room:
                            if capacity == room:
                                free_rooms.append(room)
                if reservations == Reservation.objects.none():
                    free_rooms = all_rooms
                if free_rooms:
                    return render(request, 'conference_searched_rooms.html',
                              {'free_rooms': free_rooms, 'reservation_date': reservation_date})
                else:
                    info = 'No such room'
                    return render(request, 'conference_search.html', {'info': info})
            else:
                info = 'No such room'
                return render(request, 'conference_search.html', {'info': info})

        # ------------------------------CAPACITY & PROJEKTOR-----------------------------------------------------
        if min_capacity and projector == 'on':
            projector_on = ConferenceRoom.objects.filter(projector='True')
            searched_room = ConferenceRoom.objects.filter(capacity__gte=min_capacity)
            free_rooms=[]
            if searched_room and projector_on:
                all_rooms = ConferenceRoom.objects.all()
                for room in all_rooms:
                    print(room)
                    if room in projector_on:
                        print("TU")
                        for capacity in searched_room:
                            if capacity == room:
                                print(room)
                                free_rooms.append(room)
                                print(free_rooms)
                if free_rooms:
                    return render(request, 'conference_searched_rooms.html', {'free_rooms': free_rooms, 'info': info})
                else:
                    info = 'No such room'
                    return render(request, 'conference_search.html', {'info': info})
            else:
                info = 'No such room'
                return render(request, 'conference_search.html', {'info': info})

        # ------------------------------DATE-----------------------------------------------------
        if reservation_date:
            now = datetime.now().strftime("%Y-%m-%d")
            free_rooms = []
            booked_rooms = []
            if now < str(reservation_date):
                reservations = Reservation.objects.filter(date=reservation_date)
                all_rooms = ConferenceRoom.objects.all()
                for reservation in reservations:
                    if reservation.conference_room not in booked_rooms:
                        booked_rooms.append(reservation.conference_room)
                for room in all_rooms:
                    if room not in booked_rooms:
                        free_rooms.append(room)
                if reservations == Reservation.objects.none():
                    free_rooms = all_rooms
                return render(request, 'conference_searched_rooms.html',
                              {'free_rooms': free_rooms, 'reservation_date': reservation_date})
            else:
                info = "Incorrect date!!!"
                return render(request, 'conference_search.html', {'info': info})

        # ------------------------------CAPACITY-----------------------------------------------------
        if min_capacity:
            free_rooms = ConferenceRoom.objects.filter(capacity__gte=min_capacity)
            if free_rooms:
                return render(request, 'conference_searched_rooms.html', {'free_rooms': free_rooms})
            else:
                info = 'No such room'
                return render(request, 'conference_search.html', {'info': info})

        # ------------------------------PROJECTOR-----------------------------------------------------
        if projector == 'on':
            free_rooms = ConferenceRoom.objects.filter(projector='True')
            return render(request, 'conference_searched_rooms.html', {'free_rooms': free_rooms})

        info = "Incorrect input"
        return render(request, 'conference_search.html', {'info': info})

