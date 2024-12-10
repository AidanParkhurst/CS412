from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login

from .models import Club, Competition, TournamentEntry, Competitor, Match
from .forms import ClubCreationForm, CompCreationForm

class Home(ListView):
    '''Home page, displays upcoming competitions'''

    model = Competition
    template_name = 'project/home.html'
    context_object_name = 'competitions'

class AllClubs(ListView):
    '''List all clubs'''

    model = Club
    template_name = 'project/all_clubs.html'
    context_object_name = 'clubs'

class ClubDetail(DetailView):
    '''Club detail page'''

    model = Club
    template_name = 'project/club.html'
    context_object_name = 'club'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['competitors'] = self.object.competitor_set.all()

        if self.request.user.is_authenticated and self.object.LEADER == self.request.user:
            context['is_leader'] = True

        return context
    
class EditClub(LoginRequiredMixin, UpdateView):
    '''Edit a club'''

    model = Club
    template_name = 'project/edit_club.html'
    form_class = ClubCreationForm

    def get(self, request, pk):
        club = Club.objects.get(pk=pk)
        if not (self.request.user.is_authenticated and club.LEADER == self.request.user):
            return redirect('view_club', pk)

        return super().get(self)

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('view_club', args=[self.object.pk])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CompetitionDetail(DetailView):
    '''Competition detail page'''

    model = Competition
    template_name = 'project/competition.html'
    context_object_name = 'competition'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            club = Club.objects.filter(LEADER=self.request.user)

            if self.object.HOST.LEADER == self.request.user:
                context['is_host'] = True
            
            if club.exists() and TournamentEntry.objects.filter(ENTRANT=club[0], COMPETITION=self.object).exists():
                context['is_entrant'] = True
        
        return context

class GenerateBracket(LoginRequiredMixin, View):
    '''Generate the bracket for a competition'''

    def get_login_url(self):
        return reverse('login')

    def get(self, request, pk):
        comp = Competition.objects.get(pk=pk)
        if request.user.is_authenticated and request.user == comp.HOST.LEADER:
            comp.create_bracket()

        return redirect('view_bracket', pk)

    def post(self, request, pk):
        comp = Competition.objects.get(pk=pk)
        if request.user.is_authenticated and request.user == comp.HOST.LEADER:
            comp.create_bracket()

        return redirect('view_bracket', pk)

class BracketView(DetailView):
    '''View the bracket for a competition'''

    model = Competition
    template_name = 'project/bracket.html'
    context_object_name = 'competition'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.object.HOST.LEADER == self.request.user:
            context['is_host'] = True
        if self.object.get_matches().count() == 0:
            self.object.create_bracket()
        context['matches'] = self.object.get_matches()
        context['mat_range'] = range(self.object.MATCHES_PER_COMPETITOR)
        return context
    
class CreateCompetition(LoginRequiredMixin, CreateView):
    '''Create a new competition'''

    template_name = 'project/create_competition.html'
    form_class = CompCreationForm

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        TournamentEntry.objects.create(ENTRANT=self.object.HOST, COMPETITION=self.object)
        return super().get_success_url()

    def form_valid(self, form):
        club = Club.objects.get(LEADER=self.request.user)
        form.instance.HOST = club 
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = CompCreationForm()
    
        return context

class JoinCompetition(LoginRequiredMixin, View):
    '''Join a competition'''

    def get_login_url(self):
        return reverse('login')

    def get(self, request, pk):
        comp = Competition.objects.get(pk=pk)
        club = Club.objects.get(LEADER=request.user)
        if not TournamentEntry.objects.filter(ENTRANT=club, COMPETITION=comp).exists():
            TournamentEntry.objects.create(ENTRANT=club, COMPETITION=comp)
        return redirect('view_competition', pk) 
    
    def post(self, request, pk):
        return self.get(request, pk)

class LeaveCompetition(LoginRequiredMixin, View):
    '''Leave a competition'''

    def get_login_url(self):
        return reverse('login')

    def get(self, request, pk):
        comp = Competition.objects.get(pk=pk)
        club = Club.objects.get(LEADER=request.user)
        TournamentEntry.objects.filter(ENTRANT=club, COMPETITION=comp).delete()
        return redirect('view_competition', pk) 
    
    def post(self, request, pk):
        return self.get(request, pk)
    
class SignUp(CreateView):
    '''Sign up page'''

    template_name = 'project/signup.html'
    form_class = ClubCreationForm

    def get_success_url(self):
        return reverse('view_club', args=[self.object.pk])
    
    def form_valid(self, form):
        print(self.request.POST)
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        form.instance.LEADER = user
        username = self.request.POST['username']
        password = self.request.POST['password1']
        authenticated = authenticate(username=username, password=password)
        login(self.request, authenticated)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

class AddCompetitor(LoginRequiredMixin, View):
    '''Add a competitor'''

    def get_login_url(self):
        return reverse('login')

    def post(self, request, pk):
        club = Club.objects.get(pk=pk)
        Competitor.objects.create(TEAM=club,
                                  FULL_NAME=request.POST['FULL_NAME'],
                                  WEIGHT=request.POST['WEIGHT'],
                                  GENDER=request.POST['GENDER'],
                                  BELT_LEVEL=request.POST['BELT_LEVEL'])

        return redirect('edit_club', pk)

class UpdateCompetitor(LoginRequiredMixin, View):
    '''Update a competitor'''

    def get_login_url(self):
        return reverse('login')

    def post(self, request, pk):
        competitor = Competitor.objects.get(pk=pk)
        competitor.FULL_NAME = request.POST['FULL_NAME']
        competitor.WEIGHT = request.POST['WEIGHT']
        competitor.GENDER = request.POST['GENDER']
        competitor.BELT_LEVEL = request.POST['BELT_LEVEL']
        competitor.save()
        return redirect('edit_club', competitor.TEAM.pk)

class DeleteCompetitor(LoginRequiredMixin, View):
    '''Delete a competitor'''

    def get_login_url(self):
        return reverse('login')

    def post(self, request, pk):
        Competitor.objects.get(pk=pk).delete()
        return redirect('edit_club', request.POST['club_id'])
    
class SetWinner(LoginRequiredMixin, View):
    '''Set the winner of a match'''

    def get_login_url(self):
        return reverse('login')

    def post(self, request, pk):
        match = Match.objects.get(pk=pk)
        if match.WINNER is None or match.WINNER.pk != int(request.POST['winner']):
            match.SCORE = 1
            match.WINNER = Competitor.objects.get(pk=request.POST['winner'])
        else: # Allow for swapping between win by points and win by submission
            if match.SCORE == 1:
                match.SCORE = 2
            else:
                match.SCORE = 0
                match.WINNER = None
        match.save()
        return redirect('view_bracket', match.COMPETITION.pk)