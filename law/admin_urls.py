from django.urls import path

from law.admin_views import IndexView, NewLaw, ApproveView, RejectView, ViewLaw, ViewC, FeedbackView, Removed_Lowyer, \
    Client_RejectView, Removed_Client
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('',IndexView.as_view()),
    path('NewLaw',NewLaw.as_view()),
path('ApproveView',ApproveView.as_view()),
    path('RejectView',RejectView.as_view()),
    path('ViewLaw',ViewLaw.as_view()),
    path('ViewC',ViewC.as_view()),
    path('FeedbackView',FeedbackView.as_view()),
    path('removed_lowyer',Removed_Lowyer.as_view()),
    path('reject_client',Client_RejectView.as_view()),
    path('remove_client',Removed_Client.as_view()),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
        ),
        name='logout'
    ),

]
def urls():
      return urlpatterns,'admin','admin'