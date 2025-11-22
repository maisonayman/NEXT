from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


# =======================
# User Authentication
# =======================
class User(AbstractUser):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email=models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    college = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)


    
    # حل مشكلة reverse accessor clash
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # أي اسم فريد
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # أي اسم فريد
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


# =======================
# Courses & Admin CMS
# =======================
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    is_premium = models.BooleanField(default=False)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content_type_choices = [('video', 'Video'), ('text', 'Text'), ('quiz', 'Quiz'), ('flashcard', 'Flashcard')]
    content_type = models.CharField(max_length=20, choices=content_type_choices, default='text')
    content_url = models.TextField(null=True, blank=True)  # link for video or content
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.title}"


# =======================
# Quizzes & Flashcards
# =======================
class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    question = models.TextField()
    answer = models.TextField()
    # Optional: multiple choice options
    options = models.JSONField(null=True, blank=True)


class Flashcard(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='flashcards')
    front = models.TextField()
    back = models.TextField()


# =======================
# Enrollment & Payment
# =======================
#class Enrollment(models.Model):
 #   student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
  #  course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
   # enrolled_at = models.DateTimeField(auto_now_add=True)
    #completed = models.BooleanField(default=False)


#class Payment(models.Model):
#    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='payment')
#    amount = models.DecimalField(max_digits=8, decimal_places=2)
#    payment_method_choices = [('stripe', 'Stripe'), ('paypal', 'PayPal')]
#    payment_method = models.CharField(max_length=20, choices=payment_method_choices)
#    paid_at = models.DateTimeField(auto_now_add=True)
#    status_choices = [('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')]
#    status = models.CharField(max_length=20, choices=status_choices, default='pending')
