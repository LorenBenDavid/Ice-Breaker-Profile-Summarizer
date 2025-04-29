from flask import Flask, render_template, request, jsonify
from ice_breaker import ice_break
from agents.linkedin_lookup_agents import lookup as lookup

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    print(f"🔍 Processing name: {name}")

    # מצא את ה-LinkedIn URL באמצעות ה-lookup
    linkedin_result = lookup(name=name)

    if isinstance(linkedin_result, dict):
        linkedin_username = linkedin_result.get("output", "")
    else:
        linkedin_username = linkedin_result

    # ניקוי אוטומטי אם יצא טקסט במקום לינק
    if "http" in linkedin_username:
        start = linkedin_username.find("http")
        linkedin_username = linkedin_username[start:].strip()

# הסרה של נקודה מסוף הלינק אם קיימת
    if linkedin_username.endswith("."):
        linkedin_username = linkedin_username[:-1]

    if isinstance(linkedin_username, dict):
        linkedin_username = linkedin_username.get("output", "")

    # בדיקת תקינות הקישור
    if not linkedin_username or "Unable to find" in linkedin_username or "Unfortunately" in linkedin_username:
        return jsonify({"error": "Unable to find LinkedIn profile for the provided name."}), 400

    # שלח את ה-URL ל-Scrapin.io API כדי לשלוף את המידע
    person_info, profile_pic_url = ice_break(linkedin_username)

    if person_info is None:
        return jsonify({"error": "No data available for the provided name."}), 500

    return jsonify({
        "summary": person_info.summary,
        "facts": person_info.facts,
        "picture_url": profile_pic_url,
    })


if __name__ == "__main__":
    # הפעלת השרת ב-debug עם פורט 5001 (אם 5000 תפוס)
    app.run(host="0.0.0.0", port=5001, debug=True)
