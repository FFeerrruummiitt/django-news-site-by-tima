from django.contrib import admin
from .models import Category, News, Comments

admin.site.register(Category)

class AdminNews(admin.ModelAdmin):
    list_display = ('title', 'category', 'add_time')

admin.site.register(News, AdminNews)

class AdminComments(admin.ModelAdmin):
    list_display = ('news', 'email', 'comment', 'status')

admin.site.register(Comments,AdminComments)