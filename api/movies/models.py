from django.db import models


class Movie(models.Model):
    """
    Model for movie representation

    This model define the necessaries field to identify a movie. Its attributes
    are:
        - title: As the movie title
        - category: As movie category
        - cast: As many to many relation with the actors who act in the film
    """

    title = models.CharField(
        primary_key=True,
        max_length=50,
        verbose_name="Movie title",
        blank=False,
        null=False,
        unique=True
    )

    category = models.CharField(
        max_length=20,
        verbose_name="Movie category",
        blank=False,
        null=False
    )

    cast = models.ManyToManyField(
        'actors.Actor',
        verbose_name="Movie Actors",
        related_name="movies"
    )

    def __str__(self):
        return f"<Movie {self.pk}: {self.title} ({self.category})>"
