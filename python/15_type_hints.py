# Materi 15: Type Hints - typing module
# Type hints membantu static analysis, IDE support, dan dokumentasi kode.

from typing import (
    List, Dict, Set, Tuple, Optional, Union, Any, Callable,
    TypeVar, Generic, Protocol, Literal, Final, ClassVar,
    overload, final, runtime_checkable, Annotated
)
from typing_extensions import TypedDict, NotRequired, ReadOnly
from dataclasses import dataclass, field
from enum import Enum
import abc

# ============================================
# 1. Basic Type Hints
# ============================================
print("=== 1. Basic Type Hints ===")

# Primitive types
name: str = "Hayyan"
age: int = 25
height: float = 170.5
is_student: bool = True

# Collection types (Python 3.9+ bisa gunakan list[], dict[], dll)
# Python 3.8- butuh import dari typing
numbers: List[int] = [1, 2, 3, 4, 5]
scores: Dict[str, int] = {"math": 90, "english": 85}
unique_ids: Set[int] = {1, 2, 3}
coordinates: Tuple[float, float] = (10.5, 20.3)

# Optional = Union[T, None]
def greet(name: Optional[str] = None) -> str:
    if name is None:
        return "Hello, stranger!"
    return f"Hello, {name}!"

print(f"Greet: {greet()}")
print(f"Greet with name: {greet('Hayyan')}")

