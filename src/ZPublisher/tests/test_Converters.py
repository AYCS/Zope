##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import sys
import unittest

if sys.version_info >= (3, ):
    unicode = str


class ConvertersTests(unittest.TestCase):

    def test_field2string_with_string(self):
        from ZPublisher.Converters import field2string
        to_convert = 'to_convert'
        self.assertEqual(field2string(to_convert), to_convert)

    def test_field2string_with_unicode_default_encoding(self):
        from ZPublisher.Converters import field2string
        to_convert = u'to_convert'
        self.assertEqual(field2string(to_convert),
                         to_convert.encode('utf-8'))

    def test_field2string_with_filelike_object(self):
        from ZPublisher.Converters import field2string
        to_convert = 'to_convert'

        class Filelike:
            def read(self):
                return to_convert
        self.assertEqual(field2string(Filelike()), to_convert)

    def test_field2lines_with_list(self):
        from ZPublisher.Converters import field2lines
        to_convert = ['one', 'two']
        self.assertEqual(field2lines(to_convert), to_convert)

    def test_field2lines_with_tuple(self):
        from ZPublisher.Converters import field2lines
        to_convert = ('one', 'two')
        self.assertEqual(field2lines(to_convert), list(to_convert))

    def test_field2lines_with_empty_string(self):
        from ZPublisher.Converters import field2lines
        to_convert = ''
        self.assertEqual(field2lines(to_convert), [])

    def test_field2lines_with_string_no_newlines(self):
        from ZPublisher.Converters import field2lines
        to_convert = 'abc def ghi'
        self.assertEqual(field2lines(to_convert), [to_convert])

    def test_field2lines_with_string_with_newlines(self):
        from ZPublisher.Converters import field2lines
        to_convert = 'abc\ndef\nghi'
        self.assertEqual(field2lines(to_convert), to_convert.splitlines())

    def test_field2ulines_with_list(self):
        from ZPublisher.Converters import field2ulines
        to_convert = [u'one', 'two']
        self.assertEqual(field2ulines(to_convert),
                         [unicode(x) for x in to_convert])

    def test_field2ulines_with_tuple(self):
        from ZPublisher.Converters import field2ulines
        to_convert = (u'one', 'two')
        self.assertEqual(field2ulines(to_convert),
                         [unicode(x) for x in to_convert])

    def test_field2ulines_with_empty_string(self):
        from ZPublisher.Converters import field2ulines
        to_convert = ''
        self.assertEqual(field2ulines(to_convert), [])

    def test_field2ulines_with_string_no_newlines(self):
        from ZPublisher.Converters import field2ulines
        to_convert = u'abc def ghi'
        self.assertEqual(field2ulines(to_convert), [to_convert])

    def test_field2ulines_with_string_with_newlines(self):
        from ZPublisher.Converters import field2ulines
        to_convert = u'abc\ndef\nghi'
        self.assertEqual(field2ulines(to_convert), to_convert.splitlines())
