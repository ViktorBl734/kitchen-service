from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.models import Cook, Dish, DishType, Ingredient


class ViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        self.dishtype = DishType.objects.create(name="Salad")
        self.dish = Dish.objects.create(name="Olivier", price=10, type=self.dishtype)
        self.ingredient = Ingredient.objects.create(name="Potato")
        self.dish.ingredients.add(self.ingredient)
        self.user.dishes.add(self.dish)

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/index.html")

    def test_dish_list_view(self):
        response = self.client.get(reverse("dish-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dish.name)

    def test_dish_detail_view(self):
        response = self.client.get(reverse("dish-detail", kwargs={"pk": self.dish.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dish.name)

    def test_dish_create_view(self):
        response = self.client.post(reverse("dish-create"), {
            "name": "Borscht",
            "description": "Soup",
            "price": 50,
            "type": self.dishtype.id,
            "cooks": [self.user.id],
            "ingredients": [self.ingredient.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(name="Borscht").exists())

    def test_dish_update_view(self):
        response = self.client.post(reverse("dish-update", kwargs={"pk": self.dish.pk}), {
            "name": "Olivier Updated",
            "description": "Salad",
            "price": 15,
            "type": self.dishtype.id,
            "cooks": [self.user.id],
            "ingredients": [self.ingredient.id]
        })
        self.assertEqual(response.status_code, 302)
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, "Olivier Updated")

    def test_dish_delete_view(self):
        response = self.client.post(reverse("dish-delete", kwargs={"pk": self.dish.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dish.objects.filter(pk=self.dish.pk).exists())

    def test_toggle_assign_to_dish(self):
        dish = Dish.objects.create(name="Test Dish", price=20, type=self.dishtype)
        url = reverse("toggle-dish-assign", kwargs={"pk": dish.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(dish in self.user.dishes.all())

    def test_cook_list_view(self):
        response = self.client.get(reverse("cook-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_cook_detail_view(self):
        response = self.client.get(reverse("cook-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_ingredient_list_view(self):
        response = self.client.get(reverse("ingredient-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ingredient.name)

    def test_dishtype_list_view(self):
        response = self.client.get(reverse("dishtype-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dishtype.name)
