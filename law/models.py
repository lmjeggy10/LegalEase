from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserType(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    type = models.CharField(max_length=50)


class Lawyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=50)
    emnumber = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='images/')
    education = models.CharField(max_length=50)
    parea = models.CharField(max_length=50)
    speci = models.CharField(max_length=50)
    con_password= models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    exper_lowyer= models.CharField(max_length=50, null=True)
    payment = models.CharField(max_length=50, null=True)



class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    con_password= models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    payment = models.CharField(max_length=50, null=True)

class Feedback(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    feed = models.CharField(max_length=50)


class Ask(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50)
    file = models.ImageField(upload_to='images/')
    status = models.CharField(max_length=50)

class Appointment(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date=models.CharField(max_length=50,null=True)
    time=models.CharField(max_length=50,null=True)
    reason = models.CharField(max_length=50,null=True)
    status = models.CharField(max_length=50,null=True)