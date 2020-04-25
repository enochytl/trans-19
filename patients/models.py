from django.db import models

# Create your models here.

class Patients(models.Model):
    name = models.CharField(max_length = 50)
    
    id_document_no  = models.CharField(max_length = 50)
    date_of_birth = models.DateField()
    date_of_confirmation = models.DateField()
    case_no = models.CharField(max_length = 20, primary_key=True)
    def __str__(self):
        return self.name

class Locations_visited(models.Model):
    name = models.CharField(max_length = 50)
    start_date = models.DateField()
    end_date = models.DateField()
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

    case_no = models.ForeignKey(
        Patients,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

