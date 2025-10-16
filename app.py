# app.py
import os
from package import app, authentication
from flask import jsonify, request, render_template, send_from_directory

# ==============================
# 🏠 Root Route
# ==============================


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Lead Generation API!"})


# ==============================
# 🧍‍♂️ Signup Route
# ==============================
@app.route("/api/signup", methods=["POST"])
def signup():
    payload = request.json
    result = authentication.sign_up(payload)
    return jsonify(result), 200 if result["status"] == "success" else 400


# ==============================
# 🔐 Login Route
# ==============================
@app.route("/api/login", methods=["POST"])
def login():
    payload = request.json
    result = authentication.sign_in(payload)
    return jsonify(result), 200 if result["status"] == "success" else 400


# ==============================
# 🚪 Logout Route
# ==============================
@app.route("/api/logout", methods=["POST"])
def logout():
    result = authentication.sign_out()
    return jsonify(result), 200 if result["status"] == "success" else 400


# ==============================
# ⚠️ Error Handlers
# ==============================
@app.errorhandler(404)
def page_not_found(e):
    return render_template("pages/404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("pages/500.html"), 500


@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'robots.txt',
                               mimetype='text/plain')


# ==============================
# 🚀 Entry Point
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
