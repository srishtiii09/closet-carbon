import base64
import os
from flask import Flask, request, render_template, session
from groq import Groq
from eco_engine import analyse_garment   

# ── Load environment variables from your hidden .env file ───────────────────
from dotenv import load_dotenv
load_dotenv()  

app = Flask(__name__)
app.secret_key = os.urandom(24)          

# ── Securely load the Groq client using your environment variable ───────────
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return render_template("index.html", error="No image uploaded")

    image_file = request.files["image"]
    image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # ── Read wear count from form (0 if not provided / new garment) ──────────
    try:
        wear_count = int(request.form.get("wear_count", 0))
    except ValueError:
        wear_count = 0

    try:
        # ── Groq call ────────────────────────────────────────────────────────
        completion = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Analyze the fabric(s) in this clothing image. "
                                "If more than one fabric, list all separated by commas. "
                                "Respond ONLY in this exact format, nothing else:\n"
                                "Fabric: <fabric name(s)>\n"
                                "EcoPoints: <number 1-10>"
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "data:image/jpeg;base64," + base64_image
                            },
                        },
                    ],
                }
            ],
            temperature=0.1,
            max_tokens=50,
        )

        raw_result = completion.choices[0].message.content.strip()
        print("AI RESULT:", raw_result)

        # ── Parse Groq response ───────────────────────────────────────────────
        fabric_label = None
        groq_eco_points = None

        for line in raw_result.splitlines():
            line = line.strip()
            if line.lower().startswith("fabric:"):
                fabric_label = line.split(":", 1)[1].strip()
            elif line.lower().startswith("ecopoints:"):
                try:
                    groq_eco_points = float(line.split(":", 1)[1].strip())
                except ValueError:
                    groq_eco_points = None

        # ── Run eco engine ────────────────────────────────────────────────────
        eco = None
        if fabric_label:
            eco = analyse_garment(fabric_label, wear_count)

        return render_template(
            "index.html",
            result=raw_result,           
            fabric_label=fabric_label,
            groq_eco_points=groq_eco_points,
            eco=eco,                     
            wear_count=wear_count,
        )

    except Exception as e:
        print("AI ERROR:", e)
        return render_template("index.html", error=str(e))


# ── Wear logger (AJAX endpoint for "I wore this today" button) ───────────────
@app.route("/log_wear", methods=["POST"])
def log_wear():
    from flask import jsonify
    data = request.get_json(silent=True) or {}
    fabric_label = data.get("fabric_label", "")
    wear_count   = int(data.get("wear_count", 0)) + 1
    eco = analyse_garment(fabric_label, wear_count)
    return jsonify({"wear_count": wear_count, "eco": eco})


if __name__ == "__main__":
    app.run(debug=True)
