from django.contrib import admin
from .models import Article, Source


class SourceAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "spider_class", "type"]


admin.site.register(Article)
admin.site.register(Source, SourceAdmin)
