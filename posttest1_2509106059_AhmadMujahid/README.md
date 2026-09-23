# CLI Adventure 

## Deskripsi Program

**CLI Adventure** merupakan program simulasi petualangan berbasis Command Line Interface (CLI) yang dibuat dengan pendekatan Object-Oriented Programming (OOP) menggunakan Python.

Program ini menggambarkan seorang pemain yang menjalani petualangan, memiliki statistik karakter dan profesi, kemudian dapat menghadapi monster dalam sistem pertarungan otomatis.

Program dibuat dengan menerapkan materi OOP yang telah dipelajari, yaitu:

* Class dan Object
* Attribute dan Method
* Encapsulation
* Property
* Interaksi antar-object menggunakan composition
* Class Method
* Static Method

Beberapa proses yang dapat dilakukan dalam program antara lain:

1. Membuat data profesi pemain.
2. Membuat karakter pemain.
3. Membuat data monster.
4. Menampilkan dan mengolah statistik karakter.
5. Mengatur health menggunakan property dan setter.
6. Melakukan validasi nilai health.
7. Melakukan validasi nilai stat menggunakan static method.
8. Membuat profesi menggunakan class method.
9. Melengkapi equipment dengan weapon.
10. Mengaktifkan Trait ketika weapon digunakan.
11. Menambahkan bonus Strength dari Trait `Strong`.
12. Menghilangkan bonus Trait ketika weapon dilepas.
13. Melakukan pertarungan otomatis antara Player dan Monster.
14. Menentukan giliran pertama berdasarkan Agility.
15. Mengurangi health ketika karakter menerima serangan.
16. Menentukan pemenang pertarungan berdasarkan kondisi health.
17. Menguji setter dengan data valid dan tidak valid.

---

# Struktur Class

Program terdiri dari beberapa class yang saling berinteraksi. Tiga class utama yang menjadi bagian inti program adalah `Player`, `Monster`, dan `Battle`, sedangkan class lainnya digunakan sebagai pendukung sistem.

---

## 1. Class `Player`

Class `Player` digunakan untuk merepresentasikan karakter yang dikendalikan pemain dalam petualangan.

### Atribut Instance

* `name` → menyimpan nama karakter.
* `level` → menyimpan level karakter.
* `health` → menyimpan health karakter melalui property.
* `profession` → menyimpan profesi yang dimiliki Player.
* `stats` → menyimpan statistik karakter.
* `traits_manager` → mengelola Trait yang dimiliki atau sedang aktif pada Player.

### Atribut Private

* `__health` → menyimpan nilai health secara private sehingga perubahan nilai dilakukan melalui property.

### Method

* `__init__()` → membuat object Player dan menginisialisasi data awal.
* `__apply_profession_stats()` → menerapkan bonus statistik dari profesi.
* `take_damage()` → mengurangi health Player ketika menerima serangan.
* `is_alive()` → memeriksa apakah Player masih hidup.
* `attack()` → melakukan serangan terhadap target.

### Property

* `health` → getter untuk membaca health.
* `health.setter` → setter untuk mengubah health dengan validasi agar nilainya tidak negatif.

Player juga memiliki object `Stats`, `Profession`, dan `TraitsManajer`, sehingga class ini berinteraksi dengan beberapa object lain dalam program.

---

## 2. Class `Monster`

Class `Monster` digunakan untuk merepresentasikan lawan yang dapat ditemui oleh Player dalam pertarungan.

### Atribut Instance

* `name` → nama monster.
* `rarity` → tingkat kelangkaan monster.
* `monster_type` → tipe monster.
* `health` → health monster.
* `stats` → statistik monster.

### Atribut Private

* `__health` → menyimpan health monster secara private.

### Method

* `__init__()` → membuat object Monster.
* `take_damage()` → mengurangi health monster.
* `is_alive()` → memeriksa kondisi hidup monster.
* `attack()` → menyerang target menggunakan Strength.

### Property

* `health` → getter untuk membaca health.
* `health.setter` → setter untuk mengubah health dan mencegah health bernilai negatif.

---

## 3. Class `Battle`

Class `Battle` bertanggung jawab terhadap jalannya pertarungan antara Player dan Monster.

