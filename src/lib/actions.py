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


def _read_countries() -> list:
    """Lee el CSV y devuelve una lista de países.

    Cada país se representa como [nombre, poblacion, superficie, continente].
    En caso de no haber países en el archivo, devuelve una lista vacía.
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
        name: str,
        population: int,
        surface: str
) -> int:
    """
    Esta función valida los datos de entrada y, si son válidos,
    actualiza los datos del país. Retorna 0 si la operación fue
    exitosa o 1 si la operación falló
    """
    try:
        if name is not None:
            name = validate_string(name)
        population = validate_integer(population)
        surface = validate_integer(surface)
    except (ValueError, TypeError):
        return 1

    countries = _read_countries()

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


def search_country_by_name(name: str) -> list | None:
    """Busca países por nombre. Devuelve una lista
    con coincidencias exactas o parciales. De otra
    manera, devuelve None.
    """
    try:
        name = validate_string(name)
    except ValueError:
        return None
    
    countries = _read_countries()
    result = []
    for country in countries:
        if name.lower() in country[0].lower():
            result.append(country)

    return result


def search_countries_by_continent(continent: str) -> list:
    """Busca países por continente. Retorna una lista
    de países o una lista vacía. 
    """
    try:
        continent = validate_string(continent)
    except ValueError:
        return []

    countries = _read_countries()
    result = []
    for country in countries:
        if continent.lower() == country[3].lower():
            result.append(country)

    return result


def search_countries_by_population_range(
        min_population=None,
        max_population=None
) -> list:
    """Busca países por rango de población. Retorna la lista de países
    o una lista vacía.
    """
    if min_population is not None:
        try:
            min_population = validate_integer(min_population)
        except (ValueError, TypeError):
            return []

    if max_population is not None:
        try:
            max_population = validate_integer(max_population)
        except (ValueError, TypeError):
            return []

    countries = _read_countries()
    result = []
    for country in countries:
        if (max_population is not None) and (country[1] <= max_population):
            result.append(country)
        elif (min_population is not None) and (country[1] >= min_population):
            result.append(country)

    return result


def search_countries_by_surface_range(
        min_surface=None,
        max_surface=None
) -> list:
    """Busca países por rango de superficie. Retorna la lista de países
    o una lista vacía.
    """
    if min_surface is not None:
        try:
            min_surface = validate_integer(min_surface)
        except (ValueError, TypeError):
            return []

    if max_surface is not None:
        try:
            max_surface = validate_integer(max_surface)
        except (ValueError, TypeError):
            return []

    countries = _read_countries()
    result = []
    for country in countries:
        if (min_surface is not None) and (country[2] >= min_surface):
            result.append(country)
        elif (max_surface is not None) and (country[2] <= max_surface):
            result.append(country)
            
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

def average_surface() -> int:
    """Calcula el promedio de la superficie de todos los
    países cargados y devuelve el valor total. Si no hay
    países, devuelve 0.
    """
    countries = _read_countries()
    if not countries:
        return 0

    total = 0
    for country in countries:
        total += country[2]

    return int(total / len(countries))

def countries_per_continent() -> dict:
    """Devuelve un diccionario con los continentes
    como clave y la cantidad de países en ellos
    como valor. En caso de no existir países cargados
    en el archivo .csv, la función devolverá un
    diccionario vacío.
    """
    result = {}
    for country in _read_countries():
        continent = country[3]
        result[continent] = result.get(continent, 0) + 1
    return result

def sort_countries(sort=None, order=None) -> None:
    """Recibe como parámetros el tipo de ordenamiento
    que debe llevar a cabo. Siempre retorna None. 
    """
    countries = _read_countries()
    if not sort:
        return countries

    if sort in ("nombre", "poblacion", "superficie"):
        reverse = order == "desc"
        key_map = {
            "nombre": lambda c: c[0].lower(),
            "poblacion": lambda c: c[1],
            "superficie": lambda c: c[2],
        }

    return sorted(countries, key=key_map[sort], reverse=reverse)

