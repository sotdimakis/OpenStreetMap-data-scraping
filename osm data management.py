import tkinter as tk
from tkinter import messagebox, Menu
from PIL import Image, ImageTk
import overpy
from shapely.geometry import Point
import geopandas as gpd
import webbrowser
import folium
from folium import plugins
import os

# Περιέχει keys και values σε μορφή dictionary μιας εκδοχής του open street
# ετσι ώστε να μπορούν να αξιοποιθούν για την κατασκευή του παρακάτω προγράμματος
KEY_VALUES = {
    "aeroway": [
        "aerodrome",
        "apron",
        "control_tower",
        "control_center",
        "gate",
        "hangar",
        "helipad",
        "heliport",
        "navigationaid",
        "beacon",
        "runway",
        "taxilane",
        "taxiway",
        "terminal",
        "windsock",
        "highway_strip"
    ],
    "amenity": [
        "animal_boarding",
        "animal_shelter",
        "arts_centre",
        "atm",
        "bank",
        "bar",
        "bench",
        "bbq",
        "bicycle_parking",
        "bicycle_rental",
        "biergarten",
        "bus_station",
        "cafe",
        "casino",
        "car_rental",
        "car_sharing",
        "car_wash",
        "clinic",
        "clock",
        "cinema",
        "college",
        "community_centre",
        "coworking_space",
        "crematorium",
        "dentist",
        "doctors",
        "drinking_water",
        "embassy",
        "fast_food",
        "fire_station",
        "fountain",
        "fuel",
        "gambling",
        "grave_yard",
        "hospital",
        "kindergarten",
        "library",
        "marketplace",
        "nightclub",
        "parking",
        "pharmacy",
        "place_of_worship",
        "planetarium",
        "police",
        "post_box",
        "post_office",
        "prison",
        "pub",
        "recycling",
        "restaurant",
        "school",
        "shelter",
        "shower",
        "social_facility",
        "social_centre",
        "swingerclub",
        "taxi",
        "theatre",
        "toilets",
        "townhall",
        "university",
        "vending_machine",
        "veterinary"
    ],
    "boundary": [
        "administrative",
        "maritime",
        "national_park",
        "religious_administration",
        "protected_area"
    ],
    "building": [
        "apartments",
        "commercial",
        "farm",
        "hotel",
        "house",
        "industrial",
        "retail",
        "yes"
    ],
    "crop": [
        "bananas",
        "barley",
        "berry_plants",
        "corn",
        "dairy",
        "dry_farming",
        "feed_lot",
        "field_cropland",
        "flowers",
        "grape",
        "grass",
        "hay",
        "native_pasture",
        "no",
        "orchid",
        "potatoes",
        "poultry",
        "rape",
        "rice",
        "strawberry",
        "yes",
        "wheat"
    ],
    "cuisine": [
        "bagel",
        "barbecue",
        "bougatsa",
        "burger",
        "cake",
        "casserole",
        "chicken",
        "coffee_shop",
        "crepe",
        "couscous",
        "curry",
        "dessert",
        "donut",
        "doughnut",
        "empanada",
        "fish",
        "fish_and_chips",
        "fried_food",
        "friture",
        "gyro",
        "ice_cream",
        "kebab",
        "mediterranean",
        "noodle",
        "pancake",
        "pasta",
        "pie",
        "pizza",
        "regional",
        "sandwich",
        "sausage",
        "savory_pancakes",
        "seafood",
        "steak_house",
        "sub",
        "sushi",
        "tapas",
        "vegan",
        "vegetarian",
        "wings"
    ],
    "craft": [
        "agricultural_engines",
        "basket_maker",
        "beekeeper",
        "blacksmith",
        "brewery",
        "boatbuilder",
        "carpenter",
        "caterer",
        "confectionery",
        "dressmaker",
        "electrician",
        "gardener",
        "glaziery",
        "handicraft",
        "hvac",
        "insulation",
        "jeweller",
        "key_cutter",
        "optician",
        "painter",
        "photographer",
        "plumber",
        "roofer",
        "tailor",
        "watchmaker",
        "winery"
    ],
    "emergency": [
        "ambulance_station",
        "assembly_point",
        "defibrillator",
        "fire_extinguisher",
        "fire_hydrant",
        "phone",
        "siren",
        "water_tank"
    ],
    "highway": [
        "motorway",
        "trunk",
        "primary",
        "secondary",
        "tertiary",
        "unclassified",
        "residential",
        "living_street",
        "service",
        "track",
        "road",
        "footway",
        "pedestrian",
        "cycleway",
        "steps",
        "path",
        "construction",
        "bus_stop",
        "crossing",
        "mini_roundabout",
        "speed_camera",
        "stop",
        "street_lamp",
        "traffic_signals",
        "turning_circle"
    ],
    "cycleway": [
        "lane",
        "opposite",
        "opposite_lane",
        "track",
        "opposite_track",
        "share_busway",
        "shared_lane"
    ],
    "junction": [
        "roundabout",
        "jughandle",
        "filter",
        "yes"
    ],
    "historic": [
        "archaeological_site",
        "aircraft",
        "battlefield",
        "boundary_stone",
        "building",
        "castle",
        "cannon",
        "city_gate",
        "citywalls",
        "farm",
        "fort",
        "manor",
        "memorial",
        "monument",
        "ruins",
        "rune_stone",
        "ship",
        "wayside_cross",
        "wayside_shrine",
        "yes"
    ],
    "landuse": [
        "allotments",
        "basin",
        "brownfield",
        "cemetery",
        "commercial",
        "construction",
        "farm",
        "farmland",
        "farmyard",
        "forest",
        "garages",
        "grass",
        "greenfield",
        "industrial",
        "landfill",
        "meadow",
        "military",
        "orchard",
        "plant_nursery",
        "quarry",
        "railway",
        "reservoir",
        "residential",
        "retail",
        "vineyard"
    ],
    "leisure": [
        "fishing",
        "garden",
        "golf_course",
        "hackerspace",
        "marina",
        "miniature_golf",
        "nature_reserve",
        "park",
        "pitch",
        "playground",
        "sports_centre",
        "stadium",
        "swimming_pool",
        "track",
        "water_park"
    ],
    "natural": [
        "bay",
        "beach",
        "cave_entrance",
        "cliff",
        "crater",
        "coastline",
        "fell",
        "fumarole",
        "glacier",
        "grassland",
        "heath",
        "mud",
        "peak",
        "saddle",
        "sand",
        "scree",
        "scrub",
        "spring",
        "stone",
        "tree",
        "tree_row",
        "volcano",
        "water",
        "wetland",
        "wood"
    ],
    "office": [
        "accountant",
        "administrative",
        "architect",
        "association",
        "company",
        "educational_institution",
        "employment_agency",
        "estate_agent",
        "forestry",
        "foundation",
        "government",
        "guide",
        "insurance",
        "it",
        "lawyer",
        "newspaper",
        "ngo",
        "notary",
        "political_party",
        "quango",
        "register",
        "religion",
        "research",
        "tax",
        "telecommunication",
        "travel_agent",
        "water_utility"
    ],
    "place": [
        "allotments",
        "archipelago",
        "city",
        "continent",
        "county",
        "country",
        "district",
        "farm",
        "hamlet",
        "island",
        "islet",
        "isolated_dwelling",
        "locality",
        "municipality",
        "neighbourhood",
        "province",
        "state",
        "suburb",
        "region",
        "town",
        "village"
    ],
    "power": [
        "cable",
        "plant",
        "generator",
        "line",
        "minor_line",
        "pole",
        "substation",
        "switch",
        "tower",
        "transformer"
    ],
    "produce": [
        "berries",
        "cassava",
        "cereal",
        "christmas_trees",
        "cork",
        "crocodile",
        "dry_farming",
        "fire_wood",
        "fish",
        "flowers",
        "forage",
        "hay",
        "herbs",
        "hide",
        "hop",
        "latex",
        "lavender",
        "live_animal",
        "maize",
        "maple_syrup",
        "meat",
        "mussels",
        "nut",
        "oil",
        "olive",
        "oysters",
        "prawns",
        "rape",
        "rice",
        "seaweed",
        "shrimp",
        "spice",
        "sugarcane",
        "sunflower",
        "tea",
        "timber",
        "turf",
        "vegetable"
    ],
    "public_transport": [
        "stop_position",
        "platform",
        "station",
        "stop_area"
    ],
    "shop": [
        "alcohol",
        "antiques",
        "art",
        "baby_goods",
        "bakery",
        "bag",
        "bathroom_furnishing",
        "beauty",
        "bed",
        "beverages",
        "bicycle",
        "books",
        "boutique",
        "butcher",
        "car",
        "car_repair",
        "car_parts",
        "carpet",
        "charity",
        "cheese",
        "chemist",
        "chocolate",
        "clothes",
        "coffee",
        "computer",
        "confectionery",
        "convenience",
        "copyshop",
        "cosmetics",
        "craft",
        "curtain",
        "deli",
        "department_store",
        "dairy",
        "dry_cleaning",
        "doityourself",
        "electronics",
        "erotic",
        "fabric",
        "farm",
        "fashion",
        "fishing",
        "florist",
        "frame",
        "funeral_directors",
        "furniture",
        "general",
        "gift",
        "hairdresser",
        "hardware",
        "hearing_aids",
        "herbalist",
        "hifi",
        "hunting",
        "interior_decoration",
        "jewelry",
        "kiosk",
        "kitchen",
        "greengrocer",
        "grocery",
        "leather",
        "laundry",
        "mall",
        "massage",
        "medical_supply",
        "mobile_phone",
        "money_lender",
        "motorcycle",
        "music",
        "musical_instrument",
        "newsagent",
        "optician",
        "organic",
        "outdoor",
        "pasta",
        "pet",
        "photo",
        "scuba_diving",
        "seafood",
        "second_hand",
        "shoes",
        "sports",
        "stationery",
        "supermarket",
        "tailor",
        "tattoo",
        "tea",
        "ticket",
        "tobacco",
        "toys",
        "travel_agency",
        "tyres",
        "vacant",
        "variety_store",
        "video",
        "video_games",
        "water_sports",
        "weapons",
        "wine"
    ],
    "sport": [
        "9pin",
        "10pin",
        "american_football",
        "archery",
        "athletics",
        "australian_football",
        "base",
        "badminton",
        "baseball",
        "beachvolleyball",
        "billiards",
        "bmx",
        "boules",
        "bowls",
        "boxing",
        "canoe",
        "chess",
        "climbing",
        "climbing_adventure",
        "cycling",
        "equestrian",
        "free_flying",
        "golf",
        "handball",
        "horse_racing",
        "karting",
        "kitesurfing",
        "model_aerodrome",
        "motocross",
        "motor",
        "multi",
        "roller_skating",
        "rugby_league",
        "rugby_union",
        "running",
        "sailing",
        "shooting",
        "skateboard",
        "skiing",
        "soccer",
        "swimming",
        "tennis",
        "volleyball"
    ],
    "railway": [
        "abandoned",
        "buffer_stop",
        "construction",
        "crossing",
        "disused",
        "funicular",
        "halt",
        "level_crossing",
        "miniature",
        "narrow_gauge",
        "preserved",
        "rail",
        "station",
        "subway",
        "subway_entrance",
        "switch",
        "tram",
        "tram_stop"
    ],
    "route": [
        "bicycle",
        "bus",
        "ferry",
        "hiking",
        "mtb",
        "pipeline",
        "piste",
        "power",
        "railway",
        "road",
        "ski",
        "train",
        "tram"
    ],
    "tourism": [
        "alpine_hut",
        "apartement",
        "attraction",
        "artwork",
        "camp_site",
        "caravan_site",
        "chalet",
        "gallery",
        "guest_house",
        "hostel",
        "hotel",
        "information",
        "motel",
        "museum",
        "picnic_site",
        "theme_park",
        "viewpoint",
        "zoo",
        "yes"
    ],
    "trees": [
        "almond_trees",
        "apple_trees",
        "apricot_trees",
        "avocado_trees",
        "banana_plants",
        "bayberry",
        "blackberry",
        "blueberry",
        "cacao_plants",
        "cherry_trees",
        "chestnut_trees",
        "coconut_palms",
        "coffea_plants",
        "cranberry",
        "custard_apple",
        "date_palms",
        "durian_trees",
        "ginkgo_trees",
        "governor's_plum",
        "guava_trees",
        "hazel_plants",
        "lemon_trees",
        "lychee_trees",
        "macadamia_trees",
        "mandarin_trees",
        "mango_trees",
        "mulberrie_trees",
        "olive_trees",
        "orange_trees",
        "papaya_trees",
        "peach_trees",
        "pear_trees",
        "pecan_trees",
        "persimmon_trees",
        "pineapple_plants",
        "pistachio_trees",
        "plum_trees",
        "pomegranate_trees",
        "rambutan_trees",
        "raspberry",
        "sand_pear",
        "tea_plants",
        "walnut_trees"
    ],
    "waterway": [
        "canal",
        "ditch",
        "dam",
        "dock",
        "drain",
        "river",
        "riverbank",
        "stream",
        "weir"
    ]
}