### Atribut Instance

* `player` → menyimpan object Player yang mengikuti pertarungan.
* `enemy` → menyimpan object Monster yang menjadi lawan.

### Method

* `__init__()` → menerima Player dan Monster sebagai peserta battle.
* `determine_first_turn()` → menentukan siapa yang mendapatkan giliran pertama berdasarkan nilai Agility.
* `start()` → menjalankan pertarungan secara bergantian sampai salah satu peserta kalah.

Mekanisme pertarungan sederhana yang digunakan:

```text
Bandingkan Agility
       ↓
Tentukan giliran pertama
       ↓
Attacker menyerang target
       ↓
Kurangi Health target
       ↓
Cek apakah target masih hidup
       ↓
Jika masih hidup → giliran berganti
       ↓
Ulangi sampai salah satu kalah
```

---

## 4. Class `Stats`

Class `Stats` digunakan untuk menyimpan statistik karakter.

### Atribut Instance

* `strength`
* `agility`
* `defense`
* `intelligence`
* `charisma`

### Method

* `__init__()` → membuat kumpulan statistik.
* `add()` → menambahkan nilai statistik dari object `Stats` lain.

### Static Method

* `is_valid_stat()` → memeriksa apakah nilai statistik valid, yaitu tidak negatif.

Static method tidak membutuhkan object `Stats` tertentu karena hanya melakukan pemeriksaan nilai.

Contoh:

```python
Stats.is_valid_stat(10)
```

akan menghasilkan `True`, sedangkan:

```python
Stats.is_valid_stat(-5)
```

akan menghasilkan `False`.

---

## 5. Class `Profession`

Class `Profession` menyimpan profesi yang dimiliki oleh Player beserta bonus statistiknya.

### Atribut Instance

* `name` → nama profesi.
* `stats` → bonus statistik profesi.

### Method

* `__init__()` → membuat object profesi.

### Class Method

* `create_default()` → membuat object `Profession` dengan statistik awal default.

Class method menggunakan `cls` untuk membuat object dari class `Profession`.

Contoh:

```python
Profession.create_default("Adventurer")
```

---

## 6. Class `Equipment`

Class `Equipment` digunakan untuk menyimpan equipment yang sedang digunakan oleh karakter.

### Atribut Instance

* `armor` → menyimpan armor yang digunakan.
* `weapon` → menyimpan weapon yang digunakan.

### Method

* `equip_weapon()` → memasang weapon dan mengaktifkan Trait yang dimiliki weapon.
* `unequip_weapon()` → melepas weapon dan menghilangkan efek Trait dari weapon.

Pada program saat ini, mekanisme Trait yang digunakan dalam pengujian adalah `Strong`.

---

## 7. Class `Weapon`

Class `Weapon` merepresentasikan senjata yang dapat digunakan oleh Player.

### Atribut Instance

* `name` → nama weapon.
* `trait` → Trait yang melekat pada weapon.

Weapon dapat membawa Trait tertentu. Dalam pengujian program, weapon menggunakan Trait `Strong`.

---

## 8. Class `TraitsManajer`

`TraitsManajer` digunakan untuk mengatur Trait yang aktif pada Player.

### Atribut Instance

* `traits` → menyimpan kumpulan Trait.

### Method

* `add_trait()` → menambahkan Trait.
* `apply_trait()` → menerapkan efek Trait kepada Player.
* `remove_trait()` → menghilangkan efek Trait tertentu dari Player.

Untuk implementasi saat ini, Trait yang digunakan adalah `Strong`.

---

## 9. Class `Strong`

`Strong` merupakan Trait yang memberikan bonus Strength.

### Atribut Kelas

* `name` → nama Trait.
* `target` → stat yang dipengaruhi, yaitu Strength.
* `value` → nilai bonus Strength sebesar 5.

Ketika weapon yang memiliki Trait `Strong` digunakan:

```text
Equip Weapon
      ↓
Strong aktif
      ↓
Strength +5
```

Ketika weapon dilepas:

```text
Unequip Weapon
      ↓
Strong dinonaktifkan
      ↓
Strength -5
```

---

# Panduan Menjalankan Program

