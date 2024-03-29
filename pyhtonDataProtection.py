import requests
import re
import json
import uuid
from urllib.parse import urlparse
import tldextract  # You need to install this package


# Function to remove HTML tags from descriptions
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_authority_name(website_url):
    if not website_url:
        return ''
    
    # Parse the URL and split the path to get individual segments
    parsed_url = urlparse(website_url)
    path_segments = [segment for segment in parsed_url.path.strip('/').split('/') if segment]

    # Define lists for generic domain parts and common subdomain prefixes
    generic_domains = ['gov', 'com', 'org', 'net', 'edu', 'co', 'gv', 'justice'] # avant en moins : 'gv', 'justice'
    common_prefixes = ['www']

    # Extract the domain and subdomain parts
    domain_parts = parsed_url.netloc.split('.')
    domain = domain_parts[1] if len(domain_parts) >= 2 else '' # avant : domain = domain_parts[-2] if len(domain_parts) >= 2 else ''

    subdomain = domain_parts[0] if len(domain_parts) > 2 else ''

    print("domain_parts = ", domain_parts)
    print("domain = ", domain)
    print("subdomain = ", subdomain)
    print("path_segments = ", path_segments)

    # Use the first significant path segment if the domain is generic and the subdomain is a common prefix
    if domain in generic_domains and (not subdomain or subdomain in common_prefixes) and path_segments:
        return path_segments[0]
    elif subdomain and subdomain not in common_prefixes:
        return subdomain
    else:
        return domain

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
    "authors": ["Eliott LALLEMENT, Theo PAGES"],
    "type": "country-data-protection",
    "category": "GDPR",
    "source": "https://www.cnil.fr/sites/cnil/modules/custom/cnil_map_dpa/assets/js/cnil-map-datas.js",
    "uuid": str(uuid.uuid4()),
    "version": 1,
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
    authority_name = get_authority_name(website_url)

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
