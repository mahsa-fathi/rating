from django.db import models
from django.db import transaction
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.title} - {self.author.id}"

    @property
    def rate(self):
        volume = 0
        number_of_rates = 0
        for user_rating in self.userrating_set.all():
            volume += user_rating.rate
            number_of_rates += 1
        if number_of_rates == 0:
            return None
        return volume / number_of_rates

    @property
    def number_of_rates(self):
        number_of_rates = 0
        for _ in self.userrating_set.all():
            number_of_rates += 1
        return number_of_rates


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('user', 'post')
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
