# Generated by Django 5.0.2 on 2024-02-28 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0005_expense_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='expDateTime',
            field=models.DateField(verbose_name='datefield'),
        ),
    ]
