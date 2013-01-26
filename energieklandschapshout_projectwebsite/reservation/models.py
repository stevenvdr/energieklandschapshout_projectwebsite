from django.db import models
from cms.models import CMSPlugin
from django.utils.translation import ugettext_lazy as _

class ReservationPlugin(CMSPlugin):
    name = models.CharField(max_length=100)
    inform_mail = models.EmailField(max_length=100, help_text=_('Who needs to be contacted if there are new reservations'))

    def delete(self):
        Reservation.objects.filter(reservation_list=self).delete()
        super(ReservationPlugin, self).delete(*args, **kwargs)

    def __unicode__(self):
        return "Reservation for " + self.name

    def __str__(self):
        return unicode(self).encode('utf-8')

class Reservation(models.Model):
    date = models.DateField(verbose_name="Datum")
    reservation_list = models.ForeignKey(ReservationPlugin)
    approved = models.BooleanField(default=False)
    
    contact_name = models.CharField(verbose_name="Naam", max_length=100)
    contact_mail = models.EmailField(verbose_name="E-mailadres", max_length=100)
    contact_phone = models.CharField(verbose_name="Telefoonnummer", max_length=30)

    class Meta:
        ordering = ['date']
        #unique_together = (("date", "reservation_list"),)
