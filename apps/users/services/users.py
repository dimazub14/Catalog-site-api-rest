from typing import Any, Dict

from apps.users.models import User


class UserService:
    """Class-collection of business logic related to user"""

    @classmethod
    def _create_user(cls, data: Dict[str, Any]) -> "User":
        """Static method return created user object"""
        user = User.objects.create_user(**data)
        return user

    @classmethod
    def create(cls, data: Dict[str, Any]) -> "User":
        """Create user"""
        user = cls._create_user(data=data)
        return user

    @classmethod
    def get(cls, data: Dict[str, Any]) -> "User":
        """Get user by dict"""
        return User.objects.get(**data)

    @classmethod
    def exists(cls, data: Dict[str, Any]) -> bool:
        """Check if user exists"""
        return User.objects.filter(**data).exists()

    @classmethod
    def change_password(cls, user: "User", password: str) -> None:
        user.set_password(password)
        user.save(update_fields=["password"])
        # Notification
