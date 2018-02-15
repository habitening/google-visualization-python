"""Test the gviz_api module some more.

These also serve as a regression test.
"""

import datetime
import unittest

import gviz_api

class MoreDataTableTest(unittest.TestCase):
    def setUp(self):
        self.accepted_types = ('string', 'number', 'boolean',
                               'date', 'datetime', 'timeofday')
        """Tuple of string accepted value types."""

    def test_DataTableJSONEncoder(self):
        """Test the JSON encoder."""
        encoder = gviz_api.DataTableJSONEncoder()

        for value in [None, 42, '', []]:
            self.assertRaises(TypeError, encoder.default, value)
        for value, expected in [
            (datetime.datetime(2001, 2, 3, 4, 5, 6),
             'Date(2001,1,3,4,5,6)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 7),
             'Date(2001,1,3,4,5,6,0)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 78),
             'Date(2001,1,3,4,5,6,0)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 789),
             'Date(2001,1,3,4,5,6,0)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 7890),
             'Date(2001,1,3,4,5,6,7)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 78900),
             'Date(2001,1,3,4,5,6,78)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 789000),
             'Date(2001,1,3,4,5,6,789)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16),
             'Date(2011,11,13,14,15,16)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 7),
             'Date(2011,11,13,14,15,16,0)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 78),
             'Date(2011,11,13,14,15,16,0)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 789),
             'Date(2011,11,13,14,15,16,0)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 7890),
             'Date(2011,11,13,14,15,16,7)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 78900),
             'Date(2011,11,13,14,15,16,78)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 789000),
             'Date(2011,11,13,14,15,16,789)'),
            (datetime.date(2001, 2, 3), 'Date(2001,1,3)'),
            (datetime.date(2004, 5, 6), 'Date(2004,4,6)'),
            (datetime.date(2007, 8, 9), 'Date(2007,7,9)'),
            (datetime.date(2010, 11, 12), 'Date(2010,10,12)'),
            (datetime.time(1, 2, 3), [1, 2, 3]),
            (datetime.time(4, 5, 6, 7), [4, 5, 6]),
            (datetime.time(7, 8, 9, 78), [7, 8, 9]),
            (datetime.time(10, 11, 12, 789), [10, 11, 12]),
            (datetime.time(13, 14, 15, 7890), [13, 14, 15]),
            (datetime.time(16, 17, 18, 78900), [16, 17, 18]),
            (datetime.time(19, 20, 21, 789000), [19, 20, 21]),
            (datetime.time(22, 23, 24, 25, None), [22, 23, 24])]:
            self.assertEqual(encoder.default(value), expected)

    def test_CoerceValue(self):
        """Test coercing a single value to the specified type."""
        for value in [None, 42, '', [], 'foobar']:
            self.assertRaises(gviz_api.DataTableException,
                              gviz_api.DataTable.CoerceValue, 42, value)
            self.assertIsNone(gviz_api.DataTable.CoerceValue(None, value))
        for value_type in self.accepted_types:
            for value in [value_type.upper(), value_type.title(),
                          ' ' + value_type, value_type + '    ',
                          ' ' + value_type + ' ']:
                self.assertRaises(gviz_api.DataTableException,
                                  gviz_api.DataTable.CoerceValue,
                                  42, value)
                self.assertRaises(gviz_api.DataTableException,
                                  gviz_api.DataTable.CoerceValue,
                                  (42, 'foobar'), value)
                self.assertRaises(gviz_api.DataTableException,
                                  gviz_api.DataTable.CoerceValue,
                                  (42, 'foobar', {}), value)
                self.assertIsNone(gviz_api.DataTable.CoerceValue(None, value))
            self.assertIsNone(gviz_api.DataTable.CoerceValue(None, value_type))
            self.assertRaises(gviz_api.DataTableException,
                              gviz_api.DataTable.CoerceValue,
                              (42,), value_type)
            self.assertRaises(gviz_api.DataTableException,
                              gviz_api.DataTable.CoerceValue,
                              (1, 2, 3, 4), value_type)
            # Test third element of tuple is not a dict
            self.assertRaises(gviz_api.DataTableException,
                              gviz_api.DataTable.CoerceValue,
                              (1, 2, 3), value_type)
            # Test second element of tuple is not a string
            self.assertRaises(gviz_api.DataTableException,
                              gviz_api.DataTable.CoerceValue,
                              (1, 2), value_type)

        # Test "string"
        value_type = 'string'
        for value, expected in [
            ('', ''),
            ('foobar', 'foobar'),
            (u'fo\u00f6b\u00e4r', u'fo\u00f6b\u00e4r'),
            (42, '42'),
            (3.14, '3.14'),
            (-42, '-42'),
            (-3.14, '-3.14'),
            (True, 'True'),
            (False, 'False'),
            (datetime.date(2001, 2, 3), '2001-02-03'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6), '2001-02-03 04:05:06'),
            (datetime.time(1, 2, 3), '01:02:03')]:
            self.assertEqual(
                gviz_api.DataTable.CoerceValue(value, value_type),
                expected)
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None), value_type),
                (expected, None))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None, {}), value_type),
                (expected, None, {}))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar'), value_type),
                (expected, 'foobar'))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar', {}),
                                               value_type),
                (expected, 'foobar', {}))

        # Test "number"
        value_type = 'number'
        for value in ['', [], 'foobar']:
            self.assertRaises(gviz_api.DataTableException,
                              gviz_api.DataTable.CoerceValue,
                              value, value_type)
        for value in [42, 3.14, -42, -3.14]:
            self.assertEqual(
                gviz_api.DataTable.CoerceValue(value, value_type),
                value)
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None), value_type),
                (value, None))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None, {}), value_type),
                (value, None, {}))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar'), value_type),
                (value, 'foobar'))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar', {}),
                                               value_type),
                (value, 'foobar', {}))

        # Test "boolean"
        value_type = 'boolean'
        for value in [False, 0, '', []]:
            self.assertFalse(gviz_api.DataTable.CoerceValue(value, value_type))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None), value_type),
                (False, None))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None, {}), value_type),
                (False, None, {}))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar'), value_type),
                (False, 'foobar'))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar', {}),
                                               value_type),
                (False, 'foobar', {}))
        for value in [True, 1, 42, 3.14, 'foobar', ['bar', 'baz']]:
            self.assertTrue(gviz_api.DataTable.CoerceValue(value, value_type))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None), value_type),
                (True, None))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None, {}), value_type),
                (True, None, {}))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar'), value_type),
                (True, 'foobar'))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar', {}),
                                               value_type),
                (True, 'foobar', {}))

        # Test "date"
        value_type = 'date'
        for value in [42, '', []]:
            self.assertRaises(gviz_api.DataTableException,
                              gviz_api.DataTable.CoerceValue,
                              value, value_type)
        expected = datetime.date(2001, 2, 3)
        for value in [expected, datetime.datetime(2001, 2, 3, 4, 5, 6)]:
            self.assertEqual(
                gviz_api.DataTable.CoerceValue(value, value_type),
                expected)
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None), value_type),
                (expected, None))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None, {}), value_type),
                (expected, None, {}))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar'), value_type),
                (expected, 'foobar'))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar', {}),
                                               value_type),
                (expected, 'foobar', {}))

        # Test "datetime"
        value_type = 'datetime'
        for value in [42, '', []]:
            self.assertRaises(gviz_api.DataTableException,
                              gviz_api.DataTable.CoerceValue,
                              value, value_type)
        expected = datetime.datetime(2001, 2, 3, 4, 5, 6)
        self.assertEqual(
            gviz_api.DataTable.CoerceValue(expected, value_type), expected)
        self.assertEqual(
            gviz_api.DataTable.CoerceValue((expected, None), value_type),
            (expected, None))
        self.assertEqual(
            gviz_api.DataTable.CoerceValue((expected, None, {}), value_type),
            (expected, None, {}))
        self.assertEqual(
            gviz_api.DataTable.CoerceValue((expected, 'foobar'), value_type),
            (expected, 'foobar'))
        self.assertEqual(
            gviz_api.DataTable.CoerceValue((expected, 'foobar', {}),
                                           value_type),
            (expected, 'foobar', {}))

        # Test "timeofday"
        value_type = 'timeofday'
        for value in [42, '', []]:
            self.assertRaises(gviz_api.DataTableException,
                              gviz_api.DataTable.CoerceValue,
                              value, value_type)
        expected = datetime.time(4, 5, 6)
        for value in [expected, datetime.datetime(2001, 2, 3, 4, 5, 6)]:
            self.assertEqual(
                gviz_api.DataTable.CoerceValue(value, value_type),
                expected)
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None), value_type),
                (expected, None))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, None, {}), value_type),
                (expected, None, {}))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar'), value_type),
                (expected, 'foobar'))
            self.assertEqual(
                gviz_api.DataTable.CoerceValue((value, 'foobar', {}),
                                               value_type),
                (expected, 'foobar', {}))

    def test_EscapeForJSCode(self):
        """Test JavaScript code escaping."""
        for value in [None, 42]:
            self.assertRaises(AttributeError,
                              gviz_api.DataTable.EscapeForJSCode, value, 42)

        encoder = gviz_api.DataTableJSONEncoder()
        for value, expected in [
            (None, 'null'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6),
             'new Date(2001,1,3,4,5,6)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 7),
             'new Date(2001,1,3,4,5,6,0)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 78),
             'new Date(2001,1,3,4,5,6,0)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 789),
             'new Date(2001,1,3,4,5,6,0)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 7890),
             'new Date(2001,1,3,4,5,6,7)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 78900),
             'new Date(2001,1,3,4,5,6,78)'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6, 789000),
             'new Date(2001,1,3,4,5,6,789)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16),
             'new Date(2011,11,13,14,15,16)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 7),
             'new Date(2011,11,13,14,15,16,0)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 78),
             'new Date(2011,11,13,14,15,16,0)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 789),
             'new Date(2011,11,13,14,15,16,0)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 7890),
             'new Date(2011,11,13,14,15,16,7)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 78900),
             'new Date(2011,11,13,14,15,16,78)'),
            (datetime.datetime(2011, 12, 13, 14, 15, 16, 789000),
             'new Date(2011,11,13,14,15,16,789)'),
            (datetime.date(2001, 2, 3), 'new Date(2001,1,3)'),
            (datetime.date(2004, 5, 6), 'new Date(2004,4,6)'),
            (datetime.date(2007, 8, 9), 'new Date(2007,7,9)'),
            (datetime.date(2010, 11, 12), 'new Date(2010,10,12)')]:
            self.assertEqual(
                gviz_api.DataTable.EscapeForJSCode(encoder, value), expected)

    def test_ToString(self):
        """Test converting a single value to a string."""
        for value, expected in [
            (None, '(empty)'),
            ('', ''),
            ('foobar', 'foobar'),
            (u'fo\u00f6b\u00e4r', u'fo\u00f6b\u00e4r'),
            (42, '42'),
            (3.14, '3.14'),
            (-42, '-42'),
            (-3.14, '-3.14'),
            (True, 'true'),
            (False, 'false'),
            (datetime.date(2001, 2, 3), '2001-02-03'),
            (datetime.datetime(2001, 2, 3, 4, 5, 6), '2001-02-03 04:05:06'),
            (datetime.time(1, 2, 3), '01:02:03')]:
            self.assertEqual(gviz_api.DataTable.ToString(value), expected)

    def test_ColumnTypeParser(self):
        """Test parsing a single column description."""
        for value in [None, 42, '', [],
                      ['foo'], ['foo', 'bar'], ['foo', 'bar', 'baz'],
                      # Test unsupported type
                      ('foo', 'bar'), ('foo', 'bar', 'baz'),
                      # Test non-dict fourth element
                      ['foo', 'bar', 'baz', 42],
                      ('foo', 'bar', 'baz', []),
                      # Test non-string elements
                      (1,), (1, 2), (1, 2, 3), (1, 2, 3, 4),
                      ('foo', 42), ('foo', 'string', 42),
                      # Test tuple that is too long
                      (1, 2, 3, 4, 5)]:
            self.assertRaises(gviz_api.DataTableException,
                              gviz_api.DataTable.ColumnTypeParser, value)
        expected = {'id': 'foo', 'label': 'foo',
                    'type': 'string', 'custom_properties': {}}
        self.assertEqual(gviz_api.DataTable.ColumnTypeParser('foo'),
                         expected)
        self.assertEqual(gviz_api.DataTable.ColumnTypeParser(('foo',)),
                         expected)
        for value_type in self.accepted_types:
            for value in [' ' + value_type, value_type + '    ',
                          ' ' + value_type + ' ']:
                expected['id'] = value
                expected['label'] = value
                self.assertEqual(
                    gviz_api.DataTable.ColumnTypeParser(value), expected)
                self.assertEqual(
                    gviz_api.DataTable.ColumnTypeParser((value,)), expected)
                self.assertRaises(gviz_api.DataTableException,
                                  gviz_api.DataTable.ColumnTypeParser,
                                  (value, value))
            for value in [value_type.upper(), value_type.title()]:
                expected['id'] = value
                expected['label'] = value
                self.assertEqual(
                    gviz_api.DataTable.ColumnTypeParser(value), expected)
                self.assertEqual(
                    gviz_api.DataTable.ColumnTypeParser((value,)), expected)
                expected['type'] = value_type
                self.assertEqual(
                    gviz_api.DataTable.ColumnTypeParser((value, value)),
                    expected)
                expected['label'] = 'foobar'
                self.assertEqual(gviz_api.DataTable.ColumnTypeParser(
                    (value, value, 'foobar')), expected)
                expected['custom_properties'] = {'bar': 'baz'}
                self.assertEqual(gviz_api.DataTable.ColumnTypeParser(
                    (value, value, 'foobar', {'bar': 'baz'})), expected)
                # Reset expected dict
                expected['type'] = 'string'
                expected['custom_properties'] = {}

    def test_TableDescriptionParser(self):
        """Test parsing a table description."""
        for value in [None, 42, '', [], {},
                      # Test unsupported type
                      ('foo', 'bar'), ('foo', 'bar', 'baz'),
                      # Test non-dict fourth element
                      ('foo', 'bar', 'baz', []),
                      # Test non-string elements
                      (1,), (1, 2), (1, 2, 3), (1, 2, 3, 4),
                      ('foo', 42), ('foo', 'string', 42),
                      # Test tuple that is too long
                      (1, 2, 3, 4, 5)]:
            self.assertRaises(gviz_api.DataTableException,
                              gviz_api.DataTable.TableDescriptionParser, value)

        expected = [{'id': 'foo', 'label': 'foo',
                     'type': 'string', 'custom_properties': {},
                     'depth': -1, 'container': 'scalar'}]
        self.assertEqual(gviz_api.DataTable.TableDescriptionParser('foo', -1),
                         expected)

        for value, expected in [
            ('foo', [{'id': 'foo', 'label': 'foo',
                      'type': 'string', 'custom_properties': {},
                      'depth': 0, 'container': 'scalar'}]),
            (('foo',), [{'id': 'foo', 'label': 'foo',
                         'type': 'string', 'custom_properties': {},
                         'depth': 0, 'container': 'scalar'}]),
            ([('foo', self.accepted_types[0], 'foobar'),
              ('bar', self.accepted_types[1]),
              ('baz', self.accepted_types[2], 'baz', {'bar': 'baz'})],
             [{'id': 'foo', 'label': 'foobar',
               'type': self.accepted_types[0], 'custom_properties': {},
               'depth': 0, 'container': 'iter'},
              {'id': 'bar', 'label': 'bar',
               'type': self.accepted_types[1], 'custom_properties': {},
               'depth': 0, 'container': 'iter'},
              {'id': 'baz', 'label': 'baz', 'type': self.accepted_types[2],
               'custom_properties': {'bar': 'baz'},
               'depth': 0, 'container': 'iter'}]),
            ({('foo', self.accepted_types[0], 'foobar'): [
                ('bar', self.accepted_types[1]),
                ('baz', self.accepted_types[2], 'baz', {'bar': 'baz'})]},
             [{'id': 'foo', 'label': 'foobar',
               'type': self.accepted_types[0], 'custom_properties': {},
               'depth': 0, 'container': 'dict'},
              {'id': 'bar', 'label': 'bar',
               'type': self.accepted_types[1], 'custom_properties': {},
               'depth': 1, 'container': 'iter'},
              {'id': 'baz', 'label': 'baz', 'type': self.accepted_types[2],
               'custom_properties': {'bar': 'baz'},
               'depth': 1, 'container': 'iter'}]),
            ({'foo': (self.accepted_types[0], 'foobar'),
              'bar': (self.accepted_types[1]),
              'baz': (self.accepted_types[2], 'baz', {'bar': 'baz'})},
             [{'id': 'bar', 'label': 'bar',
               'type': self.accepted_types[1], 'custom_properties': {},
               'depth': 0, 'container': 'dict'},
              {'id': 'baz', 'label': 'baz', 'type': self.accepted_types[2],
               'custom_properties': {'bar': 'baz'},
               'depth': 0, 'container': 'dict'},
              {'id': 'foo', 'label': 'foobar',
               'type': self.accepted_types[0], 'custom_properties': {},
               'depth': 0, 'container': 'dict'}])]:
            self.assertEqual(
                gviz_api.DataTable.TableDescriptionParser(value),
                expected)
            data_table = gviz_api.DataTable(value)
            self.assertEqual(data_table.columns, expected)
            self.assertEqual(data_table.NumberOfRows(), 0)

    def test_SetRowsCustomProperties(self):
        """Test setting the custom properties for a row."""
        data_table = gviz_api.DataTable(
            [('name', 'string'), ('value', 'number')])
        self.assertEqual(data_table.NumberOfRows(), 0)
        for value in [None, 3.14]:
            self.assertRaises(TypeError, data_table.SetRowsCustomProperties,
                              value, value)
            self.assertRaises(TypeError, data_table.SetRowsCustomProperties,
                              [value], value)

    def test_AppendData(self):
        """Test adding data to a DataTable instance."""
        data_table = gviz_api.DataTable(
            [('name', 'string'), ('value', 'number')])
        self.assertEqual(data_table.NumberOfRows(), 0)
        self.assertRaises(gviz_api.DataTableException,
                          data_table.AppendData, {'foo': 42})
        data_table.AppendData([('one', 1)])
        self.assertEqual(data_table.NumberOfRows(), 1)
        self.assertEqual(data_table._ToJSonObj(), {
            'cols': [{'id': 'name', 'label': 'name', 'type': 'string'},
                     {'id': 'value', 'label': 'value', 'type': 'number'}],
            'rows': [{'c': [{'v': 'one'}, {'v': 1}]}]})
        data_table.AppendData([('two', 2), ('three', 3)])
        self.assertEqual(data_table.NumberOfRows(), 3)
        self.assertEqual(data_table._ToJSonObj(), {
            'cols': [{'id': 'name', 'label': 'name', 'type': 'string'},
                     {'id': 'value', 'label': 'value', 'type': 'number'}],
            'rows': [{'c': [{'v': 'one'}, {'v': 1}]},
                     {'c': [{'v': 'two'}, {'v': 2}]},
                     {'c': [{'v': 'three'}, {'v': 3}]}]})
        data_table.LoadData([])
        self.assertEqual(data_table.NumberOfRows(), 0)
        data_table.AppendData([('bar', 2), ('baz', 3)])
        self.assertEqual(data_table.NumberOfRows(), 2)
        self.assertEqual(data_table._ToJSonObj(), {
            'cols': [{'id': 'name', 'label': 'name', 'type': 'string'},
                     {'id': 'value', 'label': 'value', 'type': 'number'}],
            'rows': [{'c': [{'v': 'bar'}, {'v': 2}]},
                     {'c': [{'v': 'baz'}, {'v': 3}]}]})
        data_table.SetRowsCustomProperties(1, {'foo': 'bar'})
        self.assertEqual(data_table.NumberOfRows(), 2)
        self.assertEqual(data_table._ToJSonObj(), {
            'cols': [{'id': 'name', 'label': 'name', 'type': 'string'},
                     {'id': 'value', 'label': 'value', 'type': 'number'}],
            'rows': [{'c': [{'v': 'bar'}, {'v': 2}]},
                     {'c': [{'v': 'baz'}, {'v': 3}], 'p': {'foo': 'bar'}}]})
        data_table.LoadData([(u'fo\u00f6b\u00e4r', 42)])
        self.assertEqual(data_table.NumberOfRows(), 1)
        self.assertEqual(data_table._ToJSonObj(), {
            'cols': [{'id': 'name', 'label': 'name', 'type': 'string'},
                     {'id': 'value', 'label': 'value', 'type': 'number'}],
            'rows': [{'c': [{'v': u'fo\u00f6b\u00e4r'}, {'v': 42}]}]})
        self.assertRaises(IndexError, data_table.SetRowsCustomProperties,
                          1, {'foo': 'bar'})
        data_table.SetRowsCustomProperties([-1], {'foo': 'bar'})
        self.assertEqual(data_table.NumberOfRows(), 1)
        self.assertEqual(data_table._ToJSonObj(), {
            'cols': [{'id': 'name', 'label': 'name', 'type': 'string'},
                     {'id': 'value', 'label': 'value', 'type': 'number'}],
            'rows': [{'c': [{'v': u'fo\u00f6b\u00e4r'}, {'v': 42}],
                      'p': {'foo': 'bar'}}]})

        data_table = gviz_api.DataTable(
            {('name', 'string'): ('value', 'number')})
        self.assertEqual(data_table.NumberOfRows(), 0)
        self.assertRaises(gviz_api.DataTableException,
                          data_table.AppendData, [('foo', 42)])
        # This is a problem
        data_table.AppendData({})
        self.assertEqual(data_table.NumberOfRows(), 1)
        self.assertEqual(data_table._ToJSonObj(), {
            'cols': [{'id': 'name', 'label': 'name', 'type': 'string'},
                     {'id': 'value', 'label': 'value', 'type': 'number'}],
            'rows': [{'c': [None, None]}]})
        data_table.AppendData({'one': 1, 'two': 2, 'three': 3})
        self.assertEqual(data_table.NumberOfRows(), 4)
        self.assertEqual(data_table._ToJSonObj(), {
            'cols': [{'id': 'name', 'label': 'name', 'type': 'string'},
                     {'id': 'value', 'label': 'value', 'type': 'number'}],
            'rows': [{'c': [None, None]},
                     {'c': [{'v': 'one'}, {'v': 1}]},
                     {'c': [{'v': 'three'}, {'v': 3}]},
                     {'c': [{'v': 'two'}, {'v': 2}]}]})

        # This is a problem
        data_table.LoadData({})
        self.assertEqual(data_table.NumberOfRows(), 1)
        self.assertEqual(data_table._ToJSonObj(), {
            'cols': [{'id': 'name', 'label': 'name', 'type': 'string'},
                     {'id': 'value', 'label': 'value', 'type': 'number'}],
            'rows': [{'c': [None, None]}]})
        data_table.AppendData({'bar': 2, 'baz': 3})
        self.assertEqual(data_table.NumberOfRows(), 3)
        self.assertEqual(data_table._ToJSonObj(), {
            'cols': [{'id': 'name', 'label': 'name', 'type': 'string'},
                     {'id': 'value', 'label': 'value', 'type': 'number'}],
            'rows': [{'c': [None, None]},
                     {'c': [{'v': 'bar'}, {'v': 2}]},
                     {'c': [{'v': 'baz'}, {'v': 3}]}]})
        data_table.LoadData({u'fo\u00f6b\u00e4r': 42})
        self.assertEqual(data_table.NumberOfRows(), 1)
        self.assertEqual(data_table._ToJSonObj(), {
            'cols': [{'id': 'name', 'label': 'name', 'type': 'string'},
                     {'id': 'value', 'label': 'value', 'type': 'number'}],
            'rows': [{'c': [{'v': u'fo\u00f6b\u00e4r'}, {'v': 42}]}]})


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MoreDataTableTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
