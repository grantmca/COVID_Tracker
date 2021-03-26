from django.db import models



class Person(models.Model):

    name = models.CharField('Team Member Name', max_length=200)

    phone_number = models.CharField('Phone number', max_length=10, blank=True, default='')

    COMPANY_LIST = (
        ('Internal', 'Internal'),
        ('External', 'External'),
        ('Contractor', 'Contractor'),
        ('Other', 'Other'),
    )
    company = models.CharField('Company (Main etc.)',
                               choices=COMPANY_LIST,
                               max_length=24,
                               blank=True)

    badge_number = models.IntegerField('Employee ID Badge Number', unique=True, blank=True, null=True)

    shop = models.CharField('Plant (Admin, etc.)', max_length=24, blank=True, default='')

    line = models.CharField('Work Area or line (HR, etc.)', max_length=24, blank=True, default='')
    SHIFT_LIST = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    )
    shift = models.CharField('Shift (A, B, C)',
                               choices=SHIFT_LIST,
                               max_length=1,
                               blank=True)


    def notempty(self):
        if self.Team_Member.exist():
            return True
        else:
            return False

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Case(models.Model):
    # The date the case opened
    encounter_date = models.DateField("Date the Case Opened", blank=True, null=True)

    team_member = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='Team_Member', null=True, blank=True)

    CONCERN_LIST = (
        ('Positive', 'Positive'),
        ('Exposure', 'Exposure'),
        ('Symptom', 'Symptom'),
        ('Quarantine', 'Quarantine'),
    )
    # Original reason the case was opened / reason exposure was assumed
    concern = models.CharField('Concern(Positive, Exposure, Symptom, Quarantine)',
                               choices=CONCERN_LIST,
                               max_length=11,
                               blank=True,
                               default='')

    # a short discription of the case
    discription = models.CharField('Discription', max_length=1000, blank=True, default='')
    # The last day the employee came into work
    last_day_worked = models.DateField('Last Day Worked',blank=True, null=True)
    #Team members that have potentially been in contact with main team memebr
    close_contact = models.ManyToManyField(Person, related_name='Close_Contacts', blank=True)
    # Manager of the infected person
    manager = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='Manager', blank=True, null = True)
    # Status of the case
    CASE_LIST = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    )
    case_closed = models.CharField('Case(Open, Closed)', choices=CASE_LIST, max_length=11, blank=True, default='')

    def __str__(self):

        try:
            return self.team_member.name + " reported on " + str(self.encounter_date)

        except:

            return str(self.concern) + " on " + str(self.encounter_date)





    class Meta:
        ordering = ['-encounter_date']

class Test(models.Model):
    # date the test was taken
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='Test_Case', null=True, blank=True)
    test_date = models.DateField("Date Test Was Given", blank = True, null = True)
    results_date = models.DateField("Date Results Recieved", blank=True, null=True)
    LOC_LIST = (
        ('On-site', 'On-site'),
        ('Off-site', 'Off-site'),
    )
    # Where was the test taken
    location = models.CharField('Location of Test Taken(on-site / off-site)',
                               choices=LOC_LIST,
                               max_length=10,
                               blank=True,
                               default='')
    TEST_LIST = (
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
    )
    # Status
    test_status = models.CharField('Status(Positive/Negative)',
                                choices=TEST_LIST,
                                max_length=8,
                                blank=True,
                                default='')

    def __str__(self):

        try:

            return self.case.team_member.name + " " + str(self.test_status) + " on " + str(self.results_date)

        except:

            return str(self.test_status) + " on " + str(self.results_date)


    class Meta:
        ordering = ['-results_date']