## 1. Membuka Repository

Clone atau download repository GitHub kemudian buka folder project menggunakan Visual Studio Code.

## 2. Menjalankan Program

Pastikan Python sudah terpasang pada perangkat.

Jalankan file utama:

```bash
python main.py
```

Jika menggunakan struktur package, jalankan dari root directory project agar import antar-module dapat ditemukan dengan benar.

## 3. Memperhatikan Output

Program akan menampilkan beberapa bagian pengujian, yaitu:

1. Pengujian class method.
2. Pengujian static method.
3. Pembuatan object Player.
4. Pembuatan object Monster.
5. Pengujian getter health.
6. Pengujian setter dengan data valid.
7. Pengujian setter dengan data tidak valid.
8. Pengujian equipment.
9. Pengujian Trait `Strong`.
10. Pengujian instance method.
11. Pengujian sistem battle.

---

# Panduan Pengujian

## 1. Pengujian Class Method

Class method digunakan untuk membuat object `Profession` dengan statistik default.

Contoh:

```python
default_profession = Profession.create_default("Adventurer")

print(default_profession.name)
```


---

## 2. Pengujian Static Method

Static method digunakan untuk melakukan validasi nilai statistik.

Contoh:

```python
print(Stats.is_valid_stat(10))
print(Stats.is_valid_stat(-5))
```


---

## 3. Pengujian Data Player dan Monster

Program membuat lebih dari satu object untuk menguji class yang digunakan.

Contoh object:

```python
bravern = Player(...)
arthur = Player(...)

goblin = Monster(...)
ogre = Monster(...)
```

Object tersebut digunakan untuk menunjukkan bahwa setiap object dapat memiliki data yang berbeda.



---

## 4. Pengujian Getter

Getter `health` digunakan untuk membaca nilai health melalui property.

Contoh:

```python
print(bravern.health)
```

Akses dilakukan melalui:

```python
bravern.health
```

bukan secara langsung terhadap:

```python
bravern.__health
```



---

## 5. Pengujian Setter dengan Data Valid

Setter digunakan untuk mengubah health dengan nilai yang memenuhi aturan.

Contoh:

```python
bravern.health = 30

print(bravern.health)
```

Output menunjukkan bahwa nilai health berhasil berubah.


---

## 6. Pengujian Setter dengan Data Tidak Valid

Setter juga diuji menggunakan nilai negatif.

Contoh:

```python
bravern.health = -10

print(bravern.health)
```

Setter akan melakukan validasi sehingga health tidak disimpan sebagai nilai negatif.



---

## 7. Pengujian Equipment dan Trait `Strong`

Weapon dibuat dengan Trait `Strong`.

Contoh:

```python
sword = Weapon("Iron Sword", Strong())
equipment = Equipment()
```

Sebelum weapon digunakan, Strength Player diperiksa.

Kemudian weapon dipasang:

```python
equipment.equip_weapon(sword, bravern)
```

Trait `Strong` akan memberikan bonus Strength sebesar 5.

Setelah weapon dilepas:

```python
equipment.unequip_weapon(bravern)
```

bonus Strength dari weapon dihilangkan.

Alur:

```text
Strength awal
     ↓
Equip Iron Sword
     ↓
Strength +5
     ↓
Unequip Iron Sword
     ↓
Strength kembali
```


---

## 8. Pengujian Instance Method

Instance method diuji menggunakan method yang dimiliki object Player.

Contoh:

```python
print(bravern.is_alive())

bravern.take_damage(5)

print(bravern.health)
print(bravern.is_alive())
```

Pengujian ini menunjukkan bahwa method dapat mengubah dan memeriksa kondisi object.


---

## 9. Pengujian Battle

Program kemudian menjalankan pertarungan antara Player dan Monster.

Contoh:

```python
battle = Battle(bravern, goblin)
battle.start()
```

Battle menentukan peserta yang mendapat giliran pertama berdasarkan Agility.

Selanjutnya kedua peserta menyerang secara bergantian sampai salah satu health mencapai 0.

Alur:

```text
Bravern menyerang Goblin
Goblin menyerang Bravern
Bravern menyerang Goblin
...
Salah satu kalah
```

---

