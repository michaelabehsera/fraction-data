from django.db import models


class Order(models.Model):
    name = models.CharField('Order Name', max_length=64, unique=True)
    description = models.TextField('Order Description', blank=True)

    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', related_name='order_details', on_delete=models.CASCADE)

    customer = models.CharField('Customer\'s First and last name', max_length=255)
    age = models.IntegerField('Age', help_text='Age of person in years', blank=True)
    weight = models.IntegerField('Weight', help_text='Weight in pounds', blank=True)
    is_vegetarian = models.BooleanField(default=True, help_text='Is the respondent a vegetarian')

    def __str__(self):
        return '%s - %s' % (self.order, self.customer)
