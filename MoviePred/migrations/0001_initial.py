# Generated by Django 4.2.2 on 2023-07-10 08:33

import datetime
from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.CharField(max_length=100, null=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('date_released', models.DateField(default=datetime.date.today, null=True)),
                ('genre', models.ManyToManyField(default=None, related_name='movies', to='MoviePred.genre')),
                ('movie_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('critic_name', models.CharField(max_length=100)),
                ('content', models.TextField(max_length=10000)),
                ('review_date', models.DateField(auto_now_add=True)),
                ('movie_link', models.CharField(max_length=100, null=True)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(Decimal('0.0')), django.core.validators.MaxValueValidator(Decimal('5.0'))])),
                ('sentiment_pred', models.CharField(choices=[('positive', 'Positive'), ('negative', 'Negative')], default='positive', max_length=20)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', related_query_name='review', to='MoviePred.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', related_query_name='review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
