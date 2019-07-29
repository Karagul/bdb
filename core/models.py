from django.db import models
from django.urls import reverse


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(Archived=False)

class Country(models.Model):
    objects = models.Manager()
    abbr = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=100)
    class Meta:
        ordering = ('abbr',)
    def __str__(self):
        return self.abbr

class Currency(models.Model):
    objects = models.Manager()
    abbr = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    class Meta:
        ordering = ('abbr',)
    def __str__(self):
        return self.abbr


class BondIssue(models.Model):

    objects = models.Manager()
    active = ActiveManager()

    ISIN = models.CharField(primary_key=True, max_length=15)
    IssuerCompany = models.CharField(max_length=100)
    Ticker = models.CharField(max_length=15)
    Coupon = models.DecimalField(max_digits=5, decimal_places=3)
    Maturity = models.DateField()
    MaturityType = models.CharField(max_length=20)
    Currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    Source = models.CharField(max_length=15, blank=True)
    Moody = models.CharField(max_length=10)
    Sp = models.CharField(max_length=10, blank=True)
    Fitch = models.CharField(max_length=10, blank=True)
    BloombergCompositeRating = models.CharField(max_length=10, blank=True)

    Announce = models.DateField(blank=True)
    CollateralType = models.CharField(max_length=20)
    Country = models.ForeignKey(Country, on_delete=models.CASCADE)

    IssueDate = models.DateField(blank=True)
    OutstandingAmount = models.BigIntegerField(blank=True)
    IssuedAmount = models.BigIntegerField(blank=True)
    Underwriter = models.CharField(max_length=20, blank=True)
    MinimumPiece = models.PositiveIntegerField(blank=True)
    BidPrice = models.DecimalField(max_digits=10, decimal_places=3, blank=True)
    BidYTM = models.DecimalField(max_digits=6, decimal_places=3, blank=True)
    BidMDuration = models.DecimalField(max_digits=5, decimal_places=2, blank=True)

    Archived = models.BooleanField(default=False)

    class Meta:
        ordering = ('Maturity',)

    def __str__(self):
        return self.ISIN

    def get_absolute_url(self):
        return reverse('core:bonds_detail', args=[self.ISIN])


class Comment(models.Model):
    record = models.ForeignKey(BondIssue, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50) # Возможно, потребуется привязать к user
    email = models.EmailField()
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Комментарий {0} к {1}'.format(self.name, self.record)
