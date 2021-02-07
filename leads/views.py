from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

from agents.mixins import OrganiserandLoginRequiredMixin
from .models import Lead,Agent
from .forms import Leadform,Leadmodelform,CustomUserCreationForm
#CRUD - create, retrieve, update and delete + list

#Class based views

class SignupView(generic.CreateView):
    template_name='registration/signup.html'
    form_class=CustomUserCreationForm
    def get_success_url(self):
        return reverse("login")



class Landingpageview(generic.TemplateView):
    template_name="landing.html"

class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name="leads/leads_list.html"
    context_object_name="leads"
    def get_queryset(self):
        user=self.request.user
        if user.is_organiser:
            queryset=Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
            #filter for the agent that is logged in
            queryset=queryset.filter(agent__user=user)
        return queryset



class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    template_name="leads/lead_detail.html"
    context_object_name="lead"
    
    def get_queryset(self):
        user=self.request.user
        if user.is_organiser:
            queryset=Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
            #filter for the agent that is logged in
            queryset=queryset.filter(agent__user=user)
        return queryset




class LeadCreateView(OrganiserandLoginRequiredMixin,generic.CreateView):
    template_name="leads/lead_create.html"
    form_class=Leadmodelform

    def get_success_url(self):
        return reverse("leads:lead-list")
   
    #to send email
    def form_valid(self,form):
        send_mail(subject="Lead has been created",
        message="Go to site to see the new lead",from_email='test@test.com',
        recipient_list=["test2@test.com"]

        )
        return super(LeadCreateView,self).form_valid(form)
    
    
    context_object_name="lead"


class LeadUpdateView(OrganiserandLoginRequiredMixin,generic.UpdateView):
    template_name="leads/lead_update.html"
    
    form_class=Leadmodelform
    def get_queryset(self):
        user=self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    
    def get_success_url(self):
        return reverse('login')


class LeadDeleteView(OrganiserandLoginRequiredMixin,generic.DeleteView):
    template_name="leads/lead_delete.html"
    def get_queryset(self):
        user=self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

  
    def get_sucess_url(self):
        return reverse("leads:lead-list")



# Create your views here.
def landing_page(request):
    return render(request,'landing.html')

def lead_list(request):
    leads=Lead.objects.all()
    context={
        "leads":leads
    }
    return render(request,"leads/leads_list.html",context)
    #return HttpResponse("Hello World")
def second_page(request):
    return render(request,'second_page.html')

def lead_detail(request,pk):
    lead=Lead.objects.get(id=pk)
    print(lead)
    context={
        "lead":lead
    }
    return render(request,'leads/lead_detail.html',context)
    # return HttpResponse('here is the detailed view')

def lead_create(request):
    form=Leadmodelform()
    if request.method=='POST':
        form=Leadmodelform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context={
        "form":form
    }
    return render(request,"leads/lead_create.html",context)





def lead_update(request,pk):
    lead=Lead.objects.get(id=pk)
    form=Leadmodelform(instance=lead)
    if request.method=='POST':
        form=Leadmodelform(request.POST,instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')

    context={
        "form":form,
        "lead":lead
    }
    return render(request, "leads/lead_update.html",context)


def lead_delete(request,pk):
    lead=Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")



"""
def lead_update(request,pk):
    lead=Lead.objects.get(id=pk)
    form=Leadform()
    if request.method=='POST':
        #print("recieving post request")
        form=Leadform(request.POST)
        if form.is_valid():
            #print("form is valid")
            #print(form.cleaned_data)
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            age=form.cleaned_data['age']
            agent=Agent.objects.first()
            lead.first_name=first_name
            lead.last_name=last_name
            lead.age=age
            lead.save()
            return redirect('/leads')
    context={
        "form":form,
        "lead":lead
    }
    return render(request, "leads/lead_update.html",context)


    def lead_create(request):
    form=Leadform()
    if request.method=='POST':
        #print("recieving post request")
        form=Leadform(request.POST)
        if form.is_valid():
            #print("form is valid")
            #print(form.cleaned_data)
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            age=form.cleaned_data['age']
            agent=Agent.objects.first()
            Lead.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,
                agent=agent
            )
            return redirect('/leads')
    context={
        "form":form
    }
    return render(request,"leads/lead_create.html",context)
"""