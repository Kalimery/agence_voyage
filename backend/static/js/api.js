const API_URL = "http://127.0.0.1:5000/api";

// --------- DESTINATIONS ---------
async function getDestinations() {
    const res = await fetch(`${API_URL}/destination`);
    if (!res.ok) throw new Error("Failed to fetch destinations");
    return await res.json();
}

// --------- HOTELS ---------
async function getHotels(destination_id) {
    const res = await fetch(`${API_URL}/hotels?destination_id=${destination_id || ''}`);
    if (!res.ok) throw new Error("Failed to fetch hotels");
    return await res.json();
}

// --------- PROMOTIONS ---------
async function getPromotions(hotel_id) {
    const res = await fetch(`${API_URL}/promotions?hotel_id=${hotel_id || ''}`);
    if (!res.ok) throw new Error("Failed to fetch promotions");
    return await res.json();
}

// --------- CLIENTS / REGISTER ---------
async function registerClient(username, email_client, password) {
    const res = await fetch(`${API_URL}/clients`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, email_client, password})
    });
    if (!res.ok) throw new Error("Failed to register client");
    return await res.json();
}

// --------- LOGIN ---------
async function loginClient(email, password) {
    const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });
    if (!res.ok) throw new Error("Login failed");
    return await res.json();
}

// --------- RESERVATIONS ---------
async function createReservation(data) {
    // data = {nom_complet, email, destination_name, date_depart, date_arrive, nbr_enfants, nbr_adults, type_sejour, montant_total, id_client, id_destination}
    const res = await fetch(`${API_URL}/reservations`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("Failed to create reservation");
    return await res.json();
}

// --------- AVIS / REVIEWS ---------
async function createAvis(destination, rating, comment, id_client) {
    const res = await fetch(`${API_URL}/avis`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({destination, rating, comment, id_client})
    });
    if (!res.ok) throw new Error("Failed to submit review");
    return await res.json();
}

// --------- CONTACT MESSAGES ---------
async function createMessage(name, email_contact, message) {
    const res = await fetch(`${API_URL}/messages`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, email_contact, message})
    });
    if (!res.ok) throw new Error("Failed to send message");
    return await res.json();
}