# Tugas Besar 1 Strategi Algoritma - Ilmu Padi
## Pemanfaatan Algoritma Greedy dalam Permainan Diamonds

## Kelompok Ilmu Padi
| No. | Nama                     |   NIM    |
|:---:|:-------------------------|:--------:|
| 1.  | Debrina Veisha Rashika W | 13522025 |
| 2.  | Nabila Shikoofa Muida    | 13522069 |
| 3.  | Bagas Sambega Rosyada    | 13522071 |

## Daftar Isi
1. [Deskripsi Umum](#deskripsi-umum)
2. [Penjelasan Algoritma](#penjelasan-algoritma)
3. [Penggunaan Program](#penggunaan-program)

## Deskripsi Umum
Tugas Besar 1 Strategi Algoritma ini bertujuan untuk mengimplementasikan bot pada permainan _Diamonds_. Permainan _Diamonds_ merupakan permainan sederhana yang memiliki objektif bagi pemain untuk mendapatkan _Diamonds_ sebanyak-banyaknya pada papan permainan.

Bot yang dibuat akan menggunakan algoritma _**Greedy**_ dengan tujuan utama mendapatkan _Diamond_ sebanyak-banyaknya agar dapat memenangkan permainan.

## Penjelasan Algoritma
Kelompok menggabungkan beberapa alternatif strategi greedy pada bot agar program bot dapat menangani seluruh kemungkinan kasus dari permainan Diamond secara efektif dan tepat sasaran. Poin penting pada implementasi algoritma greedy pada bot sebagai berikut:
1. Utamakan greedy by Closest to Base karena akan memberikan keuntungan lebih besar daripada yang lain. Bot akan mencari diamond ataupun bot lawan yang berada di sekitar base. Hal ini disebabkan karena semakin dekat dengan base, jarak yang dibutuhkan untuk mengembalikan berlian semakin kecil sehingga skor yang didapat akan semakin besar.
2. Jika tidak ada solusi yang memenuhi fungsi kelayakan pada greedy by Closest to Base, maka akan dipilih aksi greedy by Shortest Path to Current Position dengan mencari berlian yang dekat dengan posisi bot pada saat itu walaupun posisi berlian jauh dari base dan tidak ada objek yang ada di sekitar base.
3. Jika tidak ada berlian yang dekat dengan bot dan posisi berlian jauh dari base maupun posisi bot pada saat itu maka akan digunakan pendekatan greedy by Chasing Diamonds untuk mengambil berlian yang terletak sangat jauh dan pada saat itu posisi berlian memang sangat jauh dari manapun.
4. Jika tidak ada berlian yang dekat maupun bot yang memenuhi untuk dikejar, maka bot akan menuju red button jika jaraknya lebih dekat dibandingkan diamond terdekat untuk reset diamonds yang ada dalam permainan.
5. Saat bot sudah memiliki cukup diamonds, bot akan kembali ke base. Saat bot menuju base, jika masih ada slot kosong pada inventory dan melewati suatu area yang masih memiliki diamonds, bot akan menuju diamond tersebut. Lalu jika terdapat teleporter yang dapat mempersingkat jarak tempuh bot ke base, bot akan memakai teleporter tersebut, jika tidak, bot akan langsung menuju ke base.

## Penggunaan Program
Sebelum proses instalasi, pengguna harus memasang _requirements_ sebagai berikut:
- NodeJS (npm)
- Docker
- yarn

1. Clone repository ini sebagai algoritma bot yang akan digunakan
```
git clone https://github.com/bagassambega/Tubes1_ilmu-padi.git
```
2. Clone repository ini sebagai _game engine_.
```
git clone 
```
3. Pemain dapat menjalankan bot dengan membuat file run.bat atau run.sh
4. Kemudian untuk menjalankan keseluruhan bot dalam file tersebut, buka terminal dan jalankan perintah: 
```
./run-bots.bat
```
atau
```
chmod +x ./run-bots.sh
./run-bots.sh
```
