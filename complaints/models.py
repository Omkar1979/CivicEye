from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Complaint(models.Model): #inherited Models class from Model
    CATEGORY_CHOICES = [
        ('Road', 'Road'),
        ('Water', 'Water'),
        ('Electricity', 'Electricity'),
        ('Waste', 'Waste'),
        ('Other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='complaints/', blank=True, null=True)
    
    # Removed the direct ManyToMany field to avoid clash with Like model
    # likes = models.ManyToManyField(User, related_name='liked_complaints', blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    class Meta:
        ordering = ['-created_at']

    @property
    def total_likes(self):
        return self.complaint_likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name='complaint_likes'   # ✅ changed related_name to avoid clash
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'complaint')  # prevent multiple likes by same user

    def __str__(self):
        return f"{self.user.username} liked {self.complaint.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.complaint.title}"


class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='shares')
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} shared {self.complaint.title}"
