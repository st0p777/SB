# Generated by Django 2.2.6 on 2020-01-07 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SB', '0026_kbitem_attachments'),
    ]

    operations = [
        migrations.AddField(
            model_name='kbcategory',
            name='queue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SB.Queue', verbose_name='Default queue when creating a ticket after viewing this category.'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='kbitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SB.KBItem', verbose_name='Knowledge base item the user was viewing when they created this ticket.'),
        ),
        migrations.AlterField(
            model_name='followupattachment',
            name='filename',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Filename'),
        ),
        migrations.AlterField(
            model_name='followupattachment',
            name='mime_type',
            field=models.CharField(blank=True, max_length=255, verbose_name='MIME Type'),
        ),
        migrations.AlterField(
            model_name='followupattachment',
            name='size',
            field=models.IntegerField(blank=True, help_text='Size of this file in bytes', verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='kbiattachment',
            name='filename',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Filename'),
        ),
        migrations.AlterField(
            model_name='kbiattachment',
            name='mime_type',
            field=models.CharField(blank=True, max_length=255, verbose_name='MIME Type'),
        ),
        migrations.AlterField(
            model_name='kbiattachment',
            name='size',
            field=models.IntegerField(blank=True, help_text='Size of this file in bytes', verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='kbitem',
            name='voted_by',
            field=models.ManyToManyField(related_name='votes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='queue',
            name='enable_notifications_on_email_events',
            field=models.BooleanField(blank=True, default=False, help_text='When an email arrives to either create a ticket or to interact with an existing discussion. Should email notifications be sent ? Note: the new_ticket_cc and updated_ticket_cc work independently of this feature', verbose_name='Notify contacts when email updates arrive'),
        ),
    ]
