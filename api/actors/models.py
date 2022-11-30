from django.db import models


class Actor(models.Model):
    """
    Model for actor representation

    This model define the necessaries field to identify an actor.
    Its attributes are:
        - name: With the actor name
        - age: With the actor age
        - gender: With the actor gender
    """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDERS = [
        ("m", GENDER_MALE),
        ("f", GENDER_FEMALE)
    ]

    name = models.CharField(
        primary_key=True,
        max_length=50,
        verbose_name="Actor name",
        blank=False,
        null=False,
        unique=True
    )

    age = models.IntegerField(
        verbose_name="Age of the Actor",
        blank=False,
        null=False
    )

    gender = models.CharField(
        max_length=6,
        verbose_name="Actors gender",
        choices=GENDERS,
        default=GENDER_MALE
    )

    def __str__(self):
        return f"<Actor {self.pk}: {self.name}>"
