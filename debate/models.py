from django.db import models

Target_exam = [
    ('Engineering', (
            ('jee-mains', 'JEE-Main'),
            ('jee-Adv', 'JEE Advanced'),
            ('bits', 'Bits'),
        )
    ),
    ('Medical', (
            ('neet', 'NEET'),
            ('Aiims', 'AIIMS'),
        )
    ),
    ('other', 'Other'),
]

class Debate(models.Model):
    title = models.CharField(max_length=200)
    pros =models.JSONField(default=dict, blank=True, null=True)
    cons =models.JSONField(default=dict, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title