# αντιστοιχία αριθμών σε κωδικούς της κάθε περιοχής
ADMIN_REGIONS = {
    "0": "GR",  # Greece
    "1": "GR-69",  # Ágion Óros
    "2": "GR-A",  # Anatolikí Makedonía kai Thráki
    "3": "GR-I",  # Attikí
    "4": "GR-G",  # Dytikí Elláda
    "5": "GR-C",  # Dytikí Makedonía
    "6": "GR-F",  # Ionía Nísia
    "7": "GR-D",  # Ípeiros
    "8": "GR-B",  # Kentrikí Makedonía
    "9": "GR-M",  # Kríti
    "10": "GR-L",  # Nótio Aigaío
    "11": "GR-J",  # Pelopónnisos
    "12": "GR-H",  # Stereá Elláda
    "13": "GR-E",  # Thessalía
    "14": "GR-K"  # Vóreio Aigaío
}


# Η συνάρτηση on_entry_click διαχειρίζεται τα βασικά πλάισια κειμένου (entry widgets) που
# εχουν δημιουργηθεί στο περιβάλλον της tkinter. Η λειτουργία της είναι να
# διαγράφει το προεπιλεγμένο κείμενο που έχει οριστεί στο κάθε widget αν ο
# χρήστης το επιλέξει, μετατρέποντας το χρώμα του κειμένου σε μαύρο.

