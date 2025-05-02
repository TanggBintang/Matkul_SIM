# Matkul_SIM
 Sistem Manajemen Seminar Wagtail
Aplikasi manajemen seminar berbasis Wagtail CMS untuk mengelola kategori, pembicara, dan pendaftaran peserta seminar.
Cara Menggunakan
Instalasi Cepat
bash# Clone repository
git clone https://github.com/username/sistem-manajemen-seminar.git
cd sistem-manajemen-seminar

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

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
