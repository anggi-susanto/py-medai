from app.models.user_model import User

from app import db

class UserRepository:
    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def save_user(self, user_entity):
        user_model = User(
            name=user_entity.name,
            username=user_entity.username,
            email=user_entity.email,
            phone=user_entity.phone,
            password=user_entity.password,
            profile_photo=user_entity.profile_photo
        )
        db.session.add(user_model)
        db.session.commit()

    def update_user(self, user):
        db.session.commit()