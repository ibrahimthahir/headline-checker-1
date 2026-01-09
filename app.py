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
    "betina", "jalang", "pelacur",

    # Makian/cacian
    "bodoh", "bangang", "sial", "celaka",
    "babi", "anjing", "haram jadah",
    "kurang ajar", "lancau", "pukimak", "barua",

    # Ejaan alternatif/kod
    "b4ru4", "puk1mak", "anj1ng", "b0d0h", "b@bi"
]

# Senarai frasa berisiko dengan 'makin'
frasa_makin_tidak_sesuai = [
    "makin benci", "makin marah", "makin teruk", "makin ganas",
    "makin melampau", "makin liar", "makin berani langgar"
]

def semak_headline(headline):
    teks = headline.lower()

    # Semak kata larangan eksplisit
    for kata in kata_larangan:
        if kata in teks:
            return {
                "status": "Tidak Selari",
                "sebab": f"Mengandungi kata tabu/larangan: '{kata}'"
            }

    # Semak frasa berisiko dengan 'makin'
    for frasa in frasa_makin_tidak_sesuai:
        if frasa in teks:
            return {
                "status": "Tidak Selari",
                "sebab": f"Frasa berisiko dikesan: '{frasa}'"
            }

    return {
        "status": "Selari",
        "sebab": "Tiada pelanggaran dikesan"
    }

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    headline = data.get("headline", "")
    result = semak_headline(headline)
    return jsonify(result)

if __name__ == '__main__':
    print("Server Flask sedang dimulakan...")
    app.run(debug=True)

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Sistem Semakan Headline Aktif dan Sedia Digunakan"

