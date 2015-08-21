# This file is part of the product_pack module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta


__all__ = ['PackagingType', 'ProductPack', 'ProductCode', 'Template']
__metaclass__ = PoolMeta


class PackagingType(ModelSQL, ModelView):
    'Packaging Type'
    __name__ = "product.packaging.type"
    name = fields.Char('Name', select=True, required=True, translate=True)
    type = fields.Selection([
            ('unit', 'Unit'),
            ('pack', 'Pack'),
            ('box', 'Box'),
            ('pallet', 'Pallet')
            ], 'Type', required=True)


class ProductPack(ModelSQL, ModelView):
    'Product Pack'
    __name__ = 'product.pack'
    _rec_name = 'packaging_type'
    product = fields.Many2One('product.template', 'Product',
        ondelete='CASCADE')
    sequence = fields.Integer('Sequence',
        help='Gives the sequence order when displaying a list of packaging.')
    packaging_type = fields.Many2One('product.packaging.type',
        'Type of Packaging', required=True)
    qty = fields.Float('Quantity by Package',
        help='The total number of products you can put by packaging.')
    weight = fields.Float('Empty Packaging Weight')
    height = fields.Float('Height')
    width = fields.Float('Width')
    length = fields.Float('Length')
    packages_layer = fields.Integer('Packagings by layer')
    layers = fields.Integer('Number of Layers',
        help='The number of layers in a pallet.')
    pallet_weight = fields.Float('Pallet Weight')
    total_packaging_weight = fields.Float('Total Packaging Weight',
        help='The weight of packagings for a full pallet (included pallet '
        'weight.')
    codes = fields.One2Many('product.code', 'product_pack', 'Codes')
    note = fields.Text('Description')

    def get_rec_name(self, name):
        return self.packaging_type.name

    @staticmethod
    def default_sequence():
        return 1

    @staticmethod
    def default_packaging_type():
        pool = Pool()
        PackagingType = pool.get('product.packaging.type')
        packaging_types = PackagingType.search([], limit=1)
        return packaging_types[0].id if packaging_types else None

    @fields.depends('weight', 'layers', 'packages_layer',
        'pallet_weight')
    def on_change_with_total_packaging_weight(self, name=None):
        if (not self.weight or not self.layers or not self.packages_layer
                or not self.pallet_weight):
            return
        return (self.weight * self.layers * self.packages_layer
            + self.pallet_weight)


class ProductCode:
    __name__ = 'product.code'
    product_pack = fields.Many2One('product.pack', 'Packaging')

    @classmethod
    def __setup__(cls):
        super(ProductCode, cls).__setup__()
        if 'product_pack' not in cls.number.on_change:
            cls.number.on_change.add('product_pack')
            cls.number.on_change.add('_parent_product_pack.product')
        if not cls.product.states.get('invisible', False):
            cls.product.states['invisible'] = True

    def on_change_number(self):
        super_on_change = getattr(super(ProductCode), 'on_change_number', {})
        res = super_on_change and super_on_change(self)
        res['product'] = (self.product_pack and self.product_pack.product.id
            or None)
        return res


class Template:
    __name__ = 'product.template'
    packagings = fields.One2Many('product.pack', 'product', 'Packagings')
