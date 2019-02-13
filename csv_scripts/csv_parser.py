import csv


def count_empty(filename):
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


def write_csv(csv_file, list_o_lists):
    with open(csv_file, 'w') as f:
        for j in range(len(list_o_lists)):
            l = list_o_lists[j]
            for i in range(len(l)):
                line = str(l[i])
                if i != len(l) - 1:
                    line += ","
                f.write(line)
            if j != len(list_o_lists) - 1:
                f.write("\n")


if __name__ == '__main__':
    filename = '/Users/cameronkuchta/Desktop/Academics/database_capstone/city_project/csv_files/inspections.csv'
    head, c = count_empty(filename)
    csv_file = '/Users/cameronkuchta/Desktop/Academics/database_capstone/city_project/csv_files/inspections_count.csv'
    write_csv(csv_file, [head, c])
    for i in range(len(head)):
        print(str(head[i]) + ":\t" + str(c[i]))
