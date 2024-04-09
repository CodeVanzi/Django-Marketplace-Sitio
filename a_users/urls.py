from django.urls import path

from a_users.views import profile_view, profile_edit

urlpatterns = [
    path('', profile_view, name='profile'),
    path('profile_edit', profile_edit, name='profile_edit')
]