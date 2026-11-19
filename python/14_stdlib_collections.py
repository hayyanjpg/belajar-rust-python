# Materi 14: Standard Library - collections
# Modul collections menyediakan struktur data khusus yang lebih powerful dari built-in.

from collections import (
    Counter, defaultdict, OrderedDict, namedtuple,
    deque, ChainMap, UserDict, UserList, UserString
)
from typing import NamedTuple

# ============================================
# 1. Counter - Menghitung Elemen
# ============================================
print("=== 1. Counter ===")

# Dari iterable
c = Counter("abracadabra")
print(f"Counter string: {c}")

# Dari list
items = ["apel", "jeruk", "apel", "mangga", "jeruk", "apel"]
c2 = Counter(items)
print(f"Counter list: {c2}")

# Dari dict/mapping
c3 = Counter({"a": 5, "b": 3, "c": 1})
print(f"Counter dict: {c3}")

# Operasi Counter
c_a = Counter(a=3, b=1)
c_b = Counter(a=1, b=2)
print(f"c_a + c_b: {c_a + c_b}")     # penjumlahan
print(f"c_a - c_b: {c_a - c_b}")     # pengurangan (hanya positif)
print(f"c_a & c_b: {c_a & c_b}")     # intersection (min)
print(f"c_a | c_b: {c_a | c_b}")     # union (max)

# Most common
print(f"Top 2: {c.most_common(2)}")

# Elements (ulangi berdasarkan count)
print(f"Elements: {list(c.elements())}")

# ============================================
# 2. defaultdict - Default Value untuk Key Tidak Ada
# ============================================
print("\n=== 2. defaultdict ===")

# defaultdict(list) - grouping
data = [
    ("buah", "apel"),
    ("buah", "jeruk"),
    ("sayur", "wortel"),
    ("buah", "mangga"),
    ("sayur", "bayam"),
]

grouped = defaultdict(list)
for kategori, item in data:
    grouped[kategori].append(item)
print(f"Grouped: {dict(grouped)}")

# defaultdict(int) - counting
text = "hello world"
char_count = defaultdict(int)
for ch in text:
    char_count[ch] += 1
print(f"Char count: {dict(char_count)}")

# defaultdict(set) - unique values per key
unique_grouped = defaultdict(set)
for kategori, item in data:
    unique_grouped[kategori].add(item)
print(f"Unique grouped: {dict(unique_grouped)}")

# defaultdict dengan factory custom
def default_factory():
    return {"count": 0, "items": []}

custom_dd = defaultdict(default_factory)
custom_dd["a"]["count"] += 1
custom_dd["a"]["items"].append("item1")
print(f"Custom factory: {dict(custom_dd)}")

# ============================================
# 3. OrderedDict - Dictionary Urutan Insert (Python 3.7+ dict sudah ordered)
# ============================================
print("\n=== 3. OrderedDict ===")

# OrderedDict masih berguna untuk:
# - move_to_end()
# - popitem(last=True/False)

od = OrderedDict()
od["a"] = 1
od["b"] = 2
od["c"] = 3
print(f"OrderedDict: {od}")

# Move to end
od.move_to_end("a")
print(f"Move 'a' to end: {od}")

# Pop last (LIFO)
last = od.popitem(last=True)
print(f"Pop last: {last}, remaining: {od}")

# Pop first (FIFO)
first = od.popitem(last=False)
print(f"Pop first: {first}, remaining: {od}")

# ============================================
# 4. namedtuple - Tuple dengan Nama Field
# ============================================
print("\n=== 4. namedtuple ===")

# Definisi
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
print(f"Point: {p}, x={p.x}, y={p.y}")

# Unpacking
x, y = p
print(f"Unpacked: x={x}, y={y}")

# _asdict() -> OrderedDict
print(f"As dict: {p._asdict()}")

# _replace() -> new instance dengan field berubah
p2 = p._replace(x=100)
print(f"Replace x: {p2}")

# _fields
print(f"Fields: {p._fields}")

