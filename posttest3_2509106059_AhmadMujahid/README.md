# CLI Adventure - The Missing Apple

## Deskripsi Program

**CLI Adventure** merupakan game petualangan berbasis Command Line Interface (CLI) yang dibuat menggunakan Python 3.14.2 dengan pendekatan Object-Oriented Programming (OOP).

Pemain berperan sebagai petualang muda di Kota Fernley, Kerajaan Akhetaria. Pemain menjalani event, mengelola perlengkapan, dan menyelesaikan quest **The Missing Apple**, yaitu penyelidikan pencurian apel di ladang Pak Warrey.

Pilihan menghadapi goblin dan Orachulm menentukan hasil penyelidikan. Pertarungan berjalan otomatis; setiap kekalahan mengurangi satu nyawa dan nyawa nol mengakhiri petualangan. Pemain juga memperoleh EXP, dengan lima poin stat pada setiap kenaikan level.

---

# 1. Relasi UML

## Class Diagram

Diagram perlu memuat nama kelas, atribut atau method utama, serta garis relasi. Gambar diagram disimpan sebagai **`images/uml_class_diagram.png`**.

<!-- ![Class Diagram CLI Adventure](images/uml_class_diagram.png) -->

Gambar belum ditambahkan. Setelah PNG tersedia, hapus penanda komentar HTML pada baris gambar di atas.

Acuan kelas untuk menggambar diagram:

| Class | Atribut / method utama |
|---|---|
| Character | `_name`, `_stats`, `__trait_manager`, `get_info()` |
| Player | `_lives`, `level`, `_stat_points`, `inventory`, `equipment` |
| Monster | `rarity`, `monster_type`, `get_info()` |
| Combatant | `owner`, `__health`, `attack(target)` |
| Inventory | `items`, `add_item()`, `remove_item()` |
| Equipment | `main_hand`, `off_hand`, `equip_from_inventory()` |
| Item | `name`, `price`, `description` |
| TraitManager | `traits`, `add_trait()`, `remove_trait()` |
| Event | `_completed`, `get_choices()`, `resolve()`, `validate_choice()` |
| MonsterEvent | `monster`, `get_choices()`, `resolve()` |
| MerchantEvent | `stock`, `get_choices()`, `resolve()` |
| TavernEvent | `rest_cost`, `get_choices()`, `resolve()` |
| StoryEvent | `nodes`, `get_choices()`, `resolve()` |

Relasi yang digambarkan:

```text
Asosiasi:
Combatant ..> Combatant : attack(target)

Agregasi:
Inventory o-- Item

Komposisi:
Player *-- Inventory
Player *-- Equipment
Character *-- TraitManager

Inheritance:
Character <|-- Player
Character <|-- Monster
Event <|-- MonsterEvent
Event <|-- MerchantEvent
Event <|-- TavernEvent
Event <|-- StoryEvent
```

Wajik kosong agregasi dan wajik penuh komposisi ditempatkan pada sisi pemilik. Panah segitiga inheritance mengarah ke superclass. Notasi asosiasi `..>` mengikuti asosiasi/dependensi searah pada Modul 4.

## Asosiasi

`Combatant.attack(target)` menerima Combatant lain sebagai parameter untuk menerima serangan. Target hanya digunakan dalam operasi tersebut dan tidak dimiliki oleh penyerang.

## Agregasi

`Inventory` menampung objek `Item` yang dibuat di luar inventory. Item tetap ada ketika dikeluarkan dan dapat dipindahkan ke equipment atau pedagang, sehingga siklus hidupnya tidak bergantung pada Inventory.

## Komposisi

`Player` membuat objek `Inventory` dan `Equipment` di dalam constructor sebagai bagian internal pemain. `Character` juga membuat `TraitManager` sendiri; objek bagian tersebut dikelola untuk karakter pemiliknya, bukan dibagikan sebagai bagian milik beberapa karakter.

---

# 2. Abstraksi

## Abstract Class dan Abstract Method

Class `Event` pada `code/events/event.py` menggunakan `ABC` dan mempunyai dua abstract method:

```python
class Event(ABC):
    @abstractmethod
    def get_choices(self, session) -> list:
        pass

    @abstractmethod
    def resolve(self, session, choice_id: str, payload=None) -> EventResult:
        pass
```

`get_choices()` menentukan tindakan yang tersedia, sedangkan `resolve()` memproses pilihan pemain. Keduanya wajib diimplementasikan oleh `MonsterEvent`, `MerchantEvent`, `TavernEvent`, dan `StoryEvent`.

## Method Konkret Bersama

`Event.validate_choice()` merupakan method konkret yang digunakan oleh seluruh subclass melalui pemanggilan di dalam `resolve()`. Method ini memastikan event belum selesai, ID pilihan tersedia, dan pilihan tidak terkunci sebelum tindakan diproses.

## Inheritance, super(), dan Atribut Khusus

Setiap subclass Event memanggil `super().__init__(...)` untuk menginisialisasi data bersama, kemudian menambahkan atribut khusus:

| Subclass | Atribut khusus |
|---|---|
| MonsterEvent | `monster` |
| MerchantEvent | `stock` |
| TavernEvent | `rest_cost` |
| StoryEvent | `nodes`, `current_node_id` |

Encapsulation digunakan melalui atribut protected seperti `Event._completed` dan `Player._stat_points`, serta atribut private seperti `Combatant.__health` dan `TraitEntry.__stack`. Property menyediakan pembacaan data, sementara method mengatur perubahan sesuai aturan program.

## Bukti Abstract Class Tidak Dapat Diinstansiasi

