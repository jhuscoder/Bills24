import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings


class BillService(models.Model):
	name = models.CharField(max_length=120)
	icon = models.CharField(max_length=255, blank=True, null=True)
	slug = models.SlugField(max_length=120, unique=True)

	class Meta:
		verbose_name = 'bill service'
		verbose_name_plural = 'bill services'

	def __str__(self):
		return self.name


class BillTransaction(models.Model):
	STATUS_PENDING = 'pending'
	STATUS_SUCCESS = 'success'
	STATUS_FAILED = 'failed'

	STATUS_CHOICES = (
		(STATUS_PENDING, 'Pending'),
		(STATUS_SUCCESS, 'Success'),
		(STATUS_FAILED, 'Failed'),
	)

	tx_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
	service = models.ForeignKey(BillService, on_delete=models.PROTECT)
	amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
	external_reference = models.CharField(max_length=255, blank=True, null=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	response = models.JSONField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'bill transaction'
		verbose_name_plural = 'bill transactions'

	def __str__(self):
		return f"{self.service} - {self.tx_id}"

