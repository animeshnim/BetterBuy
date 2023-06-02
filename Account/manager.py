from django.contrib.auth.base_user import BaseUserManager


class MyUserManager(BaseUserManager):
    use_in_migrations = True


    # Methods
    def create_user(self, email, password, **other_info):
        if not email:
            raise ValueError('Email is required!')

        email = self.normalize_email(email)
        user = self.model(email = email, **other_info)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password, **other_info):
        other_info.setdefault('is_staff', True)
        other_info.setdefault('is_superuser', True)
        other_info.setdefault('is_active', True)

        # Verification/Debugging
        if other_info.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if other_info.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **other_info)