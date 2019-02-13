import csv


def count_non_empty(filename):
    '''
    Count the number of entries in each column that are not empty.
    :param filename: csv file to examine
    :return: header, count: The header of each column and the number of non-empty entries.
    '''
    with open(filename, "r") as csvfile:
        datareader = csv.reader(csvfile)
        header = next(datareader)
        count = [0]*len(header)

        for row in datareader:
            for i in range(len(row)):
                val = row[i]
                if val.strip() != "":
                    count[i] += 1

    return header, count


def write_csv(csv_file, list_o_lists, write_type='w'):
    '''
    Create a csv file using a list of lists that declares rows and columns.
    :param csv_file: The file to create.
    :param list_o_lists: Each sublist is a row and
    :return:
    '''
    with open(csv_file, write_type) as f:
        for j in range(len(list_o_lists)):
            row = list_o_lists[j]
            line = ''
            for i in range(len(row)):
                line += str(row[i])
                if i != len(row) - 1:
                    line += ","
            line += "\n"
            f.write(line)


if __name__ == '__main__':
    filename = '/Users/cameronkuchta/Desktop/Academics/database_capstone/city_project/csv_files/inspections.csv'
    head, c = count_non_empty(filename)
    csv_file = '/Users/cameronkuchta/Desktop/Academics/database_capstone/city_project/csv_files/inspections_count.csv'
    write_csv(csv_file, [head, c])
    for i in range(len(head)):
        print(str(head[i]) + ":\t" + str(c[i]))