def on_entry_click(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, tk.END)
        entry.config(fg='black')  # χρώμα κειμένου μαυρο


# Η συνάρτηση on_focus_click λειτουργεί αντίστοιχα με την προηγούμενη.Επαναφέρει το
# προεπιλεγμένο κείμενο που έχει οριστεί στο κάθε entry widget αν ο χρήστης το αποεπιλέξει,
# μετατρέποντας το χρωμα του κειμένου σε γκρι

def on_focus_out(entry, default_text):
    if entry.get() == '':
        entry.insert(0, default_text)
        entry.config(fg='grey')  # default χρωμα γκρι


# Η συνάρτηση search_button_clicked αποτελεί τον πυρήνα το προγράμματος αφού εμπεριέχει
# την αναζήτηση των δεδομένων του Open Street Map, επεξεργάζεται τα αποτελέσματα που
# λαμβάνει και τα παρουσιάζει σε έναν χάρτη της βιβλιοθήκης folium

def search_button_clicked():
    administrative_region = number_entry.get().lower()
    key = key_entry.get().lower()
    value = value_entry.get().lower()

    # παρακάτω γίνεται αρχικά έλεγχος για την ορθότητα της τιμής του 1ου entry box.

    if administrative_region.isdigit() and 1 <= int(administrative_region) <= 14:

        # Εάν ο χρήστης ορθώς έχει εισάγει ψηφίο το οποίο μάλιστα βρισκεταί μεταξυ
        # του 1 και του 14, δημιουργείται ένα αντικείμενο Overpass της βιβλιοθήκης overpy,
        # το οποίο αργότερα εκτελεί το query (γραμμένο ως όρισμα σε γλώσα του overpass API)
        # σύμφωνα πάντα με τα στοιχεία που έχει εισάγει ο χρήστης.

        api = overpy.Overpass()
        r = api.query(f"""
        [out:json][timeout:25];
        area["ISO3166-2"="{ADMIN_REGIONS[administrative_region]}"][admin_level=5];
        (nwr(area)["{key}"="{value}"];
        );
        out center;
        """)

        # Με χρήση του module Point της βιβλιοθήκης shapely, παρακάτω δημιουργούνται σημεία
        # με τις συντεταγμένες που προκύπτουν για κάθε node, way και relation απο το query
        # του open street map

        points_array = []
        points_array += [Point(float(node.lon), float(node.lat)) for node in r.nodes]
        points_array += [Point(way.center_lon, way.center_lat) for way in r.ways]
        points_array += [Point(rel.center_lon, rel.center_lat) for rel in r.relations]

        # Αν η λίστα που δημιουργήθηκε δεν ειναι κενή τοτε το πρόγραμμα συνεχίζει δημιουργώντας
        # ενα αντικείμενο geoseries της βιβλιοθήκης geopandas(αποτελεί ουσιαστικά μια λίστα
        # που περιέχει set συντεταγμένων)

        if len(points_array) != 0:
            points_series = gpd.GeoSeries(points_array)

            # εδώ δημιουργείται ενα geodataframe (αντικείμενο σαν πίνακας), με μία λιστα
            # εν ονόματι geometry που περιέχει τα σετ των συντεταγμένων για κάθε σημείο απο
            # το geoseries που έχει δημιουργηθεί.

            results_gdf = gpd.GeoDataFrame(geometry=points_series, crs=4326)

            # το παρακάτω κομμάτι αφορά την αρχικοποίηση ενός χάρτη της βιβλιοθήκης
            # folium και την εισαγωγή τόσο των 2 διαφορετικών layers στον χάρτη,
            # όσο και την εισαγωγή των στοιχείων στα δυο layers.

            map = folium.Map(location=[38, 24], zoom_start=7, tiles=None)

            folium_points = folium.FeatureGroup(name="anchor points", show=True)
            folium.TileLayer(tiles='OpenStreetMap').add_to(folium_points)
            folium_points.add_to(map)
            folium_heat = folium.FeatureGroup(name="heat", show=False)
            folium.TileLayer(tiles='cartodbdark_matter').add_to(folium_heat)
            folium_heat.add_to(map)

            with open("query_results.txt", "w", encoding="utf-8") as file:
                for idx, point in enumerate(results_gdf.geometry):
                    coordinates = [point.xy[1][0], point.xy[0][0]]

                    name = ""
                    osm_id = ""
                    coords = f": {coordinates[0]}, {coordinates[1]}"
                    phone_number = ""
                    address = ""

                    if idx < len(r.nodes):
                        node = r.nodes[idx]
                        name = node.tags.get("name", "")
                        osm_id = f": {node.id}"
                        phone_number = node.tags.get("phone", "")
                        address = node.tags.get("addr:street", "") + " " + node.tags.get("addr:housenumber", "")

                    elif len(r.nodes) <= idx < len(r.nodes) + len(r.ways):
                        way = r.ways[idx - len(r.nodes)]
                        name = way.tags.get("name", "")
                        osm_id = f": {way.id}"
                        phone_number = way.tags.get("phone", "")
                        address = way.tags.get("addr:street", "") + " " + way.tags.get("addr:housenumber", "")

                    elif idx >= len(r.nodes) + len(r.ways):
                        rel = r.relations[idx - (len(r.nodes) + len(r.ways))]
                        name = rel.tags.get("name", "")
                        osm_id = f": {rel.id}"
                        phone_number = rel.tags.get("phone", "")
                        address = rel.tags.get("addr:street", "") + " " + rel.tags.get("addr:housenumber", "")

                    info_string = f"Name: {name}\nID: {osm_id}\nCoordinates: {coordinates[0]}, {coordinates[1]}\nPhone: {phone_number}\nAddress: {address}\n\n"

                    file.write(info_string)

            for idx, point in enumerate(results_gdf.geometry):
                coordinates = [point.xy[1][0], point.xy[0][0]]

                name = ""
                osm_id = ""
                coords = f": {coordinates[0]}, {coordinates[1]}"
                phone_number = ""
                address = ""

                if idx < len(r.nodes):
                    node = r.nodes[idx]
                    name = node.tags.get("name", "")
                    osm_id = f": {node.id}"
                    phone_number = node.tags.get("phone", "")
                    address = node.tags.get("addr:street", "") + " " + node.tags.get("addr:housenumber", "")

                elif len(r.nodes) <= idx < len(r.nodes) + len(r.ways):
                    way = r.ways[idx - len(r.nodes)]
                    name = way.tags.get("name", "")
                    osm_id = f": {way.id}"
                    phone_number = way.tags.get("phone", "")
                    address = way.tags.get("addr:street", "") + " " + way.tags.get("addr:housenumber", "")

                elif idx >= len(r.nodes) + len(r.ways):
                    rel = r.relations[idx - (len(r.nodes) + len(r.ways))]
                    name = rel.tags.get("name", "")
                    osm_id = f": {rel.id}"
                    phone_number = rel.tags.get("phone", "")
                    address = rel.tags.get("addr:street", "") + " " + rel.tags.get("addr:housenumber", "")

                popup_content = f"<strong>Name:</strong> {name}<br> \
                                    <strong>ID:</strong> {osm_id}<br> \
                                    <strong>Coordinates:</strong> {coords}<br> \
                                    <strong>Phone:</strong> {phone_number}<br> \
                                    <strong>Address:</strong> {address}"

                folium.features.CircleMarker(location=coordinates,
                                             radius=8,
                                             color="green",
                                             fill=True,
                                             fill_color="orange",
                                             fill_opacity=0.3,
                                             popup=folium.Popup(popup_content, max_width=300)).add_to(folium_points)

            heat_data = [[point.xy[1][0], point.xy[0][0]] for point in results_gdf.geometry]

            plugins.HeatMap(heat_data, radius=40, blur=30, use_local_extrema=True, tiles="Cartodb dark_matter").add_to(
                folium_heat)

            folium.LayerControl().add_to(map)

            # ο χάρτης αποθηκέυεται ως αρχείο html στο ίδιο directory οπου τρέχει η εφαρμογή

            map.save("folium_map.html")

            # με χρήση του module open_new_tab της built in βιβλιοθήκης webbrowser,
            # το html αρχείο ανοίγει, αφού δημιουργηθεί, στον default browser.

            map_dir = os.getcwd() + os.path.sep + "folium_map.html"
            webbrowser.open_new_tab(map_dir)

        # Εφόσον δεν υπάρχουν στοιχεία για το επιλεγμένο region, ενα error message προκύπτει

        elif len(points_array) == 0:
            messagebox.showerror("Error", "The data you entered didn't return any result.")
            return

    # Αν επιλεχτεί η περιοχή με αριθμό 0 απο το ADMIN_REGIONS εκτελείται ένας όμοιος με τον παραπάνω κωδικα
    # αλλά για όλη την έκταση της Ελλάδας και οχι για μι συγκεκριμένη περιοχή

    elif administrative_region == "0":
        api = overpy.Overpass()
        r = api.query(f"""
                [out:json][timeout:25];
                area["ISO3166-1"="GR"][admin_level=2];
                (nwr(area)["{key}"="{value}"];
                );
                out center;
                """)

        points_array = []
        points_array += [Point(float(node.lon), float(node.lat)) for node in r.nodes]
        points_array += [Point(float(way.center_lon), float(way.center_lat)) for way in r.ways]
        points_array += [Point(float(rel.center_lon), float(rel.center_lat)) for rel in r.relations]

        if len(points_array) != 0:
            points_series = gpd.GeoSeries(points_array)

            results_gdf = gpd.GeoDataFrame(geometry=points_series, crs=4326)

            map = folium.Map(location=[38, 24], zoom_start=7, tiles=None)

            folium_points = folium.FeatureGroup(name="anchor points", show=True)
            folium.TileLayer(tiles='OpenStreetMap').add_to(folium_points)
            folium_points.add_to(map)
            folium_heat = folium.FeatureGroup(name="heat", show=False)
            folium.TileLayer(tiles='cartodbdark_matter').add_to(folium_heat)
            folium_heat.add_to(map)

            with open("query_results.txt", "w", encoding="utf-8") as file:
                for idx, point in enumerate(results_gdf.geometry):
                    coordinates = [point.xy[1][0], point.xy[0][0]]

                    name = ""
                    osm_id = ""
                    coords = f": {coordinates[0]}, {coordinates[1]}"
                    phone_number = ""
                    address = ""

                    if idx < len(r.nodes):
                        node = r.nodes[idx]
                        name = node.tags.get("name", "")
                        osm_id = f": {node.id}"
                        phone_number = node.tags.get("phone", "")
                        address = node.tags.get("addr:street", "") + " " + node.tags.get("addr:housenumber", "")

                    elif len(r.nodes) <= idx < len(r.nodes) + len(r.ways):
                        way = r.ways[idx - len(r.nodes)]
                        name = way.tags.get("name", "")
                        osm_id = f": {way.id}"
                        phone_number = way.tags.get("phone", "")
                        address = way.tags.get("addr:street", "") + " " + way.tags.get("addr:housenumber", "")

                    elif idx >= len(r.nodes) + len(r.ways):
                        rel = r.relations[idx - (len(r.nodes) + len(r.ways))]
                        name = rel.tags.get("name", "")
                        osm_id = f": {rel.id}"
                        phone_number = rel.tags.get("phone", "")
                        address = rel.tags.get("addr:street", "") + " " + rel.tags.get("addr:housenumber", "")

                    info_string = f"Name: {name}\nID: {osm_id}\nCoordinates: {coordinates[0]}, {coordinates[1]}\nPhone: {phone_number}\nAddress: {address}\n\n"

                    file.write(info_string)

            for idx, point in enumerate(results_gdf.geometry):
                coordinates = [point.xy[1][0], point.xy[0][0]]

                name = ""
                osm_id = ""
                coords = f": {coordinates[0]}, {coordinates[1]}"
                phone_number = ""
                address = ""

                if idx < len(r.nodes):
                    node = r.nodes[idx]
                    name = node.tags.get("name", "")
                    osm_id = f": {node.id}"
                    phone_number = node.tags.get("phone", "")
                    address = node.tags.get("addr:street", "") + " " + node.tags.get("addr:housenumber", "")

                elif len(r.nodes) <= idx < len(r.nodes) + len(r.ways):
                    way = r.ways[idx - len(r.nodes)]
                    name = way.tags.get("name", "")
                    osm_id = f": {way.id}"
                    phone_number = way.tags.get("phone", "")
                    address = way.tags.get("addr:street", "") + " " + way.tags.get("addr:housenumber", "")

                elif idx >= len(r.nodes) + len(r.ways):
                    rel = r.relations[idx - (len(r.nodes) + len(r.ways))]
                    name = rel.tags.get("name", "")
                    osm_id = f": {rel.id}"
                    phone_number = rel.tags.get("phone", "")
                    address = rel.tags.get("addr:street", "") + " " + rel.tags.get("addr:housenumber", "")

                popup_content = f"<strong>Name:</strong> {name}<br> \
                                    <strong>ID:</strong> {osm_id}<br> \
                                    <strong>Coordinates:</strong> {coords}<br> \
                                    <strong>Phone:</strong> {phone_number}<br> \
                                    <strong>Address:</strong> {address}"

                folium.features.CircleMarker(location=coordinates,
                                             radius=8,
                                             color="green",
                                             fill=True,
                                             fill_color="orange",
                                             fill_opacity=0.3,
                                             popup=folium.Popup(popup_content, max_width=300)).add_to(folium_points)

            heat_data = [[point.xy[1][0], point.xy[0][0]] for point in results_gdf.geometry]

            plugins.HeatMap(heat_data, radius=40, blur=30, tiles="Cartodb dark_matter").add_to(folium_heat)

            folium.LayerControl().add_to(map)

            map.save("folium_map.html")

            map_dir = os.getcwd() + os.path.sep + "folium_map.html"
            webbrowser.open_new_tab(map_dir)

        elif len(points_array) == 0:
            messagebox.showerror("Error", "The data you entered didn't return any result.")
            return
    else:
        messagebox.showerror("Error", "The region number you entered is not valid.")
        return  # αν ο αριθμός της περιοχής δεν είναι έγκυρος


