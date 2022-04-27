from .models import Wine

wine_types = ['red', 'sparkling', 'white', 'rosé']

countries = list(Wine.objects.values('wine_country').distinct())

sellers = [
    {
    "rank": 1,
    "id": 1,
    "name": "Wein Direktimport Scholz GmbH",
    "info": [
        {"label": "address", "content": "Wolbecker Straße 302 48155 Münster"},
        {"label": "tel", "content": "0251 39729960"},
        {"label": "email", "content": "info@wein-direktimport.de"}
    ],
    "lat": "51.9507",
    "lon": "7.6705",
    "url": "https://www.wein-direktimport.de/"
    },
    {
        "rank": 2,
        "id": 2,
        "name": "divino Weinhandel Tobias Voigt",
        "info": [
            {"label": "address", "content": "Vogelrohrsheide 80 48167 Münster"},
            {"label": "tel", "content": "0251 62 79 184"},
            {"label": "email", "content": "info@divino.de"}
        ],
        "lat": "51.9177774",
        "lon": "7.6811747",
        "url": "https://www.divino.de/"
    },
    {
        "rank": 3,
        "id": 3,
        "name": "Jacques Weindepot",
        "info": [
            {"label": "address", "content": "Warendorfer Str. 22 48145 Münster-Mauritz"},
            {"label": "tel", "content": "0251/36384"},
            {"label": "email", "content": "mauritz@jacques.de"}
        ],
        "lat": "51.9286764",
        "lon": "7.6085188",
        "url": "https://www.jacques.de/"
    }]

keys_taste = ['black_fruit', 'dried_fruit', 'red_fruit', 'tropical_fruit', 'tree_fruit', 'citrus_fruit', 'spices',
              'earth', 'microbio', 'vegetal', 'floral', 'non_oak', 'oak',
              ]

keys_structure = ["wine_acidity", "wine_fizziness",
                  "wine_intensity", "wine_sweetness", "wine_tannin"]
