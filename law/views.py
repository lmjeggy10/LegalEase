from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

#from Crime.models import
from law.models import UserType, Lawyer, Client


class IndexView(TemplateView):
    template_name = 'index.html'

class LoginView(TemplateView):
    template_name = 'login.html'
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password= request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            if user.last_name == '1':
                if user.is_superuser:
                    return redirect('/admin')
                elif UserType.objects.get(user_id=user.id).type == "user":
                    return redirect('/user')
                else:
                    return redirect('/law')
            else:
                return render(request,'index.html',{'message':" User Account Not Authenticated"})
        else:
            return render(request,'index.html',{'message':"Invalid Username or Password"})


class LawRegs(TemplateView):
    template_name = 'lawyer_reg.html'


    def post(self, request,*args,**kwargs):
        name = request.POST['name']
        emnumber=request.POST['emnumber']
        company = request.POST['company']
        address = request.POST['address']

        contact = request.POST['phone']
        email = request.POST['email']
        photo = request.FILES['photo']
        edu = request.POST['edu']
        parea = request.POST['parea']
        speci = request.POST['speci']
        exper_lowyer= request.POST['exper_lowyer']
        password = request.POST['password']
        con_password = request.POST['con_password']
        if password==con_password:
            user = User.objects.create_user(username=email,password=password,first_name=name,email=email,last_name=0)
            user.save()
            reg = Lawyer()
            reg.user = user
            reg.emnumber=emnumber
            reg.phone = contact
            reg.parea = parea
            reg.speci = speci
            reg.education = edu
            reg.photo = photo
            reg.company = company
            reg.address = address
            reg.payment = '500'
            reg.con_password=con_password
            reg.exper_lowyer=exper_lowyer
            reg.status= '1'
            reg.save()
            usertype = UserType()
            usertype.user = user
            usertype.type = "law"
            usertype.save()
            messages = "Register Successfully."

            return render(request, 'index.html', {'message': messages})

        else:
            messages = "password does not match"
            return render(request,'lawyer_reg.html',{'message':messages})


class UserRegister(TemplateView):
    template_name = 'user_reg.html'

    def post(self, request,*args,**kwargs):
        name = request.POST['name']
        address = request.POST['address']

        contact = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        con_password= request.POST['con_password']

        if password== con_password:
             user = User.objects.create_user(username=email,password=password,first_name=name,email=email,last_name=1)
             user.save()
             reg = Client()
             reg.user = user
             reg.address = address
             reg.phone = contact
             reg.con_password= con_password
             reg.payment = '500'
             reg.save()
             usertype = UserType()
             usertype.user = user
             usertype.type = 'user'
             usertype.save()
             messages = "Register Successfully."

             return render(request, 'user_reg.html', {'message': messages})
        else:
             messages = "Password does no t match!.."
             return render(request,'user_reg.html',{'message':messages})

class Forgot_Password(TemplateView):
    template_name = 'forgot_password.html'
    def get_context_data(self, **kwargs):
        context=super(Forgot_Password,self).get_context_data(**kwargs)
        lowyer=Lawyer.objects.filter(user__last_name='1').count()
        client =Client.objects.filter(user__last_name='1').count()
        admin=User.objects.get(is_superuser='1')
        context['lowyer'] = lowyer
        context['client'] = client
        context['admin']=admin
        return context
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        print(username)

        email= request.POST['email']
        print(email)
        user_id=self.request.user.id
        if User.objects.filter(last_name='1',username=username,email=email):
           user=User.objects.get(last_name='1',username=username,email=email)
           Type=UserType.objects.get(user_id=user.id)
           if Type.type=='law':
              lowyer=Lawyer.objects.get(user_id=user.id)
              Password=lowyer.con_password
              email = EmailMessage(
              Password,
              'Your password',
              settings.EMAIL_HOST_USER,
              [user.email],
              )
              email.fail_silently = False
              email.send()
              return render(request,'index.html',{'message':"Send mail successfully"})
           elif Type.type=='user':

              client=Client.objects.get(user_id=user.id)
              print(user)
              email = EmailMessage(
              client.con_password,
              'Your password',
              settings.EMAIL_HOST_USER,
              [user.email],
               )
              email.fail_silently = False
              email.send()
              return render(request,'index.html',{'message':"Send mail successfully"})

        else:
           return render(request,'index.html',{'message':"Tis User Is Not Exist"})




