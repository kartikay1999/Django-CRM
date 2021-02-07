from django.shortcuts import render
from django.views import generic
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from django.shortcuts import reverse
from .forms import AgentModelForm
from .mixins import OrganiserandLoginRequiredMixin
from django.core.mail import send_mail
# Create your views here.

class AgentListView(OrganiserandLoginRequiredMixin,generic.ListView):
    template_name="agent_list.html"

    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganiserandLoginRequiredMixin,generic.CreateView):
    template_name="agent_create.html"
    form_class=AgentModelForm

    
    def form_valid(self,form):
        user=form.save(commit=False)
        user.is_agent=True
        user.is_organiser=False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile

        )
        send_mail(
            subject="You are invited to be an Agent",
            message="You were added as an agent on CRM",
            from_email='admin@test.com',
            recipient_list=[user.email]
        )
        return super(AgentCreateView,self).form_valid(form)
    def get_success_url(self):
        return reverse("agents:agent-list")
   
class AgentDetailView(OrganiserandLoginRequiredMixin,generic.DetailView):
    template_name="agent_detail.html"
    context_object_name='agent'
    def get_queryset(self):
        return Agent.objects.all()


class AgentUpdateView(OrganiserandLoginRequiredMixin,generic.UpdateView):
    template_name="agent_update.html"
    form_class=AgentModelForm
    def get_queryset(self):
        return Agent.objects.all()

    def get_success_url(self):
        return reverse("agents:agent-list")

class AgentDeleteView(OrganiserandLoginRequiredMixin,generic.DeleteView):
    template_name="agent_delete.html"
    context_object_name='agent'
    def get_queryset(self):
        return Agent.objects.all()
    def get_success_url(self):
        return reverse("agents:agent-list")