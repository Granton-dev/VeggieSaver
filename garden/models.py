from django.db import models
from django.contrib.auth.models import User


class Vegetable(models.Model):
    HEALTH_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vegetables')
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True)
    planted_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='vegetables/', blank=True, null=True)
    ai_analysis = models.TextField(blank=True)
    health_status = models.CharField(max_length=20, choices=HEALTH_CHOICES, default='good')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        ordering = ['-created_at']


class ScanResult(models.Model):
    """Stores every AI scan result for a vegetable photo."""

    FRESHNESS_CHOICES = [
        ('fresh', 'Fresh'),
        ('good', 'Good — Use Within Days'),
        ('caution', 'Use Today'),
        ('spoiling', 'Spoiling'),
        ('spoiled', 'Spoiled — Discard'),
    ]

    CONDITION_CHOICES = [
        ('healthy', 'Healthy'),
        ('wilting', 'Wilting'),
        ('mouldy', 'Mouldy'),
        ('bruised', 'Bruised'),
        ('discoloured', 'Discoloured'),
        ('pest_damage', 'Pest Damage'),
        ('disease', 'Disease Detected'),
        ('unknown', 'Unknown'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scans')
    vegetable = models.ForeignKey(
        Vegetable, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='scans'
    )

    # Photo
    photo = models.ImageField(upload_to='scans/%Y/%m/%d/')
    scanned_at = models.DateTimeField(auto_now_add=True)

    # AI Identification
    identified_vegetable = models.CharField(max_length=100, blank=True)
    confidence_score = models.FloatField(default=0.0)  # 0.0 - 1.0

    # Freshness
    freshness_status = models.CharField(
        max_length=20, choices=FRESHNESS_CHOICES, default='fresh'
    )
    freshness_score = models.IntegerField(default=100)  # 0-100

    # Condition
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default='healthy'
    )

    # Detailed AI output
    full_analysis = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    meal_suggestions = models.TextField(blank=True)
    storage_tips = models.TextField(blank=True)
    days_remaining = models.IntegerField(null=True, blank=True)

    # Raw JSON from AI
    raw_ai_response = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-scanned_at']

    def __str__(self):
        return f"{self.identified_vegetable} scan — {self.freshness_status} ({self.user.username})"

    @property
    def freshness_color(self):
        colors = {
            'fresh': '#27ae60',
            'good': '#2ecc71',
            'caution': '#f39c12',
            'spoiling': '#e67e22',
            'spoiled': '#e74c3c',
        }
        return colors.get(self.freshness_status, '#999')

    @property
    def freshness_emoji(self):
        emojis = {
            'fresh': '✅',
            'good': '🟢',
            'caution': '🟡',
            'spoiling': '🟠',
            'spoiled': '🔴',
        }
        return emojis.get(self.freshness_status, '❓')


class WasteLog(models.Model):
    REASON_CHOICES = [
        ('disease', 'Disease'),
        ('pest', 'Pest Damage'),
        ('overripe', 'Overripe'),
        ('weather', 'Weather Damage'),
        ('poor_growth', 'Poor Growth'),
        ('spoiled', 'Spoiled'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waste_logs')
    vegetable = models.ForeignKey(
        Vegetable, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='waste_logs'
    )
    scan = models.ForeignKey(
        ScanResult, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='waste_logs'
    )
    vegetable_name = models.CharField(max_length=100)
    quantity_wasted = models.PositiveIntegerField()
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    notes = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vegetable_name} waste — {self.date}"

    class Meta:
        ordering = ['-date']


class GardenTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    is_ai_generated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']