from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import random, json, time

app = Flask(__name__)
CORS(app)

# Define unique items and their drop rates
unique_items = {
    "Eclipse atlatl": {"rarity": 1/224, "price": 3518409},
    "Eclipse moon helm": {"rarity": 1/224, "price": 1022178},
    "Eclipse moon chestplate": {"rarity": 1/224, "price": 1286989},
    "Eclipse moon tassets": {"rarity": 1/224, "price": 1391066},
    "Dual macuahuitl": {"rarity": 1/224, "price": 10130540},
    "Blood moon helm": {"rarity": 1/224, "price": 1140864},
    "Blood moon chestplate": {"rarity": 1/224, "price": 6133528},
    "Blood moon tassets": {"rarity": 1/224, "price": 12139841},
    "Blue moon spear": {"rarity": 1/224, "price": 704037},
    "Blue moon helm": {"rarity": 1/224, "price": 609171},
    "Blue moon chestplate": {"rarity": 1/224, "price": 2993557},
    "Blue moon tassets": {"rarity": 1/224, "price": 8373459},
}

# Define standard loot and their drop rates
standard_loot = {
    "Atlatl dart": {"quantity": (72, 120), "rarity": (5/30), "price": 198},
    "Swamp tar": {"quantity": (79, 119), "rarity": (4/30), "price": 3},
    "Sun-kissed bones": {"quantity": (6, 12), "rarity": (3/30), "price": 0},
    "Supercompost": {"quantity": (6, 12), "rarity": (3/30), "price": 65},
    "Soft clay": {"quantity": (15, 25), "rarity": (3/30), "price": 125},
    "Grimy harralander": {"quantity": (12, 18), "rarity": (3/30), "price": 690},
    "Blessed bone shards": {"quantity": (160, 179), "rarity": (2/30), "price": 0},
    "Water orb": {"quantity": (30, 45), "rarity": (2/30), "price": 802},
    "Maple seed": {"quantity": (1, 2), "rarity": (2/30), "price": 5174},
    "Wyrmling bones": {"quantity": (42, 54), "rarity": (1/30), "price": 509},
    "Grimy irit leaf": {"quantity": (12, 18), "rarity": (1/30), "price": 1263},
    "Yew seed": {"quantity": (1, 1), "rarity": (1/30), "price": 28705},
}

def simulate_loot(bosses, unique_items_pool):
    loot_received = {}
    total_value = 0

    # Step 1: Roll for unique items
    unique_drop_chance = 1 / 56
    for boss in bosses:
        if random.random() < unique_drop_chance:
            if unique_items_pool[boss]:
                chosen_item = random.choice(list(unique_items_pool[boss].keys()))
                loot_received[chosen_item] = loot_received.get(chosen_item, 0) + 1
                total_value += unique_items_pool[boss][chosen_item]["price"]
                del unique_items_pool[boss][chosen_item]  # Remove the item from the pool

    # Step 2: Roll for standard loot
    num_rolls = len(bosses) * 2  # Adjust rolls based on the number of bosses
    for _ in range(num_rolls):
        for item, details in standard_loot.items():
            if random.random() < details["rarity"]:
                quantity = random.randint(details["quantity"][0], details["quantity"][1])
                value = quantity * details["price"]
                loot_received[item] = loot_received.get(item, 0) + quantity
                total_value += value

    return loot_received, total_value, unique_items_pool

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/simulate", methods=["GET", "POST"])
def simulate():
    if request.method == "POST":
        data = request.json
        kc_count = int(data.get("kc_count", 105))
        bosses = data.get("bosses", ["Blood Moon", "Blue Moon", "Eclipse Moon"])
    elif request.method == "GET":
        kc_count = int(request.args.get("kc_count", 105))
        bosses = request.args.get("bosses", "Blood Moon,Blue Moon,Eclipse Moon").split(",")

    # Track total loot and value across all simulations
    total_loot = {}
    total_value = 0

    # Initialize the unique items pool based on selected bosses
    unique_items_pool = {
        "Blood Moon": {
            "Blood moon helm": unique_items["Blood moon helm"],
            "Blood moon chestplate": unique_items["Blood moon chestplate"],
            "Blood moon tassets": unique_items["Blood moon tassets"],
            "Dual macuahuitl": unique_items["Dual macuahuitl"],
        },
        "Blue Moon": {
            "Blue moon spear": unique_items["Blue moon spear"],
            "Blue moon helm": unique_items["Blue moon helm"],
            "Blue moon chestplate": unique_items["Blue moon chestplate"],
            "Blue moon tassets": unique_items["Blue moon tassets"],
        },
        "Eclipse Moon": {
            "Eclipse atlatl": unique_items["Eclipse atlatl"],
            "Eclipse moon helm": unique_items["Eclipse moon helm"],
            "Eclipse moon chestplate": unique_items["Eclipse moon chestplate"],
            "Eclipse moon tassets": unique_items["Eclipse moon tassets"],
        },
    }

    # Create a Response object with the generate function
    return Response(
        generate(unique_items_pool, total_loot, total_value, kc_count, bosses),
        mimetype="text/event-stream"
    )

def generate(unique_items_pool, total_loot, total_value, kc_count, bosses):
    for kc in range(1, kc_count + 1):
        loot, value, unique_items_pool = simulate_loot(bosses, unique_items_pool)
        total_value += value
        for item, quantity in loot.items():
            total_loot[item] = total_loot.get(item, 0) + quantity

        # Reset the unique items pool for a boss if all items have been obtained
        for boss in bosses:
            if not unique_items_pool[boss]:
                if boss == "Blood Moon":
                    unique_items_pool[boss] = {
                        "Blood moon helm": unique_items["Blood moon helm"],
                        "Blood moon chestplate": unique_items["Blood moon chestplate"],
                        "Blood moon tassets": unique_items["Blood moon tassets"],
                        "Dual macuahuitl": unique_items["Dual macuahuitl"],
                    }
                elif boss == "Blue Moon":
                    unique_items_pool[boss] = {
                        "Blue moon spear": unique_items["Blue moon spear"],
                        "Blue moon helm": unique_items["Blue moon helm"],
                        "Blue moon chestplate": unique_items["Blue moon chestplate"],
                        "Blue moon tassets": unique_items["Blue moon tassets"],
                    }
                elif boss == "Eclipse Moon":
                    unique_items_pool[boss] = {
                        "Eclipse atlatl": unique_items["Eclipse atlatl"],
                        "Eclipse moon helm": unique_items["Eclipse moon helm"],
                        "Eclipse moon chestplate": unique_items["Eclipse moon chestplate"],
                        "Eclipse moon tassets": unique_items["Eclipse moon tassets"],
                    }

        # Categorize loot into unique and common items
        unique_loot = {item: qty for item, qty in total_loot.items() if item in unique_items}
        common_loot = {item: qty for item, qty in total_loot.items() if item not in unique_items}

        # Replace spaces with underscores in item names for image filenames
        formatted_unique_loot = {item.replace(" ", "_"): quantity for item, quantity in unique_loot.items()}
        formatted_common_loot = {item.replace(" ", "_"): quantity for item, quantity in common_loot.items()}

        # Yield the current KC and categorized loot
        yield f"data: {json.dumps({
            'kc': kc,
            'unique_loot': formatted_unique_loot,
            'common_loot': formatted_common_loot,
            'total_value': total_value
        })}\n\n"

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)