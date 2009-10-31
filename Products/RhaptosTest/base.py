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
"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of Plone's
products are loaded, and a Plone site will be created. This happens at module
level, which makes it faster to run each test, but slows down test runner
startup.

I adapted this file from Martin Aspeli's excellent documentation here:
http://plone.org/documentation/tutorial/testing/writing-a-plonetestcase-unit-integration-test

$Id: $
"""


# Subtle: Monkey patch zope.testing by importing this module:
import patch_zope_testing

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase as ztc

from config import products_to_load_zcml
from config import products_to_install
from config import products_extension_profiles


#
# When ZopeTestCase configures Zope, it will *not* auto-load products in 
# Products/. Instead, we have to use a statement such as:
# 
#   ztc.installProduct('SimpleAttachment')
# 
# This does *not* apply to products in eggs and Python packages (i.e. not in
# the Products.*) namespace. For that, see below.
# 
# All of Plone's products are already set up by PloneTestCase.
# 


@onsetup
def setup_product():
    """Set up the package and its dependencies.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer. We could have created our
    own layer, but this is the easiest way for Plone integration tests.
    """
    
    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.

    fiveconfigure.debug_mode = True
    for zcml_file, product in products_to_load_zcml:
        zcml.load_config(zcml_file, product)
    fiveconfigure.debug_mode = False
    
    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML. Thus, we do it here. Note the use of installPackage() instead
    # of installProduct().
    # 
    # This is *only* necessary for packages outside the Products.* namespace
    # which are also declared as Zope 2 products, using 
    # <five:registerPackage /> in ZCML.

    # We may also need to load dependencies, e.g.:
    # 
    #   ztc.installPackage('borg.localrole')
    # 

    for product in products_to_install:
        ztc.installProduct(product)


# The order here is important: We first call the (deferred) function which
# installs the products we need for this product. Then, we let PloneTestCase 
# set up this product on installation.

setup_product()
ptc.setupPloneSite(products=products_to_install,
                   extension_profiles=products_extension_profiles)


class RhaptosTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit 
    test cases.
    """
    pass


class RhaptosFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
    pass
