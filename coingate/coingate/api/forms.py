from django import forms

choices = (
    ("USD", "USD"),
    ("BTC", "BTC"),
    ("EUR", "EUR"),
)


class TransactionForm(forms.Form):
    value = forms.FloatField()
    currency = forms.ChoiceField(choices=choices)