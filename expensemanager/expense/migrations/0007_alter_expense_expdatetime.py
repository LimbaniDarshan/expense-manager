# Generated by Django 5.0.2 on 2024-02-28 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0006_alter_expense_expdatetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='expDateTime',
            field=models.DateTimeField(),
        ),
    ]
