# This file is part of the product_pack module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import product

def register():
    Pool.register(
        product.ProductPack,
        product.Template,
        product.Product,
        module='product_pack', type_='model')
