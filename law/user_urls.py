from django.urls import path

from law.user_views import IndexView, ViewLaw, ViewLawDe, Appoinments, ViewAppoinments, MyLawyer, MessageDetails, \
    FeedbackSug
from django.contrib.auth import views as auth_views
from law.user_views import chatbot
from . import user_views
urlpatterns = [

    path('',IndexView.as_view()),
    path('ViewLaw',ViewLaw.as_view()),
    path('ViewLawDe',ViewLawDe.as_view()),
    path('Appoinment',Appoinments.as_view()),
    path('ViewAppoinments',ViewAppoinments.as_view()),
    path('MyLawyer',MyLawyer.as_view()),
    path('MessageDetails',MessageDetails.as_view()),
    path('FeedbackSug',FeedbackSug.as_view()),

    path('chatbot/', user_views.chatbot, name='chatbot'),
    

    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
        ),
        name='logout'
    ),


]
def urls():
      return urlpatterns,'user','user'