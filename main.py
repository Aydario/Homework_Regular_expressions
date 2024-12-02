import csv
import re


def main():
    with open('phonebook_raw.csv', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)

    try:
        for i in range(1, len(contacts_list)):
            row = ' '.join(contacts_list[i][:2]).split()
            row += contacts_list[i][len(row):]
            number = row[5]
            if 'доб' in number:
                pattern = r'(\+7|8)?\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})\s*\(?([доб]*).?\s*(\d+)\)?'
                pattern_replace = r'+7(\2)\3-\4-\5 \6.\7'
                result = re.sub(pattern, pattern_replace, number)
                row[5] = result
            else:
                pattern = r'(\+7|8)?\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})'
                pattern_replace = r'+7(\2)\3-\4-\5'
                result = re.sub(pattern, pattern_replace, number)
                row[5] = result
            contacts_list[i].clear()
            contacts_list[i].extend(row)
            for j in range(i + 1, len(contacts_list) - 1):
                new_row = ' '.join(contacts_list[j][:2]).split()
                new_row += contacts_list[j][len(new_row):]
                if new_row[0] == row[0] and new_row[1] == row[1] and \
                        (new_row[2] == row[2] or row[2] and not new_row[2] or not row[2] and new_row[2]):
                    for k in range(3, len(row)):
                        if not contacts_list[i][k]:
                            contacts_list[i][k] = contacts_list[j][k]
                    del contacts_list[j]
                    break
    except IndexError:
        with open('phonebook_from_main.csv', 'w', encoding='utf-8', newline='') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(contacts_list)


if __name__ == '__main__':
    main()