# Union - beberapa tipe mungkin
def process(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return f"Number: {value}"
    return f"String: {value}"

print(f"Process int: {process(42)}")
print(f"Process str: {process('hello')}")

# Any - tipe apa saja (hindari jika memungkinkan)
def flexible(value: Any) -> Any:
    return value

# ============================================
# 2. Callable - Type Hint untuk Fungsi
# ============================================
print("\n=== 2. Callable ===")

# Callable[[ArgTypes], ReturnType]
def apply_twice(func: Callable[[int], int], x: int) -> int:
    return func(func(x))

def double(x: int) -> int:
    return x * 2

print(f"Apply twice: {apply_twice(double, 5)}")

# Callback dengan tipe kompleks
from typing import Callable, Awaitable

async def fetch_data(callback: Callable[[str], Awaitable[None]]) -> None:
    data = "data dari server"
    await callback(data)

# ============================================
# 3. TypeVar & Generic
# ============================================
print("\n=== 3. TypeVar & Generic ===")

T = TypeVar("T")
U = TypeVar("U")

# Generic function
def first_item(items: List[T]) -> T:
    return items[0]

print(f"First int: {first_item([1, 2, 3])}")
print(f"First str: {first_item(['a', 'b', 'c'])}")

# Generic class
class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value
    
    def get(self) -> T:
        return self.value
    
    def set(self, value: T) -> None:
        self.value = value

int_box = Box(42)
str_box = Box("hello")
print(f"Int box: {int_box.get()}")
print(f"Str box: {str_box.get()}")

# Multiple type variables
class Pair(Generic[T, U]):
    def __init__(self, first: T, second: U):
        self.first = first
        self.second = second

pair = Pair("key", 123)
print(f"Pair: {pair.first}, {pair.second}")

# Constrained TypeVar
Number = TypeVar("Number", int, float)

def add_numbers(a: Number, b: Number) -> Number:
    return a + b

# add_numbers(1, 2)  # OK
# add_numbers(1.5, 2.5)  # OK
# add_numbers("a", "b")  # Error

# ============================================
# 4. Protocol - Structural Subtyping (Duck Typing)
# ============================================
print("\n=== 4. Protocol ===")

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "Drawing circle"

class Square:
    def draw(self) -> str:
        return "Drawing square"

# Fungsi menerima apapun yang punya method draw()
def render(shape: Drawable) -> None:
    print(f"Render: {shape.draw()}")

render(Circle())
render(Square())

# Protocol dengan attribute
class HasName(Protocol):
    name: str
    def greet(self) -> str: ...

class Person:
    def __init__(self, name: str):
        self.name = name
    def greet(self) -> str:
        return f"Hi, I'm {self.name}"

def say_hello(obj: HasName) -> None:
    print(obj.greet())

say_hello(Person("Hayyan"))

# @runtime_checkable untuk isinstance check
@runtime_checkable
class Serializable(Protocol):
    def to_json(self) -> str: ...

class User:
    def __init__(self, name: str):
        self.name = name
    def to_json(self) -> str:
        return f'{{"name": "{self.name}"}}'

user = User("Hayyan")
print(f"Is Serializable: {isinstance(user, Serializable)}")

# ============================================
# 5. Literal, Final, ClassVar
# ============================================
print("\n=== 5. Literal, Final, ClassVar ===")

# Literal - nilai spesifik
Status = Literal["pending", "success", "error"]
status: Status = "pending"
# status = "unknown"  # Type checker error

def set_status(s: Status) -> None:
    print(f"Status: {s}")

set_status("success")

# Final - konstanta (tidak bisa di-reassign)
MAX_SIZE: Final[int] = 100
API_URL: Final = "https://api.example.com"

# ClassVar - variable class, bukan instance
class Config:
    DEBUG: ClassVar[bool] = False
    VERSION: ClassVar[str] = "1.0.0"
    
    def __init__(self, name: str):
        self.name = name  # instance variable

print(f"Config.DEBUG: {Config.DEBUG}")

# ============================================
# 6. TypedDict - Dictionary dengan Schema
# ============================================
print("\n=== 6. TypedDict ===")

class UserDict(TypedDict):
    id: int
    name: str
    email: str
    age: NotRequired[int]  # optional field
    tags: ReadOnly[List[str]]  # read-only

# Valid
user1: UserDict = {"id": 1, "name": "Hayyan", "email": "hayyan@example.com", "tags": ["dev"]}
print(f"User1: {user1}")

# Dengan field optional
user2: UserDict = {"id": 2, "name": "Test", "email": "test@example.com", "age": 25, "tags": []}
print(f"User2: {user2}")

# Total=False -> semua field optional
class PartialUser(TypedDict, total=False):
    id: int
    name: str
    email: str

partial: PartialUser = {"name": "Partial"}
print(f"Partial: {partial}")

# ============================================
# 7. Dataclass dengan Type Hints
# ============================================
print("\n=== 7. Dataclass ===")

@dataclass
class Product:
    id: int
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def total_with_tax(self, tax_rate: float = 0.1) -> float:
        return self.price * (1 + tax_rate)

product = Product(1, "Laptop", 10000000, tags=["electronics", "sale"])
print(f"Product: {product}")
print(f"With tax: {product.total_with_tax()}")

# Frozen dataclass (immutable)
@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float

p = ImmutablePoint(1.0, 2.0)
# p.x = 10  # Error: frozen

# ============================================
# 8. Overload - Multiple Signatures
# ============================================
print("\n=== 8. Overload ===")

@overload
def process_data(data: int) -> int: ...
@overload
def process_data(data: str) -> str: ...
@overload
def process_data(data: List[int]) -> List[int]: ...

def process_data(data):
    if isinstance(data, int):
        return data * 2
    elif isinstance(data, str):
        return data.upper()
    elif isinstance(data, list):
        return [x * 2 for x in data]
    raise TypeError("Unsupported type")

print(f"Process int: {process_data(5)}")
print(f"Process str: {process_data('hello')}")
print(f"Process list: {process_data([1, 2, 3])}")

# ============================================
# 9. Abstract Base Class (ABC) dengan Type Hints
# ============================================
print("\n=== 9. ABC ===")

class Animal(abc.ABC):
    @abc.abstractmethod
    def make_sound(self) -> str: ...
    
    @abc.abstractmethod
    def move(self) -> None: ...
    
    def sleep(self) -> None:
        print("Zzz...")

class Dog(Animal):
    def make_sound(self) -> str:
        return "Woof!"
    
    def move(self) -> None:
        print("Running...")

dog = Dog()
print(f"Dog sound: {dog.make_sound()}")
dog.move()
dog.sleep()

# ============================================
# 10. Annotated - Metadata Tambahan
# ============================================
print("\n=== 10. Annotated ===")

# Annotated[type, metadata]
# Metadata bisa dipakai untuk validasi, dokumentasi, ORM, dll
from typing import Annotated

# Contoh: validasi range
PositiveInt = Annotated[int, "gt=0"]
EmailStr = Annotated[str, "format=email"]
Username = Annotated[str, "min_length=3", "max_length=20"]

def create_user(
    username: Username,
    email: EmailStr,
    age: PositiveInt
) -> dict:
    return {"username": username, "email": email, "age": age}

user = create_user("hayyan", "hayyan@example.com", 25)
print(f"Created user: {user}")

# ============================================
# 11. Self Type (Python 3.11+)
# ============================================
print("\n=== 11. Self Type ===")

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class Builder:
    def __init__(self):
        self.value = 0
    
    def add(self, x: int) -> Self:
        self.value += x
        return self
    
    def multiply(self, x: int) -> Self:
        self.value *= x
        return self
    
    def build(self) -> int:
        return self.value

result = Builder().add(5).multiply(2).add(10).build()
print(f"Builder result: {result}")

# ============================================
# 12. Type Guard - Narrowing Type
# ============================================
print("\n=== 12. Type Guard ===")

from typing import TypeGuard

def is_str_list(val: List[Any]) -> TypeGuard[List[str]]:
    return all(isinstance(x, str) for x in val)

def process_strings(items: List[Any]) -> None:
    if is_str_list(items):
        # Di sini type checker tahu items adalah List[str]
        print(f"All strings: {', '.join(items)}")
    else:
        print("Not all strings")

process_strings(["a", "b", "c"])
process_strings(["a", 1, "c"])

# ============================================
# 13. Never & NoReturn
# ============================================
print("\n=== 13. Never & NoReturn ===")

from typing import Never, NoReturn

def abort(message: str) -> Never:
    raise RuntimeError(message)

def infinite_loop() -> NoReturn:
    while True:
        pass

# abort("Error!")  # Tidak pernah return
# infinite_loop()  # Tidak pernah return

# ============================================
# 14. Forward Reference
# ============================================
print("\n=== 14. Forward Reference ===")

# Class yang merujuk ke dirinya sendiri
class Node:
    def __init__(self, value: int):
        self.value = value
        self.next: Optional["Node"] = None  # String quote untuk forward ref
    
    def append(self, value: int) -> "Node":
        if self.next is None:
            self.next = Node(value)
        else:
            self.next.append(value)
        return self
    
    def to_list(self) -> List[int]:
        result = [self.value]
        if self.next:
            result.extend(self.next.to_list())
        return result

head = Node(1).append(2).append(3)
print(f"Linked list: {head.to_list()}")

# Python 3.7+: from __future__ import annotations
# membuat semua annotations jadi string otomatis

# ============================================
# 15. Type Checking Tools
# ============================================
print("\n=== 15. Type Checking Tools ===")

# mypy - static type checker
# pip install mypy
# mypy python/15_type_hints.py

# pyright - Microsoft type checker (VS Code)
# pip install pyright
# pyright python/15_type_hints.py

# pyre - Facebook type checker
# pip install pyre-check

# ============================================
# LATIHAN TAMBAHAN
# ============================================
print("\n=== LATIHAN TAMBAHAN ===")

# Latihan 1: Generic Repository Pattern
T = TypeVar("T")

class Repository(Generic[T]):
    def __init__(self):
        self._items: Dict[int, T] = {}
        self._next_id = 1
    
    def add(self, item: T) -> int:
        id_ = self._next_id
        self._items[id_] = item
        self._next_id += 1
        return id_
    
    def get(self, id_: int) -> Optional[T]:
        return self._items.get(id_)
    
    def get_all(self) -> List[T]:
        return list(self._items.values())
    
    def delete(self, id_: int) -> bool:
        if id_ in self._items:
            del self._items[id_]
            return True
        return False

# Usage
user_repo = Repository[Dict[str, Any]]()
user_id = user_repo.add({"name": "Hayyan", "role": "developer"})
print(f"Added user with id: {user_id}")
print(f"Get user: {user_repo.get(user_id)}")

# Latihan 2: Protocol untuk Plugin System
class Plugin(Protocol):
    name: str
    def execute(self, data: Any) -> Any: ...

class UppercasePlugin:
    name = "uppercase"
    def execute(self, data: str) -> str:
        return data.upper()

class ReversePlugin:
    name = "reverse"
    def execute(self, data: str) -> str:
        return data[::-1]

plugins: List[Plugin] = [UppercasePlugin(), ReversePlugin()]
input_data = "hello"
for plugin in plugins:
    input_data = plugin.execute(input_data)
    print(f"After {plugin.name}: {input_data}")

# Latihan 3: TypedDict untuk API Response
class ApiResponse(TypedDict):
    success: bool
    data: NotRequired[Dict[str, Any]]
    error: NotRequired[str]

def handle_response(response: ApiResponse) -> None:
    if response["success"]:
        print(f"Data: {response.get('data', {})}")
    else:
        print(f"Error: {response.get('error', 'Unknown')}")

handle_response({"success": True, "data": {"user": "Hayyan"}})
handle_response({"success": False, "error": "Not found"})

# Latihan 4: Dataclass dengan Post-Init Validation
@dataclass
class Email:
    address: str
    
    def __post_init__(self):
        if "@" not in self.address:
            raise ValueError("Invalid email format")
        self.address = self.address.lower().strip()

try:
    email = Email("  HAYYAN@EXAMPLE.COM  ")
    print(f"Valid email: {email.address}")
except ValueError as e:
    print(f"Error: {e}")

# Latihan 5: Context Manager dengan Type Hints
from contextlib import contextmanager
from typing import Generator

@contextmanager
def timer() -> Generator[float, None, None]:
    import time
    start = time.perf_counter()
    yield start
    end = time.perf_counter()
    print(f"Elapsed: {end - start:.4f}s")

with timer() as start:
    sum(range(1000000))

# Latihan 6: Enum dengan Type Hints
class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

def paint(color: Color) -> str:
    return f"Painting {color.value}"

print(f"Paint: {paint(Color.RED)}")

# Latihan 7: NewType - Distinct Type
from typing import NewType

UserId = NewType("UserId", int)
ProductId = NewType("ProductId", int)

def get_user(user_id: UserId) -> str:
    return f"User {user_id}"

uid = UserId(123)
# pid = ProductId(123)  # Different type
# get_user(pid)  # Type checker error
print(f"Get user: {get_user(uid)}")