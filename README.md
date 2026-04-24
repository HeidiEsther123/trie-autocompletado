# Sistema de Autocompletado con Trie 

> **Proyecto Final — Estructura de Datos · Unidad 3**  
> Giovana Díaz y Heidi Peña | Grupo 2A | 2do cuatrimestre  
> Tecnológico de Software — Abril 2026

---

## Descripción

Sistema interactivo de autocompletado basado en un **Árbol de Prefijos (Trie)**, implementado en Python con interfaz gráfica (Tkinter). Permite insertar palabras, buscar por prefijo en tiempo real y comparar el rendimiento del Trie frente a una búsqueda lineal.

---

## Características

- **Autocompletado en tiempo real** — sugerencias al escribir cada carácter
- **Análisis de complejidad** — visualización de Big-O para cada operación
- **Benchmark integrado** — comparación experimental Trie vs. Lista lineal
- **4 conjuntos de datos predefinidos** — Programación, Países, Gastronomía mexicana, Animales
- **Inserción dinámica** — agrega tus propias palabras en tiempo de ejecución
- **Ordenación por frecuencia** — las sugerencias más usadas aparecen primero

---

## Complejidad computacional

| Operación | Trie | Lista lineal | Ganador |
|---|---|---|---|
| Inserción | O(m) | O(1) amortizado | Lista |
| Búsqueda exacta | O(m) | O(n·m) | **Trie** |
| Autocompletado | O(p + k) | O(n·m) | **Trie** |
| Espacio total | O(n·m) | O(n·m) | Empate |
| Escala con n grande | Constante | Lineal | **Trie** |

> `m` = longitud de la palabra · `p` = longitud del prefijo · `k` = resultados devueltos · `n` = total de palabras

**Ventaja clave:** la búsqueda por prefijo es O(p), completamente independiente de n. Con 1,000,000 palabras, encontrar `"pro"` toma exactamente los mismos 3 pasos que con 10 palabras.

---

## Estructura del proyecto

```
trie-autocomplete/
│
├── trie_app.py       # Código fuente principal
└── README.md
```

---

## Requisitos

- Python 3.10 o superior
- `tkinter` (incluido en la instalación estándar de Python)

No se requieren dependencias externas.

---

## Instalación y uso

```bash
# Clona o descarga el repositorio
git clone <url-del-repo>
cd trie-autocomplete

# Ejecuta la aplicación
python trie_app.py
```

---

## Estructura interna del Trie

```python
class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}  # carácter → hijo
        self.is_end: bool = False                 # ¿termina una palabra aquí?
        self.freq: int = 0                        # frecuencia de uso
```

Cada nodo representa un carácter. El camino desde la raíz hasta un nodo marcado con `is_end = True` forma una palabra válida.

---

## Algoritmos principales

### `insert(word)` — O(m)
Recorre cada carácter de la palabra. Si el carácter no existe como hijo, crea un nuevo `TrieNode`. Al terminar, marca el nodo final con `is_end = True` e incrementa su frecuencia.

### `_find_prefix_node(prefix)` — O(p)
Desciende el árbol siguiendo cada carácter del prefijo. Si algún carácter no existe, el prefijo no está en el Trie y retorna `None`.

### `autocomplete(prefix, limit)` — O(p + k)
1. Localiza el nodo del prefijo → O(p)  
2. DFS del subárbol para recolectar palabras → O(k)  
3. Ordena por frecuencia descendente → O(k log k)

---

## Módulos de la interfaz

| Pestaña | Descripción |
|---|---|
| **Demo** | Búsqueda interactiva en tiempo real con estadísticas |
| **Complejidad** | Explicación visual de Big-O y comparación con lista lineal |
| **Benchmark** | Medición experimental de tiempos de inserción y búsqueda |
| **Código** | Visualización del código fuente completo |

---

## Resultados experimentales

Con 200 palabras y 10 consultas de autocompletado:

- **Trie:** < 1 µs por búsqueda
- **Lista lineal:** entre 5 y 15 µs según el prefijo

---

## Limitaciones

- Capacidad máxima de **200 palabras** (configurable vía `Trie.MAX_WORDS`)
- No maneja similitud fonética ni corrección de errores tipográficos
- Mayor uso de memoria frente a una lista simple en vocabularios muy pequeños

---

## Casos de prueba

| Prefijo | Resultado |
|---|---|
| `"al"` | 4 coincidencias: algoritmo, álgebra, almacén, álamo |
| `"árb"` | 2 coincidencias: árbol, árbol binario |
| `"pro"` | 3 coincidencias: proceso, programa, protocolo |
| `"a"` | 10 sugerencias (límite), ordenadas por frecuencia |
| `"xyz"` | 0 coincidencias → mensaje de sin resultados |
| `" "` | Sin búsqueda activa → mensaje de instrucción |

---

## Autoras

**Giovana Díaz** y **Heidi Peña**  
Grupo 2A · 2do cuatrimestre · Tecnológico de Software
