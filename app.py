from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

def find_matching_recipes(user_ingredients):
    conn = conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'recipes.db'))
    cursor = conn.cursor()
    cursor.execute("SELECT id, dish_name, ingredients FROM recipes")
    recipes = cursor.fetchall()
    matches = []

    for recipe in recipes:
        recipe_id, dish_name, ingredients = recipe
        ingredients_list = ingredients.lower().split(", ")
        match_count = len(set(user_ingredients).intersection(set(ingredients_list)))

        if match_count >= 2:
            matches.append((recipe_id, dish_name))

    conn.close()
    return matches

def get_recipe_by_id(recipe_id):
    conn = conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'recipes.db'))
    cursor = conn.cursor()
    cursor.execute("SELECT dish_name, ingredients, instructions FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()
    conn.close()
    return recipe

@app.route('/', methods=['POST'])
def chatbot():
    data = request.json
    message = data.get('message', '')

    if message.startswith("select"):
        selected_id = int(message.split(" ")[1])
        recipe = get_recipe_by_id(selected_id)
        if recipe:
            dish_name, ingredients, instructions = recipe
            return jsonify({
                "dish_name": dish_name,
                "ingredients": ingredients,
                "instructions": instructions
            })
        else:
            return jsonify({"error": "Recipe not found."})

    else:
        user_ingredients = [ingredient.strip().lower() for ingredient in message.split(",")]
        matches = find_matching_recipes(user_ingredients)

        if matches:
            response = "You can make:\n"
            for recipe_id, dish_name in matches:
                response += f"{recipe_id}: {dish_name}\n"
            response += "\nReply with 'select <id>' to get the recipe."
            return jsonify({"reply": response})
        else:
            return jsonify({"reply": "No matching recipes found."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
