from django.db import models


class Event(models.Model):
    short = models.SlugField(max_length=64,unique=True)
    name = models.CharField(max_length=128)
    
    paymentemail = models.EmailField(max_length=128,verbose_name='Payment Receiver')

    location = models.CharField(max_length=64)
    venue = models.CharField(max_length=128)
    date = models.DateField()

    shorttext = models.TextField('Short Description', help_text='Use textile markup', blank=True)
    shorttext_html = models.TextField('Short Description (HTML)', editable=False)
    longtext = models.TextField('Long Description', help_text='Use textile markup', blank=True)
    longtext_html = models.TextField('Long Description (HTML)', editable=False)

    logo = models.ImageField(upload_to='event_logos',blank=True)

    venuefee = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Venue Fee')

    def __unicode__(self):
        return self.name

    def save(self):
        import textile
        self.shorttext_html = textile.textile(self.shorttext.encode('utf-8'),
                                              encoding='utf-8',output='utf-8')
        self.longtext_html = textile.textile(self.longtext.encode('utf-8'),
                                             encoding='utf-8',output='utf-8')
        super(Event, self).save()


class Tournament(models.Model):
    event = models.ForeignKey(Event)

    name = models.CharField(max_length=64)
    short = models.SlugField(max_length=16)
    entrytype = models.CharField(max_length=1, choices=(('I','Individual'),('T','Team')),
                                 verbose_name='Tournament Type')
    logo = models.ImageField(upload_to='game_logos', blank=True)
    
    entryfee = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Entry Fee')

    def __unicode__(self):
        return self.name


class TournamentEntry(models.Model):
    tournament = models.ForeignKey('Tournament')
    entrant = models.ForeignKey('Entrant')
    skill = models.IntegerField(default=0)

    def __smart_unicode__(self):
        return '%s in %s' % (self.entrant, self.tournament)


class Entrant(models.Model):
    event = models.ForeignKey(Event)
    tournaments = models.ManyToManyField(Tournament, through='TournamentEntry', blank=True)

    firstname = models.CharField(max_length=32, verbose_name='First Name')
    lastname = models.CharField(max_length=32, verbose_name='Last Name')
    suffix = models.CharField(max_length=4, blank=True)
    tag = models.CharField(max_length=32, unique=True, verbose_name='Nickname/Gamertag')
    team = models.CharField(max_length=16, blank=True, verbose_name='Team/Sponsor')
    prefix = models.CharField(max_length=4, blank=True, verbose_name='Team/Sponsor Prefix')
    email = models.EmailField(max_length=128, unique=True, verbose_name='Contact Email')
    
    address = models.CharField(max_length=64)
    addresscity = models.CharField(max_length=32, verbose_name='City')
    addressstate = models.CharField(max_length=32, verbose_name='State/Province')
    addresscountry = models.CharField(max_length=64, verbose_name='Country')
    addresszip = models.CharField(max_length=8, verbose_name='Zip/Postal Code')

    paymentemail = models.EmailField(max_length=128, verbose_name='Payment Email')
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Payment Amount')
    entranttype = models.CharField(max_length=1, choices=(('P','Player'),('C','Casual'),('S','Spectator'))
                                   default='P', verbose_name='Type of Entrant')
    signupdate = models.DateTimeField(auto_now_add=True, verbose_name='Date Registered')
    signuptype = models.CharField(max_length=1, choices=(('E','Early'),('N','Normal'),('L','Late'),('M','Emergency')),
                                  default='N', verbose_name='Category of Registration')
    has_paid = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    #facts = models.TextField()
    #photo = models.ImageField()

    def __unicode__(self):
        return self.tag


    
