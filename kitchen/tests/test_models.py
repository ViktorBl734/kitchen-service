from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Dish, DishType, Ingredient


class ModelsTests(TestCase):
    def test_dish_str(self):
        type = DishType.objects.create(name="testdishtype")
        dish = Dish.objects.create(name="test", price=100, type=type)
        self.assertEqual(str(dish), dish.name)

    def test_cook_str(self):
        cook = get_user_model().objects.create_user(
            username="test",
            password="testpass123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(cook),
            f"{cook.username} ({cook.first_name} {cook.last_name})"
        )

    def test_dish_type_str(self):
        dishtype = DishType.objects.create(name="testdishtype")
        self.assertEqual(str(dishtype), dishtype.name)

    def test_ingredient_str(self):
        ingredient = Ingredient.objects.create(name="test")
        self.assertEqual(str(ingredient), ingredient.name)

    def test_dish_get_absolute_url(self):
        dishtype = DishType.objects.create(name="testdishtype")
        dish = Dish.objects.create(name="testdish", price=50.0, type=dishtype)
        self.assertEqual(dish.get_absolute_url(), reverse("dish-detail", kwargs={"pk": dish.pk}))

    def test_cook_get_absolute_url(self):
        cook = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.assertEqual(cook.get_absolute_url(), reverse("cook-detail", kwargs={"pk": cook.pk}))

    def test_dish_cooks_relationship(self):
        dishtype = DishType.objects.create(name="type")
        dish = Dish.objects.create(name="testdish", price=50.0, type=dishtype)
        cook = get_user_model().objects.create_user(username="cook1", password="pass123")
        dish.cooks.add(cook)
        self.assertIn(cook, dish.cooks.all())
        self.assertIn(dish, cook.dishes.all())

    def test_ingredient_dishes_relationship(self):
        dishtype = DishType.objects.create(name="type")
        dish = Dish.objects.create(name="testdish", price=50.0, type=dishtype)
        ingredient = Ingredient.objects.create(name="Salt")
        ingredient.dishes.add(dish)
        self.assertIn(dish, ingredient.dishes.all())
        self.assertIn(ingredient, dish.ingredients.all())
