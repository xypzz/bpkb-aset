import os
import sys

# Lokasi Python aktif sekarang
python_dir = os.path.dirname(sys.executable)
python_scripts = os.path.join(python_dir, "Scripts")

print("Python aktif sekarang:", python_dir)

# Ambil PATH user dari environment
import winreg

def get_user_path():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                        "Environment", 0, winreg.KEY_READ) as key:
        try:
            value, _ = winreg.QueryValueEx(key, "Path")
            return value
        except FileNotFoundError:
            return ""

def set_user_path(new_path):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                        "Environment", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)

# Ambil PATH lama
old_path = get_user_path()
path_list = old_path.split(";") if old_path else []

# Buang entri Python39
path_list = [p for p in path_list if "Python39" not in p]

# Tambahkan Python312 jika belum ada
if python_dir not in path_list:
    path_list.append(python_dir)
if python_scripts not in path_list:
    path_list.append(python_scripts)

# Buat PATH baru
new_path = ";".join(path_list)
set_user_path(new_path)

print("\n✅ PATH berhasil diperbarui!")
print("Silakan tutup CMD lalu buka lagi, kemudian cek dengan:")
print("   where python")
print("   where pip")
