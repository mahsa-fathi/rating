from django.db import models
from django.db import transaction
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rate = models.DecimalField(max_digits=2, decimal_places=2)
    number_of_rates = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.title} - {self.user.id}"

    def add_post_rate(self, rate):
        with transaction.atomic():
            post = Post.objects.select_for_update().get(pk=self.pk)
            rate_volume = post.rate * post.number_of_rates
            post.number_of_rates = post.number_of_rates + 1
            post.rate = (rate_volume + rate) / post.number_of_rates
            post.save(update_fields=['rate', 'number_of_rates', 'updated'])

    def update_post_rate(self, old_rate, new_rate):
        with transaction.atomic():
            post = Post.objects.select_for_update().get(pk=self.pk)
            rate_volume = post.rate * post.number_of_rates
            post.rate = (rate_volume + new_rate - old_rate) / post.number_of_rates
            post.save(update_fields=['rate', 'updated'])

    def delete_post_rate(self, rate):
        with transaction.atomic():
            post = Post.objects.select_for_update().get(pk=self.pk)
            rate_volume = post.rate * post.number_of_rates
            post.number_of_rates = post.number_of_rates - 1
            post.rate = (rate_volume - rate) / post.number_of_rates
            post.save(update_fields=['rate', 'number_of_rates', 'updated'])


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.pk:
            super().save()
            self.post.add_post_rate(self.rate)
        else:
            old_rate = self.rate
            super().save()
            new_rate = self.rate
            self.post.update_post_rate(old_rate, new_rate)

    def delete(self, using=None, keep_parents=False):
        self.post.delete_post_rate(self.rate)
        super().delete()
