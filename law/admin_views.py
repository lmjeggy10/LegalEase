from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from textblob import TextBlob
import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponse
from django.template import loader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import plotly.graph_objs as go
from django.shortcuts import render
from django.db.models import Count

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# from Crime.models import PoliceStation, PoliceReg, UserReg, Criminals, Feedback, fir_reg
from law import models
from law.models import Lawyer, Client, Feedback, Appointment


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
    
class FeedbackSentimentPieChartView(View):
    def get(self, request, *args, **kwargs):
        feedbacks = Feedback.objects.all()

        sentiment_count = {'Positive': 0, 'Neutral': 0, 'Negative': 0}

        # Analyze feedback sentiments
        for feedback in feedbacks:
            analysis = TextBlob(feedback.feed)
            if analysis.sentiment.polarity > 0:
                sentiment_count['Positive'] += 1
            elif analysis.sentiment.polarity < 0:
                sentiment_count['Negative'] += 1
            else:
                sentiment_count['Neutral'] += 1

        # Generate Pie Chart
        labels = sentiment_count.keys()
        sizes = sentiment_count.values()
        colors = ['#ff9999','#66b3ff','#99ff99']
        explode = (0.1, 0, 0)  # explode 1st slice for emphasis

        plt.figure(figsize=(6,6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Convert the plot to an image in-memory
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        # Render the image in the template
        return render(request, 'admin/feedback_pie_chart.html', {'chart_image': chart_image})
    

class ClientsPerLawyerView(View):
    def get(self, request, *args, **kwargs):
        # Query to count distinct clients per lawyer through the Appointment model
        lawyer_clients = Lawyer.objects.annotate(num_clients=Count('appointment__client', distinct=True))

        # Prepare data for the bar chart
        lawyers = [lawyer.user.username for lawyer in lawyer_clients]
        client_counts = [lawyer.num_clients for lawyer in lawyer_clients]

        # Pass the data to the template
        return render(request, 'admin/clients_per_lawyer.html', {
            'lawyers': lawyers,
            'client_counts': client_counts
        })
    

def generate_lawyer_report(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lawyer_report.pdf"'

    # Create the PDF object, using the response object as its "file."
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title of the PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 50, "Lawyer Details Report")

    # Table header
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 100, "Name")
    pdf.drawString(150, height - 100, "Phone")
    pdf.drawString(250, height - 100, "Email")
    pdf.drawString(400, height - 100, "Company")
    pdf.drawString(500, height - 100, "Specialization")

    # Retrieve lawyer details from the database
    lawyers = Lawyer.objects.all()
    
    y = height - 130  # Start position for the first lawyer
    pdf.setFont("Helvetica", 10)

    # Loop through each lawyer and add their details to the PDF
    for lawyer in lawyers:
        pdf.drawString(50, y, lawyer.user.first_name)
        pdf.drawString(150, y, lawyer.phone)
        pdf.drawString(250, y, lawyer.user.email)
        pdf.drawString(400, y, lawyer.company)
        pdf.drawString(500, y, lawyer.speci)

        y -= 20  # Move the cursor down to the next line

        # Check if we need to create a new page
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica-Bold", 12)
            y = height - 50

    # Close the PDF object cleanly, and we're done.
    pdf.showPage()
    pdf.save()

    return response


def generate_client_report(request, client_id):
    # Fetch the specific client by ID
    client = Client.objects.get(id=client_id)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{client.user.first_name}_client_report.pdf"'

    # Create the PDF object, using the response object as its "file."
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title of the PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 50, f"{client.user.first_name} {client.user.last_name} Client Report")

    # Client details in the PDF
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 100, "Name:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(150, height - 100, f"{client.user.first_name} {client.user.last_name}")

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 120, "Phone:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(150, height - 120, client.phone)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 140, "Email:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(150, height - 140, client.user.email)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 160, "Address:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(150, height - 160, client.address)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 180, "Registration Fee:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(150, height - 180, f"{client.payment} Paid")

    # Close the PDF object cleanly, and we're done.
    pdf.showPage()
    pdf.save()

    return response