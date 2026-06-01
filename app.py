from flask import Flask, render_template, request
import requests
import logging
import os
from datetime import datetime

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 8080))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

CITIES = {
    "Polska": [
        ("Warszawa", 52.2297, 21.0122),
        ("Kraków", 50.0647, 19.9450),
        ("Gdańsk", 54.3520, 18.6466),
        ("Lublin", 51.2465, 22.5684),
        ("Świdnik", 51.2200, 22.6900),
    ],
    "Niemcy": [
        ("Berlin", 52.5200, 13.4050),
        ("Monachium", 48.1351, 11.5820),
        ("Hamburg", 53.5753, 9.9953),
    ],
    "Francja": [
        ("Paryż", 48.8566, 2.3522),
        ("Lyon", 45.7640, 4.8357),
    ],
    "USA": [
        ("Nowy Jork", 40.7128, -74.0060),
        ("Los Angeles", 34.0522, -118.2437),
        ("Chicago", 41.8781, -87.6298),
    ],
    "Japonia": [
        ("Tokio", 35.6762, 139.6503),
        ("Osaka", 34.6937, 135.5023),
    ],
}

WMO = {
    0: "Bezchmurnie ☀️", 1: "Głównie bezchmurnie 🌤️", 2: "Częściowe zachmurzenie ⛅",
    3: "Zachmurzenie ☁️", 45: "Mgła 🌫️", 51: "Mżawka 🌦️", 61: "Deszcz 🌧️",
    63: "Deszcz umiarkowany 🌧️", 65: "Silny deszcz 🌧️", 71: "Śnieg 🌨️",
    80: "Przelotny deszcz 🌦️", 95: "Burza ⛈️",
}


def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "relativehumidity_2m",
        "forecast_days": 1,
        "timezone": "auto",
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        cw = data["current_weather"]
        code = int(cw.get("weathercode", 0))
        humidity = data.get("hourly", {}).get("relativehumidity_2m", [None])[0]
        return {
            "temp": cw.get("temperature"),
            "wind": cw.get("windspeed"),
            "code": code,
            "desc": WMO.get(code, "Brak danych"),
            "humidity": humidity,
        }
    except Exception:
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    country = None
    city = None
    error = None

    if request.method == "POST":
        country = request.form.get("country")
        city = request.form.get("city")
        coords = None
        if country in CITIES:
            for name, lat, lon in CITIES[country]:
                if name == city:
                    coords = (lat, lon)
                    break
        if coords:
            weather = get_weather(*coords)
            if not weather:
                error = "Nie udało się pobrać pogody."
        else:
            error = "Wybierz kraj i miasto."

    return render_template("index.html", cities=CITIES, weather=weather,
                           country=country, city=city, error=error)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


log.info("=" * 60)
log.info("Data uruchomienia : %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
log.info("Autor             : Maciej Jackowski")
log.info("Port TCP          : %d", PORT)
log.info("=" * 60)