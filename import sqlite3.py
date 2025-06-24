import sqlite3
import hashlib
import os
import random
import string

# Функция для генерации пароля
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Функция для хэширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Функция для сохранения пароля в БД
def save_password_to_db(password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS passwords (hashed_password TEXT)')
    cursor.execute('INSERT INTO passwords (hashed_password) VALUES (?)', (hashed_password,))
    conn.commit()
    conn.close()

# Функция для проверки пароля
def check_password(input_password):
    hashed_input = hash_password(input_password)
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT hashed_password FROM passwords WHERE hashed_password = ?', (hashed_input,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Пример использования
new_password = generate_password()
print(f"Сгенерированный пароль: {new_password}")
save_password_to_db(new_password)

# Проверка пароля
input_password = input("Введите пароль для проверки: ")
if check_password(input_password):
    print("Пароль верный!")
else:
    print("Пароль неверный!")