from django.urls import reverse
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

BELT_LEVELS = {"White": 0, "Blue": 1, "Purple": 2, "Brown": 3, "Black": 4}

# Club:
# 	Leader (Foreign key for a User)
# 	Club Name (Text)
# 	Record (List of ints)
class Club(models.Model):
    LEADER = models.ForeignKey(User, on_delete=models.CASCADE)
    NAME = models.CharField(max_length=100)
    # TODO: Record

    def __str__(self):
        return self.NAME
    
    def get_absolute_url(self):
        return reverse('view_club', args=[str(self.id)])
    
    def get_competitors(self):
        return self.competitor_set.all()

# Competitor:
# 	Full name (text)
# 	Weight (int)
# 	Belt level (Enum)
# 	Gender (Binary, not political or nothing we’re just a combat sport)
# 	Team (Foreign key for a Club)
class Competitor(models.Model):
    FULL_NAME = models.CharField(max_length=100)
    WEIGHT = models.FloatField()
    BELT_LEVEL = models.IntegerField() # 0 = white, 1 = blue, 2 = purple, 3 = brown, 4 = black
    GENDER = models.BooleanField()
    TEAM = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return self.FULL_NAME


# Competition:
# 	Host (Foreign Key of a Club)
# 	Teams (List of foreign keys to Clubs)
# 	Location (Text)
# 	Date (Datetime)
# 	Mat Count (Int)
# 	Matches per Competitor (Int)
class Competition(models.Model):
    HOST = models.ForeignKey(Club, on_delete=models.CASCADE)
    LOCATION = models.CharField(max_length=300)
    DATE = models.DateTimeField()
    MAT_COUNT = models.IntegerField()
    MATCHES_PER_COMPETITOR = models.IntegerField()

    def __str__(self):
        return f'{self.DATE.month}/{self.DATE.day} @ {self.HOST} '
    
    def get_absolute_url(self):
        return reverse('view_competition', args=[str(self.id)])
    
    def get_teams(self):
        return [entry.ENTRANT for entry in self.tournamententry_set.all()]
    
    def get_matches(self):
        return self.match_set.all()
    
    def get_competitors(self):
        competitors = []
        for team in self.get_teams():
            competitors.extend(team.competitor_set.all())
        return competitors

    def create_bracket(self):
        # Clear existing matches
        self.match_set.all().delete()

        # Make new matches
        competitors = self.get_competitors()
        for competitor in competitors:
            print(f'Creating matches for {competitor}')
            # Find competitors of the same belt and gender, from a different team
            other_competitors = Competitor.objects.filter(BELT_LEVEL=competitor.BELT_LEVEL, GENDER=competitor.GENDER).exclude(Q(TEAM=competitor.TEAM) | Q(id=competitor.id))

            # Filter by weight
            other_competitors = other_competitors.filter(WEIGHT__range=(competitor.WEIGHT-10, competitor.WEIGHT+10))
            # Create matches
            for match_count in range(self.MATCHES_PER_COMPETITOR):
                print(f'Match {match_count}', end=' ')
                if not other_competitors.exists():
                    break
                other_competitor = other_competitors.first()
                other_competitors = other_competitors.exclude(id=other_competitor.id)
                # Check if match already exists
                if Match.objects.filter(COMPETITION=self, COMPETITOR1=competitor, COMPETITOR2=other_competitor).exists() or \
                     Match.objects.filter(COMPETITION=self, COMPETITOR1=other_competitor, COMPETITOR2=competitor).exists():
                    match_count -= 1
                    continue

                print(f'{competitor} vs. {other_competitor}')
                # Model creation
                match = Match(COMPETITION=self,
                              COMPETITOR1=competitor,
                              COMPETITOR2=other_competitor,
                              MAT_NUMBER=match_count,
                              WINNER=None,
                              SCORE=None)
                match.save()

        # Return all bracket matches related to this competition
        return self.get_matches()

    def get_completed_ratio(self):
        total_matches = self.get_matches().count()
        completed_matches = self.get_matches().filter(WINNER__isnull=False).count()

        return str(completed_matches) + '/' + str(total_matches) + ' matches completed'

    def get_scores(self):
        scores = {}
        for team in self.get_teams():
            print(team)
            scores[team] = 0

        for match in self.get_matches():
            if match.WINNER is not None and match.SCORE is not None:
                if match.WINNER.TEAM in scores:
                    scores[match.WINNER.TEAM] += match.SCORE
                else:
                    print(match.WINNER)
                    scores[match.WINNER.TEAM] = match.SCORE
        print(scores)
        return scores

# TournamentEntry:
# 	Tournament (Foreign key of a Tournament)
# 	Entrant (Foreign key of a Club)
class TournamentEntry(models.Model):
    COMPETITION = models.ForeignKey(Competition, on_delete=models.CASCADE)
    ENTRANT = models.ForeignKey(Club, on_delete=models.CASCADE)

# Match:
# 	Competitor1 (Foreign key of Competitor)
# 	Competitor2 (Foreign key of Competitor)
# 	Mat Number (Int)
# 	Result (Enum)
# 	Score (Int)
class Match(models.Model):
    COMPETITION = models.ForeignKey(Competition, on_delete=models.CASCADE)
    COMPETITOR1 = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='competitor1')
    COMPETITOR2 = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='competitor2')
    WINNER = models.ForeignKey(Competitor, on_delete=models.CASCADE, null=True, related_name='winner')
    MAT_NUMBER = models.IntegerField()
    SCORE = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.COMPETITOR1} vs. {self.COMPETITOR2}'

# User:
# 	Builtin Django params

def load_data():
    Competitor.objects.all().delete()
    Competition.objects.all().delete()
    TournamentEntry.objects.all().delete()
    Match.objects.all().delete()

    # Add competitors from sample data
    bu = Club.objects.get(NAME='BUBJJ')
    harvard = Club.objects.get(NAME='Harvard JiuJitsu')
    mit = Club.objects.get(NAME='MIT Self Defense')
    neu = Club.objects.get(NAME='NEU BJJ')
    
    print(bu)
    print(harvard)
    print(mit)
    print(neu)


    filename = 'C:\\Users\\aidan\\Desktop\\AllCompetitors.csv'
    f = open(filename)
    f.readline()
    for line in f:
        fields = line.split(',')

        try:
            school = fields[1].strip()
            match school:
                case "BU":
                    team = bu
                case "Harvard":
                    team = harvard
                case "MIT":
                    team = mit
                case "Northeastern":
                    team = neu
                case _:
                    continue

            competitor = Competitor(FULL_NAME=fields[0],
                                    WEIGHT=fields[3],
                                    GENDER=fields[4].strip().lower() == 'male',
                                    BELT_LEVEL=BELT_LEVELS[fields[5].strip().lower().capitalize()],
                                    TEAM=team)
            competitor.save()
            print(f'Created competitor: {competitor}')
        except Exception as e:
            print(e)
            continue