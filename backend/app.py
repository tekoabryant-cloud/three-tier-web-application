from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "../database/app.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "The application tier is working!"
    })


@app.route("/api/applications", methods=["POST"])
def create_application():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "error": "Name and email are required."
        }), 400

    connection = get_db_connection()

    connection.execute(
        "INSERT INTO applications (name, email) VALUES (?, ?)",
        (name, email)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Application saved successfully!"
    }), 201


if __name__ == "__main__":
    app.run(debug=True)