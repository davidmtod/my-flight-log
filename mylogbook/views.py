from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db.models.functions import TruncYear
from django.db.models import Sum
from django.db.models import Count

from .models import Logbook, LogbookForm
from .tables import LogbookTable

import django_tables2 
from django_tables2 import SingleTableView

import matplotlib.pyplot as plt
import io
import urllib, base64
import numpy as np
import datetime 
import decimal
decimal.getcontext().prec = 3

from django.db.models.functions import (Extract, ExtractDay, ExtractHour, 
        ExtractMinute, ExtractMonth, ExtractQuarter, ExtractSecond, ExtractWeek, 
        ExtractWeekDay, ExtractYear
    )

INCREASE = 100
add_hours = lambda hours, increase: hours + increase
convertItem = lambda i: i or 0 
secondsToHours = lambda i: i/3600
remove_from_string = lambda string: string[string.find(' ')+1:]

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d} ({p:.1f}%)'.format(p=pct,v=val)
    return my_autopct

def plot1():
	# PLOT 1: Chart
	N = 15
	dual   = [secondsToHours(i) for i in (convertItem(i) for i in Logbook.objects.annotate(year=ExtractYear('date_of_flight')).values('year').annotate(hours=Sum('dual_se_day')).order_by('year').values_list('hours', flat = True))]

	p1 = [secondsToHours(i) for i in (convertItem(i) for i in Logbook.objects.annotate(year=ExtractYear('date_of_flight')).values('year').annotate(hours=Sum('p1_se_day')).order_by('year').values_list('hours', flat = True))]

	ind = np.arange(N) # the x locations for the groups
	width = 0.5

	fig, ax = plt.subplots()
	ax.bar(ind, dual, color='r', width=1, edgecolor="white", linewidth=0.7)
	ax.bar(ind, p1, bottom=dual, color='b', width=1, edgecolor="white", linewidth=0.7)
	ax.set_ylabel('Hours',fontsize=6)
	ax.set_xlabel('Year',fontsize=6)
	ax.set_title('P1 vs Dual Hours Per Year',fontsize=8)

	ax.set_xticks(ind, Logbook.objects.annotate(year=ExtractYear('date_of_flight')).values('year').distinct().order_by('year').values_list('year', flat = True))
	ax.tick_params(axis='x', which='major', labelsize=6)
	labels=['Dual', 'P1']
	ax.legend(labels, loc="best", prop={"size":6})
	plt.xticks(rotation=90)
	plt.tight_layout()

	fig = plt.gcf()
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	uri = urllib.parse.quote(string)
	
	return urllib.parse.quote(string)

def hours_by_type():
	# PLOT 2

	x = list(remove_from_string(i) for i in Logbook.objects.values('aircraft_type').order_by('aircraft_type').distinct().values_list('aircraft_type', flat = True))
	y = [secondsToHours(i) for i in Logbook.objects.values('aircraft_type').order_by('aircraft_type').annotate(total_hours=Sum('total_time')).values_list('total_hours', flat = True)]
	xcount = Logbook.objects.values('aircraft_type').distinct().count()

	
	# plot
	fig, ax = plt.subplots()
	ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)
	ax.set_xlabel('Type', fontsize=6)
	ax.set_ylabel('Hours', fontsize=6)
	ax.tick_params(axis='both', which='major', labelsize=6)
	ax.set(xlim=(0,xcount), xticks=np.arange(0, xcount),
      	 ylim=(0, 200), yticks=np.arange(0, 200, step=40))
	plt.xticks(rotation=90)
	plt.title('Total Hours Per Type',fontsize=8)
	plt.tight_layout()
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())

	return urllib.parse.quote(string)

def plot3():
	# PLOT 3
	np.random.seed(3)
	x = list(Logbook.objects.values('registration').order_by('registration').distinct().values_list('registration', flat=True)) 
	y = [secondsToHours(i) for i in Logbook.objects.values('registration').order_by('registration').annotate(total_hours=Sum('total_time')).values_list('total_hours', flat = True)]
	xcount = Logbook.objects.values('registration').distinct().count()

	
	# plot
	fig, ax = plt.subplots()
	ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)
	ax.set_xlabel('Aircraft', fontsize=6)
	ax.set_ylabel('Hours', fontsize=6)
	ax.tick_params(axis='both', which='major', labelsize=6)
	ax.set(xlim=(0,xcount), xticks=np.arange(0, xcount),
      	 ylim=(0, 200), yticks=np.arange(0, 200, step=25))
	plt.xticks(rotation=90)
	plt.title('Total Hours Per Aircraft',fontsize=8)
	plt.tight_layout()
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())

	return urllib.parse.quote(string)

