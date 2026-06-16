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





# Zadanie 2 — GitHub Actions Pipeline

## Opis
Pipeline zbudowany w GitHub Actions buduje wieloarchitekturowy obraz Dockera,
skanuje go pod kątem podatności CVE i przesyła do GitHub Container Registry (ghcr.io).


Tag `latest` zapewnia łatwy dostęp do aktualnej wersji. Tag `sha-` jest niemutowalny
i pozwala odtworzyć dokładnie konkretny build (dobre praktyki CI/CD:
https://docs.docker.com/build/ci/github-actions/manage-tags-labels/).

## Schemat tagowania cache
Cache przechowywany na DockerHub jako:
`<user>/zadanie1-cache:buildcache`
Tryb `mode=max` zapisuje wszystkie warstwy pośrednie — przyspiesza kolejne buildy.

## Dlaczego Trivy zamiast Docker Scout?
- Open-source, darmowy, bez limitów
- Nie wymaga logowania

## Potwierdzenie działania
<img width="945" height="448" alt="image" src="https://github.com/user-attachments/assets/283203a1-9036-4582-81b3-701e2fac1fe9" />
<img width="945" height="406" alt="image" src="https://github.com/user-attachments/assets/21699508-69d9-462e-864f-7b8a4bab2e4f" />
<img width="1918" height="851" alt="image" src="https://github.com/user-attachments/assets/cf411f0a-0066-4eb4-a40e-c37e05846317" />

