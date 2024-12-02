import csv
import re


def format_phone_number(phone):
    if 'доб' in phone:
        pattern = r'(\+7|8)?\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})\s*\(?([доб]*).?\s*(\d+)\)?'
        pattern_replace = r'+7(\2)\3-\4-\5 \6.\7'
    else:
        pattern = r'(\+7|8)?\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})'
        pattern_replace = r'+7(\2)\3-\4-\5'
    return re.sub(pattern, pattern_replace, phone)


def merge_duplicates(contacts):
    unique_contacts = {}
    for contact in contacts[1:]:
        key = (contact[0], contact[1])  # Ключ на основе фамилии и имени
        if key not in unique_contacts:
            unique_contacts[key] = contact
        else:
            # Объединяем данные
            for i in range(len(contact)):
                if not unique_contacts[key][i]:
                    unique_contacts[key][i] = contact[i]
    return [contacts[0]] + list(unique_contacts.values())


def main():
    with open('phonebook_raw.csv', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)

    # Форматируем ФИО и проверяем не пустая ли строка
    for contact in contacts_list[1:]:
        if not contact:
            del contacts_list[contacts_list.index(contact)]
        fio = ' '.join(contact[:3]).split()
        contact[:3] = fio + [''] * (3 - len(fio))

    # Форматируем номера телефонов
    for contact in contacts_list[1:]:
        contact[5] = format_phone_number(contact[5])

    # Объединяем дубликаты
    updated_contacts = merge_duplicates(contacts_list)

    # Записываем результат
    with open('phonebook_from_updated_version.csv', 'w', encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(updated_contacts)


if __name__ == '__main__':
    try:
        main()
        print('Successfully!')
    except Exception as e:
        print(f'Error: {e}')