# δημιουργία γραφικού περιβάλλοντος
icon_dir = os.getcwd() + os.path.sep + "osm.ico"

# δημιουργια παραθυρου που θα περιέχει όλα τα γραφικά στοιχεία του προγράμματοςwindow = tk.Tk()
window = tk.Tk()
window.title("OSM Data Manipulator")
window.iconbitmap(icon_dir)
window.resizable(False, False)
window.configure(bg='#E0E0E0')

# υπολογισμος διαστασεων οθονης για εμφανιση στο κεντρο
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# δημιουργία των entry boxes
default_text_color = 'grey'
entry_font = ('Arial', 12)

# Δημιουργία του πρώτου entry box το οποίο δέχεται ως τιμες του τους αριθμούς 0-14 ο οποίοι
# αντιστοιχούν σε καποιο κωδικό μιας περιοχής σύμφωνα με το ADMIN_REGIONS

number_default_text = "Number (0-14)"
number_entry = tk.Entry(window, fg=default_text_color, font=entry_font, bd=2, relief=tk.GROOVE, bg='#F0F0F0')
number_entry.insert(0, number_default_text)
number_entry.bind('<FocusIn>', lambda event: on_entry_click(number_entry, number_default_text))
number_entry.bind('<FocusOut>', lambda event: on_focus_out(number_entry, number_default_text))
number_entry.pack(side=tk.LEFT, padx=10)

