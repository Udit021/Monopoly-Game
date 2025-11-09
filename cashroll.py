
import random

CITIES = [
    {"name": "Delhi", "price": 5000, "rent": 1000},
    {"name": "Mumbai", "price": 6000, "rent": 1200},
    {"name": "Kolkata", "price": 4000, "rent": 900},
    {"name": "Chennai", "price": 5500, "rent": 1100},
    {"name": "Bangalore", "price": 6500, "rent": 1300},
    {"name": "Hyderabad", "price": 5000, "rent": 1000},
    {"name": "Jaipur", "price": 3000, "rent": 700},
    {"name": "Pune", "price": 4500, "rent": 950},
    {"name": "Lucknow", "price": 3500, "rent": 800},
    {"name": "Ahmedabad", "price": 4000, "rent": 850}
]

def assign_starting_money(players):
    money = {}
    for player in players:
        input(f"{player}, press Enter to roll the dice: ")
        roll = random.randint(1, 6)
        print(f"{player} rolled {roll}")
        if roll >= 5:
            money[player] = 50000
        elif roll >= 3:
            money[player] = 40000
        else:
            money[player] = 30000
    print("\nStarting money assigned:")
    for p in players:
        print(f"{p}: Rs {money[p]}")
    return money

def setup_players(num):
    players = []
    for i in range(num):
        name = input(f"Enter name for Player {i + 1}: ")
        players.append(name)
    money = assign_starting_money(players)
    return [{"name": p, "cash": money[p], "position": 0, "properties": [], "alive": True, "started": False} for p in players]

def setup_cities():
    cities = []
    for city in CITIES:
        c = city.copy()
        c["owner"] = None
        cities.append(c)
    return cities

def move_player(player):
    input(f"\n{player['name']}, press Enter to roll the dice...")
    dice = random.randint(1, 6)
    print(f"{player['name']} rolled a {dice}")
    if not player["started"]:
        if dice == 6:
            player["started"] = True
            print(f"{player['name']} starts moving")
        else:
            print(f"{player['name']} needs a 6 to start.")
            return 0
    player["position"] = (player["position"] + dice) % len(CITIES)
    return dice

def buy_property(player, city):
    if player["cash"] >= city["price"]:
        choice = input(f"Buy {city['name']} for Rs {city['price']}? (y/n): ")
        if choice.lower() == "y":
            player["cash"] -= city["price"]
            player["properties"].append(city["name"])
            city["owner"] = player["name"]
            print(f"{player['name']} bought {city['name']}")

def pay_rent(player, owner, city):
    rent = city["rent"]
    if player["cash"] >= rent:
        player["cash"] -= rent
        owner["cash"] += rent
        print(f"{player['name']} paid Rs {rent} rent to {owner['name']}")
    else:
        print(f"{player['name']} is bankrupt!")
        player["cash"] = 0
        player["alive"] = False

def take_turn(player, players, cities):
    if not player["alive"]:
        return
    dice = move_player(player)
    if dice == 0:
        return
    city = cities[player["position"]]
    print(f"{player['name']} landed on {city['name']}")
    if city["owner"] is None:
        buy_property(player, city)
    elif city["owner"] != player["name"]:
        owner = next(p for p in players if p["name"] == city["owner"])
        pay_rent(player, owner, city)
    print(f"{player['name']} balance: Rs {player['cash']}")

def calculate_networth(player, cities):
    total = player["cash"]
    for city in cities:
        if city["owner"] == player["name"]:
            total += city["price"]
    return total

def play_game():
    num_players = int(input("Enter number of players (2-4): "))
    players = setup_players(num_players)
    cities = setup_cities()
    print("\nGame Start\n")
    for turn in range(20):
        print(f"\nTurn {turn + 1}")
        alive_players = [p for p in players if p["alive"]]
        if len(alive_players) <= 1:
            break
        for player in alive_players:
            take_turn(player, players, cities)
    print("\nGame Over")
    standings = sorted(players, key=lambda x: calculate_networth(x, cities), reverse=True)
    for i, p in enumerate(standings, 1):
        print(f"{i}. {p['name']} - Net Worth: Rs {calculate_networth(p, cities)}")
#file handling

play_game()
