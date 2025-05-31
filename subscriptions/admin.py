from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "start_date",
        "end_date",
        "active",
    )
    list_filter = ("active",)
    search_fields = ("user__username", "user__email")

