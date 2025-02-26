from flask import Flask, jsonify, request
import random
import re

app = Flask(__name__)

cars = [
    {"id": 1, "marca": "Bugatti", "modelo": "Chiron", "precio":2400000, "año":2020, "cv": 1500, "ancho": 2.03, "largo": 4.54, "alto": 1.21, "pulgadas_llanta": 20, "color": "Azul", "tipo_motor": "W16", "num_puertas": 2, "asientos": 2, "combustible": "Gasolina", "consumo": {"carretera": 15, "ciudad": 8, "mezclado": 10}, "foto": "https://s2.best-wallpaper.net/wallpaper/1366x768/1607/Bugatti-Chiron-blue-supercar_1366x768.jpg"},
    {"id": 2, "marca": "Lamborghini", "modelo": "Aventador", "precio":314900, "año":2011, "cv": 770, "ancho": 2.03, "largo": 4.79, "alto": 1.14, "pulgadas_llanta": 21, "color": "Amarillo", "tipo_motor": "V12", "num_puertas": 2, "asientos": 2, "combustible": "Gasolina", "consumo": {"carretera": 14, "ciudad": 7, "mezclado": 9}, "foto": "https://s1.cdn.autoevolution.com/images/gallery/LAMBORGHINI-Aventador-LP-700-4-Roadster-4692_37.jpg"},
    {"id": 3, "marca": "Ferrari", "modelo": "SF90 Stradale", "precio":489725, "año":2020, "cv": 1000, "ancho": 1.97, "largo": 4.71, "alto": 1.19, "pulgadas_llanta": 20, "color": "Rojo", "tipo_motor": "Híbrido V8", "num_puertas": 2, "asientos": 2, "combustible": "Híbrido", "consumo": {"carretera": 12, "ciudad": 6, "mezclado": 8}, "foto": "https://media.gq.com.mx/photos/5f8c83fd2e0c232544d07e0a/16:9/w_2560%2Cc_limit/ferrari-sf90-caracteristicas.jpg"},
    {"id": 4, "marca": "McLaren", "modelo": "P1", "precio":1000000, "año":2015, "cv": 903, "ancho": 1.91, "largo": 4.58, "alto": 1.19, "pulgadas_llanta": 19, "color": "Naranja", "tipo_motor": "Híbrido V8", "num_puertas": 2, "asientos": 2, "combustible": "Híbrido", "consumo": {"carretera": 13, "ciudad": 7, "mezclado": 9}, "foto": "https://www.carscoops.com/wp-content/uploads/2019/07/89233ad8-mclaren-p1-xp05-1.jpg"},
    {"id": 4, "marca": "Porsche", "modelo": "911 Turbo S", "precio":260951.43, "año":2020, "cv": 650, "ancho": 1.90, "largo": 4.53, "alto": 1.30, "pulgadas_llanta": 20, "color": "Gris", "tipo_motor": "Bóxer 6", "num_puertas": 2, "asientos": 4, "combustible": "Gasolina", "consumo": {"carretera": 9, "ciudad": 5, "mezclado": 7}, "foto": "https://automais.autosport.pt/wp-content/uploads/2020/07/2021-porsche-911-turbo-s.jpg"},
    {"id": 6, "marca": "Tesla", "modelo": "Model S Plaid", "precio":120970, "año":2021, "cv": 1020, "ancho": 1.98, "largo": 4.97, "alto": 1.44, "pulgadas_llanta": 21, "color": "Rojo", "tipo_motor": "Eléctrico", "num_puertas": 4, "asientos": 5, "combustible": "Eléctrico", "consumo": {"carretera": 0, "ciudad": 0, "mezclado": 0}, "foto": "https://cdn.motor1.com/images/mgl/oRgrE/s1/2021-tesla-model-s-plaid.jpg"},
    {"id": 7, "marca": "BMW", "modelo": "M5 Competition", "precio":151700, "año":2020, "cv": 625, "ancho": 1.91, "largo": 4.96, "alto": 1.47, "pulgadas_llanta": 20, "color": "Gris", "tipo_motor": "V8", "num_puertas": 4, "asientos": 5, "combustible": "Gasolina", "consumo": {"carretera": 10, "ciudad": 5, "mezclado": 7}, "foto": "https://wallpapercave.com/wp/wp6527664.jpg"},
    {"id": 8, "marca": "Maserati", "modelo": "Levante Trofeo", "precio":196900, "año":2021, "cv": 580, "ancho": 1.98, "largo": 5.00, "alto": 1.69, "pulgadas_llanta": 22, "color": "Negro", "tipo_motor": "V8 Biturbo", "num_puertas": 5, "asientos": 5, "combustible": "Gasolina", "consumo": {"carretera": 12, "ciudad": 7, "mezclado": 9}, "foto": "https://www.automobile-magazine.fr/asset/cms/143657/config/97738/avec-son-v8-de-590-ch-cette-version-trofeo-vient-coiffer-la-gamme-du-suv-maserati-levante.jpg"},
    {"id": 9, "marca": "Audi", "modelo": "RS7 Sportback", "precio":180080, "año":2013, "cv": 600, "ancho": 1.95, "largo": 5.01, "alto": 1.42, "pulgadas_llanta": 21, "color": "Azul", "tipo_motor": "V8 Biturbo", "num_puertas": 4, "asientos": 5, "combustible": "Gasolina", "consumo": {"carretera": 10, "ciudad": 6, "mezclado": 8}, "foto": "https://images.prismic.io/carwow/e8020fc9-e7f3-4ea0-993b-67ef3c2ffac4_LHD+Audi+RS7+Sportback+2023+Exteror-2.jpg"},
    {"id": 10, "marca": "Mercedes-Benz", "modelo": "AMG GT 63 S", "precio":195500, "año":2018, "cv": 639, "ancho": 1.96, "largo": 5.05, "alto": 1.44, "pulgadas_llanta": 21, "color": "Gris Mate", "tipo_motor": "V8 Biturbo", "num_puertas": 4, "asientos": 5, "combustible": "Gasolina", "consumo": {"carretera": 11, "ciudad": 7, "mezclado": 9}, "foto": "https://i.ytimg.com/vi/96esbly723w/maxresdefault.jpg"},
    {"id": 11, "marca": "Toyota", "modelo": "Camry", "precio":36500, "año":2019, "cv": 203, "ancho": 1.84, "largo": 4.88, "alto": 1.45, "pulgadas_llanta": 17, "color": "Gris", "tipo_motor": "Híbrido", "num_puertas": 4, "asientos": 5, "combustible": "Híbrido", "consumo": {"carretera": 22, "ciudad": 14, "mezclado": 18}, "foto": "https://i.ytimg.com/vi/cpgVncqPfTc/maxresdefault.jpg"},
    {"id": 12, "marca": "Honda", "modelo": "Accord", "precio":30000, "año":2014, "cv": 192, "ancho": 1.86, "largo": 4.89, "alto": 1.46, "pulgadas_llanta": 17, "color": "Blanco", "tipo_motor": "Híbrido", "num_puertas": 4, "asientos": 5, "combustible": "Híbrido", "consumo": {"carretera": 21, "ciudad": 13, "mezclado": 17}, "foto": "https://s1.1zoom.me/b5050/240/Honda_2018_Accord_Touring_1.5T_White_536263_1920x1200.jpg"},
    {"id": 13, "marca": "Ford", "modelo": "Fusion", "precio":13900, "año":2012, "cv": 181, "ancho": 1.85, "largo": 4.87, "alto": 1.47, "pulgadas_llanta": 18, "color": "Azul", "tipo_motor": "EcoBoost", "num_puertas": 4, "asientos": 5, "combustible": "Gasolina", "consumo": {"carretera": 20, "ciudad": 12, "mezclado": 16}, "foto": "https://cdn.motor1.com/images/mgl/PpkVK/s1/ford-fusion-a-trajetoria-no-brasil.jpg"},
    {"id": 14, "marca": "Mazda", "modelo": "Mazda6", "precio":34663, "año":2023, "cv": 187, "ancho": 1.84, "largo": 4.86, "alto": 1.45, "pulgadas_llanta": 19, "color": "Rojo", "tipo_motor": "Skyactiv-G", "num_puertas": 4, "asientos": 5, "combustible": "Gasolina", "consumo": {"carretera": 22, "ciudad": 14, "mezclado": 18}, "foto": "https://www.dsf.my/wp-content/uploads/2019/01/70625592-9964-4B27-8CBA-7306CEE53D22.jpeg"},
    {"id": 15, "marca": "Toyota", "modelo": "Corolla", "precio":25854, "año":2022, "cv": 169, "ancho": 1.79, "largo": 4.63, "alto": 1.44, "pulgadas_llanta": 16, "color": "Azul", "tipo_motor": "Híbrido", "num_puertas": 4, "asientos": 5, "combustible": "Híbrido", "consumo": {"carretera": 24, "ciudad": 15, "mezclado": 19}, "foto": "https://www.motortrend.com/uploads/sites/5/2019/02/2020-Toyota-Corolla-SE-12.jpg"},
    {"id": 16, "marca": "Ferrari", "modelo": "F8 Tributo", "precio":274000, "año":2019, "cv": 720, "ancho": 1.98, "largo": 4.61, "alto": 1.21, "pulgadas_llanta": 20, "color": "Rojo", "tipo_motor": "V8 Biturbo", "num_puertas": 2, "asientos": 2, "combustible": "Gasolina", "consumo": {"carretera": 11, "ciudad": 6, "mezclado": 8}, "foto": "https://www.hdcarwallpapers.com/walls/ferrari_f8_tributo_2019_4k_5k_2-HD.jpg"},
    {"id": 17, "marca": "Ferrari", "modelo": "812 Superfast", "precio":279999, "año":2024, "cv": 800, "ancho": 1.97, "largo": 4.66, "alto": 1.28, "pulgadas_llanta": 20, "color": "Rojo", "tipo_motor": "V12 Atmosférico", "num_puertas": 2, "asientos": 2, "combustible": "Gasolina", "consumo": {"carretera": 10, "ciudad": 5, "mezclado": 7}, "foto": "https://s3.amazonaws.com/dom-cms/Site/1c90a3d9-b6a5-43bf-9e12-20e7b5da0cad/images/812Superfast/0ffa98d53fbd50352d5fa6cd0e208920x.jpg"},
    {"id": 18, "marca": "McLaren", "modelo": "720S", "precio":284700, "año":2023, "cv": 720, "ancho": 2.05, "largo": 4.54, "alto": 1.19, "pulgadas_llanta": 19, "color": "Naranja", "tipo_motor": "V8 Biturbo", "num_puertas": 2, "asientos": 2, "combustible": "Gasolina", "consumo": {"carretera": 12, "ciudad": 7, "mezclado": 9}, "foto": "https://media.fastestlaps.com/mclaren-720s.jpg"},
    {"id": 19, "marca": "McLaren", "modelo": "750S", "precio":322400, "año":2024, "cv": 750, "ancho": 2.06, "largo": 4.55, "alto": 1.18, "pulgadas_llanta": 20, "color": "Azul", "tipo_motor": "V8 Biturbo", "num_puertas": 2, "asientos": 2, "combustible": "Gasolina", "consumo": {"carretera": 11, "ciudad": 6, "mezclado": 8}, "foto": "https://netcarflix.sfo2.cdn.digitaloceanspaces.com/0000/v3/McLaren/657fe3f5343111195fff5672/2024-750s-spider-ludus-blue-mclaren-86wcj0twjauasrt5l.jpeg"},
    {"id": 20, "marca": "Koenigsegg", "modelo": "Regera", "precio":2100000, "año":2022, "cv": 1500, "ancho": 2.05, "largo": 4.56, "alto": 1.11, "pulgadas_llanta": 20, "color": "Plata", "tipo_motor": "V8 Híbrido", "num_puertas": 2, "asientos": 2, "combustible": "Híbrido", "consumo": {"carretera": 9, "ciudad": 5, "mezclado": 7}, "foto": "https://cdn.motor1.com/images/mgl/wl4XnL/s1/koenigsegg-regera.jpg"}
]

