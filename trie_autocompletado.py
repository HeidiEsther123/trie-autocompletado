import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import time
import random
import string

class TrieNode: 
    """
    Nodo del Trie.
    Cada nodo representa un carácter en el árbol de prefijos.

    Atributos:
        children (dict): mapa carácter → TrieNode hijo
        is_end   (bool): True si el camino hasta aquí forma una palabra completa
        freq     (int) : frecuencia de inserción/uso de la palabra
    """
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end: bool = False
        self.freq: int = 0

class Trie:
    """
    Árbol de Prefijos (Trie).

    Complejidades:
        insert        → O(m)      donde m = longitud de la palabra
        search_prefix → O(p)      donde p = longitud del prefijo
        autocomplete  → O(p + k)  donde k = palabras recuperadas
        espacio total → O(n · m)  peor caso sin prefijos compartidos
    """
    MAX_WORDS = 200 

    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0
        self.node_count = 1   
        self.max_depth = 0
        self._all_words: list[str] = []
   
    def insert(self, word: str) -> bool:
        """
        Inserta una palabra en el Trie carácter a carácter.
        Retorna False si el Trie ya alcanzó MAX_WORDS.
        """
        word = word.lower().strip()
        if not word:
            return False
        if self.word_count >= self.MAX_WORDS and word not in self._all_words:
            return False

        node = self.root
        depth = 0
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
                self.node_count += 1
            node = node.children[ch]
            depth += 1

        if not node.is_end:
            node.is_end = True
            self.word_count += 1
            self._all_words.append(word)

        node.freq += 1
        if depth > self.max_depth:
            self.max_depth = depth
        return True
 
    def _find_prefix_node(self, prefix: str) -> TrieNode | None:
        """
        Desciende el árbol siguiendo cada carácter del prefijo.
        Retorna el nodo final, o None si el prefijo no existe.
        """
        node = self.root
        for ch in prefix.lower():
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _collect(self, node: TrieNode, prefix: str,
                 results: list, limit: int = 10) -> None:
        """
        Recorrido DFS desde 'node' para recolectar palabras del subárbol.
        Añade (palabra, frecuencia) a results hasta alcanzar limit.
        """
        if len(results) >= limit:
            return
        if node.is_end:
            results.append((prefix, node.freq))
        for ch in sorted(node.children.keys()):
            if len(results) >= limit:
                break
            self._collect(node.children[ch], prefix + ch, results, limit)

    def autocomplete(self, prefix: str, limit: int = 10) -> list[tuple[str, int]]:
        """
        Dado un prefijo, retorna hasta `limit` palabras sugeridas,
        ordenadas por frecuencia descendente.

        Pasos:
          1. Localizar el nodo del prefijo → O(p)
          2. DFS del subárbol para colectar palabras → O(k)
          3. Ordenar por frecuencia → O(k log k)
        """
        node = self._find_prefix_node(prefix)
        if node is None:
            return []
        results: list[tuple[str, int]] = []
        self._collect(node, prefix.lower(), results, limit)
        return sorted(results, key=lambda x: x[1], reverse=True)
  
    def search(self, word: str) -> bool:
        node = self._find_prefix_node(word)
        return node is not None and node.is_end
  
    @property
    def words(self) -> list[str]:
        return list(self._all_words)

