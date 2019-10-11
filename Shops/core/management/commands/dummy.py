from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
# from infcore.models import *
from core.models import *
from faker import Faker
import random
import os

class Command(BaseCommand):

    def handle(self, *args, **options):

        images = ['https://images.asos-media.com/products/nike-swoosh-t-shirt-in-oatmeal/12493492-1-oatmeal?$n_320w$&wid=317&fit=constrain',
                  'https://images.asos-media.com/products/new-look-miami-print-long-sleeve-sweat-in-grey-marl/13989959-1-grey?$n_320w$&wid=317&fit=constrain',
                  'https://images.asos-media.com/products/weekday-evan-key-hook-in-silver/13894790-1-silver?$n_320w$&wid=317&fit=constrain'
                  ,'https://images.asos-media.com/products/weekday-cian-key-chain-in-silver/13894678-1-silver?$n_320w$&wid=317&fit=constrain',
                  'https://images.asos-media.com/products/typo-4-luggage-packing-cells-in-pink/13844073-1-multi?$n_320w$&wid=317&fit=constrain'

                  ,'https://images.asos-media.com/products/reclaimed-vintage-unisex-floral-shirt-co-ord/13676671-1-multi?$n_320w$&wid=317&fit=constrain',
                  'https://images.asos-media.com/products/reclaimed-vintage-unisex-military-festival-jacket-with-contrast-pocket-details/11829695-1-khaki?$n_320w$&wid=317&fit=constrain',
                  'https://images.asos-media.com/products/reclaimed-vintage-unisex-t-shirt-with-branding/11820400-1-black?$n_320w$&wid=317&fit=constrain',
                  'https://images.asos-media.com/products/reclaimed-vintage-oversized-t-shirt-with-sun-and-moon-print/12071526-1-black?$n_320w$&wid=317&fit=constrain',
                  'https://images.asos-media.com/products/reclaimed-vintage-space-print-tshirt/12432197-1-black?$n_320w$&wid=317&fit=constrain',
                  'https://images.asos-media.com/products/reclaimed-vintage-unisex-gilet-in-black-with-neon-pullers/12436096-1-black?$n_320w$&wid=317&fit=constrain',
                  'https://images.asos-media.com/products/reclaimed-vintage-inspired-leather-biker-jacket-in-black/3955462-1-black?$n_320w$&wid=317&fit=constrain',
                  'https://images.asos-media.com/products/reclaimed-vintage-digital-butterfly-print-t-shirt-in-black/12757968-1-black?$n_320w$&wid=317&fit=constrain',

                  ]



        fake = Faker()

        print('Importing Product Types.\n')
        for i in range(200):
            ProductType.objects.create(name=fake.company()).save()

        print('Importing Sub Categories.\n')
        for ptype in ProductType.objects.all():
            SubCategory.objects.create(big_type=ptype,name=fake.name()).save()

        print('Importing Map Sub Categories.\n')
        for _ in SubCategory.objects.all():
            MapSubcategory.objects.create(name=fake.name(),subcategory=_).save()

        print('Importing Links.\n')
        for i in range(200):

            l_type = random.choice(LINK_TYPES)[0]
            s_name = random.choice(Link.SHOP_NAME)[0]
            x = random.choice(Link.SEX)[0]
            try:
                Link.objects.create(url=random.choice(images),link_type=l_type
                                ,shop_name=s_name,sex=x).save()
            except:
                pass

        print('Importing Products.\n')
        for i in range(200):
            randm = str(os.urandom(23), 'utf-8', errors='replace')
            list_price = float(random.choice(list(map(ord, randm))))
            link = random.choice(Link.objects.all())
            category = random.choice(SubCategory.objects.all())
            product_type = random.choice(PRODUCT_TYPES)[0]
            Product.objects.create(product_type=product_type,category=category
                                   ,url_img=random.choice(images),
                                   url_original=random.choice(images),
                                   list_price=list_price,discount_price=list_price,
                                   name=fake.name(),shop_name=random.choice(Link.SHOP_NAME)[0],
                                   link= link
                                   ).save()
