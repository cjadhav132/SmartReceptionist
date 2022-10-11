from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,
                                  ListView,CreateView,DetailView)
from .models import (ReceptionistDisplayMessage,
                     People,Meeting,Message,Voice)
from django.core.files import File
from . import forms
from .mail import Mail
import numpy as np
import os

from django.views.generic.detail import SingleObjectMixin
from .FaceRecognition.FaceDetect import Face
from .FaceRecognition.play_test import say
from .FaceRecognition.record_test import Record
import datetime
from django.contrib.auth import get_user_model
user = get_user_model()
# Create your views here.

Receptionist_loggedin = False
g_face_list = []
g_name_list = []
face = ''
record = Record()

class index(TemplateView):
    #print('reception status',Receptionist_loggedin)
    template_name = 'index.html'
    face_list = []
    name_list = []
    peoples = People.objects.all()
    #print('people',peoples)
    for people in peoples:
        #print(people.name)
        encoded_list = people.face_encoding
        numpy_array = np.array(encoded_list)
        name_list.append(people.name)
        face_list.append(numpy_array)
    global g_face_list
    g_face_list = face_list
    global g_name_list
    g_name_list = name_list
    global face
    face = Face(face_list,name_list)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['ba'] = ''
        context['reception'] = Receptionist_loggedin
        return context


class LoginOptions(TemplateView):
    template_name = 'login_option.html'


class ShowMessage(ListView):
    model = ReceptionistDisplayMessage
    template_name = 'people/ReceptionistMessage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = ReceptionistDisplayMessage.objects.filter(read=False).order_by('created_at')
        context['messages'] = messages
        for message in messages:
            # print(message.message)
            break
        return context

    def get_queryset(self):
        return ReceptionistDisplayMessage.objects.filter(read=False).order_by('created_at')


class EmployeeSignUp(CreateView):
    form_class = forms.ProfileCreateForm
    success_url = reverse_lazy('')


class Employee(LoginRequiredMixin,ListView):
    model = Meeting
    template_name = 'people/employee_detail.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        meetings = Meeting.objects.filter(start__date=datetime.date.today()).filter(employee__username=self.user)
        future_meetings = Meeting.objects.filter(start__date__gt=datetime.date.today()).filter(employee__username=self.user)
        for i in meetings:
            #print(i.purpose)
            break
        context['meetings'] = meetings
        context['future_meetings'] = future_meetings
        return context

    def get_queryset(self):
        self.user = self.request.user


class Employee_message(LoginRequiredMixin,ListView):
    model = Message
    template_name = 'people/employee_messages.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = Message.objects.filter(user__username=self.user).filter(read=False)
        for i in messages:
            i.read = True
            break
            print(i.message)
        context['messages'] = messages
        return context

    def get_queryset(self):
        self.user = self.request.user
        #print(self.user)


class CreateMeeting(LoginRequiredMixin,CreateView):
    template_name = 'people/CreateMeeting.html'
    form_class = forms.CreateMeeting
    success_url = reverse_lazy('people:detail')

    def form_valid(self, form):
        meet = form.save(commit=True)

        meet = Meeting.objects.filter(pk=meet.pk)[0]

        start_time =  meet.start.strftime("%H:%M:%S")
        start_date = meet.start.strftime("%m/%d/%Y")
        end_time =  meet.end.strftime("%H:%M:%S")
        end_date = meet.end.strftime("%m/%d/%Y")

        msg =[ "You have a meeting with : " + str(meet.employee.first_name) + ' ' + str(meet.employee.last_name)
         + ".\nRegarding : " + 
            str(meet.purpose) + ".\nAt : " + start_date + ':' + start_time + 
            "\ntill : " + end_date + end_time + ".\nPasscode for it is : " + meet.code
            ]
        
        m = Mail()
        m.send(meet.visitor.email,msg[0])
        
        
        
        return super().form_valid(form)



    def get_initial(self):
        initial = super(CreateMeeting,self).get_initial()
        initial['employee'] = self.request.user
        return initial


class MeetingDetail(LoginRequiredMixin,DetailView):
    model = Meeting
    context_object_name = 'meeting'
    template_name = 'people/MeetingDetail.html'


