import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
import logging

# Mengatur logging
logging.basicConfig(level=logging.DEBUG)

# Pengaturan halaman Streamlit
st.set_page_config(page_title="Pendapatan per Departemen", layout="wide")

# Membuat judul aplikasi
st.title("Analisis Pendapatan per Departemen")

# Mendapatkan variabel lingkungan untuk koneksi database
host = os.getenv('DB_HOST', 'localhost')
user = os.getenv('DB_USER', 'root')
password = os.getenv('DB_PASSWORD', '')
database = os.getenv('DB_NAME', 'dump_dw')

try:
    # Mengatur koneksi ke database
    db_connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    st.success("Berhasil terhubung ke database")
except mysql.connector.Error as err:
    st.error(f"Error: {err}")
    logging.error(f"Error: {err}")
    st.stop()

# Membuat cursor
cursor = db_connection.cursor()

# Contoh query SQL untuk mengambil data pendapatan per departemen
query = "SELECT DepartmentName, AVG(BaseRate) as average_pendapatan FROM dimemployee Group By DepartmentName"
cursor.execute(query)
result = cursor.fetchall()
columns = [i[0] for i in cursor.description]
df = pd.DataFrame(result, columns=columns)

# Membuat bar chart
plt.figure(figsize=(14, 7))
sns.barplot(x='DepartmentName', y='average_pendapatan', data=df)
plt.title('Pendapatan per Departemen')
plt.xlabel('Departemen')
plt.ylabel('Rata-rata Pendapatan')
plt.xticks(rotation=45)

# Menampilkan grafik di Streamlit
st.pyplot(plt)

# Penjelasan grafik
penjelasan = """
Grafik di atas menunjukkan rata-rata pendapatan karyawan di setiap departemen dalam perusahaan.
Setiap batang pada grafik mewakili satu departemen, dan tinggi batang menunjukkan rata-rata pendapatan
di departemen tersebut. Dari grafik tersebut, kita dapat melihat bahwa departemen 'Executive' memiliki
rata-rata pendapatan tertinggi dibandingkan dengan departemen lainnya. Hal ini mungkin disebabkan oleh
posisi dan tanggung jawab yang lebih tinggi di departemen ini. Sebaliknya, departemen seperti 'Shipping and Receiving'
memiliki rata-rata pendapatan yang lebih rendah, kemungkinan karena posisi di departemen ini tidak membutuhkan
keterampilan atau tanggung jawab yang sebanding dengan departemen 'Executive'.
"""

st.markdown(penjelasan)

# Menutup cursor dan koneksi
cursor.close()
db_connection.close()
