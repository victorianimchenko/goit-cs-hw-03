import psycopg2


DB_CONFIG = {
    "dbname": "task_management",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": 5432,
}


def create_tables():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS tasks;
        DROP TABLE IF EXISTS status;
        DROP TABLE IF EXISTS users;
    """)

    cursor.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER REFERENCES status(id),
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    connection.commit()

    cursor.close()
    connection.close()

    print("Tables created successfully.")


if __name__ == "__main__":
    create_tables()