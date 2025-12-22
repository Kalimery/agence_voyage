const API_URL = "http://127.0.0.1:5000/api";

// ---------- DESTINATIONS ----------
async function getDestinations() {
    const res = await fetch(`${API_URL}/destination`);
    if (!res.ok) throw await res.json();
    return await res.json();
}

// ---------- HOTELS ----------
async function getHotels(destination_id) {
    const res = await fetch(`${API_URL}/hotels?destination_id=${destination_id || ''}`);
    if (!res.ok) throw await res.json();
    return await res.json();
}

// ---------- PROMOTIONS ----------
async function getPromotions(hotel_id) {
    const res = await fetch(`${API_URL}/promotions?hotel_id=${hotel_id || ''}`);
    if (!res.ok) throw await res.json();
    return await res.json();
}

// ---------- CLIENTS ----------
async function registerClient(username, email_client, password) {
    const res = await fetch(`${API_URL}/clients`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, email_client, password})
    });
    const json = await res.json();
    if (!res.ok) throw json;
    return json;
}

// ---------- LOGIN ----------
async function loginClient(email, password) {
    const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });
    const json = await res.json();
    if (!res.ok) throw json;
    return json;
}

// ---------- RESERVATIONS ----------
async function createReservation(data) {
    const res = await fetch(`${API_URL}/reservations`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    const json = await res.json();
    if (!res.ok) throw json;
    return json;
}

// ---------- AVIS / REVIEWS ----------
async function createAvis(destination, rating, comment, id_client) {
    const res = await fetch(`${API_URL}/avis`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({destination, rating, comment, id_client})
    });
    const json = await res.json();
    if (!res.ok) throw json;
    return json;
}

// ---------- CONTACT MESSAGES ----------
async function createMessage(name, email_contact, message) {
    const res = await fetch(`${API_URL}/messages`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, email_contact, message})
    });
    const json = await res.json();
    if (!res.ok) throw json;
    return json;
}

// ---------- PAYMENTS ----------
async function createPayment(data) {
    const res = await fetch(`${API_URL}/paiements`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    const json = await res.json();
    if (!res.ok) throw json;
    return json;
}
