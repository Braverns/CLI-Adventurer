# CLI Adventure - The Missing Apple

## Deskripsi Program

**CLI Adventure** adalah game petualangan berbasis Command Line Interface (CLI) menggunakan Python dan Object-Oriented Programming (OOP).

Setelah Kerajaan Akhetaria menyatukan lima benua, seorang remaja berusia 15 tahun memulai petualangannya di Fernley. Kota terpencil di barat daya kerajaan ini hanya mempunyai satu guild dengan sedikit petualang aktif.

Pemain menerima pekerjaan **The Missing Apple** dari Pak Warrey untuk menyelidiki pencurian apel. Cara menghadapi goblin dan keputusan terhadap Orachulm menentukan penutup petualangan.

Program ini khusus pengumpulan posttest dalam bentuk CLI. Menu, narasi, battle, dan epilog menggunakan bingkai kotak. Seluruh program menggunakan standard library Python 3.14.2; tidak ada paket tambahan yang perlu diinstal.

---

# Fitur Program

1. Dua event awal: monster atau cerita pendek, lalu pedagang atau tavern.
2. Cerita satu pertemuan **Surat di Jembatan**.
3. Quest utama dengan empat pendekatan: serang, interogasi CHA, INT, atau STR.
4. Dua encounter monster selama perjalanan menuju Orachulm.
5. Auto battle satu lawan satu, giliran berdasarkan agility, dan status racun.
6. Setiap kalah battle mengurangi satu nyawa; nyawa nol mengakhiri petualangan.
7. HP combat dan status sementara direset pada battle baru.
8. Inventory sepuluh slot serta equipment dengan tujuh slot.
9. Senjata dua tangan, pergantian equipment, serta penggabungan stack trait.
10. Pedagang mendukung beli dan jual; tavern memulihkan satu nyawa berbayar atau boleh dilewati.
11. EXP, level, dan **tepat 5 poin stat pada setiap kenaikan level**.
12. Enam hasil akhir, termasuk kematian, quest gagal, dan Orc Slayer.

Scope posttest ini berakhir setelah quest utama berhasil atau gagal. Pengembangan game berikutnya merupakan proyek terpisah dari pengumpulan ini.

---

# Cara Menjalankan Program

Gunakan **Python 3.14.2**. Buka terminal pada folder repository, lalu jalankan:

```bash
python posttest3_2509106059_AhmadMujahid/code/main.py
```

Atau, dari folder `posttest3_2509106059_AhmadMujahid`:

```bash
python code/main.py
```

Nama dan seed dapat diberikan langsung:

```bash
python code/main.py --name Bravern --seed 7
```

Seed membantu mengulangi undian dengan rangkaian tindakan yang sama. Tindakan berbeda dapat mengonsumsi angka acak berbeda pula.

## Kontrol

| Input | Fungsi |
|---|---|
| Nomor pilihan | Memilih tindakan pada event aktif. |
| `profil` | Menampilkan karakter, stat, quest, dan reputasi. |
| `inventory` | Menampilkan item, equipment, dan trait aktif. |
| `equip 0` | Memasang item inventory slot 0 pada slot kompatibel yang tersedia. |
| `equip 0 main_hand` | Memilih main hand secara eksplisit untuk penggantian. |
| `unequip main_hand` | Mengembalikan equipment ke inventory. |
| `stat strength 5` | Mengalokasikan lima poin ke strength jika saldo cukup. |
| `bantuan` | Menampilkan petunjuk. |
| `keluar` | Menghentikan sesi tanpa menyimpan progres. |

Stat: `strength`, `agility`, `defense`, `intelligence`, `charisma`.

Slot: `head`, `chest`, `back`, `legs`, `boots`, `main_hand`, `off_hand`. Slot inventory menggunakan indeks mulai dari 0.

Contoh bingkai terminal:

```text
 ________________________________
| PETUALANGAN                    |
|                                |
| 1. Langsung serang goblin       |
| 2. Interogasi menggunakan CHA   |
|________________________________|
```

---

# Struktur Program

```text
posttest3_2509106059_AhmadMujahid/
├── code/
│   ├── main.py
│   ├── cli/            -> format kotak dan driver pendukung
│   ├── core/           -> sesi, pengatur event, enum, hasil aksi
│   ├── characters/     -> Character, Player, Monster, Combatant, Profession
│   ├── combat/         -> Battle
│   ├── inventory/      -> Inventory
│   ├── equipment/      -> Equipment
│   ├── items/          -> Item dan equipment
│   ├── events/         -> ABC Event beserta implementasinya
│   ├── story/          -> Quest dan The Missing Apple
│   ├── content/        -> balancing, katalog, cerita pendek, ending
│   ├── utils/          -> Stats dan sistem trait
│   └── testing/        -> demonstrasi posttest dan peluncur pengujian
├── docs/
│   ├── RANCANGAN.md
│   ├── uml_class_diagram.mmd
│   └── evidence/       -> output teks asli dari eksekusi
├── images/
│   └── README.md       -> daftar gambar yang perlu dibuat
├── tests/
└── README.md
```

Rincian atribut, tanggung jawab setiap file, dan diagram alur terdapat dalam [rancangan program](docs/RANCANGAN.md).

---

# Alur Permainan

```text
Buat karakter
      ↓
Event awal 1: monster / Surat di Jembatan
      ↓
Event awal 2: pedagang / tavern
      ↓
Terima The Missing Apple, langsung malam pertama
      ↓
Serang / interogasi CHA / INT / STR
      ↓
Battle goblin
      ├── kalah → nyawa -1 → quest gagal
      └── menang
            ├── tanpa informasi → melapor → berhasil
            └── dengan informasi → siang hari kedua
                                      ↓
                                Monster perjalanan 1
                                      ↓
                                Monster perjalanan 2
                                      ↓
                                Orachulm, malam kedua
                                  ├── kembali → melapor → berhasil
                                  └── battle
                                        ├── menang → Great Sword + Orc Slayer
                                        └── kalah → nyawa -1 → kabur
                                              ↓
                                            melapor → berhasil
```

Pada semua battle, nyawa nol langsung mengakhiri petualangan. Dua monster perjalanan dihitung sebagai event selesai meskipun pemain kalah tetapi masih hidup; keduanya tidak menggagalkan quest.

Batas tiga hari adalah konteks cerita. Waktu bergerak mengikuti adegan; pemain tidak mempunyai aksi menunggu bebas.

---

# Abstraksi

## Abstract Class `Event`

`Event` menggunakan `ABC` dengan dua abstract method:

```python
class Event(ABC):
    @abstractmethod
    def get_choices(self, session) -> list:
        pass

    @abstractmethod
    def resolve(self, session, choice_id: str, payload=None) -> EventResult:
        pass
```

Kedua method wajib diimplementasikan oleh `MonsterEvent`, `MerchantEvent`, `TavernEvent`, dan `StoryEvent`.

- `get_choices()` menentukan tindakan yang tersedia.
- `resolve()` melaksanakan tindakan dan mengembalikan hasilnya.

## Method Konkret Bersama

`Event.validate_choice()` memeriksa apakah event sudah selesai, apakah pilihan tersedia, dan apakah pilihan terkunci. Seluruh subclass memanggil method konkret ini dari `resolve()`, sehingga validasi dasar tidak perlu disalin.

## Bukti Abstract Class Tidak Bisa Diinstansiasi

Jalankan:

```bash
python code/testing/posttest_demo.py
```

Bagian **BUKTI ABSTRAKSI** mencoba membuat `Event` di dalam `try-except TypeError`. Python menolak karena `get_choices()` dan `resolve()` belum diimplementasikan. Kalimat error tepatnya dapat berbeda menurut versi Python; output sebenarnya disimpan pada [bukti demonstrasi](docs/evidence/posttest_demo.txt).

---

# Inheritance dan Encapsulation

```text
Character
├── Player
└── Monster

Event (ABC)
├── MonsterEvent
├── MerchantEvent
├── TavernEvent
└── StoryEvent

Item
└── EquippableItem
    ├── Weapon
    ├── Armor
    ├── Shield
    └── Accessory
```

Subclass menjalankan constructor parent melalui `super().__init__(...)`. Atribut unik misalnya `MonsterEvent.monster`, `MerchantEvent.stock`, `TavernEvent.rest_cost`, dan `StoryEvent.nodes`.

Atribut protected seperti `Event._completed`, `Player._lives`, dan `Player._stat_points` dikelola melalui method domain. Atribut private `Combatant.__health` dan `TraitEntry.__stack` dibaca melalui property; HP dibatasi antara nol dan maksimum, sedangkan stack invalid ditolak.

