from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib

app = Flask(__name__)
CORS(app)

# ---------- DATABASE CONFIG ----------
DB_CONFIG = {
    "host": "localhost",
    "database": "agence_voyage",
    "user": "postgres",
    "password": "admin",
    "port": 5432
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# ---------- FRONTEND ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/destination")
def destination_page():
    return render_template("destination.html")

@app.route("/reservation")
def reservation_page():
    return render_template("reservation.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/contact")
def contact_page():
    return render_template("contact.html")

@app.route("/avis")
def avis_page():
    return render_template("avis.html")

# ---------- AUTH ----------
@app.route("/api/clients", methods=["POST"])
def register_client():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    hashed = hashlib.sha256(data["password"].encode()).hexdigest()
    cur.execute(
        "INSERT INTO client (username, email_client, password) VALUES (%s,%s,%s) RETURNING id_client",
        (data["username"], data["email_client"], hashed)
    )
    client_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id_client": client_id, "message": "Client created"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    hashed = hashlib.sha256(data["password"].encode()).hexdigest()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT id_client, username FROM client WHERE email_client=%s AND password=%s",
        (data["email"], hashed)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return jsonify(user)
    return jsonify({"error": "Invalid credentials"}), 401

# ---------- DESTINATIONS ----------
@app.route("/api/destination", methods=["GET"])
def get_destinations():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM destination")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)
# ---------- HOTELS ----------
@app.route("/api/hotels", methods=["GET"])
def get_hotels():
    destination_id = request.args.get("destination_id")
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if destination_id:
        cur.execute("SELECT * FROM hotel WHERE id_destination=%s", (destination_id,))
    else:
        cur.execute("SELECT * FROM hotel")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

# ---------- PROMOTIONS ----------
@app.route("/api/promotions", methods=["GET"])
def get_promotions():
    hotel_id = request.args.get("hotel_id")
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if hotel_id:
        cur.execute("SELECT * FROM promotion WHERE id_hotel=%s", (hotel_id,))
    else:
        cur.execute("SELECT * FROM promotion")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

# ---------- RESERVATION ----------
@app.route("/api/reservations", methods=["POST"])
def create_reservation():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reservation
        (nom_complet, email, destination_name, date_depart, date_arrive,
        nbr_enfants, nbr_adults, type_sejour, montant_total, id_client, id_destination)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["nom_complet"], data["email"], data["destination_name"],
        data["date_depart"], data["date_arrive"],
        data["nbr_enfants"], data["nbr_adults"],
        data["type_sejour"], data["montant_total"],
        data["id_client"], data["id_destination"]
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Reservation added"}), 201

# ---------- CONTACT ----------
@app.route("/api/messages", methods=["POST"])
def contact():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO message (name, email_contact, message) VALUES (%s,%s,%s)",
        (data["name"], data["email_contact"], data["message"])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Message sent"}), 201

# ---------- AVIS ----------
@app.route("/api/avis", methods=["POST"])
def create_avis():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO avis (destination, rating, comment, id_client) VALUES (%s,%s,%s,%s)",
        (data["destination"], data["rating"], data["comment"], data["id_client"])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Avis added"}), 201

if __name__ == "__main__":
    app.run(debug=True)