# Default values (Python 3.7+)
from collections import namedtuple
Point3D = namedtuple("Point3D", ["x", "y", "z"], defaults=[0, 0])
p3d = Point3D(1, 2)
print(f"Point3D dengan default: {p3d}")

# NamedTuple dari typing (modern, type hints)
class Person(NamedTuple):
    nama: str
    umur: int
    kota: str = "Unknown"

person = Person("Hayyan", 25)
print(f"Person: {person}, kota: {person.kota}")

# ============================================
# 5. deque - Double-Ended Queue (Cepat di Kedua Ujung)
# ============================================
print("\n=== 5. deque ===")

# Operasi O(1) di kedua ujung
d = deque([1, 2, 3])
d.append(4)       # kanan
d.appendleft(0)   # kiri
print(f"Deque: {d}")

# Pop
print(f"Pop right: {d.pop()}")
print(f"Pop left: {d.popleft()}")

# Extend
d.extend([5, 6])
d.extendleft([-1, -2])  # note: urutan terbalik
print(f"Extended: {d}")

# Rotate
d.rotate(2)   # geser kanan
print(f"Rotate +2: {d}")
d.rotate(-1)  # geser kiri
print(f"Rotate -1: {d}")

# Maxlen - fixed size (auto remove lama)
d_fixed = deque(maxlen=3)
for i in range(10):
    d_fixed.append(i)
print(f"Maxlen 3: {d_fixed}")

# Use case: sliding window
def sliding_window(iterable, n):
    window = deque(maxlen=n)
    for item in iterable:
        window.append(item)
        if len(window) == n:
            yield tuple(window)

print(f"Sliding window 3: {list(sliding_window(range(10), 3))}")

# ============================================
# 6. ChainMap - Gabung Multiple Dict
# ============================================
print("\n=== 6. ChainMap ===")

# Search dalam urutan: dict1 -> dict2 -> dict3
defaults = {"theme": "light", "lang": "en", "font": "sans"}
user_prefs = {"theme": "dark", "lang": "id"}
runtime = {"lang": "jp"}  # override sementara

config = ChainMap(runtime, user_prefs, defaults)
print(f"Config: {dict(config)}")
print(f"  theme: {config['theme']}")   # dari user_prefs
print(f"  lang: {config['lang']}")     # dari runtime (paling awal)
print(f"  font: {config['font']}")     # dari defaults

# Update hanya ke dict pertama
config["theme"] = "auto"
print(f"After update: {dict(config.maps[0])}")

# New child context
new_context = config.new_child({"debug": True})
print(f"New child: {dict(new_context)}")

# ============================================
# 7. UserDict, UserList, UserString - Wrapper Custom
# ============================================
print("\n=== 7. UserDict/UserList/UserString ===")

# Custom dict dengan validasi
class ValidatedDict(UserDict):
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key harus string")
        if key.startswith("_"):
            raise KeyError("Key tidak boleh diawali underscore")
        super().__setitem__(key, value)

vd = ValidatedDict()
vd["nama"] = "Hayyan"
# vd[123] = "invalid"  # TypeError
# vd["_private"] = "x"  # KeyError
print(f"ValidatedDict: {vd.data}")

# Custom list dengan log
class LoggedList(UserList):
    def append(self, item):
        print(f"  [LOG] Append: {item}")
        super().append(item)
    
    def pop(self, i=-1):
        item = super().pop(i)
        print(f"  [LOG] Pop: {item}")
        return item

ll = LoggedList([1, 2])
ll.append(3)
ll.pop()
print(f"LoggedList: {ll.data}")

# ============================================
# 8. Contoh Praktis Kombinasi
# ============================================
print("\n=== 8. Contoh Praktis ===")

# Analisis log server
from collections import Counter
import re

log_entries = [
    '192.168.1.1 - GET /api/users 200',
    '192.168.1.2 - POST /api/login 200',
    '192.168.1.1 - GET /api/posts 404',
    '10.0.0.1 - GET /api/users 200',
    '192.168.1.1 - DELETE /api/users/1 200',
    '192.168.1.3 - GET /api/users 500',
]

