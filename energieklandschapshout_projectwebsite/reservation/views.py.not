from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from forms import ReservationForm
from models import Reservation,ReservationPlugin

def new_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        settings = get_object_or_404(ReservationPlugin,name=request.POST['list_name'])

        if form.is_valid():
            reservation = form.save()
            
            send_mail(_('New reservation for %s') % settings.nameSubject,
                        _('''A new reservation was made for %(name)s.
                        Contact information:
                        - Name: %(contact_name)
                        - Email: %(contact_mail)
                        - Phone number: %(contact_phone)
                        ''') % {'name': settings.name,
                                'contact_name': reservation.contact_name,
                                'contact_mail': reservation.contact_mail,
                                'contact_phone': reservation.contact_phone},
                        'info@sval.be', #TODO: add mail to settings
                        [settings.inform_mail], fail_silently=True) 
                        
            send_mail(_('New reservation for %s') % settings.nameSubject,
                        _('''You have just made a  for %(name)s. Your reservation will now be reviewed.
                        If you have further questions, please contact us at %(mail)s.
                        ''') % {'name': settings.name,
                                'mail': 'info@sval.be',},
                        'info@sval.be', #TODO: add mail to settings
                        [settings.inform_mail], fail_silently=True)
            
            return HttpResponse('SUCCESS\n' + _('Your reservation was succesful, and is now pending. You will have received an email confirming this.'))
            
        else:
            return HttpResponse('FAIL\n' + _('Some of the provided information was incorrect'))
    
    return HttpResponse('FAIL\n' + _('Incorrect request'))


@login_required
@permission_required('reservation.change_reservation')
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(pk=reservation_id)
    reservation.approved = True
    reservation.save()
    
    return HttpResponse('SUCCESS\n' + _('The reservation has been approved.'))

    
@login_required
@permission_required('reservation.change_reservation')
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(pk=reservation_id)
    reservation.delete()
    
    return HttpResponse('SUCCESS\n' + _('The reservation has been deleted.'))

