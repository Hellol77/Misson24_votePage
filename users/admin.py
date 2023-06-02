from django.contrib import admin
from .models import User, PostResult, PersonalVote
from django.contrib.auth.models import Group

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'university',
        'role',
        )
    search_fields = ('user_id',)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

class PostResultAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'team_name',
        'team_members',
        'intro_text',
        'image1',
        'imagesrc1',
        'image2',
        'imagesrc2',
        'image3',
        'imagesrc3',
        'image4',
        'imagesrc4',
        )
    search_fields = ('user_id','team_name')

admin.site.register(PostResult, PostResultAdmin)

class PersonalVoteAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'dict_json'
        )
    search_fields = ('user_id','team_name')\

admin.site.register(PersonalVote, PersonalVoteAdmin)