from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.user.models import User, UserProfile


class UserRepository:

    def create_user(
        self,
        db: Session,
        user: User
    ) -> User:

        db.add(user)
        db.flush()
        db.refresh(user)

        return user

    def create_user_profile(
        self,
        db: Session,
        profile: UserProfile
    ) -> UserProfile:

        db.add(profile)
        db.flush()
        db.refresh(profile)

        return profile

    def get_user_by_email(
        self,
        db: Session,
        email: str
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_user_by_id(
        self,
        db: Session,
        user_id: UUID
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_user_profile(
        self,
        db: Session,
        user_id: UUID
    ) -> UserProfile | None:

        return (
            db.query(UserProfile)
            .filter(UserProfile.user_id == user_id)
            .first()
        )

    def update_user(
        self,
        db: Session,
        user: User
    ) -> User:

        db.flush()
        db.refresh(user)

        return user

    def update_user_profile(
        self,
        db: Session,
        profile: UserProfile
    ) -> UserProfile:

        db.flush()
        db.refresh(profile)

        return profile

    def delete_user(
        self,
        db: Session,
        user: User
    ) -> None:

        db.delete(user)
        db.flush()