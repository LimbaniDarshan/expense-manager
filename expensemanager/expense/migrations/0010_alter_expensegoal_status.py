# Generated by Django 5.0.2 on 2024-03-13 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0009_expensegoal_expense_goal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensegoal',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('paused', 'paused'), ('not-active', 'not-active')], max_length=100),
        ),
    ]
