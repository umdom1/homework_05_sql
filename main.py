import config
import psycopg2


db_conn = psycopg2.connect (database=config.database, user=config.user, password=config.password)
print(f"Вы подключились к базе данных {config.database}")


def create_structure():
    with db_conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE person(person_id integer PRIMARY KEY, person_name varchar(40) NOT NULL, person_surname "
            "varchar(40) NOT NULL, "
            "person_email varchar(40) NOT NULL);")
        cur.execute(
            "CREATE TABLE phone(phone_id integer PRIMARY KEY, phone_number varchar(12) NOT NULL, person_id integer "
            "REFERENCES person(person_id) NOT NULL);")
    db_conn.commit()


def create_new_person(person_id, name, surname, email):
    with db_conn.cursor() as cur:
        cur.execute("INSERT INTO person VALUES (%s, %s, %s, %s);", (person_id, name, surname, email))
    print('Новые данные добавленны')
    db_conn.commit()


def create_new_phone(phone_id, phone, person_id):
    with db_conn.cursor() as cur:
        cur.execute("INSERT INTO phone VALUES (%s, %s, %s);", (phone_id, phone, person_id))
    print('Телефон дбавлен')
    db_conn.commit()


def update_person():
    with db_conn.cursor() as cur:
        update_dict = {}
        update_id = int(input('Введите person_id: '))
        name = str(input('Если хотите обновить "Имя" введите его, для продолжения нажмите enter: '))
        if name != '':
            update_dict['person_name'] = name
        surname = str(input('Если хотите обновить "Фамилию" введите его, для продолжения нажмите enter: '))
        if surname != '':
            update_dict['person_surname'] = surname
        email = str(input('Если хотите обновить "email" введите его, для продолжения нажмите enter: '))
        if email != '':
            update_dict['person_email'] = email
        for key, value in update_dict.items():
            cur.execute('UPDATE person SET "%d" = "%d" WHERE person_id=%d;', (key, value, update_id))
    print('Данные обновленны')
    db_conn.commit()


def delete_phone(phone_id):
    with db_conn.cursor() as cur:
        cur.execute("DELETE FROM phone WHERE person_id=%s", (phone_id))


def delete_person(person_id):
    with db_conn.cursor() as cur:
        cur.execute("SELECT phone_number FROM phone WHERE person_id=%s", (person_id))
        result = cur.fetchall()
        if len(result) == 0:
            cur.execute("DELETE FROM person WHERE person_id=%s;", (person_id))
        else:
            cur.execute("DELETE FROM phone WHERE person_id=%s", (person_id))
            cur.execute("DELETE FROM person WHERE person_id=%s;", (person_id))
    print(f'Данные по person_id: {person_id} удалены из базы данных')
    db_conn.commit()


def search_person():
    with db_conn.cursor() as cur:
        search_dict = {}
        name = str(input('Чтобы включить в поиск "Имя" введите его, для продолжения нажмите enter: '))
        if name != '':
            search_dict['person_name'] = name
        surname = str(input('Чтобы включить в поиск  "Фамилию" введите его, для продолжения нажмите enter: '))
        if surname != '':
            search_dict['person_surname'] = surname
        email = str(input('Чтобы включить в поиск  "email" введите его, для продолжения нажмите enter: '))
        if email != '':
            search_dict['person_email'] = email
        number = str(input('Чтобы включить в поиск  "телефон" введите его, для продолжения нажмите enter: '))
        if number != '':
            search_dict['phone_number'] = number

        search_list = []
        for key, value in search_dict.items():
            e = str(key + " = " + "'" + value + "'")
            search_list.append(e)

        date = " AND ".join(search_list)
        sql = "SELECT person_name, person_surname, person_email, phone_number " \
              "FROM person " \
              "LEFT JOIN phone on person.person_id = phone.person_id " \
              "WHERE " + (date) + ";"

        cur.execute(sql)

        result = cur.fetchall()
        print(result)


