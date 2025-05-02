# Matkul_SIM

# Cara Download CMS wigtail
pip install wagtail==4.2 (disarankan menggunakan python versi 3.11)

# Sistem Manajemen Seminar Wagtail
Aplikasi manajemen seminar berbasis Wagtail CMS untuk mengelola kategori, pembicara, dan pendaftaran peserta seminar.
Cara Menggunakan
Instalasi Cepat
bash# Clone repository
git clone https://github.com/TanggBintang/Matkul_SIM.git
cd sistem-manajemen-seminar

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
atau--------------------------------
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Buat database mysql
Buat database Mysql dengan nama database sim_seminar

# Migrasi database
python manage.py migrate

# Buat superuser
python manage.py createsuperuser

# Buat data contoh
python manage.py create_sample_data

# Jalankan server
python manage.py runserver
Akses Aplikasi

Frontend: http://localhost:8000/
Admin: http://localhost:8000/admin/
