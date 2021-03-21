from django.db import models

class ConferenceRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

class Reservation(models.Model):
    date = models.DateField()
    conference_room= models.ForeignKey(ConferenceRoom, on_delete=models.CASCADE) #sala może mieć wiele rezerwacji (każdą innego dnia)
    comment= models.TextField(null=True)

    class Meta:
        unique_together= ('date', 'conference_room') # czmu bez comment tutaj?

    def __str__(self):
        return f'{self.conference_room} {self.date}'

