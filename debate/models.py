from django.db import models
from account.models import Account

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
    tags = models.CharField(max_length=50, null=True, blank=True)
    # pros =models.JSONField(default=dict, blank=True, null=True)
    # cons =models.JSONField(default=dict, blank=True, null=True)
    # comments = models.JSONField(default=dict, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)
    like = models.ManyToManyField(Account, null=True,blank=True)

    def _str_(self):
        return self.title

class Pros(models.Model):
    debate_pros = models.ForeignKey(Debate, related_name='pros',on_delete=models.CASCADE)
    pros_tags=models.CharField(max_length=50,null=True,blank=True)
    pros = models.TextField(null=True,blank=True)
    comment = models.JSONField(default=list, blank=True, null=True)
    proslike=models.ManyToManyField(Account, null=True,blank=True)

class Cons(models.Model):
    debate_cons = models.ForeignKey(Debate, related_name='cons',on_delete=models.CASCADE)
    cons_tags = models.CharField(max_length=50, null=True, blank=True)
    cons = models.TextField(null=True,blank=True)
    comment = models.JSONField(default=list, blank=True, null=True)
    conslike = models.ManyToManyField(Account, null=True,blank=True)