from django.db import models
from django.contrib.auth.models import User


    #to return actual value instead of cartegory(1)
#     def __str__(self):
#         return self.name
        
class balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name=models.CharField(max_length=120,default="")
    income=models.IntegerField()

class expenses_block(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    category=models.CharField(max_length=30)
    Details=models.CharField(max_length=120,default="Spend")
    amount = models.FloatField(null=False)
    transaction_type = models.CharField(max_length=20)
    curr_balance=models.IntegerField(default=0)
    Date= models.DateField()