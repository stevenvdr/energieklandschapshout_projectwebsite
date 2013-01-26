from datetime import date, timedelta, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from forms import ReservationForm
from models import ReservationPlugin, Reservation

    
class CMSReservationPlugin(CMSPluginBase):
    model = ReservationPlugin
    name = _("Reservation")
    render_template = 'reservation/reservation_plugin.html'

    def render(self, context, instance, placeholder):
        request = context['request']
        context.update({
            'name':instance.name,
            })
            
        #Form was sent in
        if request.method == "POST":
            form = ReservationForm(request.POST)
            
            #Form is valid: save and send informative mails
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.reservation_list = instance
                reservation.save()

                #Send mail to responsible for the reservation
                send_mail(_('New reservation for %s') % instance.name,
                            _('A new reservation was made for %(name)s.\n') % {'name': instance.name,} + \
                            _('Contact information:\n') % {'contact_name': reservation.contact_name,} +\
                            _('- Name: %(contact_name)s\n') % {'contact_name': reservation.contact_name,} +\
                            _('- Email: %(contact_mail)s\n') % {'contact_mail': reservation.contact_mail,} +\
                            _('- Phone number: %(contact_phone)s\n') % {'contact_phone': reservation.contact_phone,},
                            'info@sval.be', #TODO: add mail to settings
                            [instance.inform_mail], fail_silently=True)

                #Send confirmation mail to the one who just reserved
                send_mail(_('New reservation for %s') % instance.name,
                            _('You have just made a reservation for %(name)s. Your reservation will now be reviewed.\n') % {'name': instance.name,} +\
                            _('If you have further questions, please contact us at %(mail)s.\n') % {'mail': "info@sval.be",},

                            'info@sval.be', #TODO: add mail to settings
                            [instance.inform_mail], fail_silently=True)

                messages.success(request, _('Your reservation was successful, and is now pending. You will have received an email confirming this.'))

                form = ReservationForm()
                
            #Form is invalid: display errors (so leave the form be)
            else:
                pass
                
        #No form data sent in
        else:
            #process administration controls
            self.administration(request)
            #Create new form
            form = ReservationForm()

        if all(key in request.GET for key in ("month","year")):
            month = date(int(request.GET['year']), int(request.GET['month']),1)
        else:
            month = date.today()

        if month.month % 12 is 0:
            next_month = date(month.year+1, 1, 1)
        else:
            next_month = date(month.year, month.month+1, 1)

        if month.month is 1:
            prev_month = date(month.year-1, 12, 1)
        else:
            prev_month = date(month.year, month.month-1, 1)

        if month.month == date.today().month and month.year == date.today().year:
            prev_month = None

        context.update({
            'calendar':self.get_calendar_context(month),
            'form':form,
            'month': month,
            'prev_month': prev_month,
            'next_month': next_month,
        })
        
        return context

    #Generate the days for the calendar
    def get_calendar_context(self, month):
        #Select first day of the month
        first_day = month
        first_day = first_day.replace(day = 1)
        
        #select first day of the next month
        if first_day.month == 12:
            last_day = date(year=first_day.year+1 , month=1, day=1)
        else:
            last_day = date(year=first_day.year, month=first_day.month+1, day=1)

        #make sure the first day of the calendar is monday (0 is monday, 6 is sunday)
        while first_day.weekday() is not 0:
            first_day = first_day - timedelta(1)
        
        #make sure last day of the calendar is sunday (so last_day is monday)
        while last_day.weekday() is not 0:
            last_day = last_day + timedelta(1)
            
        #get reservations for the calendar:
        reservations = Reservation.objects.filter(date__gte = first_day).filter(date__lt = last_day)

        #Render the context, so that every day exists
        if reservations.exists():
            list_index = 0
            reservation_list = list(reservations)
        else:
            list_index=-1
            reservation_list = []

        calendar = []
        for dates in daterange(first_day, last_day):
            #There is a reservation on that day
            if list_index != -1 and list_index<len(reservation_list) and dates == reservation_list[list_index].date:
                calendar.append({
                    'date':dates,
                    'reservation':reservation_list[list_index]
                    })
                list_index += 1
            
            #no reservation for that day
            else:
                calendar.append({
                    'date':dates,})

        return calendar
    

    def administration(self, request):
        #Approve the reservation on a given date
        if 'approve' in request.GET:
            try:
                reservation = Reservation.objects.get(date = datetime.strptime(request.GET['approve'], '%d-%m-%Y'))
                reservation.approved = True
                reservation.save()
            
                messages.success(request, _('The reservation has been approved.'))
            except (ValueError, Reservation.DoesNotExist):
                messages.error(request, _('Incorrect request.'))
        #Delete the reservation on a given date
        elif 'delete' in request.GET:
            try:
                reservation = Reservation.objects.get(date = datetime.strptime(request.GET['delete'], '%d-%m-%Y'))
                reservation.delete()

                messages.success(request, _('The reservation has been deleted.'))
            except (ValueError, Reservation.DoesNotExist):
                messages.error(request, _('Incorrect request.'))
        
        return None
        
    
#Iterate over daterange
def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + timedelta(n)    
        
        
plugin_pool.register_plugin(CMSReservationPlugin)