@app.route('/top10cars', methods=['GET'])
def get_top_10_cars():
    selected_cars = random.sample(cars, 10)
    data = []
    for c in selected_cars:
        data.append({
            "name": f"{c['marca']} {c['modelo']}",
            "cv": c["cv"],
            "foto": c["foto"]
        })
    return jsonify(data)

@app.route('/search', methods=['GET'])
def search_cars():
    """ Busca coches por marca o modelo usando regex """
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])  # Si no hay query, devolver lista vacía

    regex = re.compile(query, re.IGNORECASE)
    filtered_cars = [
        {"name": f"{c['marca']} {c['modelo']}", "cv": c["cv"], "foto": c["foto"]}
        for c in cars if regex.search(c["marca"]) or regex.search(c["modelo"])
    ]
    
    return jsonify(filtered_cars[:20])  # Devolver máximo 20 resultados

@app.route('/allcars', methods=['GET'])
def get_all_cars():
    """ Devuelve todos los coches disponibles en la base de datos. """
    data = []
    for c in cars:  
        data.append({
            "name": f"{c['marca']} {c['modelo']}",
            "cv": c["cv"],
            "foto": c["foto"]
        })
    return jsonify(data)

@app.route('/advsearch', methods=['GET'])
def advanced_search():
    """
    Filtra coches con múltiples criterios: 
    minHP, maxHP, minPrice, maxPrice, minDoors, maxDoors, minYear, maxYear, minSeats, maxSeats, brand, model, color.
    Ignora los campos que estén vacíos o no existan.
    """
    # Obtener parámetros (string vacíos -> ignorar)
    min_hp = request.args.get('minHP', '').strip()
    max_hp = request.args.get('maxHP', '').strip()
    min_price = request.args.get('minPrice', '').strip()
    max_price = request.args.get('maxPrice', '').strip()
    min_doors = request.args.get('minDoors', '').strip()
    max_doors = request.args.get('maxDoors', '').strip()
    min_year = request.args.get('minYear', '').strip()
    max_year = request.args.get('maxYear', '').strip()
    min_seats = request.args.get('minSeats', '').strip()
    max_seats = request.args.get('maxSeats', '').strip()
    brand = request.args.get('brand', '').strip().lower()
    model = request.args.get('model', '').strip().lower()
    color = request.args.get('color', '').strip().lower()

    def to_int(val):
        try:
            return int(val)
        except:
            return None

    def to_float(val):
        try:
            return float(val)
        except:
            return None

    # Convertir a enteros/float si existen
    min_hp = to_int(min_hp) if min_hp else None
    max_hp = to_int(max_hp) if max_hp else None
    min_price = to_float(min_price) if min_price else None
    max_price = to_float(max_price) if max_price else None
    min_doors = to_int(min_doors) if min_doors else None
    max_doors = to_int(max_doors) if max_doors else None
    min_year = to_int(min_year) if min_year else None
    max_year = to_int(max_year) if max_year else None
    min_seats = to_int(min_seats) if min_seats else None
    max_seats = to_int(max_seats) if max_seats else None

    results = []
    for c in cars:
        # Filtros numéricos
        if min_hp is not None and c["cv"] < min_hp:
            continue
        if max_hp is not None and c["cv"] > max_hp:
            continue
        if min_price is not None and c["precio"] < min_price:
            continue
        if max_price is not None and c["precio"] > max_price:
            continue
        if min_doors is not None and c["num_puertas"] < min_doors:
            continue
        if max_doors is not None and c["num_puertas"] > max_doors:
            continue
        if min_year is not None and c["año"] < min_year:
            continue
        if max_year is not None and c["año"] > max_year:
            continue
        if min_seats is not None and c["asientos"] < min_seats:
            continue
        if max_seats is not None and c["asientos"] > max_seats:
            continue

        # Filtros string (brand, model, color)
        # Ignoramos si brand/model/color es vacío
        if brand and brand not in c["marca"].lower():
            continue
        if model and model not in c["modelo"].lower():
            continue
        if color and color not in c["color"].lower():
            continue

        # Si pasa todos los filtros, lo añadimos al results
        results.append({
            "name": f"{c['marca']} {c['modelo']}",
            "cv": c["cv"],
            "foto": c["foto"]
        })

    return jsonify(results)

@app.route('/carinfo', methods=['GET'])
def get_car_info():
    brand = request.args.get('brand', '').strip().lower()
    model = request.args.get('model', '').strip().lower()

    for c in cars:
        # Coincidencia con marca/modelo en minúsculas
        if c['marca'].lower() == brand and c['modelo'].lower() == model:
            return jsonify({
                "brand": c["marca"],
                "model": c["modelo"],
                "price": c["precio"],
                "year": c["año"],
                "hp": c["cv"],
                "width": c["ancho"],
                "length": c["largo"],
                "height": c["alto"],
                "wheelInch": c["pulgadas_llanta"],
                "engineType": c["tipo_motor"],
                "doors": c["num_puertas"],
                "seats": c["asientos"],
                "fuel": c["combustible"],
                "color": c["color"],
                "photo": c["foto"],
                "consumption": {
                    "highway": c["consumo"]["carretera"],
                    "city": c["consumo"]["ciudad"],
                    "mixed": c["consumo"]["mezclado"]
                }
            })
    return jsonify({})  # no encontrado

# **Manejo de error 404 para rutas inexistentes**
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
