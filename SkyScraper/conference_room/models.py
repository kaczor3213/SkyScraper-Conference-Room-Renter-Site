from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=64, default="Pokój konferencyjny")
    image = models.ImageField(upload_to='img/rooms')
    description = models.TextField()
    capacity = models.IntegerField(default=15)
    projector = models.BooleanField(default=False)



class Reservation(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    notes = models.TextField()
    rooms = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('date', 'rooms')
