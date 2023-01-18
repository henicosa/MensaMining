import json

# import web crawler
from bs4 import BeautifulSoup
import pprint
pp = pprint.PrettyPrinter(indent=4)

# -- SQLite
# SELECT city, diet, COUNT(*) FROM meals WHERE diet IS NOT NULL GROUP BY city, diet ORDER BY city, diet;

zusatzstoffe = {
    "" : "",
    "1": "mit Farbstoff",
    "2": "mit Konservierungsstoff",
    "3": "mit Antioxidationsmittel",
    "4": "mit Geschmacksverstärker",
    "5": "geschwefelt",
    "6": "geschwärzt",
    "7": "gewachst",
    "8": "mit Phosphat",
    "9": "mit Süßungsmittel",
    "10": "enthält eine Phenylalaninquelle",
    "13": "kann die Aktivität und Aufmerksamkeit von Kindern beeinträchtigen",
    "14": "mit kakaohaltiger Fettglasur",
    "15": "koffeinhaltig",
    "16": "chininhaltig",
    "T\"": "enthält tierische Bestandteile",
    "T1": "enthält tierische Gelatine",
    "T2": "enthält tierisches Lab",
    "T3": "enthält Karmin",
    "T4": "enthält Sepia",
    "T5": "enthält Honig"
}

allergene = {
    "" : "",
    "Wz": "enthält Weizen",
    "Ro": "enthält Roggen",
    "Gs": "enthält Gerste",
    "Hf": "enthält Hafer",
    "Di": "enthält Dinkel",
    "Ka": "enthält Kamut (Khorasan-Weizen)",
    "Kr": "enthält Krebstiere",
    "Ei": "enthält Hühnerei",
    "Fi": "enthält Fisch",
    "Er": "enthält Erdnüsse",
    "So": "enthält Soja",
    "Mi": "enthält Milch- und Milchzucker",
    "Ma": "enthält Mandeln",
    "Ha": "enthält Haselnüsse",
    "Wa": "enthält Walnüsse",
    "Ca": "enthält Cashewnüsse",
    "Pe": "enthält Pekannüsse",
    "Pa": "enthält Paranüsse",
    "Pi": "enthält Pistazien",
    "Mc": "enthält Macadamianüsse",
    "Sel": "enthält Sellerie",
    "Sen": "enthält Senf",
    "Ses": "enthält Sesam",
    "Su": "enthält Schwefeloxid/Sulfite",
    "Lu": "enthält Lupine",
    "We": "enthält Weichtiere"
}

weitere_inhaltsstoffe = ["enthält Alkohol",
    "Fisch",
    "Geflügel",
    "Knoblauch",
    "Lamm-/Schaffleisch",
    "Rindfleisch",
    "Schweinefleisch",
    "Wildfleisch",
    "Wildschwein"]

symbolik = ['Vegane Speisen', 
    "Vegetarische Speisen",
    "mensaVital",
    "BIO-Komponenten",
    "mensaInternational",
    "mensaRegional",
    "ohne deklarationspflichtige Zusatzstoffe",
    "Kinderessen"]

def get_meals(html):
    soup = BeautifulSoup(html, 'html.parser')
    meals = []
    if soup.findAll("div", class_="row px-3 mb-2 rowMeal"):
        for meal in soup.findAll("div", class_="row px-3 mb-2 rowMeal"):
            meal_dic = {"name": get_meal_name(meal)}
            meal_dic["prices"] = get_prices(meal)
            meal_dic["allergens"] = get_allergens(meal)
            meal_dic["additives"] = get_additives(meal)
            meal_dic["diet"] = does_it_include_dead_animals(meal)
            meal_dic["quicklikes"] = get_quicklikes(meal)
            meal_dic["badges"] = get_badges(meal)
            meals.append(meal_dic)
    return meals

def does_it_include_dead_animals(meal):
    meal = str(meal)
    if 'Vegane Speisen' in meal:
        return "Vegan"
    elif "Vegetarische Speisen" in meal:
        return "Vegetarisch"
    else:
        return "Fleisch"

def get_badges(meal):
    meal = str(meal.find("div", class_="col-12 col-md-4 text-right"))
    possible_badges = weitere_inhaltsstoffe + symbolik
    badges = []
    for possible_badge in possible_badges:
        if possible_badge in meal:
            badges.append(possible_badge)
    return badges

def get_meal_name(meal):
    return remove_styling(meal.find("div", class_="mealText").contents[0])

def remove_styling(word):
    return word.replace("\n", "").replace("\n", "").strip()

def get_prices(meal):
    price_keys = str(meal.find("div", class_="mealPreiskopf").contents[0]).split(" / ")
    price_values = str(meal.find("div", class_="mealPreise").contents[0]).split(" / ")
    prices = {}
    for i in range(len(price_keys)):
        if "€" in price_values[i]:
            price_values[i] = price_values[i].replace(" €", "")
        prices[price_keys[i]] = float(price_values[i].replace(",", "."))
    return prices

def get_allergens(meal):
    try:
        allergens = str(meal.find("div", class_="allergene").contents[0]).split(": ")[1]
        if allergens.replace(" ", "").replace("\n", "") == "":
            return ""
        else:    
            allergens = [item.replace(" ", "").replace("\n", "")  for item in allergens.split(",")]
        return [allergene[allergen] for allergen in allergens]
    except:
        return ""

def get_additives(meal):
    additives = str(meal.find("div", class_="zusatzstoffe").contents[0]).split(":\n")[1]
    if additives.replace(" ", "").replace("\n", "") == "":
        return ""
    else:
        additives = [item.replace(" ", "").replace("\n", "") for item in additives.split(",")]
    return [zusatzstoffe[additive] for additive in additives]

def get_quicklikes(meal):
    try:
        quicklikes = str(meal.find("div", class_="quicklike").find("span", class_="fa-stack-1x").decode_contents())
        return 0 if quicklikes == "" else int(quicklikes)
    except:
        return 0

def get_vote_link(meal):
    return "https://www.stw-thueringen.de/" + meal.find("a", string="Gericht bewerten")["href"]

    
def analyze_mensa(path):
    with open(path, "r") as file:
        html = file.read()
        meals = get_meals(html)
        return meals
