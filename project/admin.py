from django.contrib import admin

# Register your models here
from .models import Club, Competitor, Match, Competition, TournamentEntry

admin.site.register(Club)
admin.site.register(Competitor)
admin.site.register(Match)
admin.site.register(Competition)
admin.site.register(TournamentEntry)


