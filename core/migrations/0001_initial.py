# Generated by Django 2.2.1 on 2019-06-23 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BondIssue',
            fields=[
                ('ISIN', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('IssuerCompany', models.CharField(max_length=100)),
                ('Ticker', models.CharField(max_length=15)),
                ('Coupon', models.DecimalField(decimal_places=3, max_digits=5)),
                ('Maturity', models.DateField()),
                ('MaturityType', models.CharField(max_length=20)),
                ('Source', models.CharField(blank=True, max_length=15)),
                ('Moody', models.CharField(max_length=10)),
                ('Sp', models.CharField(blank=True, max_length=10)),
                ('Fitch', models.CharField(blank=True, max_length=10)),
                ('BloombergCompositeRating', models.CharField(blank=True, max_length=10)),
                ('Announce', models.DateField(blank=True)),
                ('CollateralType', models.CharField(max_length=20)),
                ('IssueDate', models.DateField(blank=True)),
                ('OutstandingAmount', models.PositiveIntegerField(blank=True)),
                ('IssuedAmount', models.PositiveIntegerField(blank=True)),
                ('Underwriter', models.CharField(blank=True, max_length=20)),
                ('MinimumPiece', models.PositiveIntegerField(blank=True)),
                ('BidPrice', models.DecimalField(blank=True, decimal_places=3, max_digits=6)),
                ('BidYTM', models.DecimalField(blank=True, decimal_places=3, max_digits=6)),
                ('BidMDuration', models.DecimalField(blank=True, decimal_places=2, max_digits=5)),
                ('Archived', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('Maturity',),
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('abbr', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('abbr',),
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('abbr', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Country')),
            ],
            options={
                'ordering': ('abbr',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.BondIssue')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='bondissue',
            name='Country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Country'),
        ),
        migrations.AddField(
            model_name='bondissue',
            name='Currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Currency'),
        ),
    ]
