from flask import Flask, jsonify
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route("/Lookup/<Plate>")

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
        browser = p.chromium.launch(headless=False)
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

@app.route("/latest")
def Latest():
    url='https://www.automobile.tn/fr/guide/dernieres-immatriculations.html'


    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        main = page.inner_html('.cms-prose')

        soup = BeautifulSoup(main, 'html.parser')

        TUN = soup.find('span', class_="mx-1 flex justify-around rounded-[7px] border-2 border-white py-3 text-[30px] text-white").get_text(strip=True)
        RS = soup.find('span' , class_="mx-1 flex justify-around rounded-[7px] border-2 border-white py-3 text-[30px] text-white flex-row-reverse").get_text(strip=True)
        MC = (soup.find_all('span', class_="mx-1 flex justify-around rounded-[7px] border-2 border-white py-3 text-[30px] text-white flex-row-reverse")[5]).get_text(strip=True)
        
        Plates = {
            'MC':'MOTO '+MC[3:],
            'TUN':TUN[:3]+' TUN '+TUN[7:],
            'RS':'RS '+RS[3:]
 
        }

        return Plates



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
