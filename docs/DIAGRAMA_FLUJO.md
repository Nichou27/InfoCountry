# Diagrama de flujo — Operaciones principales de InfoCountry

El siguiente diagrama está en formato [Mermaid](https://mermaid.js.org/) y puede visualizarse en GitHub, GitLab, VS Code u otros visores de Mermaid.

```mermaid
flowchart TD
    A([Inicio: Usuario abre InfoCountry]) --> B[Menú lateral]
    B --> C{Selección de opción}

    C -->|Países| D[Mostrar directorio de países]
    D --> D1[Leer paises.csv]
    D1 --> D2[Renderizar tabla de países]
    D2 --> B

    C -->|Buscar y filtrar| E[Formulario de búsqueda]
    E --> E1[Ingresar filtros: nombre, continente, población, superficie, orden]
    E1 --> E2[Aplicar filtros sobre paises.csv]
    E2 --> E3{¿Hay resultados?}
    E3 -->|Sí| E4[Mostrar tabla filtrada]
    E3 -->|No| E5[Mostrar: No se encontraron países]
    E4 --> B
    E5 --> B

    C -->|Agregar país| F[Formulario Agregar país]
    F --> F1[Ingresar nombre, población, superficie, continente]
    F1 --> F2{¿Datos válidos?}
    F2 -->|No| F3[Mostrar error: campos vacíos o inválidos]
    F2 -->|Sí| F4{¿País duplicado?}
    F4 -->|Sí| F5[Mostrar error: país ya existe]
    F4 -->|No| F6[Guardar país en paises.csv]
    F6 --> F7[Mostrar éxito: país agregado]
    F3 --> B
    F5 --> B
    F7 --> B

    C -->|Actualizar país| G[Formulario Actualizar país]
    G --> G1[Ingresar nombre, nueva población, nueva superficie]
    G1 --> G2{¿Datos válidos?}
    G2 -->|No| G3[Mostrar error: campos vacíos o inválidos]
    G2 -->|Sí| G4{¿País existe?}
    G4 -->|No| G5[Mostrar error: país no encontrado]
    G4 -->|Sí| G6[Actualizar población y superficie en paises.csv]
    G6 --> G7[Mostrar éxito: datos actualizados]
    G3 --> B
    G5 --> B
    G7 --> B

    C -->|Estadísticas| H[Mostrar panel Estadísticas]
    H --> H1[Leer todos los países de paises.csv]
    H1 --> H2[Calcular mayor y menor población]
    H2 --> H3[Calcular promedios de población y superficie]
    H3 --> H4[Contar países por continente]
    H4 --> H5[Mostrar tarjetas y tabla de distribución]
    H5 --> B

    style A fill:#e2e8f0,stroke:#0f2230,stroke-width:2px
    style B fill:#0f2230,color:#fff,stroke:#14b8a6,stroke-width:2px
    style F2 fill:#fdecea,stroke:#b91c1c,stroke-width:2px
    style F4 fill:#fdecea,stroke:#b91c1c,stroke-width:2px
    style G2 fill:#fdecea,stroke:#b91c1c,stroke-width:2px
    style G4 fill:#fdecea,stroke:#b91c1c,stroke-width:2px
    style E3 fill:#fdecea,stroke:#b91c1c,stroke-width:2px
```

## Resumen de operaciones

| Módulo | Entrada | Proceso principal | Salida |
|--------|---------|-------------------|--------|
| **Países** | — | Leer `paises.csv` | Tabla de países |
| **Buscar y filtrar** | Filtros de usuario | Filtrar por nombre, continente, rangos y orden | Resultados o aviso vacío |
| **Agregar país** | Datos del país | Validar → verificar duplicado → escribir CSV | Mensaje de éxito/error |
| **Actualizar país** | Nombre y nuevos datos | Validar → buscar país → actualizar CSV | Mensaje de éxito/error |
| **Estadísticas** | — | Agregar datos de `paises.csv` | Métricas y distribución por continente |

El archivo de datos persistente es `src/lib/paises.csv`.
