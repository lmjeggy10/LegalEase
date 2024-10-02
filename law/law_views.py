from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template.loader import render_to_string

import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.db.models import Count
import matplotlib.pyplot as plt
import io
import base64
from django.utils import timezone
from xhtml2pdf import pisa

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
        lawyer_id = self.request.user.id

        # 1. Number of Clients Bar Chart
        client_count = Appointment.objects.filter(lawyer__user_id=lawyer_id, status='Myclient').count()

        # Create a bar chart for total clients
        fig, ax = plt.subplots()
        ax.bar(['Clients'], [client_count])
        ax.set_ylabel('Number of Clients')
        ax.set_title('Total Number of Clients')

        # Convert bar chart to image
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        context['chart'] = image_base64

        # 2. Monthly Client Growth Line Chart
        clients_per_month = (Appointment.objects.filter(lawyer__user_id=lawyer_id, status='Myclient')
                             .annotate(month=TruncMonth('client__created_at'))
                             .values('month')
                             .annotate(client_count=Count('id'))
                             .order_by('month'))

        months = [c['month'].strftime('%B %Y') for c in clients_per_month]
        client_counts = [c['client_count'] for c in clients_per_month]

        if months and client_counts:  # Ensure there is data to plot
            fig2, ax2 = plt.subplots()
            ax2.plot(months, client_counts, marker='o')
            ax2.set_xlabel('Month')
            ax2.set_ylabel('Number of New Clients')
            ax2.set_title('Monthly Client Growth')
            ax2.set_xticks(range(len(months)))
            ax2.set_xticklabels(months, rotation=45)

            # Convert line chart to image
            buf2 = io.BytesIO()
            plt.savefig(buf2, format='png')
            buf2.seek(0)
            image_base64_2 = base64.b64encode(buf2.read()).decode('utf-8')
            buf2.close()
            context['client_growth_chart'] = image_base64_2

        return context



class GenerateReportView(View):
    template_name = 'lawyer/report_template.html'

    def get(self, request):
        # Display the report form to select a date range
        return render(request, 'lawyer/report_form.html')

    def post(self, request):
        lawyer_id = request.user.id
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Fetch clients and appointments for the lawyer
        lawyer = Lawyer.objects.get(user_id=lawyer_id)
        clients = Appointment.objects.filter(lawyer__user_id=lawyer_id, status='Myclient').select_related('client')

        # Fetch appointments within the specified date range
        appointments = Appointment.objects.filter(
            lawyer__user_id=lawyer_id,
            date__range=[start_date, end_date]
        ).select_related('client')

        # Prepare the context for the report
        context = {
            'lawyer': lawyer,
            'clients': clients,
            'appointments': appointments,
            'start_date': start_date,
            'end_date': end_date
        }

        # Generate the HTML content for the report
        html_content = render_to_string(self.template_name, context)

        # Convert the HTML content to PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="client_appointment_report_{start_date}_to_{end_date}.pdf"'
        pisa_status = pisa.CreatePDF(html_content, dest=response)

        if pisa_status.err:
            return HttpResponse('Error generating PDF <pre>' + html_content + '</pre>')
        return response