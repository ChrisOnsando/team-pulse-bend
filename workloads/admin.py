from django.contrib import admin
from workloads.models import Workload


@admin.register(Workload)
class WorkloadAdmin(admin.ModelAdmin):
    list_display = ["value", "description", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["description"]
    ordering = ["value"]
    
