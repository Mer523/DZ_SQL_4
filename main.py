import psycopg2

def create_db (cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customer_base (
        id SERIAL PRIMARY KEY, 
        name VARCHAR (80) NOT NULL, 
        surname VARCHAR (100) NOT NULL, 
        email VARCHAR (100) NOT NULL
        );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contact_details (
        phone VARCHAR (11) PRIMARY KEY, 
        client_id INTEGER REFERENCES customer_base(id)
        );
        """)
    return


def add_client (cur, name, surname, email):
    cur.execute("""
        INSERT INTO customer_base (name, surname, email)
        VALUES (%s, %s, %s)
        """, (name, surname,email))
    return
    print(cur.fetcone())

def add_phone(cur, client_id, phone):
    cur.execute("""
        INSERT INTO contact_details (client_id, phone)
        VALUES (%s, %s)
        """, (client_id, phone))
    return client_id
    print(cur.fetcone())


def change_client(cur, id, name = None, surname = None, email = None):
    cur.execute("""
        SELECT * FROM customer_base
        WHERE id = %s
        """, (id, ))
    find = cur.fetchone()
    if name is None:
        name = find[1]
    if surname is None:
        surname = find[2]
    if email is None:
        email = find[3]
    cur.execute("""
        UPDATE customer_base 
        SET name = %s, surname = %s, email = %s
        WHERE id = %s
        """, (name, surname, email, id))
    return id
    print(cur.fetcone())

def delete_phone(cur, phone):
    cur.execute("""
        SELECT * FROM contact_details;
        """)
    cur.execute("""
        DELETE FROM contact_details 
        WHERE phone = %s;
        """, (phone, ))
    return phone
    print(cur.fetchall())
        

def delete_client(cur, id):
    cur.execute("""
        DELETE FROM contact_details
        WHERE client_id = %s
        """, (id,))
    cur.execute("""
        DELETE FROM customer_base 
        WHERE id = %s
        """, (id, ))
    return id
    cur.fetchall()

def find_client(cur, name=None, surname=None, email=None, phone=None):
    if name is None:
        name = "%"
    else:
        name = "%" + name + "%"
    if surname is None:
        surname = "%"
    else:
        surname = "%" + surname + "%"
    if email is None:
        email = "%"
    else:
        email = "%" + email + "%"
    if phone is None:
        cur.execute("""
              SELECT cb.id, cb.name, cb.surname, cb.email, cd.phone FROM customer_base cb
              LEFT JOIN contact_details cd ON cb.id = cd.client_id
              WHERE cb.name LIKE %s AND cb.surname LIKE %s
              AND cb.email LIKE %s
              """, (name, surname, email))
    else:
        cur.execute("""
              SELECT cb.id, cb.name, cb.lastname, cb.email, cd.phone FROM customer_base cb
              LEFT JOIN contact_details cd ON cb.id = cd.client_id
              WHERE cb.name LIKE %s AND cb.surname LIKE %s
              AND cb.email LIKE %s AND cd.phone like %s
              """, (name, surname, email, phone))
    return cur.fetchall()


with psycopg2.connect(database = "tableproject", user = "postgres", password = "postgres") as conn:
    with conn.cursor() as cur:
        create_db(cur)
        conn.commit()
        print("Добавлен клиент ", add_client(cur, "Денис", "Васильев", "DenVas99@goooogl.ru"))
        print("Добавлен клиент ", add_client(cur, "Сережа", "Сыроежкин", "SerSiroejj@janbeh.ru"))
        print("Добавлен клиент ", add_client(cur, "Элис", "Купер", "AliceCooper@googlex.ru"))
        print("Добавлен номер телефона: ", add_phone(cur, 1, 81015242154))
        print("Добавлен номер телефона: ", add_phone(cur, 2, 81021142154))
        print("Добавлен номер телефона: ", add_phone(cur, 3, 91033442154))
        print ("Изменены данные клиента: ", change_client(cur, 3, "Олег", None, None))
        print("Номер телефона : ", delete_phone(cur, "81021142154", ), "удален")
        print("Клиент удалён с id: ", delete_client(cur, 2))
        print("Найденный клиент по имени:")
        print(find_client(cur, "Денис"))
        print("Найденный клиент по email:")
        print(find_client(cur, None, None, "AliceCooper@googlex.ru"))
        print("Найденный клиент по имени, фамилии и email:")
        print(find_client(cur, "Олег", "Купер", "AliceCooper@googlex.ru"))

conn.close()