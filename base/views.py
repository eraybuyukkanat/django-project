from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room,Topic,Message
from .forms import RoomForm,UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm


def loginPage(request):
    
    page = 'login' #context için lazımdı

    if request.user.is_authenticated:
        return redirect('home')
 
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password').lower()
        #EĞER KULLANICI BİLGİSİ YANLIŞ İSE KULLANICI BULUNAMADI
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User is does not exist')
        
        user = authenticate(request,username=username,password=password) #KOLAY OLMASI İÇİN BİLGİLERİ USER ADLI DEĞİŞKENE ATADIK

        if user is not None:                #BİLGİLER DOĞRU İSE
            login(request,user)
            return redirect('home')
        else:                               #BİLGİLER YANLIŞ İSE
            messages.error(request, 'Username or password does not exist')


    context = {'page':page}
    return render(request, 'base/login_register.html',context)



def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')
    return render(request,'base/login_register.html',{'form':form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter( #ARAMA KISMINDA FİLTRELEME İŞLEMİ
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        ) #Room modelindeki tüm objeleri getirdi

    rooms_count = rooms.count()
    topics = Topic.objects.all()

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics':topics,'rooms_count':rooms_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context) 



def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user':user,
        'rooms':rooms,
        'room_messages':room_messages,
        'topics':topics
    }
    return render(request,'base/profile.html',context)



#############################CRUD YAPISI###################################
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm() #içeriğin form olması için formun içine roomform sınıfını çağırdık
    topics = Topic.objects.all()

    if request.method=='POST': #İstek post ise ki öyle, form değişkenine istenen değeri ata ve geçerliyse kaydet işlemi
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home') #'home' --> urllerdeki home


    context = {'form':form, 'topics':topics} #İçeriğe forma atanan roomform sınıfını room_form htmldeki formla ilişkilendirdik
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #instance var olan bilgileri forma doldurmaya yaradı
    topics = Topic.objects.all()
    if request.user != room.host: #Oda sahibi o kullanıcı değil ise doğrulaması
        return HttpResponse("You are not allowed here!")

    if request.method=='POST': 
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host: #Oda sahibi o kullanıcı değil ise doğrulaması
      return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        room.delete()
        return redirect('home')
    
    return render(request,'base/delete.html',{'obj':room})
    
@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk) #Message modelindeki tüm değişkenleri getirdik id ise primary key
    
    if request.user != message.user: #Oda sahibi o kullanıcı değil ise doğrulaması
      return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        message.delete()
        return redirect('home')
    
    return render(request,'base/delete.html',{'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    return render(request, 'base/update-user.html',{'form':form})
