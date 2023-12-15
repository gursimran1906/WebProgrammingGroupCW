from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    
    profile_image = models.ImageField(upload_to='profile_images/', default='/profile_images/default.jpg', null=True)
    email = models.EmailField(blank=True, null=True)  
    date_of_birth = models.DateField(null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        through='CustomUserGroup',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        through='CustomUserPermission',
    )

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define primary key
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return (str(self.id) +" - "+ self.title )

class UserPreferences(models.Model):
    user = models.OneToOneField('api.CustomUser', on_delete=models.CASCADE, related_name='preferences')
    favorite_categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"Preferences for {self.user.username}"

class Comment(models.Model):
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('api.CustomUser', on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.publication_date} - {self.article.title}"

class CustomUserGroup(models.Model):
    custom_user = models.ForeignKey('api.CustomUser', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class CustomUserPermission(models.Model):
    custom_user = models.ForeignKey('api.CustomUser', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