def p1vsdual(p1flight, dualflight):
	# PLOT 4:  Pie Chart
	# make data
	x = [p1flight, dualflight]
	colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))
	labels = ['P1','Dual']
	values=[p1flight,dualflight]
	exploda = (0, 0.1)
	# plot

	fig4, ax = plt.subplots()
	ax.pie(x, colors=colors, center=(0,0), autopct=make_autopct(values),explode=exploda,
       	 shadow = False, frame=False, textprops={'fontsize': 6})

	plt.title('P1 vs Dual Hours Total',fontsize=8)
	
	ax.legend(labels, loc="best", prop={"size":6})
	plt.grid(False)
	plt.tight_layout()

	buf = io.BytesIO()
	fig4.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	return urllib.parse.quote(string)

def landingstype(tarmac, grass, water):
	# PLOT 5:  Pie Chart
	# make data
	x = [tarmac, grass, water]
	colors = ['#DCDCDC','#99ff99', '#66b3ff']
	labels = ['Tarmac','Grass', 'Water']
	values=[tarmac, grass, water]
	exploda = (0, 0.1, 0.1)
	# plot

	fig4, ax = plt.subplots()
	ax.pie(x, colors=colors, center=(4, 8),autopct=make_autopct(values),explode=exploda,
       	 shadow = False, frame=False, textprops={'fontsize': 8})


	plt.title('Landings By Surface Type',fontsize=8)
	ax.legend(labels, loc="best", prop={"size":6})
	plt.grid(False)
	plt.tight_layout()

	buf = io.BytesIO()
	fig4.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	return urllib.parse.quote(string)

def airifelds_visited():
	# PLOT 6
	np.random.seed(3)
	x = list(Logbook.objects.values('airfield_to').order_by('airfield_to').exclude(airfield_to="EGPK").values_list('airfield_to', flat = True).distinct())
	y = list(Logbook.objects.values('airfield_to').order_by('airfield_to').exclude(airfield_to="EGPK").annotate(times_visited=Count('airfield_to')).values_list('times_visited', flat = True))
	xcount = Logbook.objects.values('airfield_to').exclude(airfield_to="EGPK").distinct().count()

	
	# plot
	fig, ax = plt.subplots()
	ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)
	ax.set_xlabel('Airfield', fontsize=6)
	ax.set_ylabel('Times visited', fontsize=6)
	ax.tick_params(axis='both', which='major', labelsize=6)
	ax.set(xlim=(0,xcount), xticks=np.arange(0, xcount),
      	 ylim=(0, 5), yticks=np.arange(0, 5, step=1))
	plt.xticks(rotation=90)
	plt.title('Airfields Visited',fontsize=8)
	plt.tight_layout()
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())

	return urllib.parse.quote(string)


def index(request):
	plt.style.use('_mpl-gallery')

	# PLOT 1: Chart
	uri = plot1()

	# PLOT 2: Chart
	uri2 = hours_by_type()

	# PLOT 3: Chart
	uri3 = plot3()

	# PLOT4: P1 hours vs Dual hours
	p1flight = add_hours(Logbook.objects.filter(captain='SELF').count(), INCREASE)
	dualflight = add_hours(Logbook.objects.exclude(captain='SELF').count(), INCREASE)
	uri4 = p1vsdual(p1flight, dualflight)


	# PLOT5: Landing Type
	tarmaclanding = 243 #p1flight = add_hours(Logbook.objects.filter(captain='SELF').count(), INCREASE)
	grasslanding = 30 #dualflight = add_hours(Logbook.objects.exclude(captain='SELF').count(), INCREASE)
	waterlanding = 43 #uri4 = p1vsdual(p1flight, dualflight)
	uri5 = landingstype(tarmaclanding, grasslanding, waterlanding)

	# PLOT 6: Chart
	uri6= airifelds_visited()

	# Context Dictionary
	context={	'data':uri, 
			'data2':uri2,
			'data3':uri3, 
			'data4':uri4,
			'data5':uri5,
			'data6':uri6
			}

	return render(request,'mylogbook/index.html',context)


class LogbookTableView(SingleTableView):
	model = Logbook
	template_name = 'mylogbook/index.html'
	table_class = LogbookTable

def logbook_insert(request):
	form = LogbookForm()
	context = {'form': form}
	return render(request, 'mylogbook/logbook_insert.html', context)

def logbook_detail(request, log_id):
	detail_flight = Logbook.objects.filter(pk=log_id)
	context = {'detail_flight': detail_flight}
	return render(request, 'mylogbook/logbook_detail.html', context)