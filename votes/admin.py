from django.contrib import admin

from .models import UserVote, Vote

admin.site.register(Vote)
admin.site.register(UserVote)
