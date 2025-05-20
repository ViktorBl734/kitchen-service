from django import forms

from kitchen.models import Dish, Ingredient


class DishNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=250, required=False,
        label = "",
        widget=forms.TextInput(attrs={"placeholder": "Search by dish name"}),
                           )


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = "__all__"
        widgets = {
            "cooks": forms.CheckboxSelectMultiple()
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'
        widgets = {
            "dishes": forms.CheckboxSelectMultiple()
        }
