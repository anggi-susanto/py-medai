from app.repositories.user_repository import UserRepository
from app.entities.user import User

class ProfileService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_profile(self, username):
        return self.user_repository.get_user_by_username(username)

    def update_profile(self, username, name=None, email=None, phone=None, profile_photo=None):
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return None
        if name:
            user.name = name
        if email:
            user.email = email
        if phone:
            user.phone = phone
        if profile_photo:
            user.profile_photo = profile_photo
        self.user_repository.update_user(user)
        return user