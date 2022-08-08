from django.db import models
from django.contrib.auth.models import User

#TOPİC MODELİ OLUŞTURDUK
class Topic(models.Model): 
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


#ROOM MODELİNDE TOPİC VE KULLANICI SEÇMEK İÇİN DEĞİŞKENLER TANIMLADIK
class Room(models.Model):
    #ROOM DEĞİŞKENLERİNİ TANIMLADIK
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User, related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    #BU SINIF EKLENEN İÇERİKLERİ SIRALAMAMIZA YARADI
    class Meta:
        ordering = ['-updated','-created']
    
    def __str__(self):
        return self.name
 



#MESAJ MODELİNDE KULLANICI VE ODA SEÇİMİ İÇİN DEĞİŞKENLER TANIMLADIK
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50]