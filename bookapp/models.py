from django.db import models
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

# Create your models here.
class register_tbl(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.EmailField(max_length=20)
    password=models.CharField(max_length=20)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    type=models.CharField(max_length=20, choices=[('admin','Admin'),('user','User'),('manager','manager')],default='user')
    

    def __str__(self):
        return f"{self.fname} {self.lname} ({self.email})"
    
    def has_active_subscription(self):
        return self.usersubscription_set.filter(
            is_active=True,
            end_date__gt=timezone.now()
        ).exists()

class Book_tbl(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category=models.CharField(max_length=20)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/')
    pdf_file = models.FileField(upload_to='books/')
    added_on = models.DateTimeField(auto_now_add=True)
    read=models.TextField()
    trending = models.BooleanField(default=False)
    
class ReadBook_tbl(models.Model):
    book=models.ForeignKey(Book_tbl,on_delete=models.CASCADE)
    read=models.TextField()

class adminProfile_tbl(models.Model):
    admin=models.ForeignKey(Book_tbl,on_delete=models.CASCADE)

class ReadingList(models.Model):
    book=models.ForeignKey(Book_tbl,on_delete=models.CASCADE)
    user=models.ForeignKey(register_tbl,on_delete=models.CASCADE)
    qty=models.PositiveBigIntegerField(default=1)
    
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.IntegerField()  # e.g. 30 = monthly, 365 = yearly
    features = models.TextField()  # Comma-separated features
    is_active = models.BooleanField(default=True)

class UserSubscription(models.Model):
    user = models.ForeignKey(register_tbl, on_delete=models.CASCADE)  # ✅ fixed
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} → {self.plan}"

 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)


class Payment(models.Model):
    user = models.ForeignKey(register_tbl, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=(
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ), default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.plan} - {self.status}"

class UserBook(models.Model):
    user = models.ForeignKey(register_tbl, on_delete=models.CASCADE)
    book = models.ForeignKey(Book_tbl, on_delete=models.CASCADE)
    accessed_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # prevents duplicate entries