---

# Polimorfisme

## 1. Polimorfisme melalui Pewarisan

Semua turunan `Event` mengimplementasikan `get_choices()` serta `resolve()` dengan perilaku berbeda.

| Subclass | Perilaku |
|---|---|
| MonsterEvent | Meminta battle dan menyelesaikan encounter. |
| MerchantEvent | Memproses beli, jual, dan pergi. |
| TavernEvent | Memulihkan satu nyawa berbayar atau melewati tavern. |
| StoryEvent | Menyelesaikan pilihan naratif atau memulai battle cerita. |

Pada `demonstrate_polymorphism()` dalam `code/testing/posttest_demo.py`, keempat objek dimasukkan ke satu list dan dipanggil dalam **satu loop**:

```python
for event in events:
    choices = event.get_choices(session)
    choice = next(option for option in choices if option.enabled)
    result = event.resolve(session, choice.choice_id)
```

Pemanggil tidak memilih perilaku dengan rantai pemeriksaan jenis objek. GameSession juga berinteraksi melalui kontrak yang sama.

## 2. Duck Typing

`Choice` dan `ConditionalChoice` adalah dua class yang **tidak berhubungan lewat inheritance aplikasi**. Keduanya memiliki `describe()`, lalu dipanggil oleh satu fungsi:

```python
def describe_options(options):
    return [option.describe() for option in options]
```

Pilihan biasa menghasilkan label; pilihan bersyarat menambahkan nama stat dan tingkat kesulitan. Fungsi ini dipakai dalam permainan, bukan hanya demonstrasi.

## 3. Magic Method / Operator Overloading

| Class | Method | Penggunaan nyata |
|---|---|---|
| Inventory | `__len__()` | `len(player.inventory)` menghitung barang yang tersimpan. |
| Item | `__str__()` | Menampilkan nama, harga, dan deskripsi item. |
| Stats | `__str__()` | Menampilkan lima stat pada profil. |

Ini mengikuti daftar magic method yang diperbolehkan pada tugas.

## 4. Menghindari Anti-Pattern

Equipment memproses kontrak `allowed_slots`, `occupied_slots`, dan `traits`, sehingga tidak memakai rantai `if Weapon / elif Armor / elif Shield`. Event dipanggil melalui method-nya sendiri.

Pemeriksaan validasi, hasil menang/kalah, dan fase permainan tetap diperlukan sebagai aturan domain. Penggunaan `type(trait)` sebagai kunci penggabungan stack dan pencocokan status bukan rantai pemilihan perilaku berdasarkan class.

---

# Relasi UML

## Diagram Class

Sumber diagram siap diekspor: [uml_class_diagram.mmd](docs/uml_class_diagram.mmd).

**Gambar belum disediakan sesuai permintaan.** Buat `images/uml_class_diagram.png` menggunakan sumber diagram tersebut atau gambar ulang di draw.io. Setelah tersedia, aktifkan baris gambar berikut dengan menghapus penanda komentar HTML:

<!-- ![Diagram Class CLI Adventure](images/uml_class_diagram.png) -->

## 1. Asosiasi

`Combatant.attack(target)` memakai Combatant lain sebagai parameter serangan tanpa memiliki target tersebut. Diagram menggunakan panah putus-putus `..>`, mengikuti notasi asosiasi/dependensi searah dalam Modul 4.

## 2. Agregasi

`Inventory` menampung referensi `Item` yang dibuat di luar inventory. Item dapat dipindahkan atau dikeluarkan dan tetap menjadi objek mandiri; gunakan wajik kosong pada sisi Inventory.

## 3. Komposisi

`Player` membuat `Inventory` dan `Equipment` sendiri dalam constructor; `Character` juga membuat TraitManager internal. Bagian tersebut dikelola sebagai milik karakter terkait, sehingga wajik penuh berada pada sisi pemilik.

Komposisi menggambarkan kepemilikan dalam desain; tidak berarti Python memaksa objek lenyap jika referensi lain sengaja disimpan.

---

# Penerapan SOLID (Opsional)

## Single Responsibility Principle

`Battle` menghitung pertarungan, event menentukan konsekuensi, `GameSession` mengoordinasikan sesi, dan `cli/console.py` membentuk tampilan kotak. Perubahan tampilan tidak memerlukan penambahan output terminal di class Battle.

