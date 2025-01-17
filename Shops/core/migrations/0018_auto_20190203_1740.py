# Generated by Django 2.1.2 on 2019-02-03 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20181125_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('jewelry', 'jewelry'), ('trousers', 'trousers'), ('dress-shirt', 'dress-shirt'), ('jeans', 'jeans'), ('loafers', 'loafers'), ('pants', 'pants'), ('briefs', 'briefs'), ('bras', 'bras'), ('sneakers', 'sneakers'), ('t-shirt', 't-shirt'), ('formal-wear', 'formal-wear'), ('belts', 'belts'), ('bombers', 'bombers'), ('gloves', 'gloves'), ('socks', 'socks'), ('boxers', 'boxers'), ('joggers', 'joggers'), ('jackets', 'jackets'), ('wallets', 'wallets'), ('cardigans', 'cardigans'), ('backpacks', 'backpacks'), ('thongs', 'thongs'), ('eyewear', 'eyewear'), ('long-sleeves', 'long-sleeves'), ('shorts', 'shorts'), ('scarves', 'scarves'), ('suits', 'suits'), ('turtlenecks', 'turtlenecks'), ('sweatpants', 'sweatpants'), ('polo', 'polo'), ('hats', 'hats'), ('corsets-and-bodysuits', 'corsets-and-bodysuits'), ('vests', 'vests'), ('blazers', 'blazers'), ('sweatshirts', 'sweatshirts'), ('other', 'other'), ('Hoodies-and-Zipups', 'Hoodies-and-Zipups'), ('coats', 'coats'), ('crewnecks', 'crewnecks'), ('dress-pants', 'dress-pants'), ('tank-tops', 'tank-tops')], max_length=300, null=True),
        ),
    ]
