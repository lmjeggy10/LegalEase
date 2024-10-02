from django.urls import path

from law.law_views import IndexView, Profile, ViewNewAppoinments, AcceptAppo, RejectAppo, AddClient, ViewAppoinments, \
    Myclient, AskDetails, DeleteClient,MessageDetails, VisualizationView, GenerateReportView
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('',IndexView.as_view()),
    path('Profile',Profile.as_view()),
    path('ViewNewAppoinments',ViewNewAppoinments.as_view()),
    path('RejectAppo',RejectAppo.as_view()),
    path('AcceptAppo',AcceptAppo.as_view()),
    path('AddClient',AddClient.as_view()),
    path('ViewAppoinments',ViewAppoinments.as_view()),
    path('Myclient',Myclient.as_view()),
    path('AskDetails',AskDetails.as_view()),
    path('DeleteClient',DeleteClient.as_view()),
    path('MessageDetails',MessageDetails.as_view()),

    path('visualizations/', VisualizationView.as_view(), name='visualizations'),
    path('generate_report/', GenerateReportView.as_view(), name='generate_report'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
        ),
        name='logout'
    ),


]
def urls():
      return urlpatterns,'law','law'