# Δημιουργία του δέυτερου entry box το οποίο δέχεται ως τιμες του τα keys του dictionary
# KEY_VALUES που εμπεριέχονται στο λεξικό

key_default_text = "Key word"
key_entry = tk.Entry(window, fg=default_text_color, font=entry_font, bd=2, relief=tk.GROOVE, bg='#F0F0F0')
key_entry.insert(0, key_default_text)
key_entry.bind('<FocusIn>', lambda event: on_entry_click(key_entry, key_default_text))
key_entry.bind('<FocusOut>', lambda event: on_focus_out(key_entry, key_default_text))
key_entry.pack(side=tk.LEFT, padx=10)

# Δημιουργία του τρίτου entry box το οποίο δέχεται ως τιμες του τα Values του dictionary
# KEY_VALUES που εμπεριέχονται στο λεξικό

value_default_text = "Value"
value_entry = tk.Entry(window, fg=default_text_color, font=entry_font, bd=2, relief=tk.GROOVE, bg='#F0F0F0')
value_entry.insert(0, value_default_text)
value_entry.bind('<FocusIn>', lambda event: on_entry_click(value_entry, value_default_text))
value_entry.bind('<FocusOut>', lambda event: on_focus_out(value_entry, value_default_text))
value_entry.pack(side=tk.LEFT, padx=10)