DATASETS: dict[str, list[str]] = {
    "Programación": [
        "algoritmo", "arreglo", "árbol", "árbol binario", "árbol de prefijos",
        "autocompletado", "búsqueda", "búsqueda binaria", "bucle", "clase",
        "cola", "cola de prioridad", "compilador", "complejidad", "datos",
        "debugger", "función", "grafo", "hash", "herencia", "índice",
        "inserción", "iteración", "java", "javascript", "lista", "lista enlazada",
        "memoria", "método", "módulo", "nodo", "objeto", "operador",
        "parámetro", "pila", "puntero", "python", "queue", "recursión",
        "referencia", "stack", "string", "struct", "tipo", "tupla",
        "variable", "vector", "abstracción", "api", "archivo",
        "binario", "caché", "callback", "ciclo", "cifrado", "clave",
        "colección", "concurrencia", "constante", "contexto", "control",
        "depuración", "diccionario", "dirección", "enlace", "entrada",
        "espacio", "estructura", "excepción", "expresión", "flujo",
        "formato", "framework", "heurística", "importar", "interfaz",
        "kernel", "lambda", "librería", "lógica", "longitud",
        "mapa", "matriz", "montículo", "multihilo", "notación",
        "orden", "paquete", "patrón", "proceso", "programa",
        "protocolo", "prueba", "puerto", "rama", "red neuronal",
        "repositorio", "retorno", "salida", "secuencia", "servidor",
        "sintaxis", "sistema", "socket", "subprograma", "tabla",
        "template", "terminal", "tiempo de ejecución", "token", "transacción",
    ],
    "Países hispanohablantes": [
        "argentina", "bolivia", "brasil", "chile", "colombia",
        "costa rica", "cuba", "ecuador", "el salvador", "españa",
        "guatemala", "honduras", "méxico", "nicaragua", "panamá",
        "paraguay", "perú", "portugal", "puerto rico", "república dominicana",
        "uruguay", "venezuela", "buenos aires", "bogotá", "caracas",
        "lima", "santiago", "quito", "asunción", "montevideo",
        "ciudad de méxico", "madrid", "la habana", "managua", "tegucigalpa",
        "san salvador", "ciudad de panamá", "san josé", "santo domingo", "sucre",
        "latinoamérica", "iberoamérica", "castellano", "hispanoamérica", "caribe",
        "andino", "patagonia", "amazonia", "centroamérica", "sudamérica",
    ],
    "Gastronomía mexicana": [
        "aguachile", "atole", "birria", "carnitas", "ceviche",
        "chalupa", "chilaquiles", "chile en nogada", "chiles rellenos", "churros",
        "cochinita pibil", "elote", "enchilada", "flautas", "gordita",
        "guacamole", "huarache", "menudo", "molcajete", "mole",
        "pambazo", "pozole", "quesadilla", "sopa de lima", "tacos",
        "tamales", "tinga", "tlayuda", "torta", "tortilla",
        "tostada", "tepache", "mezcal", "agua de jamaica", "horchata",
        "nopales", "epazote", "chile pasilla", "chile ancho", "habanero",
        "salsa verde", "salsa roja", "guajillo", "chipotle", "adobo",
        "caldo de pollo", "sopa azteca", "arroz rojo", "frijoles refritos", "pan de muerto",
    ],
    "Animales": [
        "águila", "alacrán", "armadillo", "axolote", "ballena",
        "búho", "caballo", "camaleón", "cangrejo", "cocodrilo",
        "coyote", "delfín", "elefante", "flamenco", "gato",
        "gorila", "guajolote", "iguana", "jaguar", "jirafa",
        "leopardo", "lobo", "mariposa", "murciélago", "nutria",
        "orca", "ocelote", "perro", "quetzal", "serpiente",
        "tapir", "tecolote", "tigre", "tortuga", "venado",
        "víbora", "zorrillo", "ajolote", "borrego", "cabra",
        "caimán", "caracol", "ciervo", "cóndor", "correcaminos",
        "galápago", "guacamaya", "halcón", "hiena", "hormiga",
        "libélula", "lince", "mapache", "mono araña", "mosca",
        "nutria de río", "oso negro", "pájaro carpintero", "puma", "rinoceronte",
    ],
}

PURPLE    = "#7F77DD"
PURPLE_DK = "#534AB7"
GREEN     = "#1D9E75"
CORAL     = "#D85A30"
BG        = "#F8F8F6"
BG2       = "#EFEFED"
FG        = "#1A1A18"
FG2       = "#6B6B65"
BORDER    = "#D3D1C7"
WHITE     = "#FFFFFF"

class AutocompleteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Autocompletado con Trie")
        self.geometry("900x680")
        self.minsize(780, 580)
        self.configure(bg=BG)

        self.trie = Trie()
        self._build_ui()
        self._load_dataset("Programación")

    def _build_ui(self):
        header = tk.Frame(self, bg=PURPLE, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="Sistema de Autocompletado con Trie",
                 bg=PURPLE, fg=WHITE,
                 font=("Helvetica", 16, "bold")).pack()
        tk.Label(header, text="Proyecto Final · Estructura de Datos · Giovana Díaz y Heidi Peña",
                 bg=PURPLE, fg="#C8C4F0",
                 font=("Helvetica", 10)).pack()

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG2, foreground=FG2,
                        padding=[14, 7], font=("Helvetica", 10))
        style.map("TNotebook.Tab",
                  background=[("selected", WHITE)],
                  foreground=[("selected", PURPLE)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=12, pady=12)

        self._tab_demo(nb)
        self._tab_complexity(nb)
        self._tab_benchmark(nb)
        self._tab_code(nb)

    def _tab_demo(self, nb):
        frame = tk.Frame(nb, bg=WHITE)
        nb.add(frame, text="  Demo  ")

        left = tk.Frame(frame, bg=WHITE)
        left.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        right = tk.Frame(frame, bg=BG2, width=260)
        right.pack(side="right", fill="y", padx=(0, 0), pady=0)
        right.pack_propagate(False)

        tk.Label(left, text="Prefijo a buscar", bg=WHITE,
                 fg=FG2, font=("Helvetica", 9, "bold")).pack(anchor="w")

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", self._on_search)
        entry = tk.Entry(left, textvariable=self._search_var,
                         font=("Helvetica", 14), bd=0,
                         bg=BG, fg=FG, insertbackground=PURPLE,
                         relief="flat", highlightthickness=2,
                         highlightcolor=PURPLE, highlightbackground=BORDER)
        entry.pack(fill="x", ipady=8, pady=(4, 0))

        stats_row = tk.Frame(left, bg=WHITE)
        stats_row.pack(fill="x", pady=10)
        self._stat_labels: dict[str, tk.Label] = {}
        for key, title in [("palabras", "Palabras"), ("nodos", "Nodos"),
                            ("profundidad", "Prof. máx."), ("tiempo_us", "µs búsq.")]:
            box = tk.Frame(stats_row, bg=BG2, bd=0, relief="flat")
            box.pack(side="left", expand=True, fill="x", padx=3)
            lv = tk.Label(box, text="—", bg=BG2, fg=PURPLE,
                          font=("Helvetica", 18, "bold"))
            lv.pack(pady=(8, 0))
            tk.Label(box, text=title, bg=BG2, fg=FG2,
                     font=("Helvetica", 8)).pack(pady=(0, 8))
            self._stat_labels[key] = lv
       
        tk.Label(left, text="Sugerencias", bg=WHITE,
                 fg=FG2, font=("Helvetica", 9, "bold")).pack(anchor="w")
        self._suggestions_frame = tk.Frame(left, bg=WHITE)
        self._suggestions_frame.pack(fill="both", expand=True, pady=(4, 0))

        self._limit_label = tk.Label(left, text="", bg=WHITE,
                                     fg=CORAL, font=("Helvetica", 9, "italic"))
        self._limit_label.pack(anchor="w", pady=(6, 0))

        tk.Label(right, text="Palabras en el Trie",
                 bg=BG2, fg=FG2,
                 font=("Helvetica", 9, "bold")).pack(anchor="w", padx=12, pady=(14, 6))

        self._word_listbox = tk.Listbox(right, bg=WHITE, fg=FG,
                                        font=("Helvetica", 10),
                                        selectbackground=PURPLE,
                                        selectforeground=WHITE,
                                        bd=0, relief="flat",
                                        activestyle="none",
                                        highlightthickness=0)
        self._word_listbox.pack(fill="both", expand=True, padx=10)
        self._word_listbox.bind("<Double-Button-1>", self._on_word_click)

        sb = tk.Scrollbar(right, command=self._word_listbox.yview, bg=BG2)
        sb.pack(side="right", fill="y")
        self._word_listbox.config(yscrollcommand=sb.set)

        add_frame = tk.Frame(right, bg=BG2)
        add_frame.pack(fill="x", padx=10, pady=8)
        self._add_var = tk.StringVar()
        add_entry = tk.Entry(add_frame, textvariable=self._add_var,
                             font=("Helvetica", 10), bd=0, bg=WHITE,
                             fg=FG, relief="flat",
                             highlightthickness=1, highlightbackground=BORDER)
        add_entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 4))
        add_entry.bind("<Return>", lambda _: self._add_word())
        tk.Button(add_frame, text="Insertar", bg=PURPLE, fg=WHITE,
                  font=("Helvetica", 9, "bold"), bd=0, padx=8, pady=4,
                  activebackground=PURPLE_DK, activeforeground=WHITE,
                  cursor="hand2", command=self._add_word).pack(side="right")

        tk.Label(right, text="Cargar conjunto predefinido",
                 bg=BG2, fg=FG2, font=("Helvetica", 8)).pack(anchor="w", padx=12, pady=(4, 2))
        self._dataset_var = tk.StringVar(value="Programación")
        combo = ttk.Combobox(right, textvariable=self._dataset_var,
                             values=list(DATASETS.keys()),
                             state="readonly", font=("Helvetica", 10))
        combo.pack(fill="x", padx=10, pady=(0, 4))
        tk.Button(right, text="Cargar", bg=BG, fg=FG,
                  font=("Helvetica", 9), bd=0, pady=4,
                  relief="flat", cursor="hand2",
                  command=lambda: self._load_dataset(self._dataset_var.get())
                  ).pack(fill="x", padx=10, pady=(0, 12))

    def _tab_complexity(self, nb):
        frame = tk.Frame(nb, bg=WHITE)
        nb.add(frame, text="  Complejidad  ")
        canvas = tk.Canvas(frame, bg=WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=WHITE)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        pad = dict(padx=20, pady=6)

        def section(title):
            tk.Label(inner, text=title, bg=WHITE, fg=FG2,
                     font=("Helvetica", 9, "bold")).pack(anchor="w", **pad)

        def card(parent, op, big_o, desc, where):
            c = tk.Frame(parent, bg=BG2, bd=0)
            c.pack(side="left", fill="both", expand=True, padx=5)
            tk.Label(c, text=op, bg=BG2, fg=FG,
                     font=("Helvetica", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 2))
            tk.Label(c, text=big_o, bg=BG2, fg=PURPLE,
                     font=("Helvetica", 22, "bold")).pack(anchor="w", padx=12)
            tk.Label(c, text=desc, bg=BG2, fg=FG2,
                     font=("Helvetica", 9), wraplength=190,
                     justify="left").pack(anchor="w", padx=12, pady=(2, 4))
            tk.Label(c, text=where, bg=WHITE, fg=FG2,
                     font=("Courier", 8)).pack(fill="x", padx=12, pady=(0, 10))

        section("ANÁLISIS DE COMPLEJIDAD TEMPORAL Y ESPACIAL")
        row1 = tk.Frame(inner, bg=WHITE)
        row1.pack(fill="x", padx=20, pady=4)
        card(row1, "Inserción", "O(m)",
             "Recorre carácter a carácter. Crea nodos solo cuando no existen.",
             "m = longitud de la palabra")
        card(row1, "Búsqueda de prefijo", "O(p)",
             "Desciende el árbol siguiendo cada carácter del prefijo.",
             "p = longitud del prefijo")

        row2 = tk.Frame(inner, bg=WHITE)
        row2.pack(fill="x", padx=20, pady=4)
        card(row2, "Recuperar sugerencias", "O(p + k)",
             "Localiza el prefijo O(p), luego DFS para colectar k palabras.",
             "p = prefijo, k = palabras devueltas")
        card(row2, "Espacio total", "O(n·m)",
             "Peor caso sin prefijos compartidos. Los prefijos comunes reducen el uso.",
             "n = palabras, m = longitud media")

        section("COMPARACIÓN VS. BÚSQUEDA LINEAL")
        cols = ["Operación", "Trie", "Lista lineal"]
        rows = [
            ("Inserción",            "O(m)  ✓", "O(1) amortizado  ✓"),
            ("Búsqueda exacta",      "O(m)  ✓", "O(n·m)  ✗"),
            ("Autocompletado",       "O(p+k)  ✓", "O(n·m)  ✗"),
            ("Espacio",              "O(n·m)  ~", "O(n·m)  ~"),
            ("Escala con n grande",  "Constante  ✓", "Lineal  ✗"),
        ]
        tbl = tk.Frame(inner, bg=BG2)
        tbl.pack(fill="x", padx=20, pady=8)
        for ci, col in enumerate(cols):
            tk.Label(tbl, text=col, bg=PURPLE, fg=WHITE,
                     font=("Helvetica", 9, "bold"),
                     padx=12, pady=6, anchor="w").grid(row=0, column=ci,
                     sticky="ew", padx=1, pady=1)
        for ri, row in enumerate(rows, 1):
            for ci, cell in enumerate(row):
                color = GREEN if "✓" in cell else CORAL if "✗" in cell else FG
                bg = WHITE if ri % 2 == 0 else BG2
                tk.Label(tbl, text=cell, bg=bg, fg=color if ci > 0 else FG,
                         font=("Helvetica", 9 if ci > 0 else 9),
                         padx=12, pady=5, anchor="w").grid(
                    row=ri, column=ci, sticky="ew", padx=1, pady=1)
        for ci in range(3):
            tbl.columnconfigure(ci, weight=1)

        section("VENTAJA CLAVE DEL TRIE")
        info = tk.Frame(inner, bg="#EEECfd",
                        highlightthickness=0)
        info.pack(fill="x", padx=20, pady=6)
        tk.Label(info,
                 text=("El tiempo de búsqueda del Trie NO depende de n (número total de palabras), "
                        "solo de la longitud del prefijo p.\n\n"
                        "Con 1 000 000 palabras en el diccionario, buscar el prefijo \"pro\" sigue tomando "
                        "exactamente los mismos 3 pasos que con 10 palabras.\n\n"
                        "La lista lineal, en cambio, revisa cada palabra del corpus en cada consulta."),
                 bg="#EEECfd", fg=PURPLE_DK,
                 font=("Helvetica", 10), wraplength=780, justify="left",
                 padx=16, pady=14).pack()

        section("ESTRUCTURA DE UN NODO")
        code_frame = tk.Frame(inner, bg="#1E1E1E", bd=0)
        code_frame.pack(fill="x", padx=20, pady=6)
        code_text = (
            "class TrieNode:\n"
            "    def __init__(self):\n"
            "        self.children: dict[str, TrieNode] = {}  # carácter → hijo\n"
            "        self.is_end: bool = False                 # ¿termina una palabra?\n"
            "        self.freq: int = 0                        # frecuencia de uso"
        )
        tk.Label(code_frame, text=code_text, bg="#1E1E1E", fg="#D4D4D4",
                 font=("Courier", 10), justify="left",
                 padx=16, pady=12).pack(anchor="w")

    def _tab_benchmark(self, nb):
        frame = tk.Frame(nb, bg=WHITE)
        nb.add(frame, text="  Benchmark  ")

        top = tk.Frame(frame, bg=WHITE)
        top.pack(fill="x", padx=20, pady=14)

        tk.Label(top, text="Tamaño del corpus:", bg=WHITE, fg=FG,
                 font=("Helvetica", 10)).pack(side="left")

        self._bench_size = tk.IntVar(value=100)
        for val in [50, 100, 150, 200]:
            tk.Radiobutton(top, text=f"{val}", variable=self._bench_size,
                           value=val, bg=WHITE, fg=FG,
                           selectcolor=PURPLE, activebackground=WHITE,
                           font=("Helvetica", 10)).pack(side="left", padx=6)

        tk.Button(top, text="Ejecutar benchmark", bg=PURPLE, fg=WHITE,
                  font=("Helvetica", 10, "bold"), bd=0, padx=14, pady=6,
                  activebackground=PURPLE_DK, cursor="hand2",
                  command=self._run_benchmark).pack(side="left", padx=14)

        self._bench_status = tk.Label(top, text="", bg=WHITE, fg=FG2,
                                      font=("Helvetica", 9, "italic"))
        self._bench_status.pack(side="left")

        grid = tk.Frame(frame, bg=WHITE)
        grid.pack(fill="both", expand=True, padx=20, pady=4)

        self._bench_cards: dict[str, dict] = {}
        configs = [
            ("trie_ins",    "Trie — Inserción total",         PURPLE),
            ("list_ins",    "Lista — Inserción total",         CORAL),
            ("trie_search", "Trie — Autocompletado (10 consultas)", PURPLE),
            ("list_search", "Lista — Autocompletado (10 consultas)", CORAL),
        ]
        for idx, (key, title, color) in enumerate(configs):
            row, col = divmod(idx, 2)
            c = tk.Frame(grid, bg=BG2, bd=0)
            c.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
            tk.Label(c, text=title, bg=BG2, fg=FG2,
                     font=("Helvetica", 9)).pack(anchor="w", padx=12, pady=(10, 2))
            val_lbl = tk.Label(c, text="—", bg=BG2, fg=color,
                               font=("Helvetica", 26, "bold"))
            val_lbl.pack(anchor="w", padx=12)
            tk.Label(c, text="microsegundos", bg=BG2, fg=FG2,
                     font=("Helvetica", 8)).pack(anchor="w", padx=12)
            bar_track = tk.Frame(c, bg=BORDER, height=6)
            bar_track.pack(fill="x", padx=12, pady=(6, 14))
            bar_fill = tk.Frame(bar_track, bg=color, height=6, width=0)
            bar_fill.place(x=0, y=0, relheight=1)
            self._bench_cards[key] = {"val": val_lbl, "bar": bar_fill,
                                      "track": bar_track}

        for i in range(2):
            grid.columnconfigure(i, weight=1)
            grid.rowconfigure(i, weight=1)

        self._bench_conclusion = tk.Label(frame, text="", bg=WHITE, fg=PURPLE_DK,
                                          font=("Helvetica", 10),
                                          wraplength=820, justify="left")
        self._bench_conclusion.pack(padx=20, pady=8, anchor="w")

    def _tab_code(self, nb):
        frame = tk.Frame(nb, bg=WHITE)
        nb.add(frame, text="  Código  ")

        text = tk.Text(frame, bg="#1E1E1E", fg="#D4D4D4",
                       font=("Courier", 10), bd=0, relief="flat",
                       wrap="none", padx=16, pady=12,
                       insertbackground=WHITE)
        text.pack(fill="both", expand=True)
        sb_v = tk.Scrollbar(frame, command=text.yview)
        sb_v.pack(side="right", fill="y")
        text.config(yscrollcommand=sb_v.set)

        code = '''# ═══════════════════════════════════════════════
# IMPLEMENTACIÓN COMPLETA DEL TRIE
# ═══════════════════════════════════════════════

class TrieNode:
    """Nodo del árbol de prefijos."""
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end: bool = False  # ¿termina una palabra aquí?
        self.freq: int = 0         # frecuencia de uso

class Trie:
    """
    Árbol de Prefijos (Trie) con límite de 200 palabras.

    Complejidades:
        insert        → O(m)      m = longitud de la palabra
        search_prefix → O(p)      p = longitud del prefijo
        autocomplete  → O(p + k)  k = palabras recuperadas
        espacio       → O(n · m)  peor caso
    """

    MAX_WORDS = 200

    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0
        self.node_count = 1   # la raíz ya existe
        self.max_depth = 0

    # ── Inserción: O(m) ───────────────────────────────
    def insert(self, word: str) -> bool:
        word = word.lower().strip()
        if not word or self.word_count >= self.MAX_WORDS:
            return False

        node = self.root
        depth = 0
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
                self.node_count += 1
            node = node.children[ch]
            depth += 1

        if not node.is_end:
            node.is_end = True
            self.word_count += 1

        node.freq += 1
        self.max_depth = max(self.max_depth, depth)
        return True

    # ── Localizar nodo del prefijo: O(p) ─────────────
    def _find_prefix_node(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix.lower():
            if ch not in node.children:
                return None          # prefijo no encontrado
            node = node.children[ch]
        return node

    # ── DFS para recolectar sugerencias: O(k) ────────
    def _collect(self, node: TrieNode, prefix: str,
                 results: list, limit: int) -> None:
        if len(results) >= limit:
            return
        if node.is_end:
            results.append((prefix, node.freq))
        for ch in sorted(node.children):     # orden alfabético
            if len(results) >= limit:
                break
            self._collect(node.children[ch], prefix + ch, results, limit)

    # ── Autocompletado: O(p + k) ──────────────────────
    def autocomplete(self, prefix: str, limit: int = 10) -> list:
        """
        1. Localizar el nodo del prefijo → O(p)
        2. DFS del subárbol → O(k)
        3. Ordenar por frecuencia → O(k log k)
        """
        node = self._find_prefix_node(prefix)
        if node is None:
            return []
        results = []
        self._collect(node, prefix.lower(), results, limit)
        return sorted(results, key=lambda x: x[1], reverse=True)

# ── Uso básico ────────────────────────────────────────
if __name__ == "__main__":
    trie = Trie()
    words = ["algoritmo", "arreglo", "árbol", "árbol binario",
             "autocompletado", "búsqueda", "bucle", "compilador"]

    for w in words:
        trie.insert(w)

    prefix = "ár"
    suggestions = trie.autocomplete(prefix)
    print(f"Sugerencias para '{prefix}':")
    for word, freq in suggestions:
        print(f"  {word}  (freq={freq})")
'''
        text.insert("1.0", code)
        text.config(state="disabled")

    def _load_dataset(self, name: str):
        self.trie = Trie()
        words = DATASETS.get(name, [])
        for w in words[:Trie.MAX_WORDS]:
            self.trie.insert(w)
        self._refresh_all()

    def _add_word(self):
        word = self._add_var.get().strip()
        if not word:
            return
        ok = self.trie.insert(word)
        if ok:
            self._add_var.set("")
            self._refresh_all()
        else:
            messagebox.showwarning(
                "Límite alcanzado",
                f"El Trie ya contiene {Trie.MAX_WORDS} palabras (límite máximo).\n"
                "Carga un conjunto nuevo para continuar."
            )

    def _on_search(self, *_):
        prefix = self._search_var.get()
        t0 = time.perf_counter()
        suggestions = self.trie.autocomplete(prefix, limit=10) if prefix.strip() else []
        elapsed_us = int((time.perf_counter() - t0) * 1_000_000)

        self._stat_labels["tiempo_us"].config(
            text=f"<1" if elapsed_us < 1 else str(elapsed_us))

   
        for w in self._suggestions_frame.winfo_children():
            w.destroy()

        if not prefix.strip():
            tk.Label(self._suggestions_frame,
                     text="Escribe un prefijo para ver sugerencias...",
                     bg=WHITE, fg=FG2, font=("Helvetica", 10, "italic")
                     ).pack(anchor="w", padx=4, pady=8)
            return

        if not suggestions:
            tk.Label(self._suggestions_frame,
                     text=f'Sin coincidencias para "{prefix}"',
                     bg=WHITE, fg=CORAL, font=("Helvetica", 10, "italic")
                     ).pack(anchor="w", padx=4, pady=8)
            return

        for word, freq in suggestions:
            p = len(prefix)
            row = tk.Frame(self._suggestions_frame, bg=WHITE, cursor="hand2")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=word[:p], bg=WHITE, fg=PURPLE,
                     font=("Helvetica", 12, "bold")).pack(side="left")
            tk.Label(row, text=word[p:], bg=WHITE, fg=FG,
                     font=("Helvetica", 12)).pack(side="left")
            stars = "★" * min(freq, 5)
            tk.Label(row, text=f"  {stars}", bg=WHITE, fg="#C8C055",
                     font=("Helvetica", 10)).pack(side="right")
            row.bind("<Button-1>", lambda e, w=word: self._select_word(w))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, w=word: self._select_word(w))

    def _select_word(self, word: str):
        self._search_var.set(word)
        self.trie.insert(word) 
        self._refresh_all()

    def _on_word_click(self, event):
        sel = self._word_listbox.curselection()
        if sel:
            word = self._word_listbox.get(sel[0])
            self._search_var.set(word)

    def _refresh_all(self):

        self._stat_labels["palabras"].config(text=str(self.trie.word_count))
        self._stat_labels["nodos"].config(text=str(self.trie.node_count))
        self._stat_labels["profundidad"].config(text=str(self.trie.max_depth))

        self._word_listbox.delete(0, "end")
        for w in sorted(self.trie.words):
            self._word_listbox.insert("end", w)

  
        if self.trie.word_count >= Trie.MAX_WORDS:
            self._limit_label.config(
                text=f"⚠ Límite de {Trie.MAX_WORDS} palabras alcanzado")
        else:
            self._limit_label.config(text="")

        self._on_search()

    def _run_benchmark(self):
        n = min(self._bench_size.get(), Trie.MAX_WORDS)
        self._bench_status.config(text="Ejecutando...")
        self.update()

        base_words = []
        for words in DATASETS.values():
            base_words.extend(words)
        corpus = []
        i = 0
        while len(corpus) < n:
            w = base_words[i % len(base_words)]
            corpus.append(w if i < len(base_words) else w + str(i))
            i += 1

        prefixes = ["al", "pro", "ar", "ca", "se", "te", "ma", "bu", "li", "gr"]

        t = Trie()
        t0 = time.perf_counter()
        for w in corpus:
            t.insert(w)
        trie_ins_us = int((time.perf_counter() - t0) * 1_000_000)

        lst = []
        t0 = time.perf_counter()
        for w in corpus:
            lst.append(w)
        list_ins_us = int((time.perf_counter() - t0) * 1_000_000)

        t0 = time.perf_counter()
        for p in prefixes:
            t.autocomplete(p, 10)
        trie_search_us = int((time.perf_counter() - t0) * 1_000_000)

        t0 = time.perf_counter()
        for p in prefixes:
            [w for w in lst if w.startswith(p)][:10]
        list_search_us = int((time.perf_counter() - t0) * 1_000_000)

        results = {
            "trie_ins":    trie_ins_us,
            "list_ins":    list_ins_us,
            "trie_search": trie_search_us,
            "list_search": list_search_us,
        }
        max_ins    = max(trie_ins_us, list_ins_us, 1)
        max_search = max(trie_search_us, list_search_us, 1)

        for key, us in results.items():
            self._bench_cards[key]["val"].config(text=str(us))
            is_search = "search" in key
            max_v = max_search if is_search else max_ins
            pct = us / max_v
            self._bench_cards[key]["bar"].update_idletasks()
            track_w = self._bench_cards[key]["track"].winfo_width()
            self._bench_cards[key]["bar"].place(
                x=0, y=0, relheight=1, width=int(pct * track_w))

        ratio = (list_search_us / max(trie_search_us, 1))
        self._bench_conclusion.config(
            text=(f"Con {n} palabras: el Trie realiza las 10 búsquedas de autocompletado "
                  f"en {trie_search_us} µs, la lista lineal toma {list_search_us} µs "
                  f"({ratio:.1f}× más lento). "
                  f"La ventaja del Trie crece con n porque su búsqueda es O(p), "
                  f"independiente del tamaño del corpus.")
        )
        self._bench_status.config(text=f"Completado — {n} palabras, {len(prefixes)} consultas")

if __name__ == "__main__":
    app = AutocompleteApp()
    app.mainloop()