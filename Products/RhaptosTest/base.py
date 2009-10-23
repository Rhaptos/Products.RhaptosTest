#------------------------------------------------------------------------------#
#   base.py                                                                    #
#                                                                              #
#       Authors:                                                               #
#       Rajiv Bakulesh Shah <raj@enfoldsystems.com>                            #
#                                                                              #
#           Copyright (c) 2009, Enfold Systems, Inc.                           #
#           All rights reserved.                                               #
#                                                                              #
#               This software is licensed under the Terms and Conditions       #
#               contained within the "LICENSE.txt" file that accompanied       #
#               this software.  Any inquiries concerning the scope or          #
#               enforceability of the license should be addressed to:          #
#                                                                              #
#                   Enfold Systems, Inc.                                       #
#                   4617 Montrose Blvd., Suite C215                            #
#                   Houston, Texas 77006 USA                                   #
#                   p. +1 713.942.2377 | f. +1 832.201.8856                    #
#                   www.enfoldsystems.com                                      #
#                   info@enfoldsystems.com                                     #
#------------------------------------------------------------------------------#
"""Base class from which other Rhaptos unit test classes inherit.
$Id: $
"""


# Subtle: Monkey patch zope.testing by importing this module:
import patch_zope_testing

from Products.CMFPlone.tests.PloneTestCase import PloneTestCase
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase.layer import PloneSite
from Testing import ZopeTestCase


class RhaptosTestCase(PloneTestCase):

    # products_to_load_zcml is a list of tuples representing ZCML files to load,
    # and which products to load them from.  products_to_install is a list
    # representing products to install.  A subtle difference in these lists is that
    # in products_to_load_zcml, products are specified as actual modules, whereas
    # in products_to_install, products are specified as strings.
    products_to_load_zcml = []
    products_to_install = []

    def setUp(self):
        fiveconfigure.debug_mode = True
        for zcml_file, product in self.products_to_load_zcml:
            zcml.load_config(zcml_file, product)
        for product in self.products_to_install:
            ZopeTestCase.installProduct(product)
        fiveconfigure.debug_mode = False

    def tearDown(self):
        pass
