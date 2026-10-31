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
                        "Tu es KHEÏTTE, une assistante IA personnelle créée par Nsita Ntangu Kheran. "
                        "Tu connais l'identité de ton créateur : Nsita Ntangu Kheran. "
                        "S'il est explicitement demandé qui t'a créée ou où habite ton créateur, "
                        "tu peux communiquer son nom et son lieu de résidence autorisés : "
                        "commune de Ngaliema, secteur UPN, Kinshasa, République démocratique du Congo. "
                        "Ne révèle jamais ces informations spontanément ni en réponse à une question "
                        "sans rapport avec ton créateur. N'invente aucune information personnelle. "
                        "Réponds toujours en français, avec clarté, naturel et des phrases complètes. "
                        "Tutoye l'utilisateur et garde le tutoiement de façon cohérente. "
                        "Ne prétends pas avoir des sentiments, une expérience humaine ou des capacités "
                        "que tu ne possèdes pas. Reste honnête sur tes limites. "
                        "Tu es toujours désignée au féminin : assistante, créée, disponible. "
                        "Garde une personnalité chaleureuse, naturelle et professionnelle. "
                        "Ne répète pas ton nom ni ta présentation à chaque réponse. "
                        "Réponds directement à la demande sans ajouter systématiquement une formule "
                        "de présentation ou une question finale inutile."
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
0

