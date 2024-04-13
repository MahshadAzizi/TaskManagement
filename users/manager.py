from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password, phone_number, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """

        user = self.model(username=username, password=password, phone_number=phone_number, **extra_fields)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, username, password, phone_number, **extra_fields):
        """
        Creates and saves a superuser with the given username and password.
        """

        user = self.create_user(
            username,
            password=password,
            phone_number=phone_number,
            ** extra_fields
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
