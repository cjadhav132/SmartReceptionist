from django.conf.urls import url
from .views import (ShowMessage,Employee,Employee_message,
                    CreateMeeting,MeetingDetail,show_receptionist,
                    receptionist_standby,invite,Person,new_person,
                    receptionist_record_meeting)

app_name = 'people'

urlpatterns = [
    url(r'^messages',ShowMessage.as_view(),name='show'),
    url(r'detail',Employee.as_view(),name='detail'),
    url(r'message', Employee_message.as_view(), name='emplo_message'),
    url(r'create_meeting', CreateMeeting.as_view(), name='create_meeting'),
    url(r'receptionist_standby/(?P<name>\w+)/$', receptionist_standby, name='receptionist_standby'),
    url(r'receptionist$', show_receptionist, name='receptionist'),
    url(r'meeting/(?P<pk>\d+)$', MeetingDetail.as_view(), name='show_meeting'),
    url(r'invite(?P<pk>\d+)/$',invite,name='invite'),
    url(r'person/(?P<pk>\d+)$', Person.as_view(), name='show_person'),
    url(r'new/person$', new_person, name='new_person'),
    url(r'^rec$', receptionist_record_meeting, name='rec'),

    
]