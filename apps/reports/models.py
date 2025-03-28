from django.db import models


class AnonymousReport(models.Model):
    CATEGORY_CHOICES = [
        ('acoso', 'Acoso'),
        ('discriminacion', 'Discriminación'),
        ('fraude', 'Fraude'),
        ('otro', 'Otro'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_category_display()} - {self.submitted_at.date()}"
