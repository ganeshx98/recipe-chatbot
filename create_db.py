import sqlite3
import os

conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'recipes.db'))
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dish_name TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT NOT NULL
    )
''')

recipes = [
    ("Chicken Stir Fry", "chicken, broccoli, soy sauce, garlic", "1. Cook chicken. 2. Add broccoli. 3. Stir fry with soy sauce and garlic."),
    ("Rice Bowl", "rice, chicken, onion, soy sauce", "1. Cook rice. 2. Saute chicken and onion. 3. Combine everything with soy sauce."),
    ("Pasta Salad", "pasta, tomato, cucumber, olive oil", "1. Boil pasta. 2. Chop veggies. 3. Mix with olive oil.")
]

cursor.executemany('''
    INSERT INTO recipes (dish_name, ingredients, instructions)
    VALUES (?, ?, ?)
''', recipes)

conn.commit()
conn.close()

print("Database created with recipes.")