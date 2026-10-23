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

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"erreur": "Écris un message."}), 400

    try:
        reponse = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es KHEÏTTE, l'assistant personnel créé par "
                        "Kheran Ntangu. Réponds en français, clairement "
                        "et naturellement."
                    )
                },
                {"role": "user", "content": message}
            ]
        )
        return jsonify({
            "reponse": reponse.choices[0].message.content
        })
    except Exception:
        app.logger.exception("Erreur pendant la réponse IA")
        return jsonify({
            "erreur": "Je n'arrive pas à répondre pour le moment."
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
0

