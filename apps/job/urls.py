from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^login_success$', views.success),
	url(r'^logout$', views.destroy),
	url(r'^dashboard$', views.user_wall),
	url(r'^jobs/new$', views.add_job),
	url(r'^post_job', views.job_post),
	url(r'^jobs/(?P<my_val>\d+)$', views.display_job),
	url(r'^jobs/edit/(?P<my_val>\d+)$', views.edit_job),
	url(r'^job_edit$', views.post_editjob),
	url(r'^remove_job/(?P<my_val>\d+)$', views.delete_job),
]