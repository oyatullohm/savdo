from django.db import models
from django.utils import timezone
from django.db.models import F ,Sum


class Product(models.Model):
    TYPE = (
        (1,"qop"),
        (2,"eminsa")
    )
    name = models.CharField(max_length=55,unique=True)
    sum = models.FloatField(default=0)
    type = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.name


class Price (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE , related_name='prices')
    color = models.CharField(max_length=55)
    sum = models.FloatField(default=0)
    kl = models.FloatField(default=0)
    def __str__(self):
        return self.color


class Product_Count(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='counts')
    count = models.PositiveIntegerField(default=0)
    sum = models.FloatField(default=0)

    @property
    def total_summa(self):
        return self.count * self.sum

   
class Client(models.Model):
    TYPE= (
        (1,"Taminotchi"),
        (2,"Haridor")
    )
    type = models.IntegerField(choices=TYPE , default=2)
    phone = models.CharField(max_length=55)
    name = models.CharField(max_length=55)
    amount = models.FloatField(default=0)
    def __str__(self) :
        return self.name


class Payment(models.Model):
    TYPE = (
        (1,"Kirim"),
        (2,"Chiqim"),
        (3,"Ishlatdim"),
    )
    client = models.ForeignKey(Client,on_delete=models.SET_NULL, null=True, blank=True)
    type = models.IntegerField(choices=TYPE, default=1)
    cource = models.PositiveIntegerField(default=0)
    client_before_amount = models.FloatField(default=0)
    client_after_amount = models.FloatField(default=0)
    cash_before_amount = models.FloatField(default=0)
    cash_after_amount = models.FloatField(default=0)
    date = models.DateField()
    amount = models.FloatField(default=0)
    def __str__(self) :
        return f"{self.amount}"


class Cash(models.Model):
    amount = models.FloatField(default=0)
    
    def __str__(self) :
        return f"{self.amount}"


class IncomeItem(models.Model):
    product = models.ForeignKey(Product_Count, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    price = models.FloatField(default=0)
    @property
    def total_price(self):
        return self.price *self.count 


class Income(models.Model):
    client = models.ForeignKey(Client,on_delete=models.SET_NULL, null=True, blank=True, related_name='income_clients')
    date = models.DateField(timezone.now)
    items = models.ManyToManyField(IncomeItem,  blank=True , related_name='items')
    cource = models.PositiveIntegerField(default=0)
    client_before = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    client_after = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    loan = models.BooleanField(default=False)
    @property
    def total_summa(self):
        total = self.items.all().aggregate(
            total=Sum(F('count') * F('price'))
        )['total'] or 0
        return total
    
    @property
    def loan_type(self):
        if self.loan:
            return "nasya"
        return "naq"
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product_Count, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    price = models.FloatField(default=0)
    
    @property
    def total_price(self):
        return self.price *self.count 


class Order(models.Model):
    client = models.ForeignKey(Client,on_delete=models.SET_NULL, null=True, blank=True, related_name='order_clients')
    date = models.DateField(null=True, blank=True)
    items = models.ManyToManyField(OrderItem, blank=True , related_name='items')
    cource = models.PositiveIntegerField(default=0)
    client_before = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    client_after = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    loan = models.BooleanField(default=False)

    @property
    def total_summa(self):
        total = self.items.all().aggregate(
            total=Sum(F('count') * F('price'))
        )['total'] or 0
        return total
    
    
    @property
    def loan_type(self):
        if self.loan:
            return "nasya"
        return "naq"
    

class Cource(models.Model):
    cource = models.PositiveIntegerField(default=0)
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.cource}"
       
