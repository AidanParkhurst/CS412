from django.db import models

# Create your models here.
class Voter(models.Model):

    # Identification
    voter_id = models.CharField(max_length=12)
    last_name = models.TextField()
    first_name = models.TextField()

    # address
    street_number = models.TextField()
    street_name = models.TextField()
    apt_number = models.TextField()
    zip_code = models.TextField()

    # dates
    birthdate = models.DateField()
    reg_date = models.DateField()

    # voter behavior
    party = models.TextField()
    precinct = models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}' 
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()
    
    filename = 'C:\\Users\\aidan\\Desktop\\newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
    voter_count = 0
    for line in f:
        fields = line.split(',')
        
        try:
            # create a new instance of Result object with this record from CSV
            voter = Voter(voter_id=fields[0],
                            last_name=fields[1],
                            first_name=fields[2],
                            street_number = fields[3],
                            street_name = fields[4],
                            apt_number = fields[5],
                            zip_code = fields[6],
                            birthdate = fields[7],
                            reg_date = fields[8],
                            party = fields[9].strip(),
                            precinct = fields[10],
                            v20state = fields[11].title(),
                            v21town = fields[12].title(),
                            v21primary = fields[13].title(),
                            v22general = fields[14].title(),
                            v23town = fields[15].title(),
                            voter_score = int(fields[16].strip()))
            voter.save()
            voter_count += 1
        except Exception as e:
            print(f'Error with record: {fields}')
            print(e)
            continue
    print(f'Loaded {voter_count} voter records.')
    f.close()