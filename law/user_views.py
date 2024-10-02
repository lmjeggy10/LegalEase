import requests
from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# from Crime.models import Criminals, Feedback, UserReg, PoliceReg, fir_reg
from law.models import Lawyer, Appointment, Client, Ask, Feedback


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'user/user_index.html'
    login_url = '/'

class ViewLaw(LoginRequiredMixin,TemplateView):
    template_name = 'user/view_law.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ViewLaw,self).get_context_data(**kwargs)
        l = Lawyer.objects.filter(user__last_name='1',user__is_staff='0')
        context['l'] =  l
        return context


class ViewLawDe(LoginRequiredMixin,TemplateView):
    template_name = 'user/law_details.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ViewLawDe,self).get_context_data(**kwargs)
        id = self.request.GET['id']
        l = Lawyer.objects.filter(pk=id)
        context['l'] =  l
        return context

class Appoinments(LoginRequiredMixin,TemplateView):
    template_name = 'user/appoinment.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(Appoinments,self).get_context_data(**kwargs)
        id = self.request.GET['id']

        context['id'] =  id
        return context

    def post(self, request, *args, **kwargs):
        lawyer = request.POST['lawyer']
        reason = request.POST['reason']


        l = Lawyer.objects.get(pk=lawyer)

        c = Client.objects.get(user_id=self.request.user.id)

        b = Appointment()

        b.reason = reason
        b.status = 'Sent'
        b.client = c
        b.lawyer = l
        b.save()

        messages = "Appointment Successfully"
        return render(request, 'user/user_index.html', {'message': messages})


class ViewAppoinments(LoginRequiredMixin,TemplateView):
    template_name = 'user/my_appointment.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ViewAppoinments,self).get_context_data(**kwargs)
        l = Appointment.objects.filter(client__user_id=self.request.user.id)

        context['l'] =  l
        return context


class MyLawyer(LoginRequiredMixin,TemplateView):
    template_name = 'user/my_lawyer.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(MyLawyer,self).get_context_data(**kwargs)
        l = Appointment.objects.filter(client__user_id=self.request.user.id,status='Myclient')

        context['l'] =  l
        return context

class MessageDetails(LoginRequiredMixin, TemplateView):
    template_name = 'user/message.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(MessageDetails, self).get_context_data(**kwargs)
        l = Ask.objects.filter(client__user_id=self.request.user.id)
        context['l'] = l
        return context
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        reply = request.POST['reply']
        ask = request.POST['ask']

        b = Ask.objects.get(pk=ask)

        b.status = reply
        b.file = file
        b.save()

        messages = "Upload Successfully"
        return render(request, 'user/user_index.html', {'message': messages})

class FeedbackSug(LoginRequiredMixin,TemplateView):
    template_name = 'user/feed.html'
    login_url = '/'

    def post(self, request, *args, **kwargs):

        feed = request.POST['feed']

        c = Client.objects.get(user_id=self.request.user.id)
        b = Feedback()

        b.feed = feed
        b.client = c
        b.save()

        messages = "sent Successfully"
        return render(request, 'user/user_index.html', {'message': messages})
    

# Replace with your API key
API_KEY = 'AIzaSyBCwgPcBEKF_5jBrEppn6rhXXv9Zm3TDp0'
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

# Define predefined responses
PREDEFINED_RESPONSES = {
    "Can you tell me what this THRIVEseeds is about?": "Hi, I’m Cropsy! Our e-commerce website THRIVEseeds specializes in selling high-quality crop seeds for various agricultural needs.",
    "What kinds of crop seeds do you sell?": "Cropsy here! We offer a diverse range of crop seeds including vegetables, fruits, grains, and pulses.",
    "how are you": "I'm just a chatbot here to assist you with crop seed-related questions. How can I help you today?",
    # Add more predefined responses as needed
}

def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')

        # Retrieve or initialize conversation history
        conversation_history = request.session.get('conversation_history', [])

        # Add user message to conversation history
        conversation_history.append(f"input: {user_message}")

        # Check if the message matches any predefined response
        bot_reply = PREDEFINED_RESPONSES.get(user_message, None)

        if not bot_reply:
            # Define headers and data for the API request
            headers = {
                'Content-Type': 'application/json',
            }

            # Prepare context: Use the conversation history
            messages = [{'text': message} for message in conversation_history]

            # Prepare data with context (previous conversation)
            data = {
                'contents': [
                    {
                        'parts': messages
                    }
                ]
            }

            # Make the API request
            try:
                response = requests.post(f'{API_URL}?key={API_KEY}', headers=headers, json=data)
                response.raise_for_status()  # Raise an exception for HTTP errors

                # Parse the JSON response
                api_response = response.json()
                print("API Response:", api_response)  # For debugging

                # Extract the bot reply from the response
                bot_reply = api_response['candidates'][0]['content']['parts'][0]['text']

                # Limit the response to a certain number of sentences (e.g., 3)
                bot_reply = '. '.join(bot_reply.split('. ')[:3])  # Limits the response to 3 sentences

            except requests.RequestException as e:
                # Handle request errors
                print(f"API request error: {e}")
                bot_reply = 'Sorry, there was an error processing your request.'

        # Add bot response to conversation history
        conversation_history.append(f"output: {bot_reply}")

        # Store updated conversation history in session
        request.session['conversation_history'] = conversation_history

        return JsonResponse({'reply': bot_reply})

    # Render the chat interface if not a POST request
    return render(request, 'user/chatbot.html')