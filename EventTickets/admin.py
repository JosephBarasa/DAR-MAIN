from django.contrib import admin
from EventTickets.models import Tickets, TicketOrder, TicketOrderItem


admin.site.register(Tickets)
admin.site.register(TicketOrder)
admin.site.register(TicketOrderItem)
