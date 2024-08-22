from flask import Flask, jsonify
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from requests import get as get

app = Flask(__name__)

@app.route("/Mat=<Plate>")

def Scrape(Plate):
    url = 'https://vidange.tn'
    if 'RS' in Plate:
        Type = 'RS'
        RSN = Plate[2:]
    else:
        Type = 'TUN'
        S = Plate[:Plate.find('TUN')]
        N = Plate[Plate.find('TUN') + 3:]
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        if Type == 'RS':
            page.click("#RS")
            page.fill("#numRS", RSN)
        else:
            page.fill('#numSerie', S)
            page.fill('#numCar', N)

        page.click('button[name=btn-search-mat]')
        page.wait_for_selector("div#detail-car")
        details = page.inner_html('#detail-car')
        soup = BeautifulSoup(details, 'html.parser')
        values = soup.find_all('div', {"class": "value"})
        
        car_details = {
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
    app.run(host="0.0.0.0", port=5000)
