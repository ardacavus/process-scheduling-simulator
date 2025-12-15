import customtkinter
import os
import subprocess
import sys

# 1. CustomTkinter kütüphanesinin yolunu bul
ctk_path = os.path.dirname(customtkinter.__file__)
print(f"CustomTkinter yolu bulundu: {ctk_path}")

# 2. İşletim sistemine göre ayraç belirle (Windows için ';', Linux/Mac için ':')
separator = ';' if os.name == 'nt' else ':'

# 3. PyInstaller komutunu hazırla
# --add-data "KAYNAK_YOL;HEDEF_KLASOR_ADI"
command = [
    "pyinstaller",
    "--noconsole",       # Siyah ekran çıkmasın
    "--onefile",         # Tek bir .exe olsun
    f"--add-data={ctk_path}{separator}customtkinter", # Tema dosyalarını ekle
    "--name=CS305_Scheduler_Ultimate", # Havalı bir isim
    "gui.py"             # Ana dosyamız
]

print("\nEXE oluşturma işlemi başlıyor...")
print("Çalıştırılan komut:", " ".join(command))
print("-" * 50)

# 4. Komutu çalıştır
try:
    # subprocess.run, terminale yazdığımız komutu Python içinden çalıştırır
    subprocess.run(command, check=True, shell=(os.name == 'nt'))
    print("\n" + "="*50)
    print("✅ BAŞARILI! EXE dosyası oluşturuldu.")
    print("Dosyayı 'dist' klasörünün içinde bulabilirsin.")
    print("="*50)
except subprocess.CalledProcessError as e:
    print("\n" + "="*50)
    print("❌ HATA: EXE oluşturulurken bir sorun çıktı.")
    print("Hata detayı:", e)
    print("="*50)