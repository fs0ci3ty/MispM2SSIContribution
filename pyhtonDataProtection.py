import requests
import re
import json
import uuid
from urllib.parse import urlparse


# Function to remove HTML tags from descriptions
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

# Download the JavaScript file
url = "https://www.cnil.fr/sites/cnil/modules/custom/cnil_map_dpa/assets/js/cnil-map-datas.js"
response = requests.get(url)
data_js = response.text

# Extract the JSON data and protection level details
countries_data_match = re.search(r'var cnilmapCountriesDPA = (.*?});', data_js, re.DOTALL)
protection_levels_match = re.search(r'var cnilmapLevelProtection = ({.*?});', data_js, re.DOTALL)
edpb_membership_match = re.search(r'var cnilmapIsEDPB = ({.*?});', data_js, re.DOTALL)
afapdp_membership_match = re.search(r'var cnilmapIsAFAPDP = ({.*?});', data_js, re.DOTALL)

countries_data = json.loads(countries_data_match.group(1)) if countries_data_match else None
protection_levels = json.loads(protection_levels_match.group(1)) if protection_levels_match else None
edpb_membership = json.loads(edpb_membership_match.group(1)) if edpb_membership_match else None
afapdp_membership = json.loads(afapdp_membership_match.group(1)) if afapdp_membership_match else None

# Convert protection level keys to integers to match levelProtection values
protection_level_uuids = {int(level): str(uuid.uuid4()) for level in protection_levels}



clusters = {
    "authors": ["Eliott LALLEMENT, Théo PAGES"],
    "type": "country-data-protection",
    "clusters": []
}
# Generate protection level descriptions and clean them from HTML tags
protection_descriptions = []
for level, details in protection_levels.items():
    description = {
        "uuid": protection_level_uuids[int(level)],
        "description": clean_html(details['properties']['detail_en'])
    }
    protection_descriptions.append(description)

clusters["protection_levels"] = protection_descriptions

for feature in countries_data['features']:
    country_props = feature['properties']
    level_uuid = protection_level_uuids[country_props['levelProtection']]
    website_url = country_props.get('webSite', '')
    parsed_url = urlparse(website_url)
    authority_name = parsed_url.netloc.split('.')[1] if website_url and len(parsed_url.netloc.split('.')) > 2 else ''

    meta = {
        "protection_level_uuid": level_uuid,
        "edpb_membership": "Yes" if country_props['edpb'] == "Oui" else "No",
        "afapdp_membership": "Yes" if country_props['afapdp'] == "Oui" else "No",
    }
    
    if website_url:
        meta["regulation_website"] = website_url
    if country_props.get('address'):
        meta["address"] = country_props.get('address')
    if authority_name:
        meta["authority_name"] = authority_name

    cluster = {
        "value": country_props['name_en'],
        "uuid": str(uuid.uuid4()),
        "meta": meta
    }
    clusters["clusters"].append(cluster)



# Save the clusters and descriptions to a JSON file
with open('./data/data_protection_cluster.json', 'w') as outfile:
    json.dump(clusters, outfile, indent=4)

print("Clusters saved as data_protection_cluster.json")
