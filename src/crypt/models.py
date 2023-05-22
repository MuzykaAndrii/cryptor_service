from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Picture(models.Model):
    SINUSOIDAL = "sinusoidal"
    CIRCULAR = "sircular"
    TRANSITION = "transition"
    DRAW_METHODTS = (
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

    name = models.CharField(
        max_length=20,
        default="",
        verbose_name="Picture name",
    )
    width = models.PositiveSmallIntegerField(
        verbose_name="Picture width",
        default=255,
        validators=[MinValueValidator(100), MaxValueValidator(3000)],
    )
    height = models.PositiveSmallIntegerField(
        verbose_name="Picture height",
        default=255,
        validators=[MinValueValidator(100), MaxValueValidator(3000)],
    )
    draw_method = models.CharField(
        max_length=50,
        choices=DRAW_METHODTS,
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
    last_action_result = models.TextField(
        null=True,
        blank=True,
        verbose_name="Text of last action (encrypted or decrypted)",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date of creating",
        db_index=True,
    )
