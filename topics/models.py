from django.db import models
from django.utils.functional import cached_property


# Create your models here.
class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def top_level(self):
        return self.get_queryset().top_level()

    def children_of(self, target):
        return self.get_queryset().children_of(target)

    def children(self):
        return self.get_queryset().children()


class CategoryQuerySet(models.QuerySet):

    def top_level(self):
        return self.filter(parent__isnull=True)

    def children_of(self, target):
        return self.filter(parent=target)

    def children(self):
        return self.filter(parent__isnull=False)


class Category(models.Model):
    objects = CategoryManager()
    name = models.CharField(max_length=60)
    parent = models.ForeignKey('self',
                               blank=True,
                               null=True,
                               related_name='child',
                               on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

        unique_together = ('name', 'parent')  # no two cats with same name under parent

    @property
    def get_separator(self):
        return ' :: '

    def __str__(self):
        full_path = [self.name]
        p = self.parent

        while p is not None:
            full_path.append(p.name)
            p = p.parent

        return self.get_separator.join(full_path[::-1])


class Tag(models.Model):
    name = models.SlugField(max_length=80)

    def __str__(self):
        return self.name