# Parse
ip_counter = Counter()
endpoint_counter = Counter()
status_counter = Counter()

for entry in log_entries:
    parts = entry.split()
    ip = parts[0]
    endpoint = parts[2]
    status = parts[3]
    ip_counter[ip] += 1
    endpoint_counter[endpoint] += 1
    status_counter[status] += 1

print(f"Top IP: {ip_counter.most_common(3)}")
print(f"Top Endpoint: {endpoint_counter.most_common(3)}")
print(f"Status: {dict(status_counter)}")

# Graph adjacency list dengan defaultdict
edges = [
    ("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"),
    ("C", "D"), ("D", "E"), ("E", "A")
]

graph = defaultdict(list)
for src, dst in edges:
    graph[src].append(dst)

print(f"Graph: {dict(graph)}")

# BFS dengan deque
def bfs(graph, start):
    visited = set()
    queue = deque([start])
    order = []
    
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
    return order

print(f"BFS dari A: {bfs(graph, 'A')}")

# LRU Cache sederhana dengan OrderedDict
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return None
        # Move to end (recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove least recently used
    
    def __repr__(self):
        return f"LRUCache({list(self.cache.items())})"

lru = LRUCache(3)
lru.put("a", 1)
lru.put("b", 2)
lru.put("c", 3)
print(f"LRU: {lru}")
lru.get("a")  # akses a
lru.put("d", 4)  # b harus keluar (LRU)
print(f"LRU after: {lru}")

# ============================================
# LATIHAN TAMBAHAN
# ============================================
print("\n=== LATIHAN TAMBAHAN ===")

# Latihan 1: Word frequency dengan Counter
def word_frequency(text: str, top_n: int = 10) -> list:
    words = re.findall(r"\b\w+\b", text.lower())
    return Counter(words).most_common(top_n)

sample_text = "Python adalah bahasa pemrograman. Python itu mudah. Belajar Python menyenangkan."
print(f"Word freq: {word_frequency(sample_text, 5)}")

# Latihan 2: Inverted index dengan defaultdict
def build_inverted_index(docs: dict) -> dict:
    index = defaultdict(set)
    for doc_id, text in docs.items():
        words = re.findall(r"\b\w+\b", text.lower())
        for word in words:
            index[word].add(doc_id)
    return {k: sorted(v) for k, v in index.items()}

docs = {
    1: "Python programming language",
    2: "Java programming language",
    3: "Python and Java are popular",
}
index = build_inverted_index(docs)
print(f"Inverted index: {index}")

# Latihan 3: Queue dengan priority (heapq + Counter untuk tie-break)
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0
    
    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1
    
    def pop(self):
        return heapq.heappop(self._queue)[-1]

pq = PriorityQueue()
pq.push("task1", 1)
pq.push("task2", 3)
pq.push("task3", 2)
print(f"Priority queue: {pq.pop()}, {pq.pop()}, {pq.pop()}")

# Latihan 4: Flatten nested list dengan deque
def flatten(nested):
    result = []
    stack = deque([nested])
    while stack:
        current = stack.popleft()
        if isinstance(current, list):
            stack.extendleft(reversed(current))
        else:
            result.append(current)
    return result

nested = [1, [2, [3, 4], 5], 6, [7, 8]]
print(f"Flatten: {flatten(nested)}")

# Latihan 5: Config layering dengan ChainMap
class Config:
    def __init__(self, *layers):
        self.chain = ChainMap(*layers)
    
    def get(self, key, default=None):
        return self.chain.get(key, default)
    
    def set(self, key, value, layer=0):
        self.chain.maps[layer][key] = value
    
    def __getitem__(self, key):
        return self.chain[key]

config = Config(
    {"debug": False, "db_host": "prod"},   # base
    {"db_host": "staging"},                 # env
    {"debug": True}                         # local override
)
print(f"Config: debug={config['debug']}, db_host={config['db_host']}")
config.set("debug", False, layer=0)
print(f"After set base: debug={config['debug']}")