from flask import Flask, render_template, request
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
    Generiert Code basierend auf dem gegebenen Prompt, speichert ihn und gibt die Ausgabe zurück.
    """
    try:
        # Generierung des Outputs mit dem Modell
        output = code_generator(prompt, max_new_tokens=200, num_return_sequences=1, do_sample=True, temperature=0.7)
        if output and 'generated_text' in output[0]:
            raw_output = output[0]['generated_text'].strip()

            # Suche nach Code-Blöcken
            code_blocks = re.findall(r"```.*?\n(.*?)```", raw_output, re.DOTALL)
            if code_blocks:
                # Gefilterte Ausgabe (nur Code)
                filtered_output = "\n\n".join(set(block.strip() for block in code_blocks))
            else:
                # Keine Code-Blöcke gefunden, gesamte Ausgabe verwenden
                filtered_output = raw_output

            # Zeige nur den gefilterten Output in der Konsole
            print("\nGefilterter Output (für Konsole):\n")
            print(filtered_output)

            # Ausgabe in Datei speichern
            try:
                with open(output_file_path, "a", encoding="utf-8") as file:
                    file.write(f"### Prompt: {prompt} ###\n")
                    file.write(filtered_output + "\n\n")
            except Exception as e:
                print(f"Fehler beim Schreiben in die Datei: {e}")

            # Rückgabe der Ausgabe
            return filtered_output
        else:
            print("Keine gültige Antwort vom Modell erhalten.")
            return "Keine gültige Antwort vom Modell erhalten."
    except Exception as e:
        error_message = f"Fehler bei der Generierung: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return error_message


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


if __name__ == "__main__":
    app.run(debug=True)







#http://127.0.0.1:5000/
#meta-llama/Llama-3.1-8B-Instruct