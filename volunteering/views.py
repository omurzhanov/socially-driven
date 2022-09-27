from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Candidate, Event, Cause, Profile, Skill
from .forms import EventForm, CandidateForm

class EventListView(ListView):
    model = Event
    template_name = 'volunteering/event_list.html'
    context_object_name = 'events'
    extra_context = {'is_event': True}
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = context['events']
        cause = int(self.request.GET.get('cause', '0'))
        goodfor = int(self.request.GET.get('goodfor', '0'))
        
        context['causes'] = Cause.objects.all()
        context['cause_selected'] = cause
        context['goodfor'] = Profile.objects.all()
        context['city_selected'] = self.request.GET.get('city', 'City')
        context['country_selected'] = self.request.GET.get('country', 'Country')
        context['goodfor_selected'] = goodfor
        context['query'] = self.request.GET.get('q', '') 
        context['cities'] = {event.city for event in events}
        context['countries'] = {event.country for event in events}

        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        city = self.request.GET.get('city', 'None')
        cause = self.request.GET.get('cause', '0')
        goodfor = self.request.GET.get('goodfor', '0')

        object_list = self.model.objects.all()
        
        if query:
            object_list = object_list.filter(Q(title__icontains=query)|Q(description__icontains=query))
        
        if city != 'None':
            object_list = object_list.filter(city=city)
        
        if cause != '0':
            object_list = object_list.filter(cause__in=cause)

        if goodfor != '0':
            object_list = object_list.filter(goodfor__in=goodfor)

        return object_list


class MyEventListView(ListView):
    model = Event
    template_name = 'volunteering/my_events.html'
    context_object_name = 'events'
    extra_context = {'is_event': True}
    paginate_by = 12



    def get_queryset(self):
        object_list = self.model.objects.all()
        user = self.request.user
        object_list = object_list.filter(author=user)

        return object_list


class MyEventDetailView(DetailView):
    model = Event
    template_name = 'volunteering/my_event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = context['event']
        context['candidates'] = Candidate.objects.filter(event=event)
        return context 


class EventDetailView(DetailView):
    model = Event
    template_name = 'volunteering/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        event = context['event']
        context['is_applied'] = True if user in event.volunteers.all() else False
        return context 


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        image = request.FILES.get('image')
        if form.is_valid():
            cause = form.cleaned_data.get('cause')
            goodfor = form.cleaned_data.get('goodfor')

            causes = Cause.objects.filter(id__in=cause)
            goodfor = Profile.objects.filter(id__in=goodfor)

            f = form.save(commit=False)
            f.author = request.user

            if image:
                f.image = image
            f.save()

            for cause in causes:
                f.cause.add(cause)
            for pr in goodfor:
                f.goodfor.add(pr)    
            return HttpResponseRedirect(reverse('add-skill', kwargs={'pk':f.pk}))
    else:
        form = EventForm()
    return render(request, 'volunteering/event_create.html', {'form':form})


@login_required
def add_skill(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except:
        event = None
    if event:
        if request.method == 'POST':
            skill = request.POST.get('skill', None)
            res = request.POST.get('SUBMIT', None)
            try:
                skill_exist = Skill.objects.get(name=skill)
                event.skills.add(skill_exist)
            except:
                new_skill = Skill.objects.create(name=skill)
                new_skill.skill_events.add(event)
            if res == 'Save':
                return HttpResponseRedirect(reverse('my-event-detail', kwargs={'pk':event.pk}))

            return HttpResponseRedirect(reverse('add-skill', kwargs={'pk':event.pk}))
        else:
            return render(request, 'volunteering/add_skills.html', {'event': event})
    else:
        return render(request, 'volunteering/error.html')


@login_required
def apply_to_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except:
        event = None
    if event:
        if request.method == 'POST':
            form = CandidateForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')
                message = form.cleaned_data.get('message')
                Candidate.objects.create(email=email, phone=phone, message=message, event=event)
                event.volunteers.add(request.user)
                return HttpResponseRedirect(reverse('event-list'))
        else:
            form = CandidateForm()
        return render(request, 'volunteering/apply.html', {'form': form})
    else:
        return render(request, 'volunteering/error.html')


class DeleteEventView(DeleteView):
    model = Event
    template_name = 'volunteering/delete_event.html'
    success_url = reverse_lazy('my-events')
