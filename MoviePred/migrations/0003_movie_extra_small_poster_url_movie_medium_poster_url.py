# Generated by Django 4.2.2 on 2023-07-18 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoviePred', '0002_review_prob_neg_review_prob_pos'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='extra_small_poster_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='medium_poster_url',
            field=models.URLField(null=True),
        ),
    ]