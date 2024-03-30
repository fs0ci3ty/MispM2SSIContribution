# GDPR Data Transfer Compliance Galaxy

**Author**: fs0ci3ty & pages497

**Instructors**: Mr. Alexandre DULAUNOY [@adulau](https://github.com/adulau) & Mr. Christian STUDER [@chrisr3d](https://github.com/chrisr3d)

## Context
This project is at the intersection of cybersecurity and data protection, focusing on international data transfer compliance with the General Data Protection Regulation (GDPR). It delivers a MISP galaxy for a comprehensive visual analysis of global data transfer practices in alignment with GDPR standards.

## Galaxy Purpose
The repository hosts a MISP galaxy depicting the landscape of GDPR-compliant data transfer across nations. Key features include:
- Structured data compatible with MISP galaxies and clusters.
- Detailed descriptions of various countries' data protection levels, aiming to highlight regions offering GDPR-equivalent data privacy safeguards.
The main goal of the galaxy is to provide a list of country that offers an equivalent level of data privacy to the GDPR regulation of the European Union. 

## YARA Rule for AIL
The project also introduces a YARA rule within the AIL framework to identify Telegram API keys, bolstering cybersecurity surveillance efforts. This rule is devised based on a recognized regex pattern detailed [here](https://stackoverflow.com/a/61888374).

## Data Source Discovery and Backup Strategy
The project's data is dynamically sourced from CNIL's interactive global data protection map ('https://www.cnil.fr/en/data-protection-around-the-world'). During a detailed examination of the webpage's sources via browser inspection tools, a JavaScript file ("https://www.cnil.fr/sites/cnil/modules/custom/cnil_map_dpa/assets/js/cnil-map-datas.js") was identified as containing all pertinent information related to the map. Notably, even after omitting the version parameter in the URL, the latest version of the file is still accessible, ensuring the script's continued functionality provided the URL remains unchanged. To safeguard against potential future inaccessibility of this URL, a copy of the JavaScript file has been preserved in the `data` folder within the project's directory.

## Methodology
- Automated retrieval and parsing of CNIL data ensure up-to-date insights into global data protection statuses.
- The collated data undergoes meticulous cleaning and structuring for seamless integration into the MISP galaxy framework.
- The custom YARA rule is engineered for precise detection of Telegram API keys, thus enhancing digital security measures.

## Limitations and Future Directions
Current challenges include accurately deriving the authority name from the varied and complex URLs of data protection authorities. Future iterations will focus on refining authority name extraction and enriching the dataset with detailed legal and regulatory frameworks pertaining to data protection in each country.

## How to generate the cluster 

1. Install Python 3:
   - On Debian:
     ```
     sudo apt update
     sudo apt install python3
     ```
   - Alternatively, download from [Python's official site](https://www.python.org/downloads/).

2. Clone the project:

   ```
   git clone https://github.com/fs0ci3ty/MispM2SSIContribution.git
   ```

3. Go to the directory "MispM2SSIContribution":
   ```
   cd MispM2SSIContribution/Misp_contribution/
   ```

4. Install required Python modules:
   ```
   pip install -r requirements.txt
   ```

5. Generate the cluster by running `data_protection_cluster_automation.py`:
   ```
   python3 data_protection_cluster_automation.py
   ```

6. Check the directory data to find the file "data_protection_cluster.json".
   Note: Each time you launch the program, the file is renewed.
```