from django.db import models

# Create your models here.
class FirstTest(models.Model):
    test_1 = models.CharField(max_length=70)
    test_2 = models.IntegerField
    test_3 = models.FloatField
    test_4 = models.DateTimeField

    def __str__(self):
        return self.test_1