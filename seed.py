import random

import psycopg2
from faker import Faker


DB_CONFIG = {
    "dbname": "task_management",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": 5432,
}


fake = Faker()


def seed_database():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Додаємо статуси
    statuses = ["new", "in progress", "completed"]

    for status_name in statuses:
        cursor.execute(
            """
            INSERT INTO status (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
            """,
            (status_name,),
        )

    # Додаємо користувачів
    user_ids = []

    for _ in range(10):
        fullname = fake.name()
        email = fake.unique.email()

        cursor.execute(
            """
            INSERT INTO users (fullname, email)
            VALUES (%s, %s)
            RETURNING id;
            """,
            (fullname, email),
        )

        user_id = cursor.fetchone()[0]
        user_ids.append(user_id)

    # Отримуємо id статусів
    cursor.execute("SELECT id FROM status;")
    status_ids = [row[0] for row in cursor.fetchall()]

    # Додаємо випадкові завдання
    for _ in range(30):
        title = fake.sentence(nb_words=5)

        # Іноді залишаємо description порожнім,
        # щоб можна було протестувати відповідний SQL-запит.
        description = (
            fake.text(max_nb_chars=200)
            if random.choice([True, True, False])
            else None
        )

        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)

        cursor.execute(
            """
            INSERT INTO tasks (
                title,
                description,
                status_id,
                user_id
            )
            VALUES (%s, %s, %s, %s);
            """,
            (
                title,
                description,
                status_id,
                user_id,
            ),
        )

    connection.commit()

    cursor.close()
    connection.close()

    print("Database seeded successfully.")


if __name__ == "__main__":
    seed_database()