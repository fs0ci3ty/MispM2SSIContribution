# GDPR Data Transfer Compliance Galaxy

**Author**: fs0ci3ty & pages497

**Teachers**: Mr. Alexandre DULAUNOY [@adulau](https://github.com/adulau) & Mr. Christian STUDER [@chrisr3d](https://github.com/chrisr3d)

## Context
This project focuses on cybersecurity and data protection, specifically international data transfer under GDPR. It aims to provide a MISP galaxy for visual analysis of countries' data transfer capabilities in compliance with GDPR regulations.

## Galaxy Purpose
The repository maintains a MISP galaxy that visualizes GDPR-compliant data transfer capabilities. It includes:
- Data structured into a MISP-compatible galaxy and clusters.
- Descriptions of data protection levels within each country's cluster.

## YARA Rule for AIL
Additionally, the project offers a YARA rule for the AIL framework to detect Telegram API keys, contributing to cybersecurity monitoring. The regex used is based on a [specific format](https://stackoverflow.com/a/61888374).

## Methodology
- Automated scripts fetch and parse data from CNIL, ensuring current information on countries' data protection levels.
- Data is cleaned and structured for MISP galaxy integration.
- The YARA rule is tailored to detect Telegram API keys, enhancing cybersecurity efforts.

For setup, usage, and contribution details, please refer to the subsequent sections.

## How to use

1. Install python3 :
   On Debian : 
    ```
        sudo apt update
        sudo apt install python3
    ```
   Or : 
   Download from : ```https://www.python.org/downloads/```


2. Clone the project :
   ```
      git clone https://github.com/fs0ci3ty/MispM2SSIContribution.git
   ```
   
3. Go to the directory : "MispM2SSIContribution" :
   ```
      cd MispM2SSIContribution/
   ```
   
4. Install python modules :
   ```
      pip install --upgrade requests
      pip install --upgrade re
      pip install --upgrade json
      pip install --upgrade uuid
      pip install --upgrade tldextract
   ```
   
5. Run pyhtonDataProtection.py :
   ```
      python3 .\pyhtonDataProtection.py
   ```
   
6. Check the directory data in order to find the file : "data_protection_cluster.json"`.
   Be careful each time you launch the program, the file is renewed