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

    # Problematic case:
    if website_url == "https://www.argentina.gob.ar/aaip/datospersonales":
        return 'aaip'
    if website_url == "https://www.bahamas.gov.bs/wps/portal/public/!ut/p/b1/vZbLkqJKFEW_xQ-wyEQgYZjK-_0SgYmBIgiioKg8vr6pG3dQ9o1bNemWHBAEG9bZ-5wkIGIiJOJL8izy5F7Ul6T6vI6Z7QJIBsYUa1ikzwEFriCjrWmgk-QkiL4KJBowQFnbOraRTFoUeH3-t9uQJjZEKEc3fVXjXMCrbXO12rmRs9yxoov0mA7M0hye7IXxndFQcV7v_ISvcilLId0HbeL1d8CEg_CAosiI2zQt4vkw0NvIE6Mop_Z9W2otn2mJf2geqvwoUspry3DT8ZuU7dJOEevxXw_gfw78o4fvM5gEP2SoEnGxO390-_MH-IALiCAJEYUQ4mgaMlNE8bcVaOQPgs8u_CP4xmI0CdCXN_gBmIoE2PWgA1gTEj4RAmrrlUOjjKfRLUE3GvxhNIWchPoaGKfRM32h9-6qaZSrDggAmKOrGDdV8fxYaTneTgN3vcQ8TyXQ-R34mooHqL8NlGiLnTJCvo1pEkgWfDdw8dZIJdsCf93hy9BQzp_v4ctOYTkG0oilOJYBFMUiIigjBvGt0vFCsG2iu5y0XGuLzkbAndE4dw0wSylputrY-awdiLEgqfmjPZCpMu_7U_sUmhg7lkFVtxg2WWQlssKrDHYyJ1trgTzwOFYO_Y7P26l0Epspf9xAFiKedCdzSTzeQJM-GVcd08y-VJxPx6ZXh8Xtmrcal9CZ2sLeqxgjuLbxwLMILdz76gLUR6JRmlUrhwMnJ52lFdewxZU2r8PqzGZM1V9u-mhY5XZxXfqCeyOdGWHK9fnw_TbSyf8OGXINA7DQRKYB_UAz_fCzBV2bruB06rGs-X4E_VNlmWU0mJxspOLUAVE85W43m_0AVMh3A-G7gejNQEy9G8i8G_juKXX-_JS-fJkYDrEQkhSAiEQLRBKBvs97fvrH4QXebccjaGLArXZ1tBQdb5V7u1w_hJKWbdlKLvf1eS05RX1Pdquxbc7LR70HHVwnlxiPdeE2izw_0zal6sc5oyhJYVv91mXr0tydjnDoJYNrDrnkgtAKiOa8fmo6rQqZ-XVRyfx1RXg2-wVyrHpU/dl4/d5/L2dBISEvZ0FBIS9nQSEh":
        return 'Data Protection Commissioner' # Search by hand
    if website_url == "https://www.gov.bb/Departments/data-protection-commissioner":
        return 'Data Protection Commissioner'
    if website_url == "https://apdp.bj/":
        return 'apdp'
    if website_url == "https://www.privacy.bm":
        return 'Privacy Commissioner for Bermuda (PrivCom)'
    if website_url == "https://cpd.by":
        return 'cpd'
    if website_url == "https://azop.hr/":
        return 'azop'
    if website_url == "https://personaldata.ge/en":
        return 'Personal Data Protection Service (PDPS)'
    if website_url == "https://www.moc.gov.gh/agencies/data-protection-commission-dpc":
        return 'Data Protection Commission (DPC)'
    if website_url == "https://odpa.gg/about-us":
        return 'odpa'
    if website_url == "https://www.gov.il/en/departments/the_privacy_protection_authority/govil-landing-page":
        return 'The Privacy Protection Authority'
    if website_url == "https://jerseyoic.org/":
        return 'jerseyoic'
    if website_url == "https://dzlp.mk/en":
        return 'dzlp'
    if website_url == "https://home.inai.org.mx/":
        return 'inai'
    if website_url == "https://ansice.td/":
        return 'ansice'
        
    
    # Parse the URL and split the path to get individual segments
    parsed_url = urlparse(website_url)
    path_segments = [segment for segment in parsed_url.path.strip('/').split('/') if segment]

    # Define lists for generic domain parts and common subdomain prefixes
    generic_domains = ['gov', 'com', 'org', 'net', 'edu', 'co', 'gv', 'justice','bj','by','ge','gg','mk'] 
    common_prefixes = ['www']
    # Extract the domain and subdomain parts
    domain_parts = parsed_url.netloc.split('.')
    domain = domain_parts[1] if len(domain_parts) >= 2 else '' # avant : domain = domain_parts[-2] if len(domain_parts) >= 2 else ''
    subdomain = domain_parts[0] if len(domain_parts) > 2 else ''

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
    "source": url,
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
