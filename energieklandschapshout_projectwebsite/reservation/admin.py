from django.contrib import admin
from django.utils.translation import ugettext as _

from models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ("reservation_list","date","contact_name")
    list_filter = ("approved",)


admin.site.register(Reservation,ReservationAdmin)