# Setup & Deployment Guide — `WidyatamaX/WidyatamaX`

Ikuti langkah singkat berikut untuk mempublikasikan profil GitHub ini ke akun **@WidyatamaX**:

## 1. Buat Repositori Khusus Profil di GitHub
1. Buka https://github.com/new
2. Isi **Repository name** persis sama dengan username kamu: `WidyatamaX`
   *(GitHub akan menampilkan banner hijau: "WidyatamaX/WidyatamaX is a special repository")*
3. Pilih **Public**.
4. **Jangan** centang *Add a README file* (karena kita sudah punya di folder ini).
5. Klik **Create repository**.

## 2. Push Folder Ini ke GitHub
Jalankan perintah ini di PowerShell dari dalam folder `WidyatamaX`:

```powershell
git init -b main
git add .
git commit -m "feat: OMORI Headspace GitHub profile"
git remote add origin https://github.com/WidyatamaX/WidyatamaX.git
git push -u origin main
```

## 3. Aktifkan Izin Write untuk GitHub Actions (Penting!)
Agar **Profile Summary Cards**, **3D Contribution Graph**, dan **Snake** ter-generate otomatis:
1. Buka repo `WidyatamaX/WidyatamaX` → tab **Settings** → **Actions** → **General**.
2. Di bagian **Workflow permissions**, pilih **Read and write permissions**, lalu klik **Save**.
3. Buka tab **Actions**:
   - Pilih **Generate 3D & Snake Contribution Graphs** → klik **Run workflow** → **Run workflow**.
   - Pilih **Generate Profile Summary Cards** → klik **Run workflow** → **Run workflow**.
4. Tunggu ~1–2 menit sampai kedua workflow selesai (centang hijau). Refresh halaman profil https://github.com/WidyatamaX — semua grafik dan kartu stats akan langsung muncul!

## 4. Tips Tambahan Setelah Ganti Username
- Di repo [`WidyatamaX/OpenFormu`](https://github.com/WidyatamaX/OpenFormu), jangan lupa perbarui bagian **About → Website** ke `https://widyatamax.github.io/OpenFormu/` supaya sinkron dengan username baru.

## 5. Cara Mengedit Profil di Masa Depan
Semua teks, proyek, stack, dan palet warna ada di `scripts/build_svgs.py`.
Setelah mengedit data di skrip tersebut, jalankan ulang:

```powershell
python scripts/build_svgs.py
```

Semua file SVG desktop (`assets/`) dan mobile (`assets/m/`) akan diperbarui otomatis.
