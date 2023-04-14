from django.db import models
from django.urls import reverse
from datetime import date

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)
class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Create your models here.
class Finch(models.Model):
    species = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    habitat = models.CharField(max_length=300)
    note = models.CharField(max_length=750)
    toys = models.ManyToManyField(Toy)

    def __str__(self):
        return self.species

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)


class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"

    class Meta:
        ordering = ['-date']
