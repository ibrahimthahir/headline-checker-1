from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from difflib import SequenceMatcher

app = Flask(__name__)
CORS(app)

# Senarai kata larangan eksplisit (anda yang tentukan)
kata_larangan = [
    # Lucah/tabu
    "fitnah", "hoax", "lucah", "kebencian",
    "kote", "puki", "tetek", "butuh",
    "jubur", "air mani", "air mazi",
    "betina", "jalang", "pelacur", "onani", "bogel", "bulu pubis",
    "taik", "fak",

    # Makian/cacian
    "bodoh", "bangang", "sial", "celaka",
    "babi", "anjing", "haram jadah",
    "kurang ajar", "lancau", "pukimak", "barua", "bangsat",

    # Ejaan alternatif/kod
    "b4ru4", "puk1mak", "anj1ng", "b0d0h", "b@bi", "k*te", "4nj1ng"
]

# Frasa berisiko
frasa_makin_tidak_sesuai = [
    "makin benci", "makin marah", "makin teruk", "makin ganas",
    "makin melampau", "makin liar", "makin berani langgar"
]

# Frasa lucah (anda yang tentukan)
frasa_lucah = [
    "keluarkan air mani",
    "bergetar ovari",
    "betina nak mengawan",
    "rangsangan seksual",
    "nafsu syahwat",
    "aksi ghairah",
    "berahi melampau",
    "video lucah",
    "gambar bogel",
    "cerita seks"
]

# Pola regex untuk ejaan kreatif (selamat)
pola_lucah = [
    r"l[\W_]*u[\W_]*c[\W_]*a?[\W_]*h",
    r"s[e3][kq]s",
    r"b[o0]g[e3]l"
]

pola_makian = [
    r"h[i1]na",
    r"c[e3]rc[a@]",
    r"k[u*]t[u*]k"
]

# ⭐ Pola Regex Generik Untuk Ejaan Kreatif (Selamat & Berfungsi)
pola_generik = [
    r"[a@4]",          # variasi huruf A
    r"[i1!|]",         # variasi huruf I
    r"[o0]",           # variasi huruf O
    r"[u*]",           # variasi huruf U
    r"(.)\1{1,}",      # huruf berganda
    r"[\W_]+",         # simbol di antara huruf
]

def hampir_sama(a, b):
    """Fuzzy matching untuk ejaan hampir sama."""
    return SequenceMatcher(None, a, b).ratio() > 0.80

def padan_regex(teks, pola_list):
    for pola in pola_list:
        if re.search(pola, teks):
            return True
    return False

def semak_headline(headline):
    if not headline:
        return {
            "status": "Selari",
            "sebab": ["Tiada tajuk diberikan"],
            "panjang": 0
        }

    teks = headline.lower()
    sebab = []

    # Semak kata larangan eksplisit
    for kata in kata_larangan:
        if kata in teks:
            sebab.append(f"Mengandungi kata tabu/larangan: '{kata}'")

    # Semak frasa lucah
    for frasa in frasa_lucah:
        if frasa in teks:
            sebab.append(f"Frasa lucah dikesan: '{frasa}'")

    # Semak frasa 'makin'
    for frasa in frasa_makin_tidak_sesuai:
        if frasa in teks:
            sebab.append(f"Frasa berisiko dikesan: '{frasa}'")

    # Semak regex ejaan kreatif khusus
    if padan_regex(teks, pola_lucah):
        sebab.append("Pola ejaan kreatif berkaitan kandungan tidak sesuai dikesan")

    if padan_regex(teks, pola_makian):
        sebab.append("Pola ejaan kreatif berkaitan makian dikesan")

    # ⭐ Semak regex generik (huruf simbol, nombor, jarak, ulang)
    if padan_regex(teks, pola_generik):
        sebab.append("Pola ejaan kreatif generik dikesan (berpotensi kata sensitif)")

    # Fuzzy matching
    for kata in teks.split():
        for larangan in kata_larangan:
            if hampir_sama(kata, larangan):
                sebab.append(f"Perkataan hampir sama dengan kata larangan: '{kata}'")

    status = "Selari" if not sebab else "Tidak Selari"

    return {
        "status": status,
        "sebab": sebab if sebab else ["Tiada pelanggaran dikesan"],
        "panjang": len(headline)
    }

@app.route('/')
def home():
    return "Sistem Semakan Headline Aktif dan Sedia Digunakan"

@app.route('/check', methods=['POST'])
def check():
    data = request.json or {}
    headline = data.get("headline", "")
    result = semak_headline(headline)
    return jsonify(result)

if __name__ == '__main__':
    print("Server Flask sedang dimulakan...")
    app.run(debug=True)

