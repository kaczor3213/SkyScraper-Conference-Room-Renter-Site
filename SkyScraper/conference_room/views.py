from django.shortcuts import render, Http404, redirect
from .models import *
from django.template import loader
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import calendar
import re

context = {}
current_date = datetime.now().date()

def give_status(room):
    if room.reservation_set.filter(date=current_date) == None:
        return True
    else:
        return False


#widok ze wszystkimi salami, i ich statusy na dany dzień
#odnośnik do utworzenia, odnośnik do modyfikacji, odnośnik do usunięcia
class RoomMenu(View):

    def get(self, request):

        room_context = {
            'r_id':'',
            'r_img':'',
            'r_name':'',
            'r_status':'',
            'r_description':'',
        }

        rooms = ""
        template = loader.get_template("conference_room/card.htm")
        for room in Room.objects.all():
            room_context['r_id'] = room.pk
            room_context['r_img'] = room.image.name
            room_context['r_name'] = room.name
            room_context['r_status'] = give_status(room)
            room_context['r_description'] = room.description
            rooms += template.render(room_context)
        context['rooms'] = rooms
        return render(request, 'conference_room/menu.htm', context)
    def post(self, request):
        raise Http404('Ups!, coś poszło nie tak...')

#widok dodania nowej sali
class RoomCreate(View):
    
    def get(self, request):
        return render(request, 'conference_room/create.htm', context)

    def post(self, request):
        for k, v in request.POST.items():
            print(k, v)
            if v is None:
                raise Http404("Some of the form input is empty!")
        image = request.FILES['image']
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector")
        description = request.POST.get("descritpion")

        #add result context
        create_room_context = {
            'approved_result': ''
        }
        #add image file validation

        try:
            capacity = int(capacity)
            if capacity < 5:
                raise ValueError("Given capacity of a room was lower than 5.")
        except ValueError as e:
            raise Http404("Capacity must be a digit number >=5.\n "+str(e))

        try:
            projector = bool(int(projector))
        except ValueError as e:
            raise Http404("Projector availability must be a boolean value!"+str(e))
            
        try:
            Room.objects.create(name=name, capacity=capacity, projector=projector, description=description, image=request.FILES['image'])
        except Exception as e:
            raise Http404(str(e))
        else:
            return render(request, 'conference_room/create.htm', context)



        

#widok formularz do sprawdzenia dostępności pokoi w danym terminie
class RoomPicker(View):
    def get(self, request):
        pass
    def post(self, request):
        pass

#widok konkretnej sali, detale
#wyświetlić kalendarz z rezerwacjami + wyświetlenie notki
class RoomDetails(View):

    def get(self, request, room_id):
        year = datetime.now().year
        month = datetime.now().month

        room_context = {
            'r_id':'',
            'r_img':'',
            'r_name':'',
            'r_status':'',
            'r_description':'',
            'min_date': current_date.__str__,
            'max_date': (current_date + timedelta(days=365)).__str__,
        }

        print(room_context['min_date'])
        print(room_context['max_date'])

        room = Room.objects.get(pk=int(room_id))

        room_context['r_id'] = room.pk
        room_context['r_img'] = room.image.name
        room_context['r_name'] = room.name
        room_status_icon_approved = '<i style="color:green" class="fas fa-check"></i>'
        room_status_icon_denied = '<i style="color:red" class="fas fa-times"></i>'
        if give_status(room):
            room_context['r_status'] = room_status_icon_approved
        else:
            room_context['r_status'] = room_status_icon_approved
        room_context['r_description'] = room.description

        return render(request, 'conference_room/details.htm', room_context)
    
    def post(self, request, room_id):
        reservation_date = request.POST.get('reservation_date')
        print(reservation_date)
        if request.POST.get('reservation_date') == None or re.search(r'\d{4}-{2}-{2}',request.POST.get('reservation_date')):
            raise Http404("Bad date!")
        else:
            return redirect(f'/rooms/reserve/{room_id}/{reservation_date}')
#widok edycji sali

class RoomModify(View):
   
    def get(self, request, room_id):

        room_context = {
            'image':'',
            'name':'',
            'capacity':'',
            'projector_yes':'',
            'projector_no':'',
            'description':'',
            }

        room = Room.objects.get(pk=room_id)

        room_context['image'] = room.image
        room_context['name'] = room.name
        room_context['capacity'] = room.capacity
        room_context['description'] = room.description
        print(room.description)
        if room.projector == True:
            room_context['projector_yes'] = "checked"
        else:
            room_context['projector_no'] = "checked"


        return render(request, 'conference_room/modify.htm', room_context)

    def post(self, request, room_id):
        for k, v in request.POST.items():
            print(k, v)
            if v is None:
                raise Http404("Some of the form input is empty!")
        image = request.FILES['image']
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector")
        description = request.POST.get("descritpion")

        #add result context
        create_room_context = {
            'approved_result': ''
        }
        #add image file validation

        try:
            capacity = int(capacity)
            if capacity < 5:
                raise ValueError("Given capacity of a room was lower than 5.")
        except ValueError as e:
            raise Http404("Capacity must be a digit number >=5.\n "+str(e))

        try:
            projector = bool(int(projector))
        except ValueError as e:
            raise Http404("Projector availability must be a boolean value!"+str(e))
            
        try:
            Room.objects.filter(pk=room_id).update(name=name, capacity=capacity, projector=projector, description=description, image=request.FILES['image'])
        except Exception as e:
            raise Http404(str(e))
        else:
            return render(request, 'conference_room/create.htm', context)


#widok rezerwacji sali
#podać date rezerwacji -> walidacja, potwierdzenie
class RoomReserve(View):
    def get(self, request):
        pass
    def post(self, request):
        pass

#widok potwierdzenia usunięcia sali

class RoomDelete(View):
    def get(self, request):
        pass
    def post(self, request):
        pass
