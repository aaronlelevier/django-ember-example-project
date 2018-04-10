from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Avg, Sum

from review.models import RawReview, Review
from util.models import AbstractModel


class AbstractCustomer(AbstractModel):
    name = models.CharField(max_length=25)
    image = models.URLField()
    phone_number = models.CharField(max_length=12)

    class Meta:
        abstract = True


class SitterManager(models.Manager):

    def populate(self):
        for r in RawReview.objects.all():
            try:
                user = User.objects.get(username=r.sitter_email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=r.sitter_email, email=r.sitter_email)

            try:
                self.get(user=user)
            except Sitter.DoesNotExist:
                self.create(user=user, name=r.sitter, image=r.sitter_image)

    def set_scores(self):
        sitters = {}
        for r in (Review.objects.values('sitter__name', 'sitter__user__username')
                                .annotate(stays=Count('rating'))
                                .annotate(rating=Avg('rating'))):
            sitters[r['sitter__user__username']] = r

        for s in self.all():
            setattr(s, 'stays', sitters[s.user.username]['stays'])
            setattr(s, 'ratings_score', sitters[s.user.username]['rating'])
            setattr(s, 'sitter_score', s.calc_sitter_score())
            setattr(s, 'overall_score', s.calc_overall_score())
            s.save()


class Sitter(AbstractCustomer):
    # keys
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # fields
    stays = models.PositiveIntegerField(default=0)
    ratings_score = models.FloatField(default=0)
    sitter_score = models.FloatField(default=0)
    overall_score = models.FloatField(default=0)

    objects = SitterManager()

    def calc_sitter_score(self):
        return (sum(1 for let in {s for s in self.name.lower()} if let.isalpha()) / 26)*5

    def calc_overall_score(self):
        if self.stays == 0:
            return self.sitter_score
        elif self.stays >= 10:
            return self.ratings_score
        return self.stays * .1 * self.ratings_score + (self.sitter_score * (1 - (self.stays * .1)))


class OwnerManager(models.Manager):
    
    def populate(self):
        for r in RawReview.objects.all():
            try:
                user = User.objects.get(username=r.owner_email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=r.owner_email, email=r.owner_email)

            try:
                self.get(user=user)
            except Owner.DoesNotExist:
                self.create(user=user, name=r.owner, dogs=r.dogs)


class Owner(AbstractCustomer):
    # keys
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # fields
    dogs = models.CharField(max_length=200)

    objects = OwnerManager()
