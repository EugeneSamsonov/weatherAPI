from django.db import models

from users.models import User

# Create your models here.
class UserHistory(models.Model):
    user = models.ForeignKey(to=User, verbose_name="Пользователь", on_delete=models.CASCADE, blank=True)

    city = models.CharField(max_length=255, verbose_name="Город")

    temp = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Температура")
    temp_max = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Максимальная температура")
    temp_min = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Минимальная температура")

    humidity = models.PositiveSmallIntegerField(verbose_name="Влажность")

    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Скорость ветра")
    wind_direction = models.PositiveSmallIntegerField(verbose_name="Направление ветра")

    weather = models.CharField(max_length=255, verbose_name="Погода")
    weather_desc = models.TextField(verbose_name="Описание погоды")

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    sunrise = models.DateTimeField(auto_now=False, auto_now_add=False)
    sunset = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = 'history'
        verbose_name = "история запросов"
        verbose_name_plural = "Истории запросов"
        ordering = ("id", )
    

    def __str__(self) -> str:
        return f"{self.pk} | {self.user.username} | {self.city} | {self.timestamp}"
