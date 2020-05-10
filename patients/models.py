from django.db import models

# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length = 50)
    
    id_document_no  = models.CharField(max_length = 50)
    date_of_birth = models.DateField()
    date_of_confirmation = models.DateField()
    case_no = models.CharField(max_length = 20, primary_key=True)
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length = 50)
    x = models.DecimalField(max_digits=11, decimal_places=6)
    y = models.DecimalField(max_digits=11, decimal_places=6)

    # Address
    address_line_1 = models.CharField(max_length = 100, null=True, blank=True)
    address_line_2 = models.CharField(max_length = 100, null=True, blank=True)
    address_line_3 = models.CharField(max_length = 100, null=True, blank=True)

    # details of specific place
    description = models.TextField(blank=True)

    class Category_choices(models.TextChoices):
        home = "home", "Home"
        work = "work", "Work"
        vacation = "vac", "Vacation"
    category = models.CharField(
        max_length=10,
        choices=Category_choices.choices,
        default=Category_choices.home
    )
    class District_choices(models.TextChoices):
        
        cw = "1", "Central and Western"
        e = "2", "Eastern"
        s = "3", "Southern"
        wc = "4", "Wan Chai"
        ssp = "5", "Sham Shui Po"
        kc = "6", "Kowloon City"
        kt = "7", "Kwun Tong"
        wts = "8", "Wong Tai Sin"
        ytm = "9", "Yau Tsim Mong"
        i = "10", "Islands"
        kwts = "11", "Kwai Tsing"
        n = "12", "North"
        sk = "13", "Sai Kung"
        st = "14", "Sha Tin"
        tp = "15", "Tai Po"
        tw = "16", "Tsuen Wan"
        tm = "17", "Tuen Mun"
        yl = "18", "Yuen Long"
    district = models.CharField(
        max_length=10,
        choices=District_choices.choices,
        default=District_choices.cw
    )

    def __str__(self):
        return self.name

class VisitingRecord(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    loc = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)
    case_no = models.CharField(max_length=20)
    
    def __str__(self):
        return self.case_no
