"""
Test for models in core app.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(**params):
    """Create a sample user"""
    return get_user_model().objects.create_user(**params)


class ModelTests(TestCase):
    """Test for models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected_email)

    def test_new_user_withou_email_raises_error(self):
        """Test creating user without email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123 ')

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'sample123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a new recipe"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'sample123'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample Recipe',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a new tag"""
        user = create_user(email='test@example.com', password='sample123')
        tag = models.Tag.objects.create(user=user, name='Sample Tag')

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating a new ingredient"""
        user = create_user(
            email='sample@example.com',
            password='sample123'
        )
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Sample Ingredient'
        )

        self.assertEqual(str(ingredient), ingredient.name)
