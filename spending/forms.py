from django import forms


class NewSpendingForm(forms.Form):
    """
    Форма для добавления новой траты
    """
    tlg_id = forms.CharField(max_length=15)
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)
    category = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500, required=False)
