
import streamlit as st
import math
import random

# Konfigurasi Halaman
st.set_page_config(
    page_title="Smart Physics Calculator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Kustom untuk tampilan menarik
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .formula-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .step-box {
        background-color: #e8f4f8;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 3px solid #2ca02c;
    }
    .quiz-correct {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        color: #155724;
    }
    .quiz-wrong {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        color: #721c24;
    }
    .constant-box {
        background-color: #fff3cd;
        padding: 8px;
        border-radius: 5px;
        margin: 3px 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    .hero-text {
        text-align: center;
        font-size: 1.2rem;
        color: #555;
        margin: 20px 0;
    }
    .feature-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA & KONSTANTA ====================
PHYSICS_CONSTANTS = {
    "Kecepatan cahaya (c)": {"nilai": 2.998e8, "satuan": "m/s"},
    "Konstanta gravitasi (G)": {"nilai": 6.674e-11, "satuan": "N·m²/kg²"},
    "Konstanta Planck (h)": {"nilai": 6.626e-34, "satuan": "J·s"},
    "Muatan elektron (e)": {"nilai": 1.602e-19, "satuan": "C"},
    "Massa elektron (mₑ)": {"nilai": 9.109e-31, "satuan": "kg"},
    "Massa proton (mₚ)": {"nilai": 1.673e-27, "satuan": "kg"},
    "Massa neutron (mₙ)": {"nilai": 1.675e-27, "satuan": "kg"},
    "Konstanta Boltzmann (k)": {"nilai": 1.381e-23, "satuan": "J/K"},
    "Konstanta Avogadro (Nₐ)": {"nilai": 6.022e23, "satuan": "mol⁻¹"},
    "Permeabilitas vakum (μ₀)": {"nilai": 4*math.pi*1e-7, "satuan": "N/A²"},
    "Permitivitas vakum (ε₀)": {"nilai": 8.854e-12, "satuan": "F/m"},
    "Percepatan gravitasi bumi (g)": {"nilai": 9.81, "satuan": "m/s²"},
    "Tekanan atmosfer standar (atm)": {"nilai": 1.013e5, "satuan": "Pa"},
    "Suhu triple point air": {"nilai": 273.16, "satuan": "K"},
}

UNIT_TABLE = {
    "Panjang": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001, "μm": 1e-6, "nm": 1e-9, "ft": 0.3048, "in": 0.0254, "mi": 1609.34},
    "Massa": {"kg": 1, "g": 0.001, "mg": 1e-6, "ton": 1000, "lb": 0.4536, "oz": 0.02835},
    "Waktu": {"s": 1, "min": 60, "hr": 3600, "day": 86400, "ms": 0.001},
    "Suhu": {"C": "special", "K": "special", "F": "special", "R": "special"},
    "Tekanan": {"Pa": 1, "kPa": 1000, "MPa": 1e6, "bar": 1e5, "atm": 101325, "mmHg": 133.322, "psi": 6894.76},
    "Energi": {"J": 1, "kJ": 1000, "cal": 4.184, "kcal": 4184, "Wh": 3600, "kWh": 3.6e6, "eV": 1.602e-19},
    "Daya": {"W": 1, "kW": 1000, "MW": 1e6, "hp": 745.7},
    "Kerapatan": {"kg/m³": 1, "g/cm³": 1000, "kg/L": 1000, "g/mL": 1000, "lb/ft³": 16.018},
    "Viskositas": {"Pa·s": 1, "Poise": 0.1, "cP": 0.001, "mPa·s": 0.001},
    "Gaya": {"N": 1, "kN": 1000, "dyne": 1e-5, "kgf": 9.81, "lbf": 4.448},
}

# ==================== FUNGSI KONVERSI ====================
def convert_temperature(val, from_unit, to_unit):
    if from_unit == to_unit:
        return val
    # Konversi ke Celsius dulu
    if from_unit == "C":
        c = val
    elif from_unit == "K":
        c = val - 273.15
    elif from_unit == "F":
        c = (val - 32) * 5/9
    elif from_unit == "R":
        c = val * 5/9 - 273.15
    else:
        return None
    # Konversi dari Celsius ke target
    if to_unit == "C":
        return c
    elif to_unit == "K":
        return c + 273.15
    elif to_unit == "F":
        return c * 9/5 + 32
    elif to_unit == "R":
        return (c + 273.15) * 9/5
    return None

def auto_convert(value, from_unit, to_unit, category):
    if category == "Suhu":
        return convert_temperature(value, from_unit, to_unit)

    units = UNIT_TABLE.get(category, {})
    if from_unit not in units or to_unit not in units:
        return None

    # Konversi ke unit dasar, lalu ke target
    base_value = value * units[from_unit]
    return base_value / units[to_unit]

# ==================== KALKULATOR KERAPATAN ====================
def calc_density(mass, volume, mass_unit, vol_unit):
    # Konversi ke kg dan m³
    mass_kg = auto_convert(mass, mass_unit, "kg", "Massa")
    vol_m3 = auto_convert(volume, vol_unit, "m", "Panjang")**3 if vol_unit in UNIT_TABLE["Panjang"] else None

    if vol_unit == "L" or vol_unit == "dm³":
        vol_m3 = volume * 0.001
    elif vol_unit == "mL" or vol_unit == "cm³":
        vol_m3 = volume * 1e-6
    elif vol_unit == "ft³":
        vol_m3 = volume * 0.0283
    elif vol_unit == "in³":
        vol_m3 = volume * 1.639e-5
    else:
        # Coba konversi dari tabel panjang
        try:
            vol_m3 = auto_convert(volume, vol_unit, "m", "Panjang")**3
        except:
            vol_m3 = volume * 1e-3  # default L

    density = mass_kg / vol_m3 if vol_m3 else 0
    return density, mass_kg, vol_m3

# ==================== KALKULATOR VISKOSITAS ====================
def calc_viscosity(force, area, velocity, gradient, f_unit, a_unit, v_unit, g_unit):
    # η = (F/A) / (dv/dy) = shear stress / shear rate
    # Konversi satuan ke SI
    f_si = auto_convert(force, f_unit, "N", "Gaya") if f_unit != "N" else force
    a_si = auto_convert(area, a_unit, "m", "Panjang")**2 if a_unit in UNIT_TABLE["Panjang"] else area

    if a_unit == "cm²":
        a_si = area * 1e-4
    elif a_unit == "mm²":
        a_si = area * 1e-6
    elif a_unit == "ft²":
        a_si = area * 0.0929
    elif a_unit == "in²":
        a_si = area * 0.000645

    v_si = auto_convert(velocity, v_unit, "m", "Panjang") if v_unit in UNIT_TABLE["Panjang"] else velocity

    if g_unit in UNIT_TABLE["Panjang"]:
        g_si = auto_convert(gradient, g_unit, "m", "Panjang")
    else:
        g_si = gradient

    shear_stress = f_si / a_si if a_si else 0
    shear_rate = v_si / g_si if g_si else 0
    viscosity = shear_stress / shear_rate if shear_rate else 0

    return viscosity, shear_stress, shear_rate, f_si, a_si, v_si, g_si

# ==================== KALKULATOR SUDUT REPOSISI ====================
def calc_repose_angle(mu_s):
    # θ = arctan(μs)
    theta_rad = math.atan(mu_s)
    theta_deg = math.degrees(theta_rad)
    return theta_deg, theta_rad

# ==================== DATA QUIZ ====================
QUIZ_QUESTIONS = [
    {
        "type": "pilihan_ganda",
        "soal": "Sebuah balok bermassa 5 kg dikenai gaya 20 N. Berapa percepatan balok tersebut?",
        "pilihan": ["2 m/s²", "4 m/s²", "5 m/s²", "0.25 m/s²"],
        "jawaban": "4 m/s²",
        "pembahasan": "Menggunakan Hukum II Newton: F = m × a → a = F/m = 20 N / 5 kg = 4 m/s²"
    },
    {
        "type": "pilihan_ganda",
        "soal": "Berapa kerapatan air pada suhu 4°C?",
        "pilihan": ["1000 kg/m³", "1 kg/m³", "100 kg/m³", "10 kg/m³"],
        "jawaban": "1000 kg/m³",
        "pembahasan": "Air pada suhu 4°C memiliki kerapatan maksimum sebesar 1000 kg/m³ atau 1 g/cm³."
    },
    {
        "type": "isian",
        "soal": "Sebuah benda jatuh bebas dari ketinggian 20 m. Berapa kecepatan benda saat menyentuh tanah? (g = 10 m/s², tulis angka saja)",
        "jawaban": "20",
        "pembahasan": "Menggunakan v² = 2gh → v = √(2×10×20) = √400 = 20 m/s"
    },
    {
        "type": "pilihan_ganda",
        "soal": "Satuan viskositas dinamis dalam SI adalah...",
        "pilihan": ["Poise", "Stokes", "Pa·s", "N/m²"],
        "jawaban": "Pa·s",
        "pembahasan": "Satuan viskositas dinamis dalam SI adalah Pa·s (Pascal-second). 1 Pa·s = 10 Poise."
    },
    {
        "type": "pilihan_ganda",
        "soal": "Jika koefisien gesek statis μₛ = 0.5, berapa sudut reposisi maksimum?",
        "pilihan": ["26.6°", "30°", "45°", "60°"],
        "jawaban": "26.6°",
        "pembahasan": "θ = arctan(μₛ) = arctan(0.5) ≈ 26.565° ≈ 26.6°"
    },
    {
        "type": "isian",
        "soal": "Konversikan 25°C ke Kelvin! (tulis angka saja)",
        "jawaban": "298.15",
        "pembahasan": "K = C + 273.15 = 25 + 273.15 = 298.15 K"
    },
    {
        "type": "pilihan_ganda",
        "soal": "Tekanan hidrostatik di kedalaman 10 m dalam air (ρ = 1000 kg/m³) adalah...",
        "pilihan": ["98000 Pa", "100000 Pa", "101325 Pa", "50000 Pa"],
        "jawaban": "98000 Pa",
        "pembahasan": "P = ρgh = 1000 × 9.8 × 10 = 98000 Pa"
    },
    {
        "type": "pilihan_ganda",
        "soal": "Energi kinetik sebuah benda bermassa 2 kg yang bergerak dengan kecepatan 10 m/s adalah...",
        "pilihan": ["10 J", "100 J", "200 J", "50 J"],
        "jawaban": "100 J",
        "pembahasan": "Ek = ½mv² = ½ × 2 × 10² = 100 J"
    },
    {
        "type": "isian",
        "soal": "Berapa gaya gravitasi antara dua benda bermassa 1000 kg dan 2000 kg yang berjarak 10 m? (G = 6.67×10⁻¹¹, tulis dalam bentuk desimal dengan 4 angka di belakang koma)",
        "jawaban": "0.0013",
        "pembahasan": "F = G(m₁m₂)/r² = 6.67×10⁻¹¹ × (1000×2000)/100 = 1.334×10⁻⁶ N. Jika dibulatkan: 0.0000013 N"
    },
    {
        "type": "pilihan_ganda",
        "soal": "Hukum Archimedes berlaku untuk...",
        "pilihan": ["Benda yang tenggelam", "Benda yang mengapung", "Benda dalam fluida", "Semua benar"],
        "jawaban": "Semua benar",
        "pembahasan": "Hukum Archimedes berlaku untuk semua benda yang berada dalam fluida, baik tenggelam, mengapung, atau melayang."
    },
]

# ==================== SIDEBAR NAVIGASI ====================
st.sidebar.markdown("<h1 style='text-align:center;'>⚛️ Smart Physics</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📋 Menu Navigasi",
    ["🏠 Beranda", "📚 Rumus & Cheat Sheet", "🧮 Kalkulator", "🔄 Unit Converter", "📝 Quiz Fisika"]
)

# ==================== HALAMAN BERANDA ====================
if menu == "🏠 Beranda":
    st.markdown("<div class='main-header'>⚛️ Smart Physics Calculator</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-text'>Aplikasi kalkulator fisika cerdas dengan langkah pengerjaan, konversi satuan otomatis, dan latihan soal interaktif untuk mahasiswa fisika dasar.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🧮</div>
            <h3>Kalkulator Cerdas</h3>
            <p>Kerapatan, Viskositas, Sudut Reposisi dengan langkah pengerjaan lengkap dan penjelasan rumus.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔄</div>
            <h3>Auto Converter</h3>
            <p>Konversi satuan otomatis untuk berbagai besaran fisika: panjang, massa, suhu, tekanan, energi, dan lainnya.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📝</div>
            <h3>Quiz Interaktif</h3>
            <p>Latihan soal pilihan ganda dan isian dengan pembahasan otomatis untuk persiapan ujian fisika dasar.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='sub-header'>🔬 Pengenalan Materi Fisika Dasar</div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📐 Mekanika", "🌡️ Termodinamika", "⚡ Listrik & Magnet", "🔊 Gelombang"])

    with tab1:
        st.markdown("""
        ### Mekanika Klasik
        Mekanika adalah cabang fisika yang mempelajari gerak benda dan gaya yang menyebabkannya. 

        **Topik Utama:**
        - **Kinematika**: Gerak lurus, gerak parabola, gerak melingkar
        - **Dinamika**: Hukum Newton, gaya gesek, momentum
        - **Energi**: Energi kinetik, energi potensial, usaha
        - **Fluida**: Tekanan, hukum Pascal, hukum Archimedes, viskositas

        **Aplikasi Praktis:**
        - Perancangan jembatan dan bangunan
        - Aerodinamika kendaraan
        - Sistem hidrolik
        """)

    with tab2:
        st.markdown("""
        ### Termodinamika
        Mempelajari hubungan antara panas, kerja, energi, dan sifat materi.

        **Topik Utama:**
        - **Suhu dan Kalor**: Konduksi, konveksi, radiasi
        - **Hukum Termodinamika 0-3**: Kesetimbangan, kekekalan, entropi
        - **Gas Ideal**: Persamaan keadaan, teori kinetik gas
        - **Perubahan Fase**: Kalor laten, diagram fase

        **Konsep Kunci:**
        - Entropi mengukur ketidakteraturan sistem
        - Efisiensi mesin Carnot adalah batas teoritis
        """)

    with tab3:
        st.markdown("""
        ### Listrik & Magnet
        Mempelajari muatan listrik, medan listrik, dan medan magnet.

        **Topik Utama:**
        - **Elektrostatika**: Hukum Coulomb, medan listrik, potensial
        - **Arus Listrik**: Hukum Ohm, rangkaian DC, daya listrik
        - **Magnetostatika**: Gaya Lorentz, medan magnet, induksi
        - **Induksi Elektromagnetik**: Hukum Faraday, hamburan gelombang EM

        **Aplikasi:**
        - Generator dan motor listrik
        - Transformator
        - Gelombang radio dan komunikasi
        """)

    with tab4:
        st.markdown("""
        ### Gelombang & Optika
        Mempelajari perambatan gangguan melalui medium dan zat.

        **Topik Utama:**
        - **Gelombang Mekanik**: Gelombang tali, gelombang suara
        - **Gelombang EM**: Spektrum elektromagnetik, polarisasi
        - **Optika Geometris**: Pembiasan, pemantulan, lensa, cermin
        - **Optika Fisis**: Interferensi, difraksi, polarisasi

        **Fenomena Menarik:**
        - Efek Doppler pada gelombang suara
        - Interferensi Young (celah ganda)
        - Prisma dan dispersi cahaya
        """)

    st.markdown("---")
    st.info("💡 **Tips**: Gunakan menu di sidebar untuk mengakses fitur kalkulator, konverter, dan quiz!")

# ==================== HALAMAN RUMUS & CHEAT SHEET ====================
elif menu == "📚 Rumus & Cheat Sheet":
    st.markdown("<div class='main-header'>📚 Rumus & Cheat Sheet Fisika</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 Tabel Satuan", "🔢 Konstanta Fisika", "📖 Rumus Penting"])

    with tab1:
        st.markdown("<div class='sub-header'>📋 Tabel Satuan SI dan Konversi</div>", unsafe_allow_html=True)

        satuan_data = {
            "Besaran Pokok": [
                ["Panjang", "meter", "m"],
                ["Massa", "kilogram", "kg"],
                ["Waktu", "second", "s"],
                ["Arus listrik", "ampere", "A"],
                ["Suhu", "kelvin", "K"],
                ["Jumlah zat", "mole", "mol"],
                ["Intensitas cahaya", "candela", "cd"]
            ],
            "Besaran Turunan": [
                ["Kecepatan", "m/s"],
                ["Percepatan", "m/s²"],
                ["Gaya", "Newton (N = kg·m/s²)"],
                ["Energi", "Joule (J = N·m)"],
                ["Daya", "Watt (W = J/s)"],
                ["Tekanan", "Pascal (Pa = N/m²)"],
                ["Muatan listrik", "Coulomb (C = A·s)"],
                ["Potensial listrik", "Volt (V = W/A)"],
                ["Resistansi", "Ohm (Ω = V/A)"],
                ["Kapasitansi", "Farad (F = C/V)"],
                ["Frekuensi", "Hertz (Hz = s⁻¹)"],
                ["Kerapatan", "kg/m³"],
                ["Viskositas", "Pa·s (Pascal-second)"]
            ]
        }

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Besaran Pokok SI**")
            st.table(satuan_data["Besaran Pokok"])
        with col_b:
            st.markdown("**Besaran Turunan SI**")
            st.table(satuan_data["Besaran Turunan"])

        st.markdown("---")
        st.markdown("**Prefix Metric (Awalan SI)**")
        prefix_data = [
            ["Tera (T)", "10¹²", "1.000.000.000.000"],
            ["Giga (G)", "10⁹", "1.000.000.000"],
            ["Mega (M)", "10⁶", "1.000.000"],
            ["Kilo (k)", "10³", "1.000"],
            ["Hekto (h)", "10²", "100"],
            ["Deka (da)", "10¹", "10"],
            ["Desi (d)", "10⁻¹", "0,1"],
            ["Senti (c)", "10⁻²", "0,01"],
            ["Mili (m)", "10⁻³", "0,001"],
            ["Mikro (μ)", "10⁻⁶", "0,000001"],
            ["Nano (n)", "10⁻⁹", "0,000000001"],
            ["Piko (p)", "10⁻¹²", "0,000000000001"]
        ]
        st.table(prefix_data)

    with tab2:
        st.markdown("<div class='sub-header'>🔢 Konstanta Fisika Fundamental</div>", unsafe_allow_html=True)
        st.markdown("Konstanta-konstanta ini digunakan secara universal dalam perhitungan fisika.")

        for name, data in PHYSICS_CONSTANTS.items():
            st.markdown(f"""
            <div class='constant-box'>
                <b>{name}</b> = {data['nilai']:.4e} {data['satuan']}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Catatan Penting:**")
        st.markdown("""
        - Kecepatan cahaya **c** adalah batas kecepatan maksimum di alam semesta
        - Konstanta Planck **h** menghubungkan energi dengan frekuensi (E = hf)
        - Konstanta gravitasi **G** digunakan dalam hukum gravitasi universal Newton
        - Konstanta Boltzmann **k** menghubungkan energi dengan suhu untuk partikel individual
        """)

    with tab3:
        st.markdown("<div class='sub-header'>📖 Rumus-Rumus Penting Fisika Dasar</div>", unsafe_allow_html=True)

        rumus_categories = {
            "Mekanika": [
                ("Hukum II Newton", "F = m · a", "Gaya = massa × percepatan"),
                ("Energi Kinetik", "Ek = ½ m v²", "Energi gerak = ½ × massa × kecepatan²"),
                ("Energi Potensial Gravitasi", "Ep = m g h", "Energi posisi = massa × gravitasi × ketinggian"),
                ("Momentum", "p = m v", "Momentum = massa × kecepatan"),
                ("Gerak Jatuh Bebas", "h = ½ g t²", "Ketinggian = ½ × gravitasi × waktu²"),
                ("Gerak Lurus Berubah Beraturan", "v = v₀ + a t", "Kecepatan akhir = awal + percepatan × waktu"),
                ("Gaya Gesek", "f = μ N", "Gaya gesek = koefisien gesek × gaya normal"),
            ],
            "Fluida": [
                ("Tekanan Hidrostatik", "P = ρ g h", "Tekanan = kerapatan × gravitasi × kedalaman"),
                ("Hukum Archimedes", "Fa = ρf V g", "Gaya apung = kerapatan fluida × volume × gravitasi"),
                ("Debit (Aliran)", "Q = A v", "Debit = luas penampang × kecepatan aliran"),
                ("Hukum Bernoulli", "P + ½ρv² + ρgh = konstan", "Energi per satuan volume konstan sepanjang aliran"),
                ("Viskositas (Newton)", "η = τ / (dv/dy)", "Viskositas = tegangan geser / laju regangan"),
                ("Kerapatan", "ρ = m / V", "Kerapatan = massa / volume"),
            ],
            "Termodinamika": [
                ("Persamaan Gas Ideal", "PV = nRT", "Tekanan×Volume = mol×konstanta gas×Suhu"),
                ("Kalor", "Q = m c ΔT", "Kalor = massa × kalor jenis × perubahan suhu"),
                ("Kalor Laten", "Q = m L", "Kalor = massa × kalor laten"),
                ("Efisiensi Carnot", "η = 1 - T₂/T₁", "Efisiensi = 1 - (suhu rendah/suhu tinggi) dalam Kelvin"),
                ("Energi Kinetik Gas", "Ek = 3/2 kT", "Energi rata-rata = 3/2 × konstanta Boltzmann × suhu"),
            ],
            "Listrik & Magnet": [
                ("Hukum Ohm", "V = I R", "Tegangan = arus × resistansi"),
                ("Daya Listrik", "P = V I = I²R = V²/R", "Daya = tegangan × arus"),
                ("Hukum Coulomb", "F = k q₁q₂/r²", "Gaya elektrostatik = konstanta × muatan²/jarak²"),
                ("Medan Listrik", "E = F/q = kQ/r²", "Medan = gaya/muatan uji"),
                ("Gaya Lorentz", "F = q(v × B)", "Gaya = muatan × (kecepatan × medan magnet)"),
                ("Induksi Faraday", "ε = -dΦ/dt", "GGL induksi = -laju perubahan fluks magnet"),
            ],
            "Gelombang & Optika": [
                ("Kecepatan Gelombang", "v = f λ", "Kecepatan = frekuensi × panjang gelombang"),
                ("Energi Foton", "E = h f", "Energi = konstanta Planck × frekuensi"),
                ("Hukum Snellius", "n₁ sin θ₁ = n₂ sin θ₂", "Indeks bias × sin sudut = konstan"),
                ("Pembesaran Lensa", "M = -s'/s = h'/h", "Pembesaran = -jarak bayangan/jarak benda"),
                ("Persamaan Lensa", "1/f = 1/s + 1/s'", "1/fokus = 1/jarak benda + 1/jarak bayangan"),
            ]
        }

        for category, formulas in rumus_categories.items():
            with st.expander(f"📌 {category}"):
                for name, formula, desc in formulas:
                    st.markdown(f"""
                    <div class='formula-box'>
                        <b>{name}</b><br>
                        <span style='font-size:1.3em; color:#1f77b4;'>{formula}</span><br>
                        <span style='color:#666; font-size:0.9em;'>{desc}</span>
                    </div>
                    """, unsafe_allow_html=True)

# ==================== HALAMAN KALKULATOR ====================
elif menu == "🧮 Kalkulator":
    st.markdown("<div class='main-header'>🧮 Smart Physics Calculator</div>", unsafe_allow_html=True)
    st.markdown("Isi nilai yang diketahui, sistem akan menghitung secara otomatis dengan langkah pengerjaan lengkap!")

    calc_type = st.selectbox(
        "Pilih Kalkulator:",
        ["📊 Kerapatan (Density)", "🍯 Viskositas (Kekentalan)", "📐 Sudut Reposisi", "🔄 Konversi Satuan"]
    )

    # --- KALKULATOR KERAPATAN ---
    if calc_type == "📊 Kerapatan (Density)":
        st.markdown("<div class='sub-header'>📊 Kalkulator Kerapatan (ρ = m/V)</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            mass = st.number_input("Massa (m):", min_value=0.0, value=1.0, step=0.1)
            mass_unit = st.selectbox("Satuan Massa:", ["kg", "g", "mg", "ton", "lb"])
        with col2:
            volume = st.number_input("Volume (V):", min_value=0.0, value=1.0, step=0.1)
            vol_unit = st.selectbox("Satuan Volume:", ["m³", "L", "cm³", "mL", "ft³", "mm³"])

        if st.button("🔍 Hitung Kerapatan", type="primary"):
            if mass <= 0 or volume <= 0:
                st.error("❌ Massa dan volume harus lebih besar dari 0!")
            else:
                # Konversi ke SI
                mass_kg = auto_convert(mass, mass_unit, "kg", "Massa")

                # Konversi volume
                vol_conversions = {
                    "m³": mass, "L": 0.001, "cm³": 1e-6, "mL": 1e-6, 
                    "ft³": 0.0283168, "mm³": 1e-9
                }
                vol_m3 = volume * vol_conversions.get(vol_unit, 1)

                density = mass_kg / vol_m3

                st.success("✅ Perhitungan Berhasil!")

                st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

                st.markdown(f"""
                <div class='step-box'>
                    <b>Langkah 1:</b> Konversi satuan ke SI<br>
                    Massa = {mass} {mass_unit} = {mass_kg:.6f} kg<br>
                    Volume = {volume} {vol_unit} = {vol_m3:.6e} m³
                </div>
                <div class='step-box'>
                    <b>Langkah 2:</b> Masukkan ke rumus kerapatan<br>
                    ρ = m / V = {mass_kg:.6f} / {vol_m3:.6e}
                </div>
                <div class='step-box'>
                    <b>Langkah 3:</b> Hasil akhir<br>
                    <span style='font-size:1.5em; color:#1f77b4;'><b>ρ = {density:.4f} kg/m³</b></span><br>
                    = {density/1000:.4f} g/cm³<br>
                    = {density*0.001:.4f} kg/L
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div class='sub-header'>📖 Penjelasan Rumus:</div>", unsafe_allow_html=True)
                st.info("""
                **Kerapatan (ρ)** adalah ukuran massa per satuan volume suatu zat. 
                Rumus: **ρ = m/V**

                - **ρ** (rho) = kerapatan (kg/m³)
                - **m** = massa benda (kg)
                - **V** = volume benda (m³)

                **Interpretasi Fisika:**
                - Air murni: ρ ≈ 1000 kg/m³ (pada 4°C)
                - Udara: ρ ≈ 1.225 kg/m³ (pada 15°C, 1 atm)
                - Besi: ρ ≈ 7870 kg/m³
                - Kerapatan relatif (specific gravity) = ρ_zat / ρ_air
                """)

    # --- KALKULATOR VISKOSITAS ---
    elif calc_type == "🍯 Viskositas (Kekentalan)":
        st.markdown("<div class='sub-header'>🍯 Kalkulator Viskositas Dinamis (η = τ / γ̇)</div>", unsafe_allow_html=True)

        st.markdown("""
        Viskositas dinamis dihitung dari tegangan geser (shear stress) dan laju regangan (shear rate).
        Untuk fluida Newton: **η = (F/A) / (dv/dy)**
        """)

        col1, col2 = st.columns(2)
        with col1:
            force = st.number_input("Gaya Geser (F):", min_value=0.0, value=10.0, step=0.1)
            f_unit = st.selectbox("Satuan Gaya:", ["N", "kN", "dyne", "kgf", "lbf"])
            area = st.number_input("Luas Penampang (A):", min_value=0.0, value=1.0, step=0.1)
            a_unit = st.selectbox("Satuan Luas:", ["m²", "cm²", "mm²", "ft²", "in²"])
        with col2:
            velocity = st.number_input("Kecepatan (v):", min_value=0.0, value=1.0, step=0.1)
            v_unit = st.selectbox("Satuan Kecepatan:", ["m/s", "cm/s", "mm/s", "km/h", "ft/s"])
            gradient = st.number_input("Gradien Kecepatan/Jarak (dy):", min_value=0.0, value=0.1, step=0.01)
            g_unit = st.selectbox("Satuan Gradien:", ["m", "cm", "mm", "ft", "in"])

        if st.button("🔍 Hitung Viskositas", type="primary"):
            if area <= 0 or gradient <= 0:
                st.error("❌ Luas dan gradien harus lebih besar dari 0!")
            else:
                # Konversi ke SI
                f_si = auto_convert(force, f_unit, "N", "Gaya") if f_unit != "N" else force

                area_conv = {"m²": 1, "cm²": 1e-4, "mm²": 1e-6, "ft²": 0.092903, "in²": 0.00064516}
                a_si = area * area_conv.get(a_unit, 1)

                v_si = auto_convert(velocity, v_unit, "m", "Panjang") if v_unit in UNIT_TABLE["Panjang"] else velocity
                if v_unit == "km/h":
                    v_si = velocity * 1000 / 3600
                elif v_unit == "cm/s":
                    v_si = velocity * 0.01
                elif v_unit == "mm/s":
                    v_si = velocity * 0.001
                elif v_unit == "ft/s":
                    v_si = velocity * 0.3048

                g_si = auto_convert(gradient, g_unit, "m", "Panjang") if g_unit in UNIT_TABLE["Panjang"] else gradient

                shear_stress = f_si / a_si
                shear_rate = v_si / g_si
                viscosity = shear_stress / shear_rate

                st.success("✅ Perhitungan Berhasil!")

                st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

                st.markdown(f"""
                <div class='step-box'>
                    <b>Langkah 1:</b> Konversi semua satuan ke SI<br>
                    Gaya = {force} {f_unit} = {f_si:.4f} N<br>
                    Luas = {area} {a_unit} = {a_si:.4e} m²<br>
                    Kecepatan = {velocity} {v_unit} = {v_si:.4f} m/s<br>
                    Gradien = {gradient} {g_unit} = {g_si:.4f} m
                </div>
                <div class='step-box'>
                    <b>Langkah 2:</b> Hitung Tegangan Geser (Shear Stress)<br>
                    τ = F/A = {f_si:.4f} / {a_si:.4e} = {shear_stress:.4f} Pa (N/m²)
                </div>
                <div class='step-box'>
                    <b>Langkah 3:</b> Hitung Laju Regangan (Shear Rate)<br>
                    γ̇ = dv/dy = {v_si:.4f} / {g_si:.4f} = {shear_rate:.4f} s⁻¹
                </div>
                <div class='step-box'>
                    <b>Langkah 4:</b> Hitung Viskositas Dinamis<br>
                    <span style='font-size:1.5em; color:#1f77b4;'><b>η = τ / γ̇ = {viscosity:.4f} Pa·s</b></span><br>
                    = {viscosity*10:.4f} Poise<br>
                    = {viscosity*1000:.4f} cP (centiPoise)
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div class='sub-header'>📖 Penjelasan Rumus:</div>", unsafe_allow_html=True)
                st.info("""
                **Viskositas Dinamis (η)** mengukur kekentalan fluida — resistensi terhadap aliran shear.

                **Rumus Newton untuk Viskositas:**
                **η = τ / γ̇**

                Dimana:
                - **η** = viskositas dinamis (Pa·s)
                - **τ** (tau) = tegangan geser = F/A (Pa atau N/m²)
                - **γ̇** (gamma-dot) = laju regangan = dv/dy (s⁻¹)
                - **F** = gaya geser (N)
                - **A** = luas penampang (m²)
                - **dv/dy** = gradien kecepatan per jarak (m/s per m = s⁻¹)

                **Referensi Viskositas:**
                - Air (20°C): ~1.002 cP = 0.001002 Pa·s
                - Madu: ~2000-10000 cP
                - Oli mesin (SAE 30): ~100-200 cP
                - Darah (37°C): ~3-4 cP
                """)

    # --- KALKULATOR SUDUT REPOSISI ---
    elif calc_type == "📐 Sudut Reposisi":
        st.markdown("<div class='sub-header'>📐 Kalkulator Sudut Reposisi (θ = arctan μₛ)</div>", unsafe_allow_html=True)

        st.markdown("""
        **Sudut reposisi** adalah sudut maksimum suatu bidang miring agar benda di atasnya tidak mulai meluncur.
        Rumus: **θ = arctan(μₛ)**
        """)

        mu_s = st.number_input("Koefisien Gesek Statis (μₛ):", min_value=0.0, max_value=10.0, value=0.5, step=0.01)

        if st.button("🔍 Hitung Sudut Reposisi", type="primary"):
            theta_deg, theta_rad = calc_repose_angle(mu_s)

            st.success("✅ Perhitungan Berhasil!")

            st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class='step-box'>
                <b>Langkah 1:</b> Identifikasi rumus<br>
                Sudut reposisi: θ = arctan(μₛ) = arctan({mu_s})
            </div>
            <div class='step-box'>
                <b>Langkah 2:</b> Hitung dalam radian<br>
                θ = arctan({mu_s}) = {theta_rad:.6f} rad
            </div>
            <div class='step-box'>
                <b>Langkah 3:</b> Konversi ke derajat<br>
                θ = {theta_rad:.6f} × (180/π) = <span style='font-size:1.5em; color:#1f77b4;'><b>{theta_deg:.2f}°</b></span>
            </div>
            <div class='step-box'>
                <b>Langkah 4:</b> Verifikasi dengan komponen gaya<br>
                tan(θ) = {math.tan(math.radians(theta_deg)):.4f} ≈ μₛ = {mu_s}<br>
                (Selisih akibat pembulatan derajat)
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div class='sub-header'>📖 Penjelasan Rumus:</div>", unsafe_allow_html=True)
            st.info("""
            **Sudut Reposisi (Angle of Repose)** adalah sudut maksimum suatu permukaan miring relatif terhadap horizontal 
            di mana material padat (benda) masih dapat bertahan tanpa meluncur.

            **Derivasi Rumus:**
            Pada kondisi kritis (akan meluncur):
            - Gaya gesek maksimum: fₘₐₓ = μₛN = μₛmg cos(θ)
            - Komponen gaya gravitasi sejajar bidang: mg sin(θ)
            - Saat kritis: mg sin(θ) = μₛmg cos(θ)
            - tan(θ) = μₛ
            - **θ = arctan(μₛ)**

            **Aplikasi Praktis:**
            - Desain tangki silo dan hopper
            - Teknik pertambangan (desain lereng tambang)
            - Farmasi (aliran serbuk obat)
            - Teknik sipil (stabilitas lereng tanah)

            **Referensi μₛ:**
            - Kayu pada kayu (kering): 0.25-0.5 → θ = 14°-26.6°
            - Karet pada aspal: 0.6-0.8 → θ = 31°-38.7°
            - Baja pada baja: 0.15-0.2 → θ = 8.5°-11.3°
            """)

    # --- KONVERSI SATUAN ---
    elif calc_type == "🔄 Konversi Satuan":
        st.markdown("<div class='sub-header'>🔄 Kalkulator Konversi Satuan</div>", unsafe_allow_html=True)

        category = st.selectbox("Kategori Besaran:", list(UNIT_TABLE.keys()))

        col1, col2, col3 = st.columns([2, 1, 2])

        units = list(UNIT_TABLE[category].keys())

        with col1:
            from_unit = st.selectbox("Dari:", units)
            value = st.number_input("Nilai:", value=1.0, step=0.1)

        with col2:
            st.markdown("<br><br><h2 style='text-align:center;'>➡️</h2>", unsafe_allow_html=True)

        with col3:
            to_unit = st.selectbox("Ke:", units)

        if st.button("🔄 Konversi", type="primary"):
            result = auto_convert(value, from_unit, to_unit, category)

            if result is not None:
                st.success(f"✅ **{value} {from_unit} = {result:.6g} {to_unit}**")

                st.markdown("<div class='sub-header'>📋 Langkah Pengerjaan:</div>", unsafe_allow_html=True)

                if category == "Suhu":
                    st.markdown(f"""
                    <div class='step-box'>
                        <b>Konversi Suhu:</b><br>
                        {value}°{from_unit} → {result:.4f}°{to_unit}<br>
                        <i>(Menggunakan rumus konversi suhu spesifik)</i>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    base = value * UNIT_TABLE[category][from_unit]
                    st.markdown(f"""
                    <div class='step-box'>
                        <b>Langkah 1:</b> Konversi ke unit dasar SI<br>
                        {value} {from_unit} = {value} × {UNIT_TABLE[category][from_unit]} = {base:.6e} (unit dasar)
                    </div>
                    <div class='step-box'>
                        <b>Langkah 2:</b> Konversi ke target<br>
                        {base:.6e} / {UNIT_TABLE[category][to_unit]} = {result:.6g} {to_unit}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("❌ Konversi tidak valid!")

# ==================== HALAMAN UNIT CONVERTER ====================
elif menu == "🔄 Unit Converter":
    st.markdown("<div class='main-header'>🔄 Auto Unit Converter</div>", unsafe_allow_html=True)
    st.markdown("Konversi satuan otomatis untuk berbagai besaran fisika dengan langkah pengerjaan.")

    converter_type = st.selectbox(
        "Pilih Kategori Konversi:",
        ["📏 Panjang", "⚖️ Massa", "⏱️ Waktu", "🌡️ Suhu", "💨 Tekanan", "⚡ Energi", "🔌 Daya", "📊 Kerapatan", "🍯 Viskositas", "💪 Gaya"]
    )

    category_map = {
        "📏 Panjang": "Panjang", "⚖️ Massa": "Massa", "⏱️ Waktu": "Waktu",
        "🌡️ Suhu": "Suhu", "💨 Tekanan": "Tekanan", "⚡ Energi": "Energi",
        "🔌 Daya": "Daya", "📊 Kerapatan": "Kerapatan", "🍯 Viskositas": "Viskositas", "💪 Gaya": "Gaya"
    }

    cat = category_map[converter_type]
    units = list(UNIT_TABLE[cat].keys())

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        from_u = st.selectbox("Dari Satuan:", units, key="from")
        val = st.number_input("Masukkan Nilai:", value=1.0, step=0.1)

    with col2:
        st.markdown("<br><br><h1 style='text-align:center;'>⇄</h1>", unsafe_allow_html=True)

    with col3:
        to_u = st.selectbox("Ke Satuan:", units, key="to")

    if st.button("🚀 Konversi Sekarang", type="primary", use_container_width=True):
        result = auto_convert(val, from_u, to_u, cat)

        if result is not None:
            st.balloons()
            st.markdown(f"""
            <div style='background-color:#e8f4f8; padding:20px; border-radius:15px; text-align:center; margin:20px 0;'>
                <h2 style='color:#1f77b4; margin:0;'>{val} {from_u}</h2>
                <h1 style='margin:10px 0;'>⬇️</h1>
                <h2 style='color:#ff7f0e; margin:0;'>= {result:.6g} {to_u}</h2>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📋 Lihat Langkah Pengerjaan"):
                if cat == "Suhu":
                    st.markdown(f"""
                    **Rumus Konversi Suhu:**
                    - Celcius → Kelvin: K = C + 273.15
                    - Celcius → Fahrenheit: F = C × 9/5 + 32
                    - Celcius → Rankine: R = (C + 273.15) × 9/5
                    - Fahrenheit → Celcius: C = (F - 32) × 5/9

                    **Hasil:** {val}°{from_u} = {result:.4f}°{to_u}
                    """)
                else:
                    base_val = val * UNIT_TABLE[cat][from_u]
                    st.markdown(f"""
                    **Langkah 1: Konversi ke Unit Dasar SI**

                    Faktor konversi {from_u} ke unit dasar = {UNIT_TABLE[cat][from_u]}

                    {val} {from_u} × {UNIT_TABLE[cat][from_u]} = {base_val:.6e} (unit dasar SI)

                    **Langkah 2: Konversi ke Satuan Target**

                    Faktor konversi unit dasar ke {to_u} = 1/{UNIT_TABLE[cat][to_u]}

                    {base_val:.6e} ÷ {UNIT_TABLE[cat][to_u]} = **{result:.6g} {to_u}**
                    """)
        else:
            st.error("❌ Konversi gagal. Periksa satuan yang dipilih.")

    st.markdown("---")
    st.markdown("<div class='sub-header'>📊 Tabel Konversi Cepat</div>", unsafe_allow_html=True)

    quick_conversions = {
        "Panjang": [("1 m", "100 cm", "3.281 ft", "39.37 in"), ("1 km", "0.621 mi", "3281 ft", "100000 cm")],
        "Massa": [("1 kg", "1000 g", "2.205 lb", "35.27 oz"), ("1 ton", "1000 kg", "2205 lb", "1e6 g")],
        "Suhu": [("0°C", "32°F", "273.15 K", "491.67°R"), ("100°C", "212°F", "373.15 K", "671.67°R")],
        "Tekanan": [("1 atm", "101325 Pa", "1.013 bar", "760 mmHg"), ("1 bar", "100000 Pa", "0.987 atm", "750 mmHg")],
        "Energi": [("1 J", "0.239 cal", "0.000278 Wh", "6.24e18 eV"), ("1 kWh", "3.6e6 J", "860 kcal", "3.6e9 mJ")],
        "Kerapatan": [("1 g/cm³", "1000 kg/m³", "1 kg/L", "62.43 lb/ft³"), ("1 kg/m³", "0.001 g/cm³", "0.001 kg/L", "0.062 lb/ft³")],
    }

    if cat in quick_conversions:
        for row in quick_conversions[cat]:
            cols = st.columns(len(row))
            for i, val_str in enumerate(row):
                with cols[i]:
                    st.metric(label="", value=val_str)

# ==================== HALAMAN QUIZ ====================
elif menu == "📝 Quiz Fisika":
    st.markdown("<div class='main-header'>📝 Quiz Fisika Dasar</div>", unsafe_allow_html=True)
    st.markdown("Latihan soal pilihan ganda dan isian singkat dengan pembahasan otomatis. Kategori: **Kuliah Dasar**")

    # Inisialisasi state
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_answered' not in st.session_state:
        st.session_state.quiz_answered = set()
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = 0

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='background-color:#f0f2f6; padding:15px; border-radius:10px; text-align:center;'>
            <h3>🏆 Skor: {st.session_state.quiz_score} / {len(QUIZ_QUESTIONS)}</h3>
            <progress value={st.session_state.quiz_score} max={len(QUIZ_QUESTIONS)} style='width:100%; height:20px;'></progress>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Tampilkan semua soal
    for idx, q in enumerate(QUIZ_QUESTIONS):
        with st.container():
            st.markdown(f"<div class='sub-header'>Soal {idx+1} ({q['type'].replace('_', ' ').title()})</div>", unsafe_allow_html=True)
            st.markdown(f"**{q['soal']}**")

            answered = idx in st.session_state.quiz_answered

            if q['type'] == "pilihan_ganda":
                user_answer = st.radio(
                    f"Pilih jawaban (Soal {idx+1}):",
                    q['pilihan'],
                    key=f"pg_{idx}",
                    disabled=answered
                )

                if not answered:
                    if st.button(f"✅ Submit Jawaban Soal {idx+1}", key=f"btn_pg_{idx}"):
                        st.session_state.quiz_answered.add(idx)
                        if user_answer == q['jawaban']:
                            st.session_state.quiz_score += 1
                            st.success("✅ Benar!")
                        else:
                            st.error(f"❌ Salah! Jawaban yang benar: **{q['jawaban']}**")
                        st.info(f"📖 **Pembahasan:** {q['pembahasan']}")
                        st.rerun()
                else:
                    # Tampilkan hasil yang tersimpan
                    # Cek apakah jawaban benar (perlu cek dari state, tapi simpelnya kita cek dari score logic)
                    # Untuk sederhana, tampilkan pembahasan saja
                    st.info(f"📖 **Pembahasan:** {q['pembahasan']}")

            else:  # isian
                user_answer = st.text_input(
                    f"Jawaban Anda (Soal {idx+1}):",
                    key=f"isian_{idx}",
                    disabled=answered
                )

                if not answered:
                    if st.button(f"✅ Submit Jawaban Soal {idx+1}", key=f"btn_isian_{idx}"):
                        if user_answer.strip():
                            st.session_state.quiz_answered.add(idx)
                            # Cek jawaban (toleransi untuk angka)
                            try:
                                user_val = float(user_answer.strip().replace(',', '.'))
                                correct_val = float(q['jawaban'].replace(',', '.'))
                                if abs(user_val - correct_val) < 0.01 * max(abs(correct_val), 1):
                                    st.session_state.quiz_score += 1
                                    st.success("✅ Benar!")
                                else:
                                    st.error(f"❌ Salah! Jawaban yang benar: **{q['jawaban']}**")
                            except:
                                if user_answer.strip().lower() == q['jawaban'].strip().lower():
                                    st.session_state.quiz_score += 1
                                    st.success("✅ Benar!")
                                else:
                                    st.error(f"❌ Salah! Jawaban yang benar: **{q['jawaban']}**")
                            st.info(f"📖 **Pembahasan:** {q['pembahasan']}")
                            st.rerun()
                        else:
                            st.warning("⚠️ Masukkan jawaban terlebih dahulu!")
                else:
                    st.info(f"📖 **Pembahasan:** {q['pembahasan']}")

            st.markdown("---")

    # Tombol reset
    if st.button("🔄 Reset Quiz", type="secondary"):
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = set()
        st.rerun()

    if st.session_state.quiz_score == len(QUIZ_QUESTIONS):
        st.balloons()
        st.markdown("""
        <div style='background-color:#d4edda; padding:20px; border-radius:15px; text-align:center; margin-top:20px;'>
            <h1 style='color:#155724;'>🎉 Selamat! 🎉</h1>
            <h2 style='color:#155724;'>Anda telah menjawab semua soal dengan benar!</h2>
            <p style='font-size:1.2em;'>Skor sempurna: {}/{}</p>
        </div>
        """.format(len(QUIZ_QUESTIONS), len(QUIZ_QUESTIONS)), unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align:center; color:#888;'>⚛️ Smart Physics Calculator v1.0<br>Built with Streamlit</p>", unsafe_allow_html=True)