Pada `code/testing/posttest_demo.py`, program mencoba membuat Event melalui `try-except TypeError`:

```python
try:
    Event("abstract", "Event abstrak", "Tidak dapat dibuat langsung")
except TypeError as error:
    show_box("1. BUKTI ABSTRAKSI", [type(error).__name__ + ": " + str(error)])
```

Python menolak instansiasi karena dua abstract method belum diimplementasikan. Pada Python 3.14.2, pesan error menyebut abstract method `get_choices` dan `resolve`.

**Screenshot:** simpan kotak bagian **1. BUKTI ABSTRAKSI** sebagai `images/bukti_abstraksi.png`.

<!-- ![Bukti Abstract Class Tidak Dapat Diinstansiasi](images/bukti_abstraksi.png) -->

---

# 3. Polimorfisme

## Polimorfisme melalui Pewarisan

Keempat subclass Event meng-override `get_choices()` dan `resolve()` dengan perilaku berbeda:

| Subclass | Perilaku resolusi |
|---|---|
| MonsterEvent | Memulai pertarungan melawan monster. |
| MerchantEvent | Memproses pembelian, penjualan, atau pergi. |
| TavernEvent | Memulihkan satu nyawa berbayar atau pergi. |
| StoryEvent | Memproses keputusan cerita dan konsekuensinya. |

Fungsi `demonstrate_polymorphism()` memasukkan objek-objek tersebut dalam satu list dan memanggil method yang sama melalui satu loop:

```python
for event in events:
    choices = event.get_choices(session)

    for choice in choices:
        if choice.enabled:
            result = event.resolve(session, choice.choice_id)
            break
```

Perilaku ditentukan oleh implementasi masing-masing objek, bukan pemeriksaan jenis objek di pemanggil.

**Screenshot:** simpan kotak bagian **2. POLIMORFISME VIA PEWARISAN** sebagai `images/polimorfisme_pewarisan.png`.

<!-- ![Polimorfisme melalui Pewarisan](images/polimorfisme_pewarisan.png) -->

## Duck Typing

`Choice` dan `ConditionalChoice` adalah dua class tanpa hubungan pewarisan satu sama lain maupun superclass aplikasi bersama. Keduanya memiliki method `describe()`.

Keduanya dipanggil melalui fungsi `describe_options()` dalam `code/cli/console.py`:

```python
def describe_options(options) -> list[str]:
    descriptions = []

    for option in options:
        description = option.describe()
        descriptions.append(description)

    return descriptions
```

`Choice.describe()` menghasilkan label pilihan biasa. `ConditionalChoice.describe()` menambahkan nama stat dan kesulitan pemeriksaan pada label. Fungsi yang sama digunakan saat menampilkan pilihan permainan.

## Operator Overloading / Magic Method

| Class | Magic method | Penggunaan |
|---|---|---|
| Inventory | `__len__()` | Menghitung jumlah barang melalui `len(inventory)`. |
| Item | `__str__()` | Menampilkan nama, harga, dan deskripsi item. |
| Stats | `__str__()` | Menampilkan lima stat karakter pada profil. |

Magic method tersebut mengikuti bentuk yang diperbolehkan dalam posttest dan digunakan pada output program.

**Screenshot:** simpan kotak bagian **3. DUCK TYPING** dan **4. MAGIC METHOD DAN RELASI** sebagai `images/duck_typing_magic_method.png`.

<!-- ![Duck Typing dan Magic Method](images/duck_typing_magic_method.png) -->

## Menghindari Anti-Pattern

Event diproses melalui method `get_choices()` dan `resolve()`, tanpa rantai `if/elif` yang memilih perilaku berdasarkan tipe Event. Equipment memakai data `allowed_slots`, `occupied_slots`, dan `traits`, sehingga tidak memerlukan cabang terpisah untuk setiap class equipment.

---

# 4. Prinsip SOLID (Opsional)

## Single Responsibility Principle

`Battle` menangani perhitungan pertarungan, event menentukan konsekuensi, dan `cli/console.py` menangani format output. Perubahan bentuk kotak tidak mengharuskan perubahan pada perhitungan battle.

## Open/Closed Principle

`GameSession` memanggil Event melalui kontrak bersama. Perilaku event dapat diperluas melalui subclass tanpa menambah rantai pemeriksaan tipe pada pemanggil; pendaftaran kontennya tetap dilakukan dalam EventDirector.

---

# 5. Output Program

Jalankan permainan dari folder `posttest3_2509106059_AhmadMujahid`:

```bash
python code/main.py
```

Jalankan demonstrasi abstraksi dan polimorfisme:

```bash
python code/testing/posttest_demo.py
```

Alternatif untuk menjalankan seluruh demonstrasi:

```bash
python code/testing/testing.py
```

Demonstrasi dijalankan menggunakan Python 3.14.2 dan menampilkan bukti abstraksi, overriding, duck typing, magic method, relasi objek, serta poin kenaikan level.

**Screenshot permainan:** simpan tampilan cerita atau epilog sebagai `images/output_permainan.png`.

<!-- ![Output Permainan](images/output_permainan.png) -->

**Screenshot pengujian:** simpan kotak **HASIL PENGUJIAN** pada akhir demonstrasi sebagai `images/hasil_pengujian.png`.

<!-- ![Hasil Pengujian](images/hasil_pengujian.png) -->

Gambar belum dibuat. Semua tempat gambar sudah disiapkan di README ini; setelah menambahkan PNG ke folder images, hapus penanda komentar HTML pada baris gambar terkait.
