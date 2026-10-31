import os
import requests
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


# SUPABASE_AUTH_ROUTES

def supabase_auth(endpoint, payload):
    url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    key = os.environ.get("SUPABASE_ANON_KEY", "")

    if not url or not key:
        return None, "Configuration Supabase manquante."

    try:
        response = requests.post(
            f"{url}/auth/v1/{endpoint}",
            headers={
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=20
        )
        try:
            result = response.json()
        except ValueError:
            result = {}

        return (result, None) if response.ok else (None, result.get("msg") or result.get("message") or result.get("error_description") or "Vérifie ton adresse e-mail et ton mot de passe.")
    except requests.RequestException:
        return None, "Impossible de joindre le service d'authentification."

@app.route("/inscription", methods=["POST"])
def inscription():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"erreur": "E-mail et mot de passe obligatoires."}), 400

    resultat, erreur = supabase_auth("signup", {
        "email": email,
        "password": password
    })

    if erreur:
        return jsonify({"erreur": erreur}), 400

    return jsonify({
        "message": "Inscription reçue. Vérifie ta boîte e-mail pour confirmer ton compte si nécessaire.",
        "utilisateur": (resultat.get("user") or {}).get("email")
    }), 201

@app.route("/connexion", methods=["POST"])
def connexion():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"erreur": "E-mail et mot de passe obligatoires."}), 400

    resultat, erreur = supabase_auth("token?grant_type=password", {
        "email": email,
        "password": password
    })

    if erreur:
        return jsonify({"erreur": erreur}), 401

    return jsonify({
        "message": "Connexion réussie.",
        "access_token": resultat.get("access_token"),
        "refresh_token": resultat.get("refresh_token"),
        "expires_in": resultat.get("expires_in"),
        "utilisateur": (resultat.get("user") or {}).get("email")
    }), 200

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

