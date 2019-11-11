# This file is part of the product_pack module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from sql import Null
from trytond.model import ModelView, ModelSQL, fields, Check
from trytond.pool import PoolMeta
from trytond.pyson import Eval


__all__ = ['ProductPack', 'Template']


class ProductPack(ModelSQL, ModelView):
    'Product Pack'
    __name__ = 'product.pack'

    name = fields.Char('Name', select=True, required=True, translate=True)
    product = fields.Many2One('product.template', 'Product',
        ondelete='CASCADE', required=True)
    sequence = fields.Integer('Sequence',
        help='Gives the sequence order when displaying a list of packaging.')
    qty = fields.Float('Quantity by Package',
        digits=(16, Eval('uom_digits', 2)), depends=['uom_digits'],
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
        'on_change_with_uom')
    uom_digits = fields.Function(fields.Integer('Unit Digits'),
        'on_change_with_uom_digits')

    @classmethod
    def __setup__(cls):
        super(ProductPack, cls).__setup__()
        cls._order = [('product', 'ASC'), ('sequence', 'ASC')]
        t = cls.__table__()
        cls._sql_constraints += [
            ('check_product_pack_qty_pos',
                Check(t, (t.qty == Null) | (t.qty >= '0')),
                'Quantity by Package of Package must be positive.'),
            ]

    def get_rec_name(self, name=None):
        rec_name = self.name
        if self.qty:
            rec_name = '%s (%s %s)' % (rec_name, self.qty, self.uom.rec_name)
        return rec_name

    @staticmethod
    def order_sequence(tables):
        table, _ = tables[None]
        return [table.sequence == None, table.sequence]

    @staticmethod
    def default_sequence():
        return 1

    @fields.depends('product', '_parent_product.default_uom')
    def on_change_with_uom(self, name=None):
        if self.product:
            return self.product.default_uom.id
        return

    @fields.depends('uom')
    def on_change_with_uom_digits(self, name=None):
        if self.uom:
            return self.uom.digits
        return 2

    @fields.depends('weight', 'layers', 'packages_layer',
        'pallet_weight')
    def on_change_with_total_packaging_weight(self, name=None):
        if (not self.weight or not self.layers or not self.packages_layer
                or not self.pallet_weight):
            return
        return (self.weight * self.layers * self.packages_layer
            + self.pallet_weight)


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'
    packagings = fields.One2Many('product.pack', 'product', 'Packagings')
