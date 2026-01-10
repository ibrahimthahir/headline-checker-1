from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Senarai kata larangan eksplisit (lucah + makian/cacian + ejaan alternatif)
kata_larangan = [
    # Lucah/tabu
    "fitnah", "hoax", "lucah", "kebencian",
    "kote", "puki", "tetek", "butuh",
    "jubur", "air mani", "air mazi",
    "betina", "jalang", "pelacur", "onani", "bogel", "bulu pubis",
    "taik",

    # Makian/cacian
    "bodoh", "bangang", "sial", "celaka",
    "babi", "anjing", "haram jadah",
    "kurang ajar", "lancau", "pukimak", "barua", "bangsat", 

    # Ejaan alternatif/kod
    "b4ru4", "puk1mak", "anj1ng", "b0d0h", "b@bi", "k*te", "4nj1ng"
]

# Senarai frasa berisiko dengan 'makin'
frasa_makin_tidak_sesuai = [
    "makin benci", "makin marah", "makin teruk", "makin ganas",
    "makin melampau", "makin liar", "makin berani langgar"
]

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

    # Semak frasa berisiko dengan 'makin'
    for frasa in frasa_makin_tidak_sesuai:
        if frasa in teks:
            sebab.append(f"Frasa berisiko dikesan: '{frasa}'")

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

