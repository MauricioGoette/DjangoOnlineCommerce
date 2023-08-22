from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField

# from urllib.request import urlopen
# # from tempfile import NamedTemporaryFile
# from django.core.files.temp import NamedTemporaryFile
# from django.core.files import File

# from django.db.models import signals

# # import os
# # import urllib.request
# # from six.moves import urllib

# from django.db import models
# import urllib.request
# from io import BytesIO
# from django.core.files import File


CATEGORY_CHOICES = (
    ('TE', 'Teclados'),
    ('MO', 'Mouses'),
    ('GA', 'Gabinetes'),
    ('MT', 'Monitores')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


# Default

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):

    # ItemName
    title = models.CharField(max_length=1000)
    # Price
    # price = models.DecimalField(
    #     blank=True, null=True, max_digits=10, decimal_places=2)
    price = models.FloatField(blank=True, null=True)
    discount_price = models.FloatField(blank=True, null=True)
    # Category
    category = models.CharField(max_length=1000)
    label = models.CharField(choices=LABEL_CHOICES,
                             max_length=1, blank=True, null=True)
    # UrlSLug
    slug = models.SlugField()
    # internalID = models.CharField(max_length=1000, primary_key=True)
    # FirstDescription
    description = models.TextField(blank=True, null=True)
    # AditionalInformation
    info = models.TextField(blank=True, null=True)
    # Images
    image = models.ImageField(
        blank=True, null=True, upload_to='items_images', default='/img/noImage.JPG')
    image_url = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    # # def save(self, *args, **kwargs):
    # #     if self.image_url and not self.image:
    # #         response = urllib.request.urlopen(self.image_url)
    # #         image_data = response.read()
    # #         image_name = self.image_url.split("/")[-1]

    # #         temp_image = BytesIO(image_data)
    # #         self.image.save(image_name, File(temp_image), save=False)

    # #     super().save(*args, **kwargs)

    # # Image Url to Imagefield
    # def get_remote_image(self, *args, **kwargs):
    #     if self.image_url:
    #         img_temp = NamedTemporaryFile(delete=True)
    #         img_temp.write(urlopen(self.image_url).read())
    #         img_temp.flush()
    #         self.image.save(f"image_{self.pk}", File(img_temp))
    #     super(Item, self).save(*args, **kwargs)
    #     return

    # # def get_remote_image(self):
    # #     """Store image locally if we have a URL"""

    # #     if self.image_url and not self.image:
    # #         result = urllib.request.urlretrieve(self.image_url)
    # #         self.image.save(
    # #                 os.path.basename(self.image_url),
    # #                 File(open(result[0], 'rb'))
    # #                 )
    # #         super(Item, self).save()
    # #         return

    # # def save(self, *args, **kwargs):
    # #     if self.image_url:
    # #         file_save_dir = self.upload_path
    # #         filename = urlparse(self.image_url).path.split('/')[-1]
    # #         urllib.request.urlretrieve(self.image_url, os.path.join(file_save_dir, filename))
    # #         self.image = os.path.join(file_save_dir, filename)
    # #         self.image_url = ''
    # #     super(Item, self).save()

    # # signals.post_save.connect(get_remote_image)

    # #Default Image
    # def default_image(self, *args, **kwargs):
    #     if not self.image:  #here
    #         self.image = '/img/noImage.JPG'
    #     super(Item, self).save(*args, **kwargs)
    #     return


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    images = models.ImageField()

    def __str__(self):
        return self.images.url


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
# post_save.connect(Item.get_remote_image, sender=settings.AUTH_USER_MODEL)
