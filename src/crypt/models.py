from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Picture(models.Model):
    SINUSOIDAL = "sinusoidal"
    CIRCULAR = "sircular"
    TRANSITION = "transition"

    PAINT_METHODTS = (
        (SINUSOIDAL, "Sinusoidal"),
        (CIRCULAR, "Circular"),
        (TRANSITION, "Transition"),
    )

    ENCRYPTION = "encryption"
    DECRYPTION = "decryption"

    LAST_ACTION = (
        (ENCRYPTION, "Encryption"),
        (DECRYPTION, "Decryption"),
    )

    width = models.PositiveSmallIntegerField(
        verbose_name="Picture width",
        default=255,
        validators=[MinValueValidator(100), MaxValueValidator(100)],
    )
    height = models.PositiveSmallIntegerField(
        verbose_name="Picture height",
        default=255,
        validators=[MinValueValidator(100), MaxValueValidator(100)],
    )
    paint_method = models.CharField(
        max_length=50,
        choices=PAINT_METHODTS,
        default=TRANSITION,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pictures",
        verbose_name="User pictures",
    )
    image = models.ImageField(
        upload_to="images/%Y/%m/%d/",
        blank=False,
        null=False,
        verbose_name="Image",
    )
    last_action = models.CharField(
        max_length=50,
        choices=LAST_ACTION,
        verbose_name="Last action with this picture",
        blank=True,
        null=True,
    )