## Open/Closed Principle

Pemanggil event menggunakan `get_choices()` dan `resolve()`. Perilaku event baru dapat ditambahkan melalui subclass tanpa menambah rantai pemeriksaan tipe pada GameSession; pendaftaran posisi kontennya tetap dilakukan pada EventDirector.

Kontrak `occupied_slots` juga memungkinkan Weapon melaporkan kebutuhan dua tangan tanpa Equipment memeriksa nama class senjata.

---

# Pengujian

Dari folder posttest3:

```bash
python -m unittest discover -s tests -v
```

Alternatif peluncur:

```bash
python code/testing/testing.py
```

Pengujian mencakup rute cerita, kematian pada berbagai encounter, transaksi, pergantian equipment dua tangan, batas stack, poin level, kontrak ABC, duck typing, dan eksekusi CLI nyata.

Output pengujian terakhir tersedia di [hasil pengujian](docs/evidence/tests.txt). Screenshot tetap dibuat dari terminal oleh pengguna.

## Rute Reproduksi Orc Slayer

Jalankan `python code/main.py --seed 7 --name Bravern`, lalu masukkan urutan ini:

```text
1
4
equip 0
1
4
stat strength 5
1
1
2
1
```

Urutannya: bantu pengelana, beli Giant Armor, pasang armor, tinggalkan pedagang, interogasi STR, alokasikan poin, lewati dua battle perjalanan, lawan Orachulm, lalu melapor.

Contoh ini berlaku untuk balancing dan konsumsi RNG saat ini. Output eksekusi tersedia di [gameplay Orc Slayer](docs/evidence/gameplay_orc_slayer.txt).

---

# Gambar yang Perlu Ditambahkan

Lihat [panduan gambar](images/README.md). Tidak ada screenshot atau diagram PNG yang diklaim sudah dibuat.

| Nama file | Isi |
|---|---|
| uml_class_diagram.png | Diagram kelas dengan asosiasi, agregasi, komposisi, dan inheritance. |
| bukti_abstraksi.png | TypeError saat Event diinstansiasi. |
| polimorfisme_pewarisan.png | Satu loop memanggil empat subclass Event. |
| duck_typing_magic_method.png | Output duck typing serta str()/len(). |
| gameplay_orc_slayer.png | Penutup Orc Slayer, nyawa, level, gold, dan reputasi. |
| hasil_pengujian.png | Ringkasan pengujian dengan hasil OK. |

Aktifkan referensi berikut setelah file gambar tersedia:

<!-- ![Bukti Abstraksi](images/bukti_abstraksi.png) -->
<!-- ![Polimorfisme Pewarisan](images/polimorfisme_pewarisan.png) -->
<!-- ![Duck Typing dan Magic Method](images/duck_typing_magic_method.png) -->
<!-- ![Gameplay Orc Slayer](images/gameplay_orc_slayer.png) -->
<!-- ![Hasil Pengujian](images/hasil_pengujian.png) -->

---

# Balancing dan Batas Versi

Angka awal implementasi: tiga nyawa, 100 gold, dan 100 HP combat pemain. EXP level berikutnya adalah `20 × level sekarang`. Setiap level memberi tepat lima poin; satu poin menaikkan satu stat sebanyak satu.

Damage adalah `max(1, strength - defense)`. Interogasi menggunakan `d20 + stat >= 18`. Harga jual setengah harga beli, dibulatkan ke bawah. Tavern berbiaya 25 gold; laporan quest memberi 40 gold dan 10 EXP.

Angka tersebut adalah nilai awal implementasi agar game dapat dijalankan; jumlah lima poin per level mengikuti keputusan tetap pengguna. Angka umum berada di `content/balance.py`, sedangkan data item dan monster berada pada katalog/constructor terkait.

---

# Referensi Materi

Penjelasan OOP mengikuti Modul 4 UML Class Relationships, Modul 5 Inheritance, Modul 6 Polimorfisme & Abstraksi, dan Modul 7 Prinsip SOLID yang diberikan pada tugas.

Program, narasi Fernley, dan The Missing Apple mengikuti rancangan proyek. Referensi Life in Adventure digunakan sebagai inspirasi hubungan cerita dan sistem, bukan penyalinan karakter atau aset game.
