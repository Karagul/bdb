from django.contrib import admin
from .models import Currency, Country, BondIssue, Comment

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('abbr', 'name')
    list_filter = ('abbr', 'name')
    search_fields = ('abbr', 'name')
    ordering = ('abbr', 'name')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('abbr', 'name', 'country')
    list_filter = ('abbr', 'name', 'country')
    search_fields = ('abbr', 'name')
    ordering = ('abbr', 'name')

@admin.register(BondIssue)
class BondIssueAdmin(admin.ModelAdmin):
    list_display = ('ISIN', 'Ticker', 'IssuerCompany',
                    'Maturity', 'Currency', 'Coupon', 'Moody',
    )
    list_filter = ('ISIN', 'Ticker', 'IssuerCompany',
                    'Maturity', 'Currency', 'Coupon', 'Moody',
    )
    search_fields = ('ISIN', 'Ticker', 'IssuerCompany',
                    'Moody', 'Country',
    )
    ordering = ('Maturity',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'record', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')
