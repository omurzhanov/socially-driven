import random 

from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.forms import PayPalPaymentsForm

from petition.models import Petition

from .models import Fundraiser, Category, Image, Comment, Donation
from .forms import FundraiserForm, ImageForm, EmailPostForm, FundraiserEditForm

def home(request):
    fundraisers = sorted(Fundraiser.objects.all(), key=lambda obj: -obj.get_percentage)
    petitions = sorted(Petition.objects.all(), key=lambda obj: -obj.get_percentage)

    return render(request, 'fundraiser/home.html', {'fundraisers': fundraisers, 'petitions': petitions})


class MyDonationListView(LoginRequiredMixin, ListView):
    model = Donation
    template_name = 'fundraiser/my_donations.html'
    context_object_name = 'donations'

    def get_queryset(self):
        object_list = self.model.objects.filter(author=self.request.user)
        return object_list
    

class MyFundDeleteView(LoginRequiredMixin, DeleteView):
    model = Fundraiser
    template_name = 'fundraiser/delete_fundraiser.html'
    success_url = reverse_lazy('my-fundraisers')
    context_object_name = 'fundraiser'

class MyFundListView(LoginRequiredMixin, ListView):
    model = Fundraiser
    template_name = 'fundraiser/my_fundraisers.html'
    context_object_name = 'fundraisers'

    def get_queryset(self):
        object_list = self.model.objects.filter(author=self.request.user)
        return object_list


class MyFundDetailView(LoginRequiredMixin, DetailView):
    model = Fundraiser
    template_name = 'fundraiser/my_fundraiser.html'
    context_object_name = 'fundraiser'
    extra_context = {'words': Comment.objects.all()}


class MyFundUpdateView(LoginRequiredMixin, UpdateView):
    model = Fundraiser
    template_name = 'fundraiser/edit_fundraiser.html'
    form_class = FundraiserEditForm
    context_object_name = 'fundraiser'


class FundDetailView(DetailView):
    model = Fundraiser
    template_name = 'fundraiser/fundraiser_detail.html'
    context_object_name = 'fundraiser'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        f = self.get_object()
        comments = f.words.all()[:5]
        donations = f.donations.all().order_by('-created')[:5]
        f = context['fundraiser']
        context['is_donator'] = True if self.request.user in f.donators.all() else False
        context['comments'] = comments
        context['donations'] = donations

        return context
    
    def post(self, request, **kwargs):
        comment = request.POST.get('comment', None)
        self.object = self.get_object()
        if comment:
            Comment.objects.create(author=request.user, fundraiser=self.object, body=comment)            
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context=context)


class FundListView(ListView):
    model = Fundraiser
    template_name = 'fundraiser/fundraiser_list.html'
    context_object_name = 'fundraisers'
    extra_context = {'is_fundraiser': True}
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = context['fundraisers']
        cause = int(self.request.GET.get('cause', '0'))
        cities = {event.city for event in events}
        if cause == 0:
            cities = {event.city for event in Fundraiser.objects.all()}

        context['causes'] = Category.objects.all()
        context['cause_selected'] = cause
        context['city_selected'] = self.request.GET.get('city', 'City')
        context['query'] = self.request.GET.get('q', '') 
        context['cities'] = cities

        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        city = self.request.GET.get('city', 'None')
        cause = self.request.GET.get('cause', '0')

        object_list = self.model.objects.all()
        
        if query:
            object_list = object_list.filter(Q(title__icontains=query)|Q(description__icontains=query))
        
        if city != 'None':
            object_list = object_list.filter(city=city)
        
        if cause != '0':
            object_list = object_list.filter(category=cause)
        object_list = sorted(object_list, key= lambda obj: -obj.get_percentage)
        return object_list


@login_required
def add_fundraiser(request):
    imageform = ImageForm()
    if request.method == 'POST':
        form = FundraiserForm(request.POST)
        images = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            for i in images:
                Image.objects.create(fundraiser=f, image=i)
            messages.success(request, 'Fundraiser created successfully')
            return HttpResponseRedirect(reverse('fund-list'))
    else:
        form = FundraiserForm()
    return render(request, 'fundraiser/add_fundraiser.html', {'form':form, 'imageform': imageform})


@login_required
def fundraiser_share(request, pk):
    fundraiser = get_object_or_404(Fundraiser, id=pk)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            _url = request.build_absolute_uri(fundraiser.get_absolute_url())
            subject = f"{cd['name']} shared with you fundraiser " \
                      f"{fundraiser.title}"
            message = f"Donate the {fundraiser.title} at {_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'omurzhanovz@gmail.com', [cd['email']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'fundraiser/share_fundraiser.html', {'fundraiser': fundraiser, 'form': form , 'sent': sent})


@login_required
def donate(request, pk):
    fundraiser = get_object_or_404(Fundraiser, id=pk)
    show = False
    if request.method == 'POST':
        print(request.POST)
        other = request.POST.get('other', '')
        radio = request.POST.get('radio-group', 'on')
        amount = other
        if radio != 'on':
            amount = radio
        
        if int(amount) > 0:
            donation = Donation.objects.create(author=request.user, fundraiser=fundraiser, amount=amount)
            request.session['donation_id'] = donation.pk
            return redirect(reverse('payment-process'))
        else:
            show = True
    return render(request, 'fundraiser/donate.html', {'show': show})


def payment_process(request):
    pk = request.session.get('donation_id')
    donation = get_object_or_404(Donation, id=pk)
    host = request.get_host()

    done = reverse('payment-done', kwargs={'pk':pk})
    cancel = reverse('payment-canceled', kwargs={'pk':pk})

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': donation.amount,
        'fundraiser': donation.fundraiser.title,
        'invoice': str(pk),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, done),
        'cancel_return': 'http://{}{}'.format(host, cancel),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'fundraiser/process.html', {'donation': donation, 'form': form})


@csrf_exempt
def payment_done(request,pk):
    donation = get_object_or_404(Donation, id=pk)
    money = donation.fundraiser.money_raised
    donation.fundraiser.money_raised = money + donation.amount
    donation.fundraiser.donators.add(request.user)
    donation.fundraiser.save()
    id = donation.fundraiser.pk
    return render(request, 'fundraiser/done.html', {'pk': id})


@csrf_exempt
def payment_canceled(request,pk):
    Donation.objects.filter(pk=pk).delete()
    return render(request, 'fundraiser/canceled.html')