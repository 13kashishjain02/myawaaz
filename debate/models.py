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
    image = models.ImageField(upload_to= "images", default="images/vegan.jpeg",null=True)
    # pros =models.JSONField(default=dict, blank=True, null=True)
    # cons =models.JSONField(default=dict, blank=True, null=True)
    # comments = models.JSONField(default=dict, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)

    def _str_(self):
        return self.title

class Pros(models.Model):
    debate_pros = models.ForeignKey(Debate, related_name='pros',on_delete=models.CASCADE)
    pros = models.TextField(null=True,blank=True)
    comments = models.JSONField(default=list, blank=True, null=True)

class Cons(models.Model):
    debate_cons = models.ForeignKey(Debate, related_name='cons',on_delete=models.CASCADE)
    cons = models.TextField(null=True,blank=True)
    comments = models.JSONField(default=dict, blank=True, null=True)