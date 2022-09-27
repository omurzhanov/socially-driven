import math

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from .models import Petition, Comment, Category, Image
from .forms import ImageForm, PetitionForm, EmailPostForm


class MyPetitionsView(ListView):
    model = Petition
    template_name = 'petitions/my_petitions_list.html'
    context_object_name = 'petitions'
    paginate_by = 5

    def get_queryset(self):
        object_list = self.model.objects.filter(author=self.request.user)
        return object_list

class PetitionListView(ListView):
    model = Petition
    template_name = 'petitions/petition_list.html'
    context_object_name = 'petitions'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        categories = {pet.category.pk for pet in context['petitions']}
        context['query'] = self.request.GET.get('q', '')
        context['is_petitions'] = True
        context['categories'] = Category.objects.filter(pk__in=categories)
        context['categories_'] = Category.objects.exclude(pk__in=categories)
        return context
    
    def get_queryset(self):
        query = self.request.GET.get('q', None)
        category = self.request.GET.get('category', None)
        object_list = self.model.objects.all()

        if query != '' and not query is None:
            object_list = object_list.filter(Q(title__icontains=query)|Q(description__icontains=query))

        if category:
            object_list = object_list.filter(category__pk=category)
            
        object_list = sorted(object_list, key= lambda obj: -obj.get_percentage)
        return object_list


class MyPetitionDetailView(LoginRequiredMixin, DetailView):
    model = Petition
    template_name = 'petitions/my_petition_detail.html'
    context_object_name = 'petition'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = self.get_object().get_image
        petitions = Petition.objects.filter(author=self.request.user)
        position = petitions.filter(created__gte=self.get_object().created).order_by('created').count()
        page = math.ceil(position/5)
        context['page'] = page
        context['images'] = self.get_object().images.exclude(id=image.id)
        context['comment_size'] = self.get_object().comments.filter(published=True).count()
        context['comments'] = self.get_object().comments.filter(published=True).order_by('-created')
        return context

class PetitionDetailView(LoginRequiredMixin, DetailView):
    model = Petition
    template_name = 'petitions/petition_detail.html'
    context_object_name = 'petition'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        image = self.get_object().get_image
        user = self.request.user
        position = Petition.objects.filter(created__gte=self.get_object().created).order_by('created').count()
        page = math.ceil(position/5)
        context['page'] = page
        context['images'] = self.get_object().images.exclude(id=image.id)
        context['is_signed'] = user.petitions.filter(pk=self.object.pk).exists()
        context['comment_size'] = self.get_object().comments.filter(published=True).count()
        context['comments'] = self.get_object().comments.filter(published=True).order_by('-created')
        return context

    def post(self, request, **kwargs):
        comment = request.POST.get('comment', None)
        comment_hide = request.POST.get('commentHide', False)
        self.object = self.get_object()
        comment_hide = not comment_hide
            
        if comment != '' and comment != None:
            Comment.objects.create(author=request.user, body=comment, 
                                   petition=self.object, published=comment_hide)
        
        self.object.signers.add(request.user)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context=context)


@login_required
def create_petition(request):
    imageform = ImageForm()
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        images = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            for i in images:
                Image.objects.create(petition=f, image=i)
            messages.success(request, 'New post uploaded successfully')
            return HttpResponseRedirect(reverse('petition-list'))
    else:
        form = PetitionForm()
    return render(request, 'petitions/create_petition.html', {'form':form, 'imageform': imageform})


class DeletePetitionView(DeleteView):
    model = Petition
    template_name = 'petitions/delete_petition.html'
    success_url = reverse_lazy('petition-list')


@login_required
def petition_share(request, pk):
    petition = get_object_or_404(Petition, id=pk)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            _url = request.build_absolute_uri(petition.get_absolute_url())
            subject = f"{cd['name']} recommends you sign " \
                      f"{petition.title}"
            message = f"Sign the {petition.title} at {_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'omurzhanovz@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'petitions/share.html', {'petition': petition, 'form': form , 'sent': sent})