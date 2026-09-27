-- 1. Отримати всі завдання певного користувача
SELECT *
FROM tasks
WHERE user_id = 1;


-- 2. Вибрати завдання за певним статусом, наприклад 'new'
SELECT *
FROM tasks
WHERE status_id = (
    SELECT id
    FROM status
    WHERE name = 'new'
);


-- 3. Оновити статус конкретного завдання на 'in progress'
UPDATE tasks
SET status_id = (
    SELECT id
    FROM status
    WHERE name = 'in progress'
)
WHERE id = 1;


-- 4. Отримати користувачів, які не мають жодного завдання
SELECT *
FROM users
WHERE id NOT IN (
    SELECT DISTINCT user_id
    FROM tasks
    WHERE user_id IS NOT NULL
);


-- 5. Додати нове завдання для конкретного користувача
INSERT INTO tasks (
    title,
    description,
    status_id,
    user_id
)
VALUES (
    'New test task',
    'Task created manually',
    (
        SELECT id
        FROM status
        WHERE name = 'new'
    ),
    1
);


-- 6. Отримати всі завдання, які ще не завершено
SELECT *
FROM tasks
WHERE status_id != (
    SELECT id
    FROM status
    WHERE name = 'completed'
);


-- 7. Видалити конкретне завдання
DELETE FROM tasks
WHERE id = 1;


-- 8. Знайти користувачів з певною електронною поштою
SELECT *
FROM users
WHERE email LIKE '%example.com%';


-- 9. Оновити ім'я користувача
UPDATE users
SET fullname = 'Updated User Name'
WHERE id = 1;


-- 10. Отримати кількість завдань для кожного статусу
SELECT
    status.name,
    COUNT(tasks.id) AS task_count
FROM status
LEFT JOIN tasks
    ON status.id = tasks.status_id
GROUP BY status.id, status.name
ORDER BY status.id;


-- 11. Отримати завдання користувачів
-- з певною доменною частиною email
SELECT
    tasks.id,
    tasks.title,
    tasks.description,
    users.fullname,
    users.email
FROM tasks
JOIN users
    ON tasks.user_id = users.id
WHERE users.email LIKE '%@example.com';


-- 12. Отримати список завдань, що не мають опису
SELECT *
FROM tasks
WHERE description IS NULL;


-- 13. Вибрати користувачів та їхні завдання
-- зі статусом 'in progress'
SELECT
    users.id AS user_id,
    users.fullname,
    tasks.id AS task_id,
    tasks.title,
    status.name AS status
FROM users
INNER JOIN tasks
    ON users.id = tasks.user_id
INNER JOIN status
    ON tasks.status_id = status.id
WHERE status.name = 'in progress';


-- 14. Отримати користувачів та кількість їхніх завдань
SELECT
    users.id,
    users.fullname,
    users.email,
    COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks
    ON users.id = tasks.user_id
GROUP BY
    users.id,
    users.fullname,
    users.email
ORDER BY users.id;