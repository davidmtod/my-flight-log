from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('logbook/', views.LogbookTableView.as_view(), name='logbook'),
	path('logbook_insert/', views.logbook_insert, name='logbook_form'),
	path('logbook_detail/<int:log_id>/', views.logbook_detail, name='logbook_detail')
]