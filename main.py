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
    db_conn.commit()


def create_new_phone(phone_id, phone, person_id):
    with db_conn.cursor() as cur:
        cur.execute("INSERT INTO phone VALUES (%s, %s, %s);", (phone_id, phone, person_id))
    db_conn.commit()


def update_person(name, surname, email, person_id):
    with db_conn.cursor() as cur:
        cur.execute("UPDATE person SET person_name=%s, person_surname=%s, person_email=%s WHERE person_id=%s;", (name, surname, email, person_id))
    db_conn.commit()


def delete_phone(phone_id):
    with db_conn.cursor() as cur:
        cur.execute("DELETE FROM phone WHERE person_id=%s", (phone_id))


def delete_person(person_id):
    with db_conn.cursor() as cur:
        cur.execute("DELETE FROM person WHERE person_id=%s;", (person_id))
    db_conn.commit()


def search_person():
    with db_conn.cursor() as cur:
        data = int(input('Выберите критерий для поиска.\n[1] -- Имя\n[2] -- Фамилия\n[3] -- email\n[4] -- Телефон: '))

        if data == 1:
            name = str(input('Введите имя для поиска: '))
            cur.execute(
                    "SELECT person_name, person_surname, person_email, phone_number "
                    "FROM person "
                    "INNER JOIN phone on person.person_id = phone.person_id "
                    "WHERE person_name=%s;", [name])
        elif data == 2:
            surname = str(input('Введите фамилию для поиска: '))
            cur.execute(
                    "SELECT person_name, person_surname, person_email, phone_number "
                    "FROM person "
                    "INNER JOIN phone on person.person_id = phone.person_id "
                    "WHERE person_surname=%s;", [surname])
        elif data == 3:
            email = str(input('Введите email для поиска: '))
            cur.execute(
                    "SELECT person_name, person_surname, person_email, phone_number "
                    "FROM person "
                    "INNER JOIN phone on person.person_id = phone.person_id "
                    "WHERE person_email=%s;", [email])
        elif data == 4:
            phone = str(input('Введите телефон для поиска: '))
            cur.execute(
                    "SELECT person_name, person_surname, person_email, phone_number "
                    "FROM person "
                    "INNER JOIN phone on person.person_id = phone.person_id "
                    "WHERE phone_number=%s;", [phone])
        result = cur.fetchall()
        print(result)

search_person()


