from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from textblob import TextBlob

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# from Crime.models import PoliceStation, PoliceReg, UserReg, Criminals, Feedback, fir_reg
from law.models import Lawyer, Client, Feedback


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'admin/admin_index.html'
    login_url = '/'


class NewLaw(LoginRequiredMixin,TemplateView):
    template_name = 'admin/approve_law.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(NewLaw,self).get_context_data(**kwargs)
        l = Lawyer.objects.filter(user__last_name='0',user__is_staff='0')
        context['l'] =  l
        return context

class FeedbackView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/view_feedback.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(FeedbackView, self).get_context_data(**kwargs)
        feedbacks = Feedback.objects.all()

        # Add sentiment analysis for each feedback
        feedback_list = []
        for feedback in feedbacks:
            analysis = TextBlob(feedback.feed)
            # Get the polarity: -1 (negative) to +1 (positive)
            sentiment = 'Neutral'
            if analysis.sentiment.polarity > 0:
                sentiment = 'Positive'
            elif analysis.sentiment.polarity < 0:
                sentiment = 'Negative'
            
            # Append feedback and sentiment as a dictionary to feedback_list
            feedback_list.append({
                'feed': feedback.feed,
                'client': feedback.client,  # Include client details
                'sentiment': sentiment
            })

        # Pass feedback with sentiment analysis to the context
        context['feedbacks'] = feedback_list
        return context
    
    
class ViewLaw(LoginRequiredMixin,TemplateView):
    template_name = 'admin/view_law.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ViewLaw,self).get_context_data(**kwargs)
        l = Lawyer.objects.filter(user__last_name='1',user__is_staff='0')
        context['l'] =  l
        return context

class RejectView(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        a= Lawyer.objects.get(user_id=user.id)
        a.status='removed'
        a.save()
        user.last_name='0'
        user.is_active='0'
        user.save()
        return render(request,'admin/admin_index.html',{'message':"Account Removed"})

class Client_RejectView(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        a= Client.objects.get(user_id=user.id)
        a.status='removed'
        a.save()
        user.last_name='0'
        user.is_active='0'
        user.save()
        return render(request,'admin/admin_index.html',{'message':"Account Removed"})

class ApproveView(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name='1'

        user.save()
        return render(request,'admin/admin_index.html',{'message':"Account Activated"})

class ViewC(LoginRequiredMixin,TemplateView):
    template_name = 'admin/view_user.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ViewC,self).get_context_data(**kwargs)
        l = Client.objects.filter(user__last_name='1',user__is_staff='0')
        context['l'] =  l
        return context

class Removed_Lowyer(TemplateView):
    template_name = 'admin/removed_lowyer.html'
    def get_context_data(self, **kwargs):
        context = super(Removed_Lowyer,self).get_context_data(**kwargs)
        l = Lawyer.objects.filter(status='removed')
        context['l'] =  l
        return context

class Removed_Client(TemplateView):
    template_name = 'admin/remove_client.html'
    def get_context_data(self, **kwargs):
        context = super(Removed_Client,self).get_context_data(**kwargs)
        l = Client.objects.filter(status='removed')
        context['l'] =  l
        return context
