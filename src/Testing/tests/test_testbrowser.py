##############################################################################
#
# Copyright (c) 2004, 2005 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tests for the testbrowser module.
"""

from AccessControl.Permissions import view
from six.moves.urllib.error import HTTPError

from OFS.SimpleItem import Item
from Testing.testbrowser import Browser
from Testing.ZopeTestCase import (
    FunctionalTestCase,
    user_name,
    user_password,
)


class CookieStub(Item):
    """This is a cookie stub."""

    def __call__(self, REQUEST):
        REQUEST.RESPONSE.setCookie('evil', 'cookie')
        return 'Stub'


class ExceptionStub(Item):
    """This is a stub, raising an exception."""

    def __call__(self, REQUEST):
        raise ValueError('dummy')


class TestTestbrowser(FunctionalTestCase):

    def test_auth(self):
        # Based on Testing.ZopeTestCase.testFunctional
        basic_auth = '%s:%s' % (user_name, user_password)
        self.folder.addDTMLDocument('secret_html', file='secret')
        self.folder.secret_html.manage_permission(view, ['Owner'])
        path = '/' + self.folder.absolute_url(1) + '/secret_html'

        # Test direct publishing
        response = self.publish(path + '/secret_html')
        self.assertEqual(response.getStatus(), 401)
        response = self.publish(path + '/secret_html', basic_auth)
        self.assertEqual(response.getStatus(), 200)
        self.assertEqual(response.getBody(), 'secret')

        # Test browser
        url = 'http://localhost' + path
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.open(url)
        self.assertTrue(browser.headers['status'].startswith('401'))

        browser.addHeader('Authorization', 'Basic ' + basic_auth)
        browser.open(url)
        self.assertTrue(browser.headers['status'].startswith('200'))
        self.assertEqual(browser.contents, 'secret')

    def test_cookies(self):
        # We want to make sure that our testbrowser correctly
        # understands cookies.
        self.folder._setObject('stub', CookieStub())

        # Test direct publishing
        response = self.publish('/test_folder_1_/stub')
        self.assertEqual(response.getCookie('evil')['value'], 'cookie')

        browser = Browser()
        browser.open('http://localhost/test_folder_1_/stub')
        self.assertEqual(browser.cookies.get('evil'), '"cookie"')

    def test_handle_errors_true(self):
        self.folder._setObject('stub', ExceptionStub())
        browser = Browser()
        with self.assertRaises(HTTPError):
            browser.open('http://localhost/test_folder_1_/stub')
        self.assertTrue(browser.headers['status'].startswith('500'))

        with self.assertRaises(HTTPError):
            browser.open('http://localhost/nothing-is-here')
        self.assertTrue(browser.headers['status'].startswith('404'))

    def test_handle_errors_false(self):
        self.folder._setObject('stub', ExceptionStub())
        browser = Browser()
        browser.handleErrors = False

        # Custom exceptions get through
        with self.assertRaises(ValueError):
            browser.open('http://localhost/test_folder_1_/stub')
        self.assertTrue(browser.contents is None)

        # HTTPException subclasses are handled
        with self.assertRaises(HTTPError):
            browser.open('http://localhost/nothing-is-here')
        self.assertTrue(browser.headers['status'].startswith('404'))

    def test_raise_http_errors_false(self):
        self.folder._setObject('stub', ExceptionStub())
        browser = Browser()
        browser.raiseHttpErrors = False

        browser.open('http://localhost/test_folder_1_/stub')
        self.assertTrue(browser.headers['status'].startswith('500'))

        browser.open('http://localhost/nothing-is-here')
        self.assertTrue(browser.headers['status'].startswith('404'))

    def test_neither_raise_nor_handle_errors(self):
        self.folder._setObject('stub', ExceptionStub())
        browser = Browser()
        browser.handleErrors = False
        browser.raiseHttpErrors = False

        # Custom exceptions get through
        with self.assertRaises(ValueError):
            browser.open('http://localhost/test_folder_1_/stub')
        self.assertTrue(browser.contents is None)

        # HTTPException subclasses are handled
        browser.open('http://localhost/nothing-is-here')
        self.assertTrue(browser.headers['status'].startswith('404'))

    def test_headers_camel_case(self):
        # The Zope2 response mungs headers so they come out
        # in camel case. We should do the same.
        self.folder._setObject('stub', CookieStub())

        browser = Browser()
        browser.open('http://localhost/test_folder_1_/stub')
        header_text = str(browser.headers)
        self.assertTrue('Content-Length: ' in header_text)
        self.assertTrue('Content-Type: ' in header_text)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTestbrowser))
    return suite
