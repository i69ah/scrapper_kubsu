from django.db import models
from django.urls import reverse


class Source(models.Model):
    """
    Article source model
    """
    class Type(models.TextChoices):
        STATIC = 'ST', 'static'
        DYNAMIC = 'DM', 'dynamic'

    name = models.CharField(max_length=255, null=False, blank=False)
    url = models.URLField(max_length=255, null=True, blank=False)
    last_page = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file_name = models.CharField(max_length=255, null=True, blank=False)
    spider_class = models.CharField(max_length=255, null=True, blank=False)
    type = models.CharField(max_length=2, choices=Type.choices, default=Type.STATIC)
    max_pages_per_session = models.IntegerField(default=10)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Article model
    """
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    annotation = models.TextField(null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    url = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(to=Source, related_name='articles', on_delete=models.CASCADE)
    label = models.CharField(max_length=255, null=True, blank=False)

    objects = models.Manager()

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'article'
        verbose_name_plural = 'articles'
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', args=[self.id])

    def get_author_view(self) -> str:
        return ', '.join(self.author.split('|'))
