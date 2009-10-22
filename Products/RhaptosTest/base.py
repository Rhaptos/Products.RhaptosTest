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

from Products.CMFPlone.tests import PloneTestCase
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase.layer import PloneSite
from Testing import ZopeTestCase


# PRODUCTS_TO_LOAD_ZCML is a list of tuples representing ZCML files to load,
# and which products to load them from.  PRODUCTS_TO_INSTALL is a list
# representing products to install.  A subtle difference in these lists is that
# in PRODUCTS_TO_LOAD_ZCML, products are specified as actual modules, whereas
# in PRODUCTS_TO_INSTALL, products are specified as strings.
#
#   import Products.RhaptosBugTrackingTool
#   from Products.RhaptosTest import base
#
#   base.PRODUCTS_TO_LOAD_ZCML = [('configure.zcml', Products.RhaptosBugTrackingTool),]
#   base.PRODUCTS_TO_INSTALL = ['RhaptosBugTrackingTool']
#
#   class TestRhaptosBugTrackingTool(base.RhaptosTestCase):
#       def test_pass(self):
#           pass

PRODUCTS_TO_LOAD_ZCML = []
PRODUCTS_TO_INSTALL = []


class RhaptosTestCase(PloneTestCase.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            for zcml_file, product in PRODUCTS_TO_LOAD_ZCML:
                zcml.load_config(zcml_file, product)
            for product in PRODUCTS_TO_INSTALL:
                ZopeTestCase.installProduct(product)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass
