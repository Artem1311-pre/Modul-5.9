from django.contrib import admin
from django.urls import path, include
from Newspaper.appointments.views import AppointmentView


urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('news/', include('news.urls')),
   path('', include('protect.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
   path('appointment_create/', AppointmentView.as_view(), name='appointment_create'),
   path('appointments/', include(('appointment.urls', 'appointments'), namespace='appointments')),

]