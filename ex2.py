from pymongo import MongoClient
from pymongo.errors import PyMongoError


# Підключення до MongoDB
# Для локальної MongoDB:
MONGO_URL = "mongodb://localhost:27017/"

# Якщо використовуєш MongoDB Atlas, заміни рядок вище
# на свій connection string.


client = MongoClient(MONGO_URL)

db = client["cats_db"]
collection = db["cats"]


def show_all_cats():
    """Виводить усі записи з колекції."""
    try:
        cats = list(collection.find())

        if not cats:
            print("Колекція порожня.")
            return

        for cat in cats:
            print(cat)

    except PyMongoError as e:
        print(f"Помилка при читанні даних: {e}")


def find_cat_by_name():
    """Шукає кота за ім'ям."""
    try:
        name = input("Введіть ім'я кота: ")

        cat = collection.find_one({"name": name})

        if cat:
            print(cat)
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")

    except PyMongoError as e:
        print(f"Помилка при пошуку кота: {e}")


def update_cat_age():
    """Оновлює вік кота за його ім'ям."""
    try:
        name = input("Введіть ім'я кота: ")
        age = int(input("Введіть новий вік кота: "))

        result = collection.update_one(
            {"name": name},
            {"$set": {"age": age}}
        )

        if result.matched_count:
            print(f"Вік кота '{name}' успішно оновлено.")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")

    except ValueError:
        print("Вік повинен бути цілим числом.")

    except PyMongoError as e:
        print(f"Помилка при оновленні віку: {e}")


def add_feature():
    """Додає нову характеристику коту за ім'ям."""
    try:
        name = input("Введіть ім'я кота: ")
        feature = input("Введіть нову характеристику: ")

        result = collection.update_one(
            {"name": name},
            {"$addToSet": {"features": feature}}
        )

        if result.matched_count:
            print(
                f"Характеристику '{feature}' "
                f"додано коту '{name}'."
            )
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")

    except PyMongoError as e:
        print(f"Помилка при додаванні характеристики: {e}")


def delete_cat():
    """Видаляє кота за ім'ям."""
    try:
        name = input("Введіть ім'я кота для видалення: ")

        result = collection.delete_one({"name": name})

        if result.deleted_count:
            print(f"Кота '{name}' успішно видалено.")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")

    except PyMongoError as e:
        print(f"Помилка при видаленні кота: {e}")


def delete_all_cats():
    """Видаляє всі документи з колекції."""
    try:
        result = collection.delete_many({})

        print(
            f"Видалено записів: {result.deleted_count}"
        )

    except PyMongoError as e:
        print(f"Помилка при видаленні записів: {e}")


def create_cat():
    """Створює новий документ з інформацією про кота."""
    try:
        name = input("Введіть ім'я кота: ")
        age = int(input("Введіть вік кота: "))

        features_input = input(
            "Введіть характеристики через кому: "
        )

        features = [
            feature.strip()
            for feature in features_input.split(",")
            if feature.strip()
        ]

        cat = {
            "name": name,
            "age": age,
            "features": features
        }

        result = collection.insert_one(cat)

        print(
            f"Кота додано. ID документа: "
            f"{result.inserted_id}"
        )

    except ValueError:
        print("Вік повинен бути цілим числом.")

    except PyMongoError as e:
        print(f"Помилка при створенні запису: {e}")


def show_menu():
    """Виводить меню програми."""
    print("\n--- MongoDB Cats ---")
    print("1 - Показати всіх котів")
    print("2 - Знайти кота за ім'ям")
    print("3 - Додати кота")
    print("4 - Оновити вік кота")
    print("5 - Додати характеристику")
    print("6 - Видалити кота")
    print("7 - Видалити всіх котів")
    print("0 - Вихід")


def main():
    try:
        # Перевіряємо з'єднання з MongoDB
        client.admin.command("ping")
        print("Підключення до MongoDB успішне.")

    except PyMongoError as e:
        print(f"Не вдалося підключитися до MongoDB: {e}")
        return

    while True:
        show_menu()

        choice = input("Оберіть дію: ")

        if choice == "1":
            show_all_cats()

        elif choice == "2":
            find_cat_by_name()

        elif choice == "3":
            create_cat()

        elif choice == "4":
            update_cat_age()

        elif choice == "5":
            add_feature()

        elif choice == "6":
            delete_cat()

        elif choice == "7":
            delete_all_cats()

        elif choice == "0":
            print("Вихід із програми.")
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()