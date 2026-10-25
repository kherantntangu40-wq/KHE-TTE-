import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

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

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return jsonify({
            "erreur": "La clé API de l'intelligence artificielle n'est pas configurée."
        }), 503

    try:
        client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        resultat = client.chat.completions.create(
            model=os.environ.get("OPENROUTER_MODEL", "google/gemma-4-26b-a4b-it:free"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es KHEÏTTE, l'assistant personnel créé par Kheran. "
                        "Réponds en français, clairement et naturellement."
                    )
                },
                {"role": "user", "content": message}
            ]
        )
        return jsonify({
            "reponse": resultat.choices[0].message.content or ""
        })
    except Exception:
        app.logger.exception("Erreur pendant la réponse IA")
        return jsonify({
            "erreur": "Je n'arrive pas à répondre pour le moment."
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