def receptionist_login(request):
    template_name = 'people/ReceptionistLogin.html'
    form = forms.ReceptionistLogin()

    if request.method == 'POST':
        form = forms.ReceptionistLogin(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            if password == "abcd":
                global Receptionist_loggedin
                Receptionist_loggedin = True

                """
                audio = Voice.objects.get(title='chi')
                a = str(audio.audio)
                a = a[7:]
                print('audio path',a)
                """
                na = "ok"
                return redirect('people:receptionist_standby',name=na)

            else:
                form = forms.ReceptionistLogin()
                return render(request,template_name,{'form':form,'error':'Wrong Password'})

    return render(request,template_name,{'form':form,'error':' '})


def receptionist_standby(request,name,**kwargs):
    if Receptionist_loggedin:
        template_name = 'people/ReceptionistStandby.html'
        msg = ""
        if name == 'no':
            msg = "No Face Found. Please try again"
        meseg = ReceptionistDisplayMessage.objects.filter(read=False).order_by('-created_at')#[0]
        if len(meseg)>0:
            mesg = meseg[0]
            meeting = Meeting.objects.filter(pk=mesg.meeting.pk)[0]
            print('visitor',meeting.visitor)
            place = meeting.visitor.voice.name
            places = place.split('/')
            file = "people/voice/" + places[-1]
            mesg.read = True
            mesg.save()
        else:
            #print("here")
            file = ''
        return render(request,template_name,{'msg':msg,'file':file})
    else:
        return redirect('receptionist_login')


face_enco = ''
name_g = ''
def show_receptionist(request):
    
    if Receptionist_loggedin:
        template_name = 'people/Receptionist.html'
        if request.method == "POST":
            data = request.POST
            req_type = data['type']
            print("type",req_type)
            meeting = data['meeting']
            print("meeting",data['meeting'])
            try:
                meet = Meeting.objects.get(pk=meeting)
            except:
                meet = Meeting.objects.get(pk=13)
                print('problem')
            print('meet code',meet.code)
            code = data['code']
            name = data['name']
            # a = say(name)

            if code == meet.code:
                if not meet.arrived:
                    msg = " has arrived.For "
                    visitor = People.objects.get(name=name)
                    emp = meet.employee
                    m = Message.objects.get_or_create(
                        user=emp,
                        meeting=meet,
                        visitor=visitor,
                        message=msg
                        )
                    print(m)
                    meet.arrived = True
                    meet.save()
                    """
                    message = Message()
                    message.user = meet.employee
                    message.visitor = People.objects.get(name=name)
                    message.message = " has arrived.For "
                    message.meeting = meet
                    message.save()
                    meet.save()
                    """
                na = "ok"
                return redirect('people:receptionist_standby',name=na)

        name = face.find()
        print('name',name)
        global name_g
        name_g = name
        if not name:
            print('none got it')
            nam = 'mm'
            a = face.add()
            global face_enco
            face_enco = a
            # print(a)
            return redirect('people:new_person')
        if name == "No Face":
            print("nahi sapadla")
            na = "no"
            return redirect('people:receptionist_standby',name=na)
        person = People.objects.get(name=name)
        person_meet = Meeting.objects.filter(visitor=person).filter(start__date=datetime.date.today())
        # TODO: send the whole query
        place = person.voice.name
        places = place.split('/')
        file = "people/voice/" + places[-1]
        

        return render(request,template_name,{'name':name, 'file':file, 'meetings':person_meet})
    else:
        return redirect('receptionist_login')


def receptionist_record_meeting(request):
    template_name = "people/ReceptionistShowMeeting.html"
    print(request.method)
    if Receptionist_loggedin:
        if request.method == "POST":
            val = record.listen()
            # print("val",val)
            data = request.POST
            meetid = data['meetid']
            meet = Meeting.objects.filter(pk=meetid)[0]
            code = meet.code
            if val == code:
                if not meet.arrived:
                    # print("sucess")
                    msg = " has arrived.For "
                    # global name
                    visitor = People.objects.get(name=name_g)
                    emp = meet.employee
                    m = Message.objects.get_or_create(
                        user=emp,
                        meeting=meet,
                        visitor=visitor,
                        message=msg
                        )
                    # print(m)
                    meet.arrived = True
                    meet.save()
            
            # print(meetid)
            na="ok"
            return redirect('people:receptionist_standby',name=na)

        val = record.listen()
        # print("In html Listen : ",val)
        meeting = Meeting.objects.filter(pk=val)[0]
        # print(meeting)
        na = "ok"
        return render(request,template_name,{'meeting':meeting})
    else:
        return redirect('receptionist_login')



# def receptionist_record_code(request):
    

def invite(request,pk):# *args,**kwargs):
    # print("hello",pk)
    message = Message.objects.get(pk=pk)
    message.read = True
    message.save()
    meet = Meeting.objects.get(pk=message.meeting.pk)
    # print(meet.visitor)
    msg = ReceptionistDisplayMessage.objects.get_or_create(meeting=meet)

    return redirect('people:detail')


def arrive(request):
    data = request.POST
    code = data['cod']
    #  print("code",code)
    na = "ok"
    return redirect('people:receptionist_standby', name=na)


class Person(LoginRequiredMixin,DetailView):
    model = People
    context_object_name = 'person'
    template_name = 'people/PersonDetail.html'

    def get_context_data(self,**kwargs):
        b =  face_enco
        # print('b',b)
        context = super().get_context_data(**kwargs)
        p_meet = Meeting.objects.filter(visitor=context['person']).order_by('-start')
        print(p_meet)
        context['meets'] = p_meet
        return context


def new_person(request):
    template_name = 'people/NewPerson.html'
    if request.method == "POST":
        data = request.POST
        name = data['name']
        email = data['email']
        encoded_array = face_enco[1]
        encoded_list = encoded_array.tolist()
        person = People.objects.get_or_create(name=name,face_encoding=encoded_list,email=email)[0]

        base = os.getcwd()
        new = os.path.join(base, 'people', 'Voice')
        os.chdir(new)
        a = say(name + "  .")
        os.chdir(base)
        file = "people/Voice/" + a
        with open(file, 'rb') as audio:
                person.voice.save(a,File(audio))



        global g_face_list
        g_face_list.append(encoded_array)
        t_fl = g_face_list
        global g_name_list
        g_name_list.append(name)
        t_nl = g_name_list
        global face
        face = Face(t_fl,t_nl)
        
        na = "ok"
        return redirect('people:receptionist_standby',name=na)

    else:
        return render(request,template_name)

