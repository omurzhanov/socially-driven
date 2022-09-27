import datetime
import math

from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.views.generic import UpdateView, DeleteView, ListView
from django.utils import timezone

from .models import Category, Post, Image
from .forms import PostForm, ImageForm


class PostListView(ListView):
    model = Post
    template_name = 'free_stuff/post_list.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all().annotate(posts_count=Count('posts'))
        posts = context['posts']

        context['city_selected'] = self.request.GET.get('city', 'All')
        context['category_selected'] = self.request.GET.get('category', 'Any')
        context['date_selected'] = self.request.GET.get('date_posted', 'Anytime')

        context['query'] = self.request.GET.get('q', '') 
        context['free_stuff'] = True
        context['categories'] = categories
        context['cities'] = {post.city for post in posts}
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        city = self.request.GET.get('city', 'None')
        category = self.request.GET.get('category', 'None')
        date_posted = self.request.GET.get('date_posted', 'None')
        
        object_list = self.model.objects.all()
        
        if query:
            object_list = object_list.filter(Q(title__icontains=query)|Q(description__icontains=query))

        if city != 'None':
            object_list = object_list.filter(city=city)
        
        if category != 'None':
            object_list = object_list.filter(category__title=category)
        
        if date_posted != 'None':
            now_ = timezone.now()
            days = datetime.timedelta(int(date_posted))
            date_ = now_ - days
            object_list = object_list.filter(created__gte=date_)
        
        return object_list

@login_required
def create_post(request):
    imageform = ImageForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        images = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            for i in images:
                Image.objects.create(post=f, image=i)
            messages.success(request, 'New post uploaded successfully')
            return HttpResponseRedirect(reverse('post-list'))
    else:
        form = PostForm()
    return render(request, 'free_stuff/create_post.html', {'form':form, 'imageform': imageform})


@login_required
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    position = Post.objects.filter(created__gte=post.created).order_by('created').count()
    page = math.ceil(position/12)
    images = Image.objects.filter(post=post)
    return render(request, 'free_stuff/post_detail.html', {'post':post, 'images': images, 'page':page})

@login_required
def my_post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    posts = Post.objects.filter(author=request.user)
    position = posts.filter(created__gte=post.created).order_by('created').count()
    page = math.ceil(position/6)
    images = Image.objects.filter(post=post)
    return render(request, 'free_stuff/my_post_detail.html', {'post':post, 'images': images, 'page':page})

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'free_stuff/edit_post.html'
    fields = ['title','category', 'description', 'phone', 'city']
    context_object_name = 'post'


class DeletePostView(DeleteView):
    model = Post
    template_name = 'free_stuff/delete_post.html'
    success_url = reverse_lazy('my-posts')

    
class MyPostsView(ListView):
    model = Post
    template_name = 'free_stuff/my_posts.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        posts = Post.objects.filter(author=self.request.user)
        return posts