# φορτωση φωτο αναζητησης απο βιβλιοθηκη pillow
search_image_dir = os.getcwd() + os.path.sep + "search.png"
search_image = Image.open(search_image_dir)
search_image = search_image.resize((20, 20))
search_photo = ImageTk.PhotoImage(search_image)

# δημιουργία του Button που εμπεριέχει την φωτογραφία αναζήτηση
search_button = tk.Button(window, image=search_photo, command=search_button_clicked, bg='#3498db', bd=2, cursor='hand2')
search_button.image = search_photo
search_button.config(pady=10)
search_button.pack(side=tk.TOP, pady=20)


def set_selected_number(selected_num):
    global num
    num = selected_num
    set_number_entry(num)  # εισαγει στο πρωτο entry box την επιλεγμενη τιμη


# η συνάρτηση create menu δημιουργεί το μενού στο interface Του widget που του επιτρέπει να
# επιλέγει τα όλα τα αποδεκτά Numbers,keys,values του προγράμματος.Βασίζεται στην χρήση της
# συνάρτησης Menu της tkinter

def create_menu():
    menu_bar = Menu(window)
    menu_bar.config(bg='#E0E0E0')
    window.config(menu=menu_bar)

    number_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="administrative regions", menu=number_menu)

    options = [
        "0: Ελλάδα",
        "1: Άγιο Όρος",
        "2: Ανατολική Μακεδονία και Θράκη",
        "3: Αττική",
        "4: Δυτική Ελλάδα",
        "5: Δυτική Μακεδονία",
        "6: Ιόνια Νησιά",
        "7: Ήπειρος",
        "8: Κεντρική Μακεδονία",
        "9: Κρήτη",
        "10: Νότιο Αιγαίο",
        "11: Πελοπόννησος",
        "12: Στερεά Ελλάδα",
        "13: Θεσσαλία",
        "14: Βόρειο Αιγαίο"
    ]

    for option in options:
        number_menu.add_command(label=option, command=lambda o=option: set_selected_number(options.index(o)))

    # Δημιουργεί το Menu keys
    key_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Keys", menu=key_menu)
    for k in KEY_VALUES.keys():
        key_menu.add_command(label=k, command=lambda key=k: set_key_entry(key))

    # Δημιουργεί το Menu values
    global value_menu
    value_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Values", menu=value_menu)


def update_menus(selected_key):
    value_menu.delete(0, tk.END)
    if selected_key in KEY_VALUES:  # φανερώνει μονο τα Values που περιεχονται στο επιλεγμένο Key
        for v in KEY_VALUES[selected_key]:
            value_menu.add_command(label=v, command=lambda value=v: set_value_entry(value))


# Οι τρεις παρακάτω συναρτήσεις διοχετεύουν την επιλογή του χρήστη στα entry boxes
def set_number_entry(num):
    number_entry.delete(0, tk.END)
    number_entry.config(fg='black')
    number_entry.insert(0, num)


def set_key_entry(key):
    key_entry.delete(0, tk.END)
    key_entry.config(fg='black')
    key_entry.insert(0, key)
    update_menus(key)


def set_value_entry(value):
    value_entry.delete(0, tk.END)
    value_entry.config(fg='black')
    value_entry.insert(0, value)


create_menu()

# εμφανιση στο κεντρο της οθονης
window_width = 700  # ιδανικες διαστασεις
window_height = 90  # >>
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# ενωση κουμπιου με το enter
window.bind('<Return>', lambda event=None: search_button.invoke())

# εκκινηση προγραμματος
window.mainloop()
