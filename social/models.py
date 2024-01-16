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
        sums = self.userrating_set.aggregate(average=models.Avg('rate'))
        rate = sums['average']
        return rate

    @property
    def number_of_rates(self):
        sums = self.userrating_set.aggregate(count=models.Count('rate'))
        number_of_rates = sums['count'] or 0
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
