from flask import Flask, render_template, request
from transformers import pipeline
import traceback
import os

# Pipeline für die Code-Generierung einrichten
code_generator = pipeline("text-generation", model="meta-llama/Llama-3.1-8B-Instruct", device=-1)

# Flask-Anwendung initialisieren
app = Flask(__name__)

# Speicherort für die generierten Dateien
output_dir = "generated_outputs"
os.makedirs(output_dir, exist_ok=True)  # Sicherstellen, dass der Ordner existiert

@app.route("/", methods=["GET", "POST"])
def index():
    output_text = ""
    output_file_path = ""

    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            try:
                # Code-Generierung mit dem eingegebenen Prompt
                output = code_generator(prompt, max_new_tokens=500, num_return_sequences=1, do_sample=True, temperature=0.7)
                if output and 'generated_text' in output[0]:
                    output_text = output[0]['generated_text'].strip()

                    # Speichere die Ausgabe in eine Datei
                    file_name = f"output_{len(os.listdir(output_dir)) + 1}.txt"
                    output_file_path = os.path.join(output_dir, file_name)
                    with open(output_file_path, "w", encoding="utf-8") as file:
                        file.write(output_text)
                else:
                    output_text = "Keine gültige Antwort vom Modell erhalten."
            except Exception as e:
                output_text = f"Fehler bei der Generierung: {str(e)}\n{traceback.format_exc()}"
        else:
            output_text = "Bitte einen gültigen Prompt eingeben."

    return render_template("index.html", output_text=output_text, output_file_path=output_file_path)

if __name__ == "__main__":
    app.run(debug=True)



#http://127.0.0.1:5000/
#meta-llama/Llama-3.1-8B-Instruct