from django import forms


class DishNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=250, required=False,
        label = "",
        widget=forms.TextInput(attrs={"placeholder": "Search by dish name"}),
                           )
