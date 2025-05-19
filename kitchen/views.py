from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from kitchen.forms import DishNameSearchForm
from kitchen.models import Cook, Dish, DishType, Ingredient



def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dishtypes = DishType.objects.count()
    num_ingredients = Ingredient.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dishtypes": num_dishtypes,
        "num_ingredients": num_ingredients,
        "num_visits": num_visits,
    }

    return render(request, "kitchen/index.html", context=context)


class CookListView(LoginRequiredMixin, ListView):
    model = Cook
    paginate_by = 4


class CookDetailView(LoginRequiredMixin, DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes")


class CookCreateView(LoginRequiredMixin, CreateView):
    model = Cook
    fields = ["username", "first_name", "last_name", "years_of_experience"]
    success_url = reverse_lazy("cook-list")


class CookUpdateView(LoginRequiredMixin, UpdateView):
    model = Cook
    fields = "__all__"
    success_url = reverse_lazy("cook-list")


class CookDeleteView(LoginRequiredMixin, DeleteView):
    model = Cook
    success_url = reverse_lazy("cook-list")


class YearsOfExperienceUpdateView(LoginRequiredMixin, UpdateView):
    model = Cook
    fields = ("years_of_experience",)
    def get_success_url(self):
        return reverse("cook-detail", kwargs={"pk": self.object.pk})


class AssignCookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        dish.cooks.add(request.user)
        dish.save()
        return redirect("dish-detail", pk=dish.pk)


class RemoveCookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        dish.cooks.remove(request.user)
        dish.save()
        return redirect("dish-detail", pk=dish.pk)


class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    paginate_by = 4
    queryset = Dish.objects.all().select_related("type")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishNameSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return Dish.objects.filter(name__icontains=name)
        return self.queryset


class DishDetailView(LoginRequiredMixin, DetailView):
    model = Dish
    queryset = Dish.objects.all().prefetch_related("cooks", "ingredients")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dish = self.object
        context["is_cook_assigned"] = dish.cooks.filter(id=self.request.user.id).exists()
        return context


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("dish-list")


class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("dish-list")


class DishDeleteView(LoginRequiredMixin, DeleteView):
    model = Dish
    success_url = reverse_lazy("dish-list")


class DishTypeListView(LoginRequiredMixin, ListView):
    model = DishType
    paginate_by = 4


class DishTypeCreateView(LoginRequiredMixin, CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("dishtype-list")


class DishTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("dishtype-list")


class DishTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = DishType
    success_url = reverse_lazy("dishtype-list")


class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    paginate_by = 4
    queryset = Ingredient.objects.all().prefetch_related("dishes")


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = reverse_lazy("ingredient-list")


@login_required
def toggle_assign_to_dish(request, pk):
    cook = Cook.objects.get(id=request.user.id)
    dish = Dish.objects.get(id=pk)

    if dish in cook.dishes.all():
        cook.dishes.remove(dish)
    else:
        cook.dishes.add(dish)

    return HttpResponseRedirect(reverse_lazy("dish-detail", args=[pk]))
