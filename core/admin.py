from django.contrib import admin
from .models import Player, Game, Attendance, Team, WeeklyStanding

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0

class GameAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]

admin.site.register(Player)
admin.site.register(Game, GameAdmin)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(WeeklyStanding)
class WeeklyStandingAdmin(admin.ModelAdmin):
    list_display = ('team', 'week', 'position', 'points')
    list_filter = ('week', 'team')
    ordering = ('week', 'position')