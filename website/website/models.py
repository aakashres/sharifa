from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        super().save()


class SiteConfig(Timestampable):
    key = models.CharField(max_length=255)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.key


MEMBERSHIP_CHOICES = None
try:
    MEMBERSHIP_CHOICES_LIST = []
    membershipObj = SiteConfig.objects.filter(key='memberships').first()
    if membershipObj:
        membershipValue = membershipObj.value.split(';')
        for index, membershipTitle in enumerate(membershipValue):
            indMembershipDetailObj = SiteConfig.objects.filter(
                key=membershipTitle + 'membership').first()
            tempTuple = (index, membershipTitle)
            MEMBERSHIP_CHOICES_LIST.append(tempTuple)
        MEMBERSHIP_CHOICES = tuple(MEMBERSHIP_CHOICES_LIST)
except:
    MEMBERSHIP_CHOICES = ()


class Membership(Timestampable):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    type = models.PositiveIntegerField(choices=MEMBERSHIP_CHOICES)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username + "_" + self.get_type_display()


def upload_location(instance, filename):
    return "%s/%s/%s" % ('users', instance.user.username, filename)


class UserProfile(Timestampable):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField()
    photo = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True)

    def getMembership(self):
        membership = Membership.objects.filter(
            user=self.user, deleted_at=None).exclude(type=0)
        return membership

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class RequestedProduct(Timestampable):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    link = models.URLField()
    remarks = models.TextField()
    number = models.PositiveIntegerField()
    quoted = models.BooleanField(default=False)
    membership = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ItemCategory(Timestampable):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    harmony_code = models.CharField(max_length=255, null=True)
    popularity = models.PositiveSmallIntegerField(default=0)
    percent_rate = models.FloatField(default=0)
    flat_rate = models.FloatField(default=0)
    volume_rate = models.FloatField(default=0)
    ecs = models.FloatField(default=0)
    vat = models.FloatField(default=13)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Item category'
        verbose_name_plural = 'Item categories'


def uploadProductPhoto(instance, filename):
    return "%s/%s/%s" % ('product', instance.title, filename)


class Product(Timestampable):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    photo = models.ImageField(
        upload_to=uploadProductPhoto, null=True, blank=True)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    approx_taxes = models.FloatField(default=0)
    domestic_shipping = models.FloatField(default=0)
    height = models.FloatField(default=0)
    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    link = models.URLField()

    def __str__(self):
        return self.title


class Quotation(Timestampable):
    requested_product = models.OneToOneField(
        RequestedProduct, related_name='quotation', on_delete=models.CASCADE)
    quoted_by = models.OneToOneField(
        User, related_name='quoter', null=True, blank=True)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    approx_taxes = models.FloatField(default=0)
    domestic_shipping = models.FloatField(default=0)
    height = models.FloatField(default=0)
    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    weight = models.FloatField(default=0)

    def __str__(self):
        return self.requested_product.title


class Page(Timestampable):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


def uploadShopLogo(instance, filename):
    return "%s/%s/%s" % ('shop', instance.name, filename)


class Shop(Timestampable):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=uploadShopLogo,
                             null=True,
                             blank=True)
    link = models.URLField(unique=True)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# sales_tax -> approx_taxes
