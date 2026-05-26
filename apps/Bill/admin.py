from django.contrib import admin
from .models import BillService, BillTransaction


@admin.register(BillService)
class BillServiceAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	search_fields = ('name', 'slug')


@admin.register(BillTransaction)
class BillTransactionAdmin(admin.ModelAdmin):
	list_display = ('tx_id', 'service', 'user', 'amount', 'status', 'created_at')
	list_filter = ('status', 'service')
	readonly_fields = ('response', 'tx_id', 'created_at', 'updated_at')
