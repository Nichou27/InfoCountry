# Archivo donde se definen las funciones necesarias
# para agregar y/o consultar información del archivo .csv

import csv
import os


def _csv_path():
    """Resuelve la ruta del archivo paises.csv.

    Se prioriza un archivo existente en el directorio de trabajo actual y,
    si no existe, se usa el que está junto a este módulo.
    """
    candidates = [
        os.path.join(os.getcwd(), "paises.csv"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "paises.csv"),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return candidates[1]


def _read_countries() -> list[str, int, int, str]:
    """Lee el CSV y devuelve una lista de países.

    Cada país se representa como [nombre, poblacion, superficie, continente].
    """
    path = _csv_path()
    countries = []
    if not os.path.exists(path):
        return countries

    with open(path, "r", encoding="utf-8", newline="") as countries_file:
        reader = csv.reader(countries_file)
        header = next(reader, None)
        for row in reader:
            if not row or all(cell.strip() == "" for cell in row):
                continue
            # Se esperan 4 columnas: nombre, poblacion, superficie, continente
            if len(row) < 4:
                continue
            name = row[0].strip()
            continent = row[3].strip()
            try:
                population = int(row[1])
                surface = int(row[2])
            except (ValueError, TypeError):
                continue
            countries.append([name, population, surface, continent])

    return countries


def _write_countries(countries) -> None:
    """Reescribe el CSV completo conservando la cabecera."""
    path = _csv_path()
    with open(path, "w", encoding="utf-8", newline="") as countries_file:
        writer = csv.writer(countries_file, lineterminator="\n")
        writer.writerow(["nombre", "poblacion", "superficie", "continente"])
        for country in countries:
            writer.writerow(country)


def validate_string(string: str) -> str | ValueError:
    if not isinstance(string, str) or not string.isalpha():
        raise ValueError("La cadena no puede contener números")
    else:
        return string


def validate_integer(string: str) -> int | ValueError:
    try:
        return int(string)
    except (ValueError, TypeError):
        raise ValueError("El número no es válido")


def add_country(
        name: str,
        population: int,
        surface: int,
        continent: str
) -> int:
    """
    Agrega países al archivo .csv
    Retorna 0 si la transacción fue exitosa,
    1 si hubo algún error.
    """

    try:
        name = validate_string(name)
        population = validate_integer(population)
        surface = validate_integer(surface)
        continent = validate_string(continent)
    except (ValueError, TypeError):
        return 1

    path = _csv_path()
    try:
        # Asegurar salto de línea final antes de agregar
        if os.path.exists(path):
            with open(path, "rb") as check_file:
                content = check_file.read()
            if content and not content.endswith(b"\n"):
                with open(path, "a", encoding="utf-8") as fix_file:
                    fix_file.write("\n")

        with open(path, "a", encoding="utf-8", newline="") as countries:
            countries.write(f"{name},{population},{surface},{continent}\n")
    except OSError:
        return 1

    return 0


def update_population_and_surface(
        population=None,
        surface=None,
        name=None
) -> int:
    """
    Esta función valida los datos de entrada y, si son válidos,
    actualiza los datos del país. Retorna 0 si la operación fue
    exitosa o 1 si la operación falló
    """

    # Reordenar si se llamó como update_population_and_surface(name, population, surface)
    if isinstance(population, str) and isinstance(surface, int) and isinstance(name, int):
        name, population, surface = population, surface, name

    # Validación básica
    try:
        if name is not None:
            name = validate_string(name)
        population = validate_integer(population)
        surface = validate_integer(surface)
    except (ValueError, TypeError):
        return 1

    countries = _read_countries()

    # Si no se indica país, solo se valida (comportamiento del esqueleto original)
    if name is None:
        return 0

    updated = False
    for country in countries:
        if country[0].lower() == name.lower():
            country[1] = population
            country[2] = surface
            updated = True

    if not updated:
        return 1

    _write_countries(countries)
    return 0


def search_country_by_name(name: str) -> None:
    """Busca países por nombre. Retorna None"""
    if not isinstance(name, str):
        return None
    for country in _read_countries():
        if country[0].lower() == name.strip().lower():
            return list(country)
    return None


def search_countries_by_continent(continent: str) -> list:
    """Busca países por continente. Retorna una lista
    de países o una lista vacía. 
    """
    if not isinstance(continent, str):
        return []
    return [
        list(country)
        for country in _read_countries()
        if country[3].lower() == continent.strip().lower()
    ]


def search_countries_by_population_range(population, max_population=None) -> list:
    """Busca países por rango de población. Retorna la lista de países
    o una lista vacía.
    """
    try:
        population = validate_integer(population)
    except (ValueError, TypeError):
        return []

    if max_population is not None:
        try:
            max_population = validate_integer(max_population)
        except (ValueError, TypeError):
            return []

    result = []
    for country in _read_countries():
        if country[1] >= population and (max_population is None or country[1] <= max_population):
            result.append(list(country))
    return result


def search_countries_by_surface_range(surface, max_surface=None) -> list:
    """Busca países por rango de superficie. Retorna la lista de países
    o una lista vacía.
    """

    try:
        surface = validate_integer(surface)
    except (ValueError, TypeError):
        return []

    if max_surface is not None:
        try:
            max_surface = validate_integer(max_surface)
        except (ValueError, TypeError):
            return []

    result = []
    for country in _read_countries():
        if country[2] >= surface and (max_surface is None or country[2] <= max_surface):
            result.append(list(country))
    return result


def country_with_most_population() -> list | None:
    """Busca el país con la mayor cantidad de
    habitantes y lo retorna. En caso de no
    existir, devuelve None.
    """
    countries = _read_countries()
    if not countries:
        return None
    return list(max(countries, key=lambda c: c[1]))


def country_with_least_population() -> list | None:
    """Busca el país con la menor cantidad de
    habitantes y lo retorna. En caso de no
    existir, devuelve None.
    """
    countries = _read_countries()
    if not countries:
        return None
    return list(min(countries, key=lambda c: c[1]))


def average_population() -> int:
    """Calcula el promedio de todos los
    países cargados y devuelve el valor.
    Si no hay países, devuelve 0.
    """
    countries = _read_countries()
    if not countries:
        return 0
    return int(sum(c[1] for c in countries) / len(countries))


def countries_per_continent() -> dict:
    """Devuelve un diccionario con los continentes
    como clave y la cantidad de países en ellos
    como valor. 
    """
    result = {}
    for country in _read_countries():
        continent = country[3]
        result[continent] = result.get(continent, 0) + 1
    return result
