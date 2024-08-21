from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.utils import timezone
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import Hotel, Room, Reservation


class HomePageView(TemplateView):
    template_name = "home.html"


class HotelsPageView(LoginRequiredMixin,ListView):
    model = Hotel
    template_name = "hotels.html"
    login_url = reverse_lazy('login')


class HotelsDetailView(LoginRequiredMixin,DetailView):
    model = Hotel
    template_name = "hotel_details.html"
    login_url = reverse_lazy('login')


class RoomDetailView(LoginRequiredMixin,DetailView):
    model = Room
    template_name = 'room_details.html'


class HotelCreateView(CreateView):
    model = Hotel
    template_name = "add_hotel.html"
    fields = ["name", "rank", "country", "city"]


class ReservationForm(forms.ModelForm):
    chosen_hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), required=True)
    chosen_room = forms.ModelChoiceField(queryset=Room.objects.all(), required=True)

    class Meta:
        model = Reservation
        fields = ['check_in_date', 'check_out_date', 'chosen_hotel', 'chosen_room']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chosen_hotel'].queryset = Hotel.objects.all()
        self.fields['chosen_room'].queryset = Room.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        chosen_hotel = cleaned_data.get('chosen_hotel')
        chosen_room = cleaned_data.get('chosen_room')
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_in_date < now().date():
            self.add_error('check_in_date', "Check-in date cannot be in the past.")

        if check_out_date and check_out_date < now().date():
            self.add_error('check_out_date', "Check-out date cannot be in the past.")

        if chosen_hotel and chosen_room:
            if chosen_room.hotel != chosen_hotel:
                self.add_error('chosen_room', "The room does not exist in the hotel")

        if check_in_date is None or check_out_date is None:
            self.add_error(None, "Check-in and check-out dates are required.")
        elif check_in_date >= check_out_date:
            self.add_error(None, "Check-in date must be before check-out date.")

        if check_in_date and check_out_date:
            if chosen_room:
                overlapping_reservations = Reservation.objects.filter(
                    room=chosen_room,
                    check_out_date__gt=check_in_date,
                    check_in_date__lt=check_out_date
                )
                if overlapping_reservations.exists():
                    error_message = "The selected room is not available for the selected dates."
                    self.add_error('chosen_room', error_message)
                    self.add_error('check_in_date', error_message)
                    self.add_error('check_out_date', error_message)
        else:
            if not check_in_date:
                self.add_error('check_in_date', "Check-in date is required.")
            if not check_out_date:
                self.add_error('check_out_date', "Check-out date is required.")

        return cleaned_data


    def save(self, commit=True):
        reservation = super().save(commit=False)
        reservation.room = self.cleaned_data['chosen_room']
        reservation.hotel = self.cleaned_data['chosen_hotel']
        if commit:
            reservation.save()
        return reservation

class ReservationFormView(LoginRequiredMixin, FormView):
    template_name = 'reservation_form.html'
    form_class = ReservationForm
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('order_confirmation', kwargs={'reservation_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_name'] = self.request.user.username 
        # context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return redirect('order_confirmation', reservation_id=self.object.pk)  # Redirect to order confirmation page

    def form_invalid(self, form):
        now = timezone.now().date() # Get the current date and time

        # Assuming `check_in_date` and `check_out_date` are the fields in your form
        check_in_date = form.cleaned_data.get('check_in_date')
        check_out_date = form.cleaned_data.get('check_out_date')

        # Check if the requested dates are in the past
        if check_in_date and check_in_date < now:
            form.add_error('check_in_date', 'Check-in date cannot be in the past.')
            return super().form_invalid(form)

        if check_out_date and check_out_date < now:
            form.add_error('check_out_date', 'Check-out date cannot be in the past.')
            return super().form_invalid(form)
        
        if 'chosen_room' in form.errors:
            for error in form.errors['chosen_room']:
                if "The room does not exist in the hotel" in error:
                    return redirect('error_room')
                if "The selected room is not available for the selected dates." in error:
                    return redirect('error_dates')
                
        if form.errors.get('__all__') and ("Check-in date must be before check-out date." in form.errors['__all__']):
            return redirect('invalid_dates')
            
        return super().form_invalid(form)
    
def order_confirmation_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'order_confirmation.html', {'reservation': reservation})

def error_room_view(request):
    return render(request, 'error_room.html',{'error_msg':'The room does not exist in the hotel'})

def error_dates_view(request):
    return render(request, 'error_dates.html', {'error_msg': 'The selected room is not available for the selected dates.'})

def invalid_dates_view(request):
    return render(request,'invalid_dates.html',{'error_msg':"Dates in reservation are invalid."})
