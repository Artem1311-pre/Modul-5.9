from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail
from datetime import datetime
from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointments = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointments.save()

        # отправляем письмо
        send_mail(
            subject=f'{appointments.client_name} {appointments.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=appointments.message,  # сообщение с кратким описанием проблемы
            from_email='comrad.heisenberg@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=[]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )

        return redirect('appointment:make_appointment')