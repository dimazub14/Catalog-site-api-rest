import factory.django

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):

    email = factory.LazyAttribute(lambda obj: "{}@test.com".format(obj.name).lower())
    name = factory.Faker("name")

    class Meta:
        model = User


class EmailFactory(factory.django.DjangoModelFactory):
    """EmailFactory"""
    email = factory.LazyAttribute(lambda obj: "@test.com".format().lower())
    name = factory.Faker("name")

    class Meta:
        model = User
