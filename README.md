# Zadanie 1

Autor: Maciej Jackowski  
GitHub: https://github.com/<twoj-link>  
DockerHub: https://hub.docker.com/<twoj-link>

## Struktura projektu

weather-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── templates/
    └── index.html

## Polecenia

### a) Budowanie obrazu

docker build -t weather-app:latest .

### b) Uruchomienie kontenera

docker run -d --name weather-app -p 8080:8080 weather-app:latest    


### c) Logi startowe
docker logs weather-app

C:\Users\Macio\Desktop\weather-app>docker logs weather-app
[2026-06-01 07:25:59 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2026-06-01 07:25:59 +0000] [1] [INFO] Listening at: http://0.0.0.0:8080 (1)
[2026-06-01 07:25:59 +0000] [1] [INFO] Using worker: sync
[2026-06-01 07:25:59 +0000] [7] [INFO] Booting worker with pid: 7
2026-06-01 07:25:59,937 ============================================================
2026-06-01 07:25:59,937 Data uruchomienia : 2026-06-01 07:25:59
2026-06-01 07:25:59,937 Autor             : Maciej Jackowski
2026-06-01 07:25:59,937 Port TCP          : 8080
2026-06-01 07:25:59,937 ============================================================


## Opis Dockerfile

Dockerfile wykorzystuje wieloetapowe budowanie obrazu. W pierwszym etapie. instalowane są zależności Pythona do virtualenv. Drugi etap kopiuje tylko gotowy virtualenv i kod aplikacji.

requirements.txt kopiowany jest przed kodem aplikacji, żeby Docker mógł cache'ować warstwę z pip install i nie powtarzać jej przy każdej zmianie w kodzie.

HEALTHCHECK, który co 30 sekund sprawdza endpoint /health. Aplikacja uruchamiana jest przez gunicorn jako użytkownik appuser.
