# voter_analytics/views.py

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
import plotly
import plotly.graph_objs as go

from . models import Voter

class VoterListView(ListView):
    '''View to display voters'''
    template_name = 'voter_analytics/voters.html'
    model = Voter 
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        # start with entire queryset
        qs = super().get_queryset()

        # filter results:
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            min_birth_year = self.request.GET['min_birth_year']
            max_birth_year = self.request.GET['max_birth_year']
            voter_score = self.request.GET['voter_score']
            if party != '': qs = qs.filter(party__iexact=party)
            if min_birth_year != '': qs = qs.filter(birthdate__year__gt=min_birth_year)
            if max_birth_year != '': qs = qs.filter(birthdate__year__lt=max_birth_year)
            if voter_score != '': qs = qs.filter(voter_score=voter_score)
        if 'v20state' in self.request.GET: qs = qs.filter(v20state=True)
        if 'v21town' in self.request.GET: qs = qs.filter(v21town=True)
        if 'v21primary' in self.request.GET: qs = qs.filter(v21primary=True)
        if 'v22general' in self.request.GET: qs = qs.filter(v22general=True)
        if 'v23town' in self.request.GET: qs = qs.filter(v23town=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get possible values for filters
        parties = Voter.objects.values('party').distinct()
        possible_parties = [party['party'] for party in parties]
        birth_dates = Voter.objects.values('birthdate')
        birth_years = [date['birthdate'].year for date in birth_dates]
        possible_birth_years = list(set(birth_years))
        context['possible_parties'] = possible_parties
        context['possible_birth_years'] = possible_birth_years

        return context
    
class VoterDetailView(DetailView):
    '''View to display details of a single voter'''
    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voter'

class VoterStatsView(ListView):
    '''View to display voter statistics'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter

    def get_queryset(self):
        # start with entire queryset
        qs = super().get_queryset()

        # filter results:
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            min_birth_year = self.request.GET['min_birth_year']
            max_birth_year = self.request.GET['max_birth_year']
            voter_score = self.request.GET['voter_score']
            if party != '': qs = qs.filter(party__iexact=party)
            if min_birth_year != '': qs = qs.filter(birthdate__year__gt=min_birth_year)
            if max_birth_year != '': qs = qs.filter(birthdate__year__lt=max_birth_year)
            if voter_score != '': qs = qs.filter(voter_score=voter_score)
        if 'v20state' in self.request.GET: qs = qs.filter(v20state=True)
        if 'v21town' in self.request.GET: qs = qs.filter(v21town=True)
        if 'v21primary' in self.request.GET: qs = qs.filter(v21primary=True)
        if 'v22general' in self.request.GET: qs = qs.filter(v22general=True)
        if 'v23town' in self.request.GET: qs = qs.filter(v23town=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get possible values for filters
        parties = Voter.objects.values('party').distinct()
        possible_parties = [party['party'] for party in parties]
        birth_dates = Voter.objects.values('birthdate')
        birth_years = [date['birthdate'].year for date in birth_dates]
        possible_birth_years = list(set(birth_years))
        context['possible_parties'] = possible_parties
        context['possible_birth_years'] = possible_birth_years

        voters = self.get_queryset()
        # First, bar chart of voters by birth year
        birth_dates = voters.values('birthdate')
        birth_years = [date['birthdate'].year for date in birth_dates]
        year_counts = {year: birth_years.count(year) for year in set(birth_years)}
        figure = go.Bar(x=list(year_counts.keys()), y=list(year_counts.values()))
        title = 'Voters by Birth Year'
        birth_year_div = plotly.offline.plot({"data": [figure],
                                             "layout_title_text": title},
                                             auto_open=False,
                                             output_type='div')
        context['birth_year_div'] = birth_year_div
        
        # Second, pie chart of voters by party
        parties = list(voters.values('party'))
        party_counts = {party['party']: 0 for party in parties}
        for party in parties:
            party_counts[party['party']] += 1
        figure = go.Pie(labels=list(party_counts.keys()), values=list(party_counts.values()))
        party_div = plotly.offline.plot({"data": [figure],
                                        "layout_title_text": title},
                                        auto_open=False,
                                        output_type='div')
        context['party_div'] = party_div

        # Last, bar chart for distribution participation in the last 5 elections
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = {election: voters.filter(**{election: True}).count() for election in elections}
        figure = go.Bar(x=list(election_counts.keys()), y=list(election_counts.values()))
        title = 'Voters by Election Participation'
        election_div = plotly.offline.plot({"data": [figure],
                                            "layout_title_text": title},
                                            auto_open=False,
                                            output_type='div')
        context['election_div'] = election_div

        return context