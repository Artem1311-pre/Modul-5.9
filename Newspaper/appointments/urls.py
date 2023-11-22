from django.urls import path
from appointments.views import AppointmentView

urlpatterns = [
    path('appointment_create/', AppointmentView.as_view(), name='appointment_create'),

]