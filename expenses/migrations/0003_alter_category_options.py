# Generated by Django 5.1.2 on 2024-11-13 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_category_alter_expenses_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
