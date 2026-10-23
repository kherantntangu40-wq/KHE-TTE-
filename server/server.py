from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__)
CORS(app)

@app.route("/")
def accueil():
    return jsonify({
        "nom": "KHEÏTTE",
        "statut": "en ligne",
        "message": "Bonjour Kheran ! Ton assistant est prêt à évoluer."
    })

@app.route("/sante")
def sante():
    return jsonify({"statut": "fonctionnel"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
0

