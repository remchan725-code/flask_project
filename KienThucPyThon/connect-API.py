import requests

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_data(pokemon_name):
    url = f"{base_url}pokemon/{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data for {pokemon_name.capitalize()}. Status code: {response.status_code}")
    print(response)
    pass

pokemon_name = "Pikachu"
pokemon_info = get_pokemon_data(pokemon_name)

if pokemon_info:
    print(f"Pokemon Name: {pokemon_info['name']}")
    print(f"Height: {pokemon_info['height']}")
    print(f"Weight: {pokemon_info['weight']}")
    print("Abilities:")
    for ability in pokemon_info['abilities']:
        print(f"- {ability['ability']['name']}")
