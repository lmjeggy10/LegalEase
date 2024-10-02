from django.urls import path

from law.admin_views import IndexView, NewLaw, ApproveView, RejectView, ViewLaw, ViewC, FeedbackView, Removed_Lowyer, \
    Client_RejectView, Removed_Client, FeedbackSentimentPieChartView, ClientsPerLawyerView, generate_lawyer_report, generate_client_report
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
    path('feedback_pie_chart/', FeedbackSentimentPieChartView.as_view(), name='feedback_pie_chart'),
    path('clients_per_lawyer/', ClientsPerLawyerView.as_view(), name='clients_per_lawyer'),
    path('generate_lawyer_report/', generate_lawyer_report, name='generate_lawyer_report'),
    path('generate_client_report/<int:client_id>/', generate_client_report, name='generate_client_report'),
    

    

    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
        ),
        name='logout'
    ),

]
def urls():
      return urlpatterns,'admin','admin'