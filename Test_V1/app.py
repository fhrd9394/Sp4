from flask import Flask, render_template, request
from transformers import pipeline
#from transformers import AutoModelForCausalLM


# Pipeline für die Code-Generierung einrichten
code_generator = pipeline("text-generation", model="bigcode/starcoder", device=-1)

# Flask-Anwendung initialisieren
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output_text = ""
    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            try:
                # Code-Generierung mit dem eingegebenen Prompt
                output = code_generator(prompt, max_new_tokens=500, num_return_sequences=1, do_sample=True, temperature=0.7)
                if output and 'generated_text' in output[0]:
                    output_text = output[0]['generated_text'].strip()
                else:
                    output_text = "Keine gültige Antwort vom Modell erhalten."
            except Exception as e:
                output_text = f"Fehler bei der Generierung: {e}"
        else:
            output_text = "Bitte einen gültigen Prompt eingeben."

    return render_template("index.html", output_text=output_text)

if __name__ == "__main__":
    app.run(debug=False)

#http://127.0.0.1:5000/
#meta-llama/Llama-3.1-8B-Instruct