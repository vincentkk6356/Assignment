import unittest
from data_parse.parse import *

class TestParse(unittest.TestCase):

    def test_convert_type(self):
        self.assertEqual(convert_type("-21", "INTEGER"),-21)
        self.assertEqual(convert_type("-21", "integer"),-21)
        self.assertEqual(convert_type("01", "INTEGER"),1)
        self.assertRaises(ValueError, convert_type, "abc", "INTEGER")
        self.assertEqual(convert_type("1", "BOOLEAN"),True)
        self.assertEqual(convert_type("0", "BOOLEAN"),False)
        self.assertRaises(ValueError, convert_type, "abc", "BOOLEAN")



    def test_load_fileformat(self):
        # invliad datatype formatfile
        formatfilepath = "./test_data/fileformat_wrong_datatype.csv"
        self.assertRaises(InvalidDataTypeException, load_fileformat, formatfilepath)

        # invliad width formatfile
        formatfilepath = "./test_data/fileformat_invalid_width.csv"
        self.assertRaises(InvalidWidthException, load_fileformat, formatfilepath)

        # invliad formatfile - missing values
        formatfilepath = "./test_data/fileformat_invalid_shortformat.csv"
        self.assertRaises(InvalidFormatException, load_fileformat, formatfilepath)

        # invliad formatfile - excessive values
        formatfilepath = "./test_data/fileformat_invalid_longformat.csv"
        self.assertRaises(InvalidFormatException, load_fileformat, formatfilepath)

        # invalid header
        formatfilepath = "./test_data/fileformat_invalid_header.csv"
        self.assertRaises(InvalidHeaderException, load_fileformat, formatfilepath)

        # empty formatfile
        formatfilepath = "./test_data/not_exist.csv"
        self.assertRaises(FileNotFoundError, load_fileformat, formatfilepath)

        # good formatfile
        formatfilepath = "./test_data/fileformat_normal1.csv"
        format = load_fileformat(formatfilepath)

        self.assertIn("width", format)
        self.assertIn("column name", format)
        self.assertIn("datatype", format)
        self.assertEqual(len(format["width"]),len(format["datatype"]),len(format["column name"]))
        self.assertGreater(len(format["width"]), 0)

        # different header order
        formatfilepath = "./test_data/fileformat_order.csv"
        self.assertDictEqual(format, load_fileformat(formatfilepath))

        # different delimiter
        formatfilepath = "./test_data/fileformat_delimiter.csv"
        self.assertDictEqual(format, load_fileformat(formatfilepath, delimiter=" "))

        # random space
        formatfilepath = "./test_data/fileformat_complex.csv"
        format = load_fileformat(formatfilepath)
        ans = {'column name': ['firstname', 'lastname',
                               'valid', 'count', 'test',
                               'valid', 'NumbEr',
                               'anotherValid', 'email'],
               'width': [10, 10, 1, 3, 1, 1, 3, 1, 3],
               'datatype': ['TEXT', 'TEXT', 'BOOLEAN',
                            'INTEGER', 'BOOLEAN', 'BOOLEAN',
                            'INTEGER', 'BOOLEAN', 'TEXT'],
               'total_width': 33}

        self.assertDictEqual(format, ans)


    def test_parse_flat_file(self):

        # normal case
        datafilename = "./test_data/fileformat_normal1_2015-06-28.txt"
        formatfilename = "./test_data/fileformat_normal1.csv"
        output = parse_flatfile(datafilename, formatfilename)
        ans = [{'name': 'Diabetes', 'valid': True, 'count': 1},
               {'name': 'Asthma', 'valid': False, 'count': -12},
               {'name': 'Stroke', 'valid': True, 'count': 103}
               ]

        self.assertEqual(len(ans), len(output))
        for i in range(len(ans)):
            self.assertDictEqual(output[i], ans[i])

        # Invalid Boolean
        datafilename = "./test_data/fileformat_invalid_boolean_2015-06-28.txt"
        formatfilename = "./test_data/fileformat_normal1.csv"

        self.assertWarnsRegex(UserWarning,
                              "is not '1' or '0' for BOOLEAN conversion",
                              parse_flatfile, datafilename, formatfilename)

        # Invalid INTEGER
        datafilename = "./test_data/fileformat_invalid_integer_2015-06-28.txt"
        formatfilename = "./test_data/fileformat_normal1.csv"

        self.assertWarnsRegex(UserWarning,
                              "is not a valid integer",
                              parse_flatfile, datafilename, formatfilename)


        # Entry length is longer than the total width length specified
        datafilename = "./test_data/fileformat_longer_entry_2015-06-28.txt"
        formatfilename = "./test_data/fileformat_normal1.csv"

        self.assertWarnsRegex(UserWarning,
                              "is unexpectedly longer",
                              parse_flatfile, datafilename, formatfilename)

        # Entry length is shorter than the total width length specified
        datafilename = "./test_data/fileformat_shorter_entry_2015-06-28.txt"
        formatfilename = "./test_data/fileformat_normal1.csv"

        self.assertWarnsRegex(UserWarning,
                              "does not have enough characters",
                              parse_flatfile, datafilename, formatfilename)


        # Multiple entry error
        datafilename = "./test_data/fileformat_multiple_errors_2015-06-28.txt"
        formatfilename = "./test_data/fileformat_normal1.csv"

        self.assertWarnsRegex(UserWarning,
                              r"Entry ignored in .*: 5",
                              parse_flatfile, datafilename, formatfilename)

        # more fields
        datafilename = "./test_data/fileformat_complex_2015-06-28.txt"
        formatfilename = "./test_data/fileformat_complex.csv"
        output = parse_flatfile(datafilename, formatfilename)

        ans = [{'firstname': 'James', 'lastname': 'Bond', 'valid': False,
                'count': 2, 'test': False, 'NumbEr': 23, 'anotherValid': True, 'email': 'his'},
               {'firstname': 'Sergio', 'lastname': 'Chan', 'valid': False,
                'count': 22, 'test': False, 'NumbEr': 3, 'anotherValid': True, 'email': 'zis'},
               {'firstname': 'May', 'lastname': 'Bond', 'valid': False,
                'count': 2, 'test': False, 'NumbEr': 23, 'anotherValid': True, 'email': 'his'}]

        self.assertEqual(len(ans), len(output))
        for i in range(len(ans)):
            self.assertDictEqual(output[i], ans[i])


if __name__ == '__main__':
    unittest.main()
