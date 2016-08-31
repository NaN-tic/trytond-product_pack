#!/usr/bin/env python
# This file is part of the product_pack module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.tests.test_tryton import ModuleTestCase
import trytond.tests.test_tryton
import unittest


class ProductPackTestCase(ModuleTestCase):
    'Test Product Pack module'
    module = 'product_pack'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductPackTestCase))
    return suite
