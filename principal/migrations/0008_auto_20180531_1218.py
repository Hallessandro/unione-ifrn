# Generated by Django 2.0.2 on 2018-05-31 15:18

from django.db import migrations
import quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0007_auto_20180531_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respostaatividade',
            name='resposta',
            field=quill.fields.RichTextField(),
        ),
    ]
