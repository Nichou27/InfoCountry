from flask import Flask, render_template, request, redirect, url_for, flash

from lib.actions import (
    add_country,
    update_population_and_surface,
    search_country_by_name,
    search_countries_by_continent,
    search_countries_by_population_range,
    search_countries_by_surface_range,
    country_with_most_population,
    country_with_least_population,
    average_population,
    average_surface,
    countries_per_continent,
    sort_countries,
    _read_countries,
)

app = Flask(__name__)
app.secret_key = "infocountry-secret-key"


def _to_int(value):
    value = (value or "").strip()
    if value == "":
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return "invalid"


@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    continent = request.args.get("continent", "").strip()
    pop_min = _to_int(request.args.get("pop_min"))
    pop_max = _to_int(request.args.get("pop_max"))
    surf_min = _to_int(request.args.get("surf_min"))
    surf_max = _to_int(request.args.get("surf_max"))
    sort_by = request.args.get("sort", "").strip()
    order = request.args.get("order", "asc").strip()

    errors = []
    if pop_min == "invalid":
        errors.append("El filtro de población mínima no es válido.")
        pop_min = None
    if pop_max == "invalid":
        errors.append("El filtro de población máxima no es válido.")
        pop_max = None
    if surf_min == "invalid":
        errors.append("El filtro de superficie mínima no es válido.")
        surf_min = None
    if surf_max == "invalid":
        errors.append("El filtro de superficie máxima no es válido.")
        surf_max = None

    for error in errors:
        flash(error, "error")

    # Obtener todos los países
    countries = _read_countries()

    # Búsqueda por nombre (parcial o exacta)
    if q:
        countries = search_country_by_name(q)

    # Filtro por continente
    if continent:
        countries = search_countries_by_continent(continent)

    # Filtro por rango de población
    if pop_min or pop_max:
        countries = search_countries_by_population_range(pop_min, pop_max)

    # Filtro por rango de superficie
    if surf_min or surf_max:
        countries = search_countries_by_surface_range(surf_min, surf_max)

    # Ordenamiento
    if sort_by is not None or order is not None:
        countries = sort_countries(sort_by, order)

    # Estadísticas (sobre todos los países, no filtrados)
    all_countries = _read_countries()
    most = country_with_most_population()
    least = country_with_least_population()
    avg_pop = average_population()
    avg_surf = average_surface()
    per_continent = countries_per_continent()

    continents = sorted({c[3] for c in all_countries})

    return render_template(
        "index.html",
        countries=countries,
        q=q,
        continent=continent,
        pop_min=request.args.get("pop_min", ""),
        pop_max=request.args.get("pop_max", ""),
        surf_min=request.args.get("surf_min", ""),
        surf_max=request.args.get("surf_max", ""),
        sort_by=sort_by,
        order=order,
        continents=continents,
        most=most,
        least=least,
        avg_pop=avg_pop,
        avg_surf=avg_surf,
        per_continent=per_continent,
    )


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name", "").strip()
    population = request.form.get("population", "").strip()
    surface = request.form.get("surface", "").strip()
    continent = request.form.get("continent", "").strip()

    if not name or not population or not surface or not continent:
        flash("No se permiten campos vacíos.", "error")
        return redirect(url_for("index"))

    result = add_country(name, population, surface, continent)
    if result == 0:
        flash("País agregado correctamente.", "success")
    else:
        flash("Error al agregar el país. Verifique los datos.", "error")
    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update():
    name = request.form.get("name", "").strip()
    population = request.form.get("population", "").strip()
    surface = request.form.get("surface", "").strip()

    if not name or not population or not surface:
        flash("No se permiten campos vacíos.", "error")
        return redirect(url_for("index"))

    result = update_population_and_surface(name, population, surface)
    if result == 0:
        flash("Datos actualizados correctamente.", "success")
    else:
        flash("Error al actualizar. Verifique el nombre y los datos.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
