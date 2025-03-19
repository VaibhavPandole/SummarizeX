from django.db import models


class SummaryBulletPoints(models.Model):
    """
    Model to store original text and summarized bullet points.
    """

    original_text = models.TextField()
    summary = models.TextField()
    bullet_points = models.TextField()
