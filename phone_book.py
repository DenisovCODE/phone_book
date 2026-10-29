from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ

# ---------- Шаг 1: разбор ФИО ----------
# Без регулярок: склеиваем первые три поля через пробел и делим по пробелу.
header, data = contacts_list[0], contacts_list[1:]

for contact in data:
    fio = " ".join(contact[:3]).split(" ")
    # Убираем возможные пустые элементы (двойные пробелы)
    fio = [part for part in fio if part]
    # Добиваем до трёх элементов пустыми строками
    while len(fio) < 3:
        fio.append("")
    contact[0], contact[1], contact[2] = fio[0], fio[1], fio[2]

# ---------- Шаг 2: форматирование телефонов (регулярки — по условию) ----------
def format_phone(phone: str) -> str:
    if not phone:
        return ""
    digits = re.sub(r"\D", "", phone)
    ext = ""
    ext_match = re.search(r"(?:доб\.?|ext\.?)\s*(\d+)", phone, flags=re.IGNORECASE)
    if ext_match:
        ext = ext_match.group(1)
        digits = digits[:11]
    if len(digits) == 11 and digits[0] in ("7", "8"):
        digits = "7" + digits[1:]
    elif len(digits) == 10:
        digits = "7" + digits
    if len(digits) != 11:
        return phone.strip()
    result = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    if ext:
        result += f" доб.{ext}"
    return result

for contact in data:
    contact[5] = format_phone(contact[5])

# ---------- Шаг 3: объединение дублей ----------
merged = {}
order = []

for contact in data:
    key = (contact[0].lower(), contact[1].lower())
    if key not in merged:
        merged[key] = contact[:]
        order.append(key)
    else:
        existing = merged[key]
        for i in range(len(contact)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]

contacts_list = [header] + [merged[k] for k in order]

# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)