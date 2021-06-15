from django.contrib import admin
from .models import Debate,Pros,Cons
# Register your models here.

class ProsInline(admin.TabularInline):
    model = Pros
    extra = 1

class ConsInline(admin.TabularInline):
    model = Cons
    extra = 1

class DebateAdmin(admin.ModelAdmin):
    list_display = ('id','title',)
    search_fields = ('id', 'title')
    readonly_fields = ()
    ordering = ('created',)
    filter_horizontal = ()
    list_filter = ()
    inlines = [ ProsInline,ConsInline ]

admin.site.register(Debate, DebateAdmin)

class ProsAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)
    readonly_fields = ()
    ordering = ()
    filter_horizontal = ()
    list_filter = ()
admin.site.register(Pros,ProsAdmin)
