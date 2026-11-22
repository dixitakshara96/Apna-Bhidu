"""Complaints app ke database models yahan define kiye gaye hain."""

# Django ke model fields aur Model base class ko import kar rahe hain.
from django.db import models


class Complaint(models.Model):
    """User ki complaint ko database table mein represent karta hai."""

    # Status ke fixed options define kar rahe hain, taaki database mein
    # status ki value consistent rahe aur user ko readable labels mil sakein.
    class Status(models.TextChoices):
        # Complaint abhi open hai aur uspe kaam shuru nahi hua hai.
        OPEN = "open", "Open"

        # Complaint par team abhi kaam kar rahi hai.
        IN_PROGRESS = "in_progress", "In progress"

        # Complaint ka solution de diya gaya hai.
        RESOLVED = "resolved", "Resolved"

        # Complaint ka process completely close kar diya gaya hai.
        CLOSED = "closed", "Closed"

    # Complaint ka short title store karta hai; maximum 200 characters allowed hain.
    title = models.CharField(max_length=200)

    # Complaint ki complete details ya problem ka description store karta hai.
    description = models.TextField()

    # Complaint kis category se related hai, jaise billing, service, ya delivery.
    category = models.CharField(max_length=100)

    # Complaint ka current status store karta hai.
    status = models.CharField(
        # Status ke text ki maximum length 20 characters rakhi gayi hai.
        max_length=20,

        # Sirf Status class mein diye gaye options hi select kiye ja sakte hain.
        choices=Status.choices,

        # Nayi complaint create hote hi uska default status OPEN hoga.
        default=Status.OPEN,
    )

    # Record create hone ka date/time Django automatically set karega.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model ke database-level options yahan configure hote hain."""

        # Latest complaints sabse pehle dikhengi (- ka matlab descending order).
        ordering = ["-created_at"]

    def __str__(self):
        """Admin panel ya shell mein complaint ka title readable text ke roop mein dikhata hai."""

        # Object ko print/display karte waqt uska title return kar rahe hain.
        return self.title
