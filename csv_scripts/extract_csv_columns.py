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
    with open(read_file, "r") as csvfile:
        datareader = csv.reader(csvfile)

        index = 0
        first = True
        while not end:
            if show_progress:
                print("Done with " + str(index * rows_per_write) + " rows.")
            index += 1

            rows = []
            for i in range(rows_per_write):
                try:
                    row = next(datareader)
                    rows_to_append = select_info(row, first)
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


def violation_select(row, first):
    rows_to_append = []
    if first:
        rows_to_append.append(['violation_id', 'parcel_id', 'violation_code'])

    else:
        # From the start of the violation codes to the end.
        for i in range(257, 307):
            if len(row[i].strip()) != 0:
                cols_to_keep = [0, 2, i]
                if valid_row(row, cols_to_keep, 'violation'):
                    # Append the violation id, parcel id, and violation code.
                    rows_to_append.append(create_row_entry(row, cols_to_keep))

    return rows_to_append


def parcel_select(row, first):
    rows_to_append = []
    if first:
        rows_to_append.append(['parcel_id', 'owner_id', 'zipcode', 'rental', 'census_tracts'])

    else:
        status_col = 20
        cols_to_keep = [1, 9, 194, 22, 5]
        if valid_row(row, cols_to_keep + [status_col], 'property') and row[status_col].strip() == 'ACTIVE':
            rows_to_append.append(create_row_entry(row, cols_to_keep))

    return rows_to_append


def owner_select(row, first):
    rows_to_append = []
    if first:
        rows_to_append.append(['owner_id', 'owner_zipcode'])

    else:
        cols_to_keep = [9, 10]
        if valid_row(row, cols_to_keep, 'property'):
            full_row = create_row_entry(row, cols_to_keep)
            # Since owner zipcode is coming from a full address, we need to get the numbers out by stripping, splitting,
            # and selecting.
            address = full_row[1]
            # Select the last entry of the split string. This can contain
            full_zip = address.split()[-1]
            zipcode = full_zip.split(sep='-')[0]

            full_row[1] = zipcode
            rows_to_append.append(full_row)

    return rows_to_append


error_file = '/Users/cameronkuchta/Documents/GitHub/City-Planning-Project/csv_files/errors.csv'
def valid_row(row, important_cols, type):
    for col in important_cols:
        if len(row[col].strip()) == 0:
            print('Error found.')
            with open(error_file, 'a') as f:
                f.write('ERROR: (' + type + ') Row did not have necessary columns. Expected value in column ' + str(col)
                        + '\n' + str(row[:5]) + '...\n')
            return False

    return True


def create_row_entry(row, cols):
    return [row[col].strip() for col in cols]


if __name__ == '__main__':
    read_files = ['/Users/cameronkuchta/Desktop/Academics/database_capstone/city_project/csv_files/violations_new.csv',
                  '/Users/cameronkuchta/Desktop/Academics/database_capstone/city_project/csv_files/properties_new.csv',
                  '/Users/cameronkuchta/Desktop/Academics/database_capstone/city_project/csv_files/properties_new.csv']
    write_files = ['/Users/cameronkuchta/Documents/GitHub/City-Planning-Project/csv_files/violations_db.csv',
                   '/Users/cameronkuchta/Documents/GitHub/City-Planning-Project/csv_files/parcel_db.csv',
                   '/Users/cameronkuchta/Documents/GitHub/City-Planning-Project/csv_files/owner_db.csv']
    select_types = [violation_select, parcel_select, owner_select]

    os.remove(error_file)

    for i in range(len(select_types)):
        extract_cols(read_files[i], write_files[i], select_types[i], show_progress=True)
