import os, glob
import csv
from typing import List, Union, Dict
import warnings
from data_parse.exceptions import *

def load_fileformat(formatfilename: str, delimiter=',') -> List[List[str]]:
    """
    This function loads the formatfile and also validate the content.
    :param formatfilename: the path to the formatfile
    :param delimiter: delimiter use to separate values in csv
    """

    with open(formatfilename, "r") as f:
        csv_reader = csv.reader(f, delimiter=delimiter)

        try:
            header = next(csv_reader)
        except StopIteration:  # empty file
            message = f"'{formatfilename}' is empty."
            raise EmptyFormatException(message)

        for i in range(len(header)):
            header[i] = header[i].lower().strip()

        if len(header) != 3 or \
            "column name" not in header or \
            "width" not in header or "datatype" not in header:  # invalid header
            message = f"'{formatfilename}' does not contain a valid header: '{delimiter.join(header)}'. " \
                      f"Please make sure the delimiter is correct."
            raise InvalidHeaderException(message)

        format = {
            "column name": [],
            "width": [],
            "datatype": [],
            "total_width": 0
        }

        datatypes = {"INTEGER", "BOOLEAN", "TEXT"}


        try:
            for i, row in enumerate(csv_reader):

                if len(row) != len(format)-1:  # header not match values
                    if len(row) > len(format):
                        message = f"'line: {i+2}' in '{formatfilename}' contains excess unknown values."
                    else:
                        message = f"'line: {i+2}' in '{formatfilename}' does not have enough values."

                    raise InvalidFormatException(message=message)

                for j in range(len(row)):
                    format[header[j]].append(row[j].strip())


                if format["datatype"][i].upper() not in datatypes:  # invalid datatype
                    message = f"'line: {i+1}' in '{formatfilename}' contains invalid datatype '{format['datatype'][i]}'."
                    raise InvalidDataTypeException(message)

                format["width"][i] = convert_type(format["width"][i], "INTEGER")
                format["datatype"][i] = format["datatype"][i].upper()
                format["total_width"] += format["width"][i]

        except ValueError as e:  # fail to convert str to int
            message = f"'line: {i+1}' in '{formatfilename}' contains invalid width '{format['width'][i]}'."
            raise InvalidWidthException(message)

        assert len(format["width"]) == len(format["datatype"]) == len(format["column name"])

    return format



def load_datafile(datafilename: str)-> List[str]:
    """
    :param datafilename: path to datafile
    """
    with open(datafilename, "r") as f:
        lines = f.read().splitlines()  # get rid of return character
    return lines


def convert_type(inp: str, type: str) -> Union[str, bool, int]:
    """
    convert the input into primitive datatype
    """

    type = type.upper()
    if type == "INTEGER":
        try:
            return int(inp)
        except ValueError:
            raise ValueError(f"'{inp}' is not a valid integer.")

    elif type == "TEXT":
        return inp

    elif type == "BOOLEAN":
        if inp == "1":
            return True
        elif inp == "0":
            return False
        else:
            raise ValueError(f"'{inp}' is not '1' or '0' for BOOLEAN conversion.")
    else:
        assert False, f"Invalid data type: {type}"




def parse_flatfile(datafilename: str, formatfilename: str) -> List[Dict]:
    """
    :param datafilename: path to datafile
    :param formatfilename: path to formatfile
    """

    format = load_fileformat(formatfilename)
    data = load_datafile(datafilename)

    formatfilename = os.path.basename(formatfilename)
    datafilename = os.path.basename(datafilename)

    if os.path.splitext(formatfilename)[0] not in os.path.splitext(datafilename)[0]:  # filetypes do not match each other according to their names
        warnings.warn(f"'{formatfilename}' may not match '{datafilename}'.")

    output = []
    ignore_count = 0
    # loop through each data entry/ line in datafile
    for line_num, line in enumerate(data):
        entry = {}
        i = 0
        n = len(line)

        # entry length sanity check
        if n > format["total_width"]:  # the line is longer than expected
            message = f"line: {line_num+1} in {datafilename} is unexpectedly longer." \
                      f" Ignore the entry."

            warnings.warn(message)
            ignore_count += 1
            continue
        elif n < format["total_width"]:
            message = f"'line: {line_num+1}' in '{datafilename}' does not have enough characters." \
                      f" Ignore the entry."
            warnings.warn(message)
            ignore_count += 1
            continue

        # loop through each field specified in the format and retrieve the field value
        try:
            for j in range(len(format["column name"])):
                col_name = format["column name"][j]
                width = format["width"][j]
                datatype = format["datatype"][j]

                entry[col_name] = convert_type(line[i:i+width].strip(), datatype)
                i += width

        except ValueError as e:
            message = f"'line: {line_num+1}' in '{datafilename}'" \
                      f" contains invalid data '{line[i:i+width].strip()}': " + str(e)
            warnings.warn(message)
            ignore_count += 1

        output.append(entry)

    if ignore_count > 0:
        warnings.warn(f"Entry ignored in {datafilename}: {ignore_count}")

    return output
