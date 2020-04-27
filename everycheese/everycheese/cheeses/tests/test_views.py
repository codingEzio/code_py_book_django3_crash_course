import pytest
from pytest_django.asserts import assertContains, assertRedirects

from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory  # noqa

from everycheese.users.models import User  # noqa
from ..models import Cheese
from ..views import CheeseListView, CheeseDetailView, CheeseCreateView
from .factories import CheeseFactory, cheese

pytestmark = pytest.mark.django_db

# Q: Where the 'rf' & 'admin_user' come from?
# A: They are the implicit fixtures provided by pytest_django.
#    More at
#    - https://pytest-django.readthedocs.io/en/latest/helpers.html
#    - https://github.com/pytest-dev/pytest-django/blob/master/pytest_django/fixtures.py


def test_good_cheese_list_view_expanded(rf):
    url = reverse("cheeses:list")
    request = rf.get(url)
    callable_obj = CheeseListView.as_view()
    response = callable_obj(request)
    assertContains(response, "Cheese List")


def test_good_cheese_list_view(rf):
    request = rf.get(reverse("cheeses:list"))
    response = CheeseListView.as_view()(request)
    assertContains(response, "Cheese List")


def test_cheese_list_contains_two_cheeses(rf):
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    request = rf.get(reverse("cheeses:list"))
    response = CheeseListView.as_view()(request)
    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)


def test_good_cheese_detail_view(rf, cheese):
    url = reverse("cheeses:detail", kwargs={"slug": cheese.slug})
    request = rf.get(url)

    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    assertContains(response, cheese.name)


def test_cheese_detail_contains_cheese_data(rf, cheese):
    url = reverse("cheeses:detail", kwargs={"slug": cheese.slug})
    request = rf.get(url)
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)


def test_good_cheese_create_view(rf, admin_user, cheese):
    request = rf.get(reverse("cheeses:add"))
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)
    assert response.status_code == 200


def test_cheese_create_form_valid(rf, admin_user):
    form_data = {
        "name": "Sample cheese",
        "description": "A sample cheese",
        "firmness": Cheese.Firmness.SEMI_SOFT,
    }
    request = rf.post(reverse("cheeses:add"), form_data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)  # noqa

    chee = Cheese.objects.get(name="Sample cheese")
    assert chee.description == "A sample cheese"
    assert chee.firmness == Cheese.Firmness.SEMI_SOFT
    assert chee.creator == admin_user
