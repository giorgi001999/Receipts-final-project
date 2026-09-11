from flask import Blueprint, render_template, request

from app.models import Recipe


main = Blueprint("main", __name__)


@main.route("/")
def home():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    sort = request.args.get("sort", "newest")

    query = Recipe.query

    if search:
        query = query.filter(
            Recipe.title.ilike(f"%{search}%") |
            Recipe.short_description.ilike(f"%{search}%")
        )

    if category:
        query = query.filter(
            Recipe.category.ilike(category)
        )

    if sort == "oldest":
        query = query.order_by(Recipe.created_at.asc())
    elif sort == "title":
        query = query.order_by(Recipe.title.asc())
    else:
        query = query.order_by(Recipe.created_at.desc())

    # Pagination
    page = request.args.get("page", 1, type=int)

    recipes = query.paginate(
        page=page,
        per_page=6,
        error_out=False
    )

    categories = Recipe.query.with_entities(
        Recipe.category
    ).distinct().all()

    categories = [item[0] for item in categories]

    return render_template(
        "main/home.html",
        recipes=recipes,
        categories=categories,
        search=search,
        category=category,
        sort=sort
    )
@main.route("/about")
def about():
    return render_template("main/about.html")