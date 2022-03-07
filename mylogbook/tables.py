from .models import Logbook

import django_tables2 

class LogbookTable(django_tables2.Table):
	class Meta:
		model = Logbook
		template_name = "django_tables2/semantic.html"
		exclude = ("log_id", "remarks", "p1_me_night", "dual_me_night", "p1_me_day", "dual_me_day", "simulated_instrument_flying")