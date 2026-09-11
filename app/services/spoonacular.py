import os

import requests
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("SPOONACULAR_API_KEY")

BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"


def search_recipe_nutrition(recipe_title):
    params = {
        "apiKey": API_KEY,
        "query": recipe_title,
        "addRecipeNutrition": True,
        "number": 1
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        return None

    recipe = data["results"][0]

    nutrition = recipe.get("nutrition")

    if not nutrition:
        return None

    return nutrition