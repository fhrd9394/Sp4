from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import traceback
import os
import re

# Pipeline für die Code-Generierung einrichten
code_generator = pipeline("text-generation", model="meta-llama/Llama-3.1-8B-Instruct", device=-1)

# Flask-Anwendung initialisieren
app = Flask(__name__)

# Speicherort für die generierte Ausgabe
output_file_path = os.path.join("generated_outputs", "all_outputs.txt")
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Sicherstellen, dass die zentrale Datei existiert
if not os.path.exists(output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write("### Generierte Ausgaben ###\n\n")


def generate_code_from_prompt(prompt):
    """
    Generiert Code basierend auf dem gegebenen Prompt und entfernt unnötige Erklärungen.
    """
    try:
        # Generierung des Outputs mit dem Modell
        output = code_generator(prompt, max_new_tokens=200, num_return_sequences=1, do_sample=True, temperature=0.7)
        if output and 'generated_text' in output[0]:
            raw_output = output[0]['generated_text'].strip()

            # Entferne unnötige Teile der Antwort, wie Erklärungen oder Text, der nicht zum Code gehört
            filtered_output = filter_code_from_explanations(raw_output)

            # Speichere die bereinigte Ausgabe in der Datei
            save_output_to_file(prompt, filtered_output)

            return filtered_output
        else:
            print("Keine gültige Antwort vom Modell erhalten.")
            return "Keine gültige Antwort vom Modell erhalten."
    except Exception as e:
        error_message = f"Fehler bei der Generierung: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return error_message


def filter_code_from_explanations(output):
    """
    Entfernt erklärende Texte und konzentriert sich nur auf den Code.
    """
    # Suche nach Codeblöcken und entferne alles, was nicht zu einem Codeblock gehört
    code_blocks = re.findall(r"```(.*?)```", output, re.DOTALL)

    if code_blocks:
        # Wenn Codeblöcke gefunden werden, gib diese zurück
        return "\n\n".join(set(block.strip() for block in code_blocks))
    else:
        # Wenn keine Codeblöcke gefunden werden, versuche den Code direkt aus der Ausgabe zu extrahieren
        # Entferne alle nicht-Code-Elemente (z.B. "In Python, das ...")
        lines = output.splitlines()
        code_lines = [line.strip() for line in lines if line.strip() and not line.startswith("#")]

        return "\n".join(code_lines).strip()


def save_output_to_file(prompt, output):
    """
    Speichert den generierten Code zusammen mit dem Prompt in einer Datei.
    """
    try:
        with open(output_file_path, "a", encoding="utf-8") as file:
            file.write(f"### Prompt: {prompt} ###\n")
            file.write(output + "\n\n")
    except Exception as e:
        print(f"Fehler beim Schreiben in die Datei: {e}")



@app.route("/", methods=["GET", "POST"])
def index():
    output_text = ""

    if request.method == "POST":
        # Prompt von der HTML-Seite abrufen
        prompt = request.form.get("prompt")

        if prompt:
            # Generiere Code mit der neuen Funktion
            output_text = generate_code_from_prompt(prompt)

    # Render die HTML-Seite mit dem Ergebnis
    return render_template(
        "index.html",
        output_text=output_text,
        output_file_path=output_file_path,
    )

@app.route("/api/generate", methods=["POST"])
def generate_code_api():
    """
    API-Endpunkt, um Code basierend auf einem Prompt zu generieren.
    """
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Kein Prompt angegeben"}), 400

    prompt = data["prompt"]
    try:
        generated_code = generate_code_from_prompt(prompt)
        return jsonify({"generated_code": generated_code}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Flask-Server nur starten, wenn app.py direkt ausgeführt wird
    app.run(debug=True)







#http://127.0.0.1:5000/
#meta-llama/Llama-3.1-8B-Instruct