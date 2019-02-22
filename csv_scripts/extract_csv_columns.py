from csv_scripts.csv_parser import write_csv
import csv
import os


# Columns for VIOLATION TABLE from the violation csv.
# VIOLATION REFERENCE, PARCEL, VIOL CODE 1, VIOL CODE 2, ...
# We need to change these separate columns of violations into rows for entries.

# Columns for PARCEL TABLE from the properties csv.
# PARCEL ID, LOT NUMBER, OWNER ID, RENTAL, LOC ZIP (remove by STATUS)

# Columns for OWNER TABLE from the properties csv.
# OWNER ID, OWNER ADDR2 (last 5 numbers)

def extract_cols(read_file, write_file, select_info, rows_per_write=1000, show_progress=False):
    end = False
    with open(read_file, "r", errors='replace') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_ALL)

        index = 0
        first = True
        row_number = 0
        while not end:
            if show_progress:
                print("Done with " + str(index * rows_per_write) + " rows.")

            rows = []
            for i in range(rows_per_write):
                row_number += 1
                try:
                    row = next(datareader)
                    rows_to_append = select_info(row, first, row_number)
                    first = False
                    for r in rows_to_append:
                        rows.append(r)
                except StopIteration:
                    end = True
                    break

            # If this is the first time to write to the file, remove all contents.
            if index == 0:
                mode = 'w'
            else:
                mode = 'a'

            write_csv(write_file, rows, write_type=mode)
            index += 1


def violation_select(row, first, row_number):
    rows_to_append = []
    if first:
        rows_to_append.append(['violation_id', 'parcel_id', 'violation_code'])

    else:
        # From the start of the violation codes to the end.
        for i in range(257, 307):
            if len(row[i].strip()) != 0:
                cols_to_keep = [0, 2, i]
                if valid_row(row, cols_to_keep, 'violation', 'violation', row_number):
                    # Append the violation id, parcel id, and violation code.
                    rows_to_append.append(create_row_entry(row, cols_to_keep))

    return rows_to_append


def parcel_select(row, first, row_number):
    rows_to_append = []
    if first:
        rows_to_append.append(['parcel_id', 'owner_id', 'zipcode', 'rental', 'census_tracts'])

    else:
        status_col = 20
        cols_to_keep = [1, 9, 194, 22, 5]
        if valid_row(row, cols_to_keep + [status_col], 'property', 'parcel', row_number) \
                and row[status_col].strip() == 'ACTIVE':
            rows_to_append.append(create_row_entry(row, cols_to_keep))

    return rows_to_append


def owner_select(row, first, row_number):
    def extract_zipcode(full_row):
        # Since owner zipcode is coming from a full address, we need to get the numbers out by stripping, splitting,
        # and selecting.
        address = full_row[1]
        # Select the last entry of the split string. This can contain
        full_zip = address.split()[-1]
        zipcode = full_zip.split(sep='-')[0]
        return zipcode

    rows_to_append = []
    if first:
        rows_to_append.append(['owner_id', 'owner_zipcode'])

    else:
        cols_to_keep = [9, 12]
        alt_cols_to_keep = [9, 13]
        if valid_row(row, cols_to_keep, 'property', 'owner', row_number) \
                and extract_zipcode([0, row[cols_to_keep[1]]]).isdigit():
            full_row = create_row_entry(row, cols_to_keep)
            zipcode = extract_zipcode(full_row)

            full_row[1] = zipcode
            rows_to_append.append(full_row)
        elif valid_row(row, alt_cols_to_keep, 'property', 'owner', row_number) \
                and extract_zipcode([0, row[alt_cols_to_keep[1]]]).isdigit():
            full_row = create_row_entry(row, alt_cols_to_keep)
            zipcode = extract_zipcode(full_row)

            full_row[1] = zipcode
            rows_to_append.append(full_row)

    return rows_to_append


error_file = '/Users/cameronkuchta/Documents/GitHub/City-Planning-Project/csv_files/errors.csv'
def valid_row(row, important_cols, file_name, table_name, row_number):
    for col in important_cols:
        if len(row[col].strip()) == 0:
            print('Error found.')
            row_problems = '['
            for i in range(len(important_cols)):
                row_problems += str(row[important_cols[i]])
                if i < len(important_cols) - 1:
                    row_problems += ', '
            row_problems += ']'

            with open(error_file, 'a') as f:
                f.write('[' + table_name + '] ERROR: (' + file_name + ') Row ' +
                        str(row_number) + ' did not have necessary columns. ' +
                        'Expected value in column ' + str(col) + '.\n'
                        + row_problems + '...\n')
            return False

    return True


def create_row_entry(row, cols):
    return [row[col].strip() for col in cols]


if __name__ == '__main__':
    read_files = ['/Users/cameronkuchta/Desktop/Academics/database_capstone/city_project/csv_files/violations_bar.csv',
                  '/Users/cameronkuchta/Desktop/Academics/database_capstone/city_project/csv_files/properties_bar.csv',
                  '/Users/cameronkuchta/Desktop/Academics/database_capstone/city_project/csv_files/properties_bar.csv']
    write_files = ['/Users/cameronkuchta/Documents/GitHub/City-Planning-Project/csv_files/violations_db.csv',
                   '/Users/cameronkuchta/Documents/GitHub/City-Planning-Project/csv_files/parcel_db.csv',
                   '/Users/cameronkuchta/Documents/GitHub/City-Planning-Project/csv_files/owner_db.csv']
    select_types = [violation_select, parcel_select, owner_select]

    if os.path.isfile(error_file):
        os.remove(error_file)

    for i in range(len(select_types)):
        extract_cols(read_files[i], write_files[i], select_types[i], show_progress=True)
