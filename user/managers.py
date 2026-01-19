from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required! ")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        return self.create_user(email=email, password=password, kwargs=kwargs)
