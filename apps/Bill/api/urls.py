from django.urls import path
from .views import ServiceListView, PayBillView
from .views import (
	APIv2RootView, BalanceView, VerifyCustomerView, AirtimeView,
	VariationsDataView, DataView, VariationsTVView, TVView,
	ElectricityView, BettingView, EpinsView, RequeryView,
)

app_name = 'bill_api'

urlpatterns = [
	path('services/', ServiceListView.as_view(), name='services'),
	path('pay/', PayBillView.as_view(), name='pay'),

	# External provider proxy endpoints (guided by JSON spec)
	path('v2/', APIv2RootView.as_view(), name='api-v2-root'),
	path('v2/balance', BalanceView.as_view(), name='api-v2-balance'),
	path('v2/verify-customer', VerifyCustomerView.as_view(), name='api-v2-verify-customer'),
	path('v2/airtime', AirtimeView.as_view(), name='api-v2-airtime'),
	path('v2/variations/data', VariationsDataView.as_view(), name='api-v2-variations-data'),
	path('v2/data', DataView.as_view(), name='api-v2-data'),
	path('v2/variations/tv', VariationsTVView.as_view(), name='api-v2-variations-tv'),
	path('v2/tv', TVView.as_view(), name='api-v2-tv'),
	path('v2/electricity', ElectricityView.as_view(), name='api-v2-electricity'),
	path('v2/betting', BettingView.as_view(), name='api-v2-betting'),
	path('v2/epins', EpinsView.as_view(), name='api-v2-epins'),
	path('v2/requery', RequeryView.as_view(), name='api-v2-requery'),
]
