from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'blog/dashboard.html')

@login_required(login_url="login")
def contact(request):
	if request.method == "POST":
		message_name = request.POST['message-name']
		message_email = request.POST['message-email']
		message = request.POST['message']

		#send mail function
		send_mail(
			'message from ' + message_name,#subject
			message,#message
			message_email,#fromEmail
			['freakoutbond2@gmail.com'],#ToEmail
			fail_silently=False
			)
		return render(request, 'blog/contact.html', {'message_name': message_name})
	else:
		return render(request, 'blog/contact.html', {})


@login_required(login_url="login")
def downloads(request):
    return render(request, 'blog/downloads.html')



def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		context = {}
		if request.method == "POST":
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username = username, password = password)
			
			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username or Password is incorrect!')

		return render(request, 'blog/login.html', context)

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == "POST":
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account created successfully for ' + user)
				return redirect('login')

		context = {'form':form}
		return render(request, 'blog/register.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def sendEmail(request):

	if request.method == 'POST':

		template = render_to_string('blog/email_template.html', {
			'name':request.POST['name'],
			'email':request.POST['email'],
			'message':request.POST['message'],
			})

		email = EmailMessage(
			request.POST['subject'],
			template,
			settings.EMAIL_HOST_USER,
			['freakoutbond2@gmail.com']
			)

		email.fail_silently=False
		email.send()

	return render(request, 'blog/email_sent.html')
