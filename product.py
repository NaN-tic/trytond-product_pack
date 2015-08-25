# This file is part of the product_pack module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta


__all__ = ['ProductPack', 'Template']
__metaclass__ = PoolMeta


class ProductPack(ModelSQL, ModelView):
    'Product Pack'
    __name__ = 'product.pack'


    name = fields.Char('Name', select=True, required=True, translate=True)
    product = fields.Many2One('product.template', 'Product',
        ondelete='CASCADE', required=True)
    sequence = fields.Integer('Sequence',
        help='Gives the sequence order when displaying a list of packaging.')
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
    note = fields.Text('Description')
    uom = fields.Function(fields.Many2One('product.uom', 'Unit'),
        'get_product_uom')

    @classmethod
    def __setup__(cls):
        super(ProductPack, cls).__setup__()
        cls._order = [('product', 'ASC'), ('sequence', 'ASC')]

    @staticmethod
    def order_sequence(tables):
        table, _ = tables[None]
        return [table.sequence == None, table.sequence]

    @staticmethod
    def default_sequence():
        return 1

    def get_product_uom(self, name=None):
        if not self.product:
            return
        return self.product.default_uom.id

    @fields.depends('weight', 'layers', 'packages_layer',
        'pallet_weight')
    def on_change_with_total_packaging_weight(self, name=None):
        if (not self.weight or not self.layers or not self.packages_layer
                or not self.pallet_weight):
            return
        return (self.weight * self.layers * self.packages_layer
            + self.pallet_weight)


class Template:
    __name__ = 'product.template'
    packagings = fields.One2Many('product.pack', 'product', 'Packagings')
