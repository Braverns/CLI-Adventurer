# Panduan Gambar Laporan

Gambar sengaja belum dibuat sesuai permintaan pengguna. Simpan PNG di folder ini menggunakan nama persis berikut, lalu aktifkan baris gambar yang sudah disiapkan dalam komentar HTML di README utama.

| File | Cara menyiapkan |
|---|---|
| uml_class_diagram.png | Buka sumber ../docs/uml_class_diagram.mmd pada editor Mermaid atau gambar ulang menggunakan draw.io. Export PNG, gunakan latar terang dan resolusi yang membuat teks terbaca. Wajik agregasi kosong dan komposisi penuh harus berada pada sisi pemilik. |
| bukti_abstraksi.png | Jalankan python code/testing/posttest_demo.py dari folder posttest3. Tangkap kotak bagian 1 yang berisi TypeError Event dan nama dua abstract method. |
| polimorfisme_pewarisan.png | Tangkap kotak bagian 2 dari perintah yang sama; pastikan nama empat subclass dan hasil method terlihat. |
| duck_typing_magic_method.png | Tangkap bagian 3 dan 4. Jika terlalu panjang, boleh pakai dua gambar tambahan dan perbarui referensinya. |
| gameplay_orc_slayer.png | Ikuti rute seed 7 pada README; tangkap kotak epilog ORC SLAYER beserta ringkasan pemain. |
| hasil_pengujian.png | Jalankan python -m unittest discover -s tests -v dan tangkap jumlah tes serta OK. |

Contoh mengaktifkan gambar:

Sebelum:
<!-- ![Bukti Abstraksi](bukti_abstraksi.png) -->

Pada README utama, ubah komentar menjadi:
```markdown
![Bukti Abstraksi](images/bukti_abstraksi.png)
```

Output teks asli tersedia di ../docs/evidence/. Jangan mengubah teks output agar terlihat lolos; jalankan ulang perintah jika program berubah.
