# Generated by Django 3.1.1 on 2020-10-12 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('accounts', '0002_auto_20201006_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='book',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='books.book'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='choice_books',
            field=models.ManyToManyField(related_name='choice_users', to='books.Book'),
        ),
        migrations.AddField(
            model_name='user',
            name='finish_books',
            field=models.ManyToManyField(related_name='finish_users', to='books.Book'),
        ),
        migrations.AddField(
            model_name='user',
            name='like_books',
            field=models.ManyToManyField(related_name='like_users', to='books.Book'),
        ),
        migrations.AddField(
            model_name='user',
            name='unlike_books',
            field=models.ManyToManyField(related_name='unlike_users', to='books.Book'),
        ),
    ]