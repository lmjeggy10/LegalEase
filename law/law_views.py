from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# from Crime.models import Criminals, PoliceReg, fir_reg, UserReg
from law.models import Lawyer, Appointment, Client, Ask


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'lawyer/law_index.html'
    login_url = '/'

class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'lawyer/myprofile.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        l = Lawyer.objects.get(user_id=self.request.user.id)
        context['l'] = l
        return context

    def post(self, request, *args, **kwargs):
        edu = request.POST['edu']
        pra = request.POST['pra']
        spe = request.POST['spe']
        id = request.POST['id']


        b = Lawyer.objects.get(pk=id)

        b.parea = pra
        b.education = edu
        b.speci = spe
        b.save()

        messages = "Update Successfully"
        return render(request, 'lawyer/myprofile.html', {'message': messages})

class ViewNewAppoinments(LoginRequiredMixin,TemplateView):
    template_name = 'lawyer/new_appointment.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ViewNewAppoinments,self).get_context_data(**kwargs)
        l = Appointment.objects.filter(lawyer__user_id=self.request.user.id,status='Sent')

        context['l'] =  l
        return context

    def post(self, request, *args, **kwargs):
        # complaint = actions.objects.get(user_id=self.request.id)
        id = request.POST['id']
        date = request.POST['date']
        time=request.POST['time']
        act = Appointment.objects.get(id=id)
        if Appointment.objects.filter(date=date,time=time):
            print("fvvfsff")
            return render(request, 'lawyer/law_index.html', {'message': "Already taken"})
        else:
        # act.complaint=complaint
            act.date = date
            act.time=time

            act.status = 'Confirm'
            act.save()

            return render(request,'lawyer/law_index.html',{'message':"Date and Time Scheduled"})

class RejectAppo(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = Appointment.objects.get(pk=id)
        user.status = 'Rejected'
        user.save()
        return render(request,'admin/admin_index.html',{'message':"Removed"})

class AcceptAppo(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = Appointment.objects.get(pk=id)
        user.status = 'Confirm'
        user.save()
        return render(request,'lawyer/law_index.html',{'message':"Accepted"})



class ViewAppoinments(LoginRequiredMixin,TemplateView):
    template_name = 'lawyer/view_appointment.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ViewAppoinments,self).get_context_data(**kwargs)
        l = Appointment.objects.filter(lawyer__user_id=self.request.user.id,status='Confirm')

        context['l'] =  l
        return context

class AddClient(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = Appointment.objects.get(pk=id)
        user.status = 'Myclient'
        user.save()
        return render(request,'lawyer/law_index.html',{'message':"Added to my client"})

class DeleteClient(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = Appointment.objects.get(pk=id).delete()
        return render(request,'lawyer/law_index.html',{'message':"Deleted"})

class Myclient(LoginRequiredMixin,TemplateView):
    template_name = 'lawyer/my_client.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(Myclient,self).get_context_data(**kwargs)
        l = Appointment.objects.filter(lawyer__user_id=self.request.user.id,status='Myclient')

        context['l'] =  l
        return context

class AskDetails(LoginRequiredMixin, TemplateView):
    template_name = 'lawyer/ask_details.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(AskDetails, self).get_context_data(**kwargs)
        id= self.request.GET['id']
        c = Client.objects.get(pk=id)
        context['c'] = c
        return context

    def post(self, request, *args, **kwargs):
        user = request.POST['user']
        reason = request.POST['reason']

        c = Client.objects.get(pk=user)
        l = Lawyer.objects.get(user_id=self.request.user.id)

        b = Ask()

        b.reason = reason
        b.client = c
        b.lawyer = l
        b.status = 'Sent'
        b.file = 'Null'
        b.save()

        messages = "Sent Successfully"
        return render(request, 'lawyer/law_index.html', {'message': messages})

class MessageDetails(LoginRequiredMixin, TemplateView):
    template_name = 'lawyer/message.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(MessageDetails, self).get_context_data(**kwargs)
        l = Ask.objects.filter(lawyer__user_id=self.request.user.id)
        context['l'] = l
        return context
    

class VisualizationView(LoginRequiredMixin, TemplateView):
    template_name = 'lawyer/visualizations.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch lawyer's clients and appointments data
        lawyer_id = self.request.user.id
        client_count = Appointment.objects.filter(lawyer__user_id=lawyer_id, status='Myclient').count()

        # Create a simple bar chart
        fig, ax = plt.subplots()
        ax.bar(['Clients'], [client_count])
        ax.set_ylabel('Number of Clients')
        ax.set_title('Total Number of Clients')

        # Convert the plot to an image that can be displayed in the template
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        context['chart'] = image_base64
        return context