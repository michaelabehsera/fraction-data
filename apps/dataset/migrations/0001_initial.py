# Generated by Django 2.0 on 2018-02-12 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Order Name')),
                ('description', models.TextField(blank=True, verbose_name='Order Description')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=255, verbose_name="Customer's First and last name")),
                ('age', models.IntegerField(blank=True, help_text='Age of person in years', verbose_name='Age')),
                ('weight', models.IntegerField(blank=True, help_text='Weight in pounds', verbose_name='Weight')),
                ('is_vegetarian', models.BooleanField(default=True, help_text='Is the respondent a vegetarian')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='dataset.Order')),
            ],
        ),
    ]
