from django.contrib import admin
from .models import User, Course, Module, Lesson, Quiz, Flashcard
# Register your models here.

# =======================
# User admin
# =======================


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'phone', 'college')
    list_filter = ('college',)
    search_fields = ('username', 'full_name', 'email', 'phone', 'college')


# =======================
# Quiz & Flashcard inlines
# =======================
class QuizInline(admin.StackedInline):
    model = Quiz
    extra = 1

class FlashcardInline(admin.StackedInline):
    model = Flashcard
    extra = 1

# =======================
# Lesson admin
# =======================
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuizInline, FlashcardInline]
    list_display = ('title', 'module', 'content_type', 'order')
    list_filter = ('content_type',)
    ordering = ('module', 'order')

# =======================
# Module admin
# =======================
class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('title', 'course', 'order')
    ordering = ('course', 'order')

# =======================
# Course admin
# =======================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]
    list_display = ('title', 'instructor', 'price', 'is_premium', 'created_at')
    list_filter = ('is_premium', 'created_at')
    search_fields = ('title', 'description', 'instructor__username')
    ordering = ('created_at',)

