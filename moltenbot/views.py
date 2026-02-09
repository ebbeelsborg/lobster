from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django import forms
from .models import MoltenBot, Execution, ExecutionLog, Organization

class DashboardView(ListView):
    model = MoltenBot
    template_name = 'moltenbot/dashboard.html'
    context_object_name = 'bots'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = Organization.objects.all()
        context['recent_executions'] = Execution.objects.order_by('-started_at')[:5]
        return context

class BotDetailView(DetailView):
    model = MoltenBot
    template_name = 'moltenbot/bot_detail.html'
    context_object_name = 'bot'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = ExecutionLog.objects.filter(execution__bot_version__bot=self.object).order_by('-timestamp')[:50]
        context['executions'] = Execution.objects.filter(bot_version__bot=self.object).order_at('-started_at')[:10]
        return context

class BotForm(forms.ModelForm):
    class Meta:
        model = MoltenBot
        fields = ['name', 'organization', 'description', 'temperature', 'max_temperature']

    def clean_temperature(self):
        temp = self.cleaned_data.get('temperature')
        if temp > 1000:
            raise forms.ValidationError("Bot temperature too high! It will melt. 🔥")
        return temp

class BotCreateView(CreateView):
    model = MoltenBot
    form_class = BotForm
    template_name = 'moltenbot/bot_form.html'
    success_url = reverse_lazy('dashboard')
