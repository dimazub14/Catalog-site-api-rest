from typing import Dict, Any

from apps.users.models import User

class UserService:
    """Class-collection of business logic related to user"""

    @classmethod
    def _create_user(cls, data: Dict[str, Any]) -> "User":
        """Static method return created user object"""
        user = User.objects.create_user(**data)  # type: ignore
        return user

    @classmethod
    def create(cls, data: Dict[str, Any]) -> "User":
        """Create user"""
        user = cls._create_user(data=data)
        return user
