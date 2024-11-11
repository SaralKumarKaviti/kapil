# Generated by Django 5.1.2 on 2024-11-05 10:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counselor_app', '0012_remove_studentpaymentdetails_registration_fee_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationPaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=150)),
                ('enrollment_id', models.CharField(max_length=50)),
                ('course_name', models.CharField(max_length=150)),
                ('payment_mode', models.CharField(choices=[('offline', 'Offline'), ('online', 'Online')], max_length=150)),
                ('register_payment_status', models.CharField(max_length=50)),
                ('paymented_on', models.DateTimeField(auto_now_add=True)),
                ('payment_by', models.CharField(max_length=150)),
                ('transaction_id', models.CharField(max_length=150)),
                ('register_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.IntegerField(default=1)),
                ('counselor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counselor_app.role')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counselor_app.manager')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counselor_app.studentenrollment')),
            ],
        ),
    ]
