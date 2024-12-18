from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Meta:
        db_table = 'user'
        verbose_name = "пользователя"
        verbose_name_plural = "Пользователи"
        ordering = ("id", )
    

    def __str__(self) -> str:
        return f"{self.username}"
