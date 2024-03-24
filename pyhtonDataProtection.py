import requests
import re
import json
import uuid

# URL of the JS file
url = "https://www.cnil.fr/sites/cnil/modules/custom/cnil_map_dpa/assets/js/cnil-map-datas.js"

# Fetch the JS file
response = requests.get(url)
data_js = response.text

# Extract the JSON portion from the JS file
match = re.search(r'var cnilmapCountriesDPA = (.*?});', data_js, re.DOTALL)
json_data = match.group(1) if match else None

# Parse the JSON data
data = json.loads(json_data)

# Define the base structure for the clusters file
clusters = {
    "authors": ["Eliott LALLEMENT, Théo PAGES"],
    "type": "country-data-protection",
    "clusters": []
}

# Iterate over each feature and append to clusters
for feature in data['features']:
    country_name = feature['properties']['name_en']
    protection_level = feature['properties']['levelProtection']
    website = feature['properties'].get('webSite', 'Not available')
    address = feature['properties'].get('address', 'Not available')
    authority_name = feature['properties'].get('popup', 'Not available').split("\n")[0]

    cluster = {
        "value": country_name,
        "uuid": str(uuid.uuid4()),
        "meta": {
            "protection_level": protection_level,
            "regulation_website": website,
            "address": address,
            "authority_name": authority_name
        }
    }
    clusters["clusters"].append(cluster)

# Save the clusters to a JSON file
with open('./data/data_protection_cluster.json', 'w') as outfile:
    json.dump(clusters, outfile, indent=4)

print("Clusters saved as data_protection_cluster.json")
