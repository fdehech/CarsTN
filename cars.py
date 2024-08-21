from flask import Flask, jsonify
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/Lookup/<Plate>")
def Scrape(Plate):
    url = 'https://vidange.tn/'
    if 'RS' in Plate:
        Type = 'RS'
        RSN = Plate[2:]
        print(f"RSN: {RSN}")
    else:
        Type = 'TUN'
        S = Plate[:Plate.find('TUN')]
        N = Plate[Plate.find('TUN') + 3:]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = browser.new_page()
        page.goto(url)
        print("CHECKPOINT 1")
        if Type == 'RS':
            page.click("#RS")
            page.fill("#numRS", RSN)
        else:
            page.fill('#numSerie', S)
            page.fill('#numCar', N)
        print("CHECKPOINT 2")
        page.click('button[name=btn-search-mat]')
        print("CHECKPOINT 3")
        page.wait_for_selector("div#detail-car", timeout=60000)
        print("CHECKPOINT 4")
        details = page.inner_html('#detail-car')
        soup = BeautifulSoup(details, 'html.parser')
        values = soup.find_all('div', {"class": "value"})
        

        car_details = {
            "Plate": Plate,
            "Marque et modèle": values[0].get_text(strip=True),
            "Type": values[4].get_text(strip=True),
            "Carosserie": values[6].get_text(strip=True),
            "Mise en circulation": values[2].get_text(strip=True),
            "Moteur": values[5].get_text(strip=True),
            "Cylindrée": values[7].get_text(strip=True),
            "Carburant": values[1].get_text(strip=True),
            "Puissance Fiscale": values[3].get_text(strip=True)
        }

        return jsonify(car_details), 200

if __name__ == "__main__":
    app.run(debug=False)
