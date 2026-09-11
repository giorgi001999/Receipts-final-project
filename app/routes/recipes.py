from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    abort,
    current_app
)

from flask_login import login_required, current_user

from app import db
from app.models import Recipe
from app.forms import RecipeForm, DeleteForm
from app.services.spoonacular import search_recipe_nutrition


recipes = Blueprint("recipes", __name__, url_prefix="/recipes")


@recipes.route("/add", methods=["GET", "POST"])
@login_required
def add_recipe():
    form = RecipeForm()

    if form.validate_on_submit():

        recipe = Recipe(
            title=form.title.data,
            short_description=form.short_description.data,
            full_recipe=form.full_recipe.data,
            category=form.category.data,
            prep_time=form.prep_time.data,
            servings=form.servings.data,
            author_id=current_user.id
        )

        db.session.add(recipe)
        db.session.commit()

        current_app.logger.info(
            "Recipe created: '%s' by user %s",
            recipe.title,
            current_user.email
        )

        return redirect(url_for("main.home"))

    return render_template(
        "recipes/add.html",
        form=form
    )


@recipes.route("/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    delete_form = DeleteForm()

    nutrition = None

    try:
        nutrition = search_recipe_nutrition(recipe.title)

    except Exception as error:
        current_app.logger.error(
            "Spoonacular API error for recipe '%s': %s",
            recipe.title,
            error
        )

    return render_template(
        "recipes/detail.html",
        recipe=recipe,
        delete_form=delete_form,
        nutrition=nutrition
    )


@recipes.route(
    "/<int:recipe_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.author_id != current_user.id:
        current_app.logger.warning(
            "Unauthorized edit attempt by %s for recipe %s",
            current_user.email,
            recipe.id
        )

        abort(403)

    form = RecipeForm(obj=recipe)

    if form.validate_on_submit():

        recipe.title = form.title.data
        recipe.short_description = form.short_description.data
        recipe.full_recipe = form.full_recipe.data
        recipe.category = form.category.data
        recipe.prep_time = form.prep_time.data
        recipe.servings = form.servings.data

        db.session.commit()

        current_app.logger.info(
            "Recipe updated: '%s' by user %s",
            recipe.title,
            current_user.email
        )

        return redirect(
            url_for(
                "recipes.recipe_detail",
                recipe_id=recipe.id
            )
        )

    return render_template(
        "recipes/edit.html",
        form=form,
        recipe=recipe
    )


@recipes.route(
    "/<int:recipe_id>/delete",
    methods=["POST"]
)
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.author_id != current_user.id:
        current_app.logger.warning(
            "Unauthorized delete attempt by %s for recipe %s",
            current_user.email,
            recipe.id
        )

        abort(403)

    current_app.logger.info(
        "Recipe deleted: '%s' by user %s",
        recipe.title,
        current_user.email
    )

    db.session.delete(recipe)
    db.session.commit()

    return redirect(url_for("main.home"))