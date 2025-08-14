#!/usr/bin/env python3
import csv
import logging
import re
import sys
import time
from argparse import ArgumentParser
from datetime import datetime
from typing import List, Optional, Tuple
from urllib.parse import urlparse

import requests

# Install deps: pip install requests

DEFAULT_URLS = [
    "https://www.congress.gov/bill/115th-congress/house-bill/4829",
    "https://www.congress.gov/bill/115th-congress/senate-bill/3502",
    "https://www.congress.gov/bill/116th-congress/house-bill/2575",
    "https://www.congress.gov/bill/116th-congress/senate-bill/1363",
    "https://www.congress.gov/bill/116th-congress/house-bill/7096",
    "https://www.congress.gov/bill/116th-congress/house-bill/827",
    "https://www.congress.gov/bill/116th-congress/senate-bill/1558",
    "https://www.congress.gov/bill/116th-congress/house-resolution/153",
    "https://www.congress.gov/bill/116th-congress/senate-bill/3901",
    "https://www.congress.gov/bill/116th-congress/senate-bill/3890",
    "https://www.congress.gov/bill/116th-congress/house-bill/7339",
    "https://www.congress.gov/bill/116th-congress/house-bill/8183",
    "https://www.congress.gov/bill/116th-congress/house-bill/8128",
    "https://www.congress.gov/bill/116th-congress/senate-bill/4082",
    "https://www.congress.gov/bill/116th-congress/house-bill/7856",
    "https://www.congress.gov/amendment/116th-congress/senate-amendment/1977",
    "https://www.congress.gov/amendment/116th-congress/senate-amendment/2301",
    "https://www.congress.gov/bill/117th-congress/senate-bill/2551",
    "https://www.congress.gov/bill/117th-congress/senate-bill/1353",
    "https://www.congress.gov/bill/117th-congress/senate-bill/1257",
    "https://www.congress.gov/bill/117th-congress/house-bill/4468",
    "https://www.congress.gov/bill/117th-congress/house-bill/4469",
    "https://www.congress.gov/bill/117th-congress/house-bill/6553",
    "https://www.congress.gov/bill/117th-congress/house-bill/7811",
    "https://www.congress.gov/bill/117th-congress/house-bill/3844",
    "https://www.congress.gov/bill/117th-congress/house-bill/3723",
    "https://www.congress.gov/bill/117th-congress/house-bill/5467",
    "https://www.congress.gov/bill/117th-congress/senate-bill/2904",
    "https://www.congress.gov/bill/117th-congress/senate-bill/1705",
    "https://www.congress.gov/bill/117th-congress/senate-bill/1260",
    "https://www.congress.gov/bill/117th-congress/house-bill/2153",
    "https://www.congress.gov/bill/117th-congress/house-bill/7683",
    "https://www.congress.gov/bill/117th-congress/senate-bill/3035",
    "https://www.congress.gov/bill/117th-congress/house-bill/7296",
    "https://www.congress.gov/bill/117th-congress/house-bill/7776",
    "https://www.congress.gov/bill/117th-congress/senate-bill/5351",
    "https://www.congress.gov/bill/118th-congress/senate-bill/1356",
    "https://www.congress.gov/bill/118th-congress/senate-bill/2770",
    "https://www.congress.gov/bill/118th-congress/house-bill/4223",
    "https://www.congress.gov/bill/118th-congress/senate-bill/1564",
    "https://www.congress.gov/bill/118th-congress/senate-bill/1596",
    "https://www.congress.gov/bill/118th-congress/house-bill/3044",
    "https://www.congress.gov/bill/118th-congress/house-bill/7694",
    "https://www.congress.gov/bill/118th-congress/house-bill/1718",
    "https://www.congress.gov/bill/118th-congress/house-bill/3369",
    "https://www.congress.gov/bill/118th-congress/senate-bill/1626",
    "https://www.congress.gov/bill/118th-congress/senate-bill/2691",
    "https://www.congress.gov/bill/118th-congress/senate-bill/2765",
    "https://www.congress.gov/bill/118th-congress/house-bill/9403",
    "https://www.congress.gov/bill/118th-congress/house-bill/8384",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4394",
    "https://www.congress.gov/bill/118th-congress/house-bill/4503",
    "https://www.congress.gov/bill/118th-congress/house-resolution/66",
    "https://www.congress.gov/bill/118th-congress/senate-bill/2293",
    "https://www.congress.gov/bill/118th-congress/house-resolution/649",
    "https://www.congress.gov/bill/118th-congress/house-bill/9309",
    "https://www.congress.gov/bill/118th-congress/senate-bill/3205",
    "https://www.congress.gov/bill/118th-congress/senate-bill/2714",
    "https://www.congress.gov/bill/118th-congress/house-bill/6881",
    "https://www.congress.gov/bill/118th-congress/house-bill/8348",
    "https://www.congress.gov/bill/118th-congress/house-bill/8353",
    "https://www.congress.gov/bill/118th-congress/house-bill/7381",
    "https://www.congress.gov/bill/118th-congress/house-bill/4814",
    "https://www.congress.gov/bill/118th-congress/house-bill/4683",
    "https://www.congress.gov/bill/118th-congress/house-bill/206",
    "https://www.congress.gov/bill/118th-congress/house-bill/6791",
    "https://www.congress.gov/bill/118th-congress/house-bill/5808",
    "https://www.congress.gov/bill/118th-congress/senate-bill/3478",
    "https://www.congress.gov/bill/118th-congress/senate-bill/2597",
    "https://www.congress.gov/bill/118th-congress/house-bill/7781",
    "https://www.congress.gov/bill/118th-congress/house-bill/6088",
    "https://www.congress.gov/bill/118th-congress/house-bill/6466",
    "https://www.congress.gov/bill/118th-congress/house-bill/7913",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4664",
    "https://www.congress.gov/bill/118th-congress/house-bill/9211",
    "https://www.congress.gov/bill/118th-congress/house-bill/9402",
    "https://www.congress.gov/bill/118th-congress/house-bill/10262",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4951",
    "https://www.congress.gov/bill/118th-congress/house-bill/9475",
    "https://www.congress.gov/bill/118th-congress/house-bill/6943",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4236",
    "https://www.congress.gov/bill/118th-congress/senate-bill/5436",
    "https://www.congress.gov/bill/118th-congress/senate-bill/3897",
    "https://www.congress.gov/bill/118th-congress/house-bill/7532",
    "https://www.congress.gov/bill/118th-congress/house-bill/9639",
    "https://www.congress.gov/bill/118th-congress/house-bill/9042",
    "https://www.congress.gov/bill/118th-congress/senate-bill/3875",
    "https://www.congress.gov/bill/118th-congress/house-bill/10125",
    "https://www.congress.gov/bill/118th-congress/house-bill/5077",
    "https://www.congress.gov/bill/118th-congress/house-bill/8756",
    "https://www.congress.gov/bill/118th-congress/house-bill/9737",
    "https://www.congress.gov/bill/118th-congress/house-bill/3831",
    "https://www.congress.gov/bill/118th-congress/house-bill/8858",
    "https://www.congress.gov/bill/118th-congress/house-bill/8668",
    "https://www.congress.gov/bill/118th-congress/senate-bill/5539",
    "https://www.congress.gov/bill/118th-congress/house-bill/9497",
    "https://www.congress.gov/bill/118th-congress/house-bill/9466",
    "https://www.congress.gov/bill/118th-congress/house-bill/10263",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4896",
    "https://www.congress.gov/bill/118th-congress/senate-bill/3162",
    "https://www.congress.gov/bill/118th-congress/house-bill/9215",
    "https://www.congress.gov/bill/118th-congress/house-bill/9720",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4495",
    "https://www.congress.gov/bill/118th-congress/senate-bill/3975",
    "https://www.congress.gov/bill/118th-congress/house-bill/9673",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4838",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4714",
    "https://www.congress.gov/bill/118th-congress/house-bill/7766",
    "https://www.congress.gov/bill/118th-congress/senate-bill/5058",
    "https://www.congress.gov/amendment/118th-congress/house-amendment/956",
    "https://www.congress.gov/bill/118th-congress/house-resolution/1600",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4596",
    "https://www.congress.gov/bill/118th-congress/senate-bill/3312",
    "https://www.congress.gov/bill/118th-congress/house-bill/8700",
    "https://www.congress.gov/bill/118th-congress/house-bill/6936",
    "https://www.congress.gov/bill/118th-congress/house-bill/9671",
    "https://www.congress.gov/bill/118th-congress/house-bill/7603",
    "https://www.congress.gov/bill/118th-congress/house-bill/10092",
    "https://www.congress.gov/bill/118th-congress/house-bill/9626",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4862",
    "https://www.congress.gov/amendment/118th-congress/house-amendment/955",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4769",
    "https://www.congress.gov/bill/118th-congress/senate-bill/4178",
    "https://www.congress.gov/bill/119th-congress/house-bill/1",
]

PartyCodeMap = {
    "D": "Democrat",
    "R": "Republican",
    "I": "Independent",
    "ID": "Independent",
    "IND": "Independent",
    "IG": "Independent",
}


def extract_bill_info_from_url(url: str) -> Tuple[str, str, str, str]:
    """Extract congress, bill_type, and bill_number from a Congress.gov URL"""
    path = urlparse(url).path
    parts = path.strip('/').split('/')
    
    if len(parts) >= 4:
        # Handle amendments (different URL structure)
        if parts[0] == "amendment":
            congress_full = parts[1]  # e.g., "116th-congress"
            amendment_type = parts[2]  # e.g., "senate-amendment"
            amendment_number = parts[3]  # e.g., "1977"
            
            # Extract congress number
            congress_match = re.search(r'(\d+)', congress_full)
            if not congress_match:
                return "", "", "", ""
            congress = congress_match.group(1)
            
            # Convert amendment type to API format
            if "senate" in amendment_type:
                api_amendment_type = "samdt"
            elif "house" in amendment_type:
                api_amendment_type = "hamdt"
            else:
                api_amendment_type = amendment_type
            
            return congress, api_amendment_type, amendment_number, ""
        
        # Handle regular bills
        congress_full = parts[1]  # e.g., "115th-congress"
        bill_type = parts[2]  # e.g., "house-bill"
        bill_number = parts[3]  # e.g., "4829"
        
        # Extract congress number (e.g., "115" from "115th-congress")
        congress_match = re.search(r'(\d+)', congress_full)
        if not congress_match:
            return "", "", "", ""
        congress = congress_match.group(1)
        
        # Convert bill type to API format
        api_bill_type = ""
        if bill_type == "house-bill":
            api_bill_type = "hr"
        elif bill_type == "senate-bill":
            api_bill_type = "s"
        elif bill_type == "house-resolution":
            api_bill_type = "hres"
        elif bill_type == "senate-resolution":
            api_bill_type = "sres"
        elif bill_type == "house-joint-resolution":
            api_bill_type = "hjres"
        elif bill_type == "senate-joint-resolution":
            api_bill_type = "sjres"
        
        return congress, api_bill_type, bill_number, ""
    
    return "", "", "", ""


def map_party(code: Optional[str]) -> Optional[str]:
    if not code:
        return None
    return PartyCodeMap.get(code.upper())


def chamber_from_bill_type(bill_type: str) -> str:
    """Extract chamber from bill type"""
    if bill_type in ["hr", "hres", "hjres", "hamdt"]:
        return "House"
    elif bill_type in ["s", "sres", "sjres", "samdt"]:
        return "Senate"
    return ""


def parse_date_to_month(date_str: str) -> str:
    """Convert date string to month name"""
    try:
        # Handle various date formats
        for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S"]:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%B")
            except ValueError:
                continue
    except:
        pass
    return ""


def fetch_bill_data(api_key: str, congress: str, bill_type: str, bill_number: str) -> Optional[dict]:
    """Fetch bill data from Congress.gov API"""
    base_url = "https://api.congress.gov/v3"
    
    # Handle amendments
    if bill_type in ["samdt", "hamdt"]:
        url = f"{base_url}/amendment/{congress}/{bill_type}/{bill_number}"
    else:
        url = f"{base_url}/bill/{congress}/{bill_type}/{bill_number}"
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            logging.warning(f"API request failed for {url}: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error fetching data for {url}: {e}")
        return None


def fetch_cosponsors_data(api_key: str, congress: str, bill_type: str, bill_number: str) -> Optional[dict]:
    """Fetch cosponsors data from Congress.gov API"""
    base_url = "https://api.congress.gov/v3"
    
    # Amendments don't have cosponsors in the same way bills do
    if bill_type in ["samdt", "hamdt"]:
        return None
    
    url = f"{base_url}/bill/{congress}/{bill_type}/{bill_number}/cosponsors"
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            logging.warning(f"API request failed for cosponsors {url}: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error fetching cosponsors data for {url}: {e}")
        return None


def process_bill_data(api_key: str, url: str) -> dict:
    """Process a single bill and extract required information"""
    row = {
        "URL": url,
        "Chamber": "",
        "Sponsor Party": "",
        "Bipartisan?": "",
        "Introduced Month": "",
        "Number of Sponsors": "",
    }
    
    try:
        # Extract bill information from URL
        congress, bill_type, bill_number, amendment_info = extract_bill_info_from_url(url)
        if not congress or not bill_type or not bill_number:
            logging.error(f"Could not parse URL: {url}")
            return row
        
        # Fetch bill data
        bill_data = fetch_bill_data(api_key, congress, bill_type, bill_number)
        if not bill_data:
            return row
        
        # Extract chamber
        chamber = chamber_from_bill_type(bill_type)
        
        # Extract sponsor party
        sponsor_party = ""
        if "bill" in bill_data:
            bill_info = bill_data["bill"]
            if "sponsors" in bill_info and bill_info["sponsors"]:
                sponsor = bill_info["sponsors"][0]
                if "party" in sponsor:
                    sponsor_party = map_party(sponsor["party"]) or ""
        elif "amendment" in bill_data:
            # Amendments have different structure
            amendment_info = bill_data["amendment"]
            if "sponsor" in amendment_info:
                sponsor = amendment_info["sponsor"]
                if "party" in sponsor:
                    sponsor_party = map_party(sponsor["party"]) or ""
        
        # Extract introduced month
        introduced_month = ""
        if "bill" in bill_data:
            bill_info = bill_data["bill"]
            if "introducedDate" in bill_info:
                introduced_month = parse_date_to_month(bill_info["introducedDate"])
        elif "amendment" in bill_data:
            # Amendments have different date structure
            amendment_info = bill_data["amendment"]
            if "updateDate" in amendment_info:
                introduced_month = parse_date_to_month(amendment_info["updateDate"])
        
        # Fetch cosponsors data
        cosponsors_data = fetch_cosponsors_data(api_key, congress, bill_type, bill_number)
        
        # Count sponsors and determine bipartisan status
        party_set = set()
        total_sponsors = 0
        
        # Add sponsor
        if sponsor_party:
            party_set.add(sponsor_party)
            total_sponsors += 1
        
        # Add cosponsors
        if cosponsors_data and "cosponsors" in cosponsors_data:
            cosponsors = cosponsors_data["cosponsors"]
            total_sponsors += len(cosponsors)
            
            for cosponsor in cosponsors:
                if "party" in cosponsor:
                    party = map_party(cosponsor["party"])
                    if party:
                        party_set.add(party)
        
        bipartisan = "True" if len(party_set) > 1 else "False"
        
        row.update({
            "Chamber": chamber,
            "Sponsor Party": sponsor_party,
            "Bipartisan?": bipartisan,
            "Introduced Month": introduced_month,
            "Number of Sponsors": str(total_sponsors),
        })
        
    except Exception as e:
        logging.exception(f"Error processing {url}: {e}")
    
    return row


def run(api_key: str, urls: List[str], out_csv: str) -> None:
    """Run the scraper with the provided API key"""
    results = []
    
    for i, url in enumerate(urls):
        logging.info(f"Processing {i + 1}/{len(urls)}: {url}")
        result = process_bill_data(api_key, url)
        results.append(result)
        
        # Add a small delay between requests to be respectful
        if i < len(urls) - 1:
            time.sleep(0.5)
    
    # Write results to CSV
    fieldnames = ["URL", "Chamber", "Sponsor Party", "Bipartisan?", "Introduced Month", "Number of Sponsors"]
    writer = csv.DictWriter(
        sys.stdout if out_csv == "-" else open(out_csv, "w", newline="", encoding="utf-8"), 
        fieldnames=fieldnames
    )
    writer.writeheader()
    for row in results:
        writer.writerow(row)


def main() -> None:
    parser = ArgumentParser(description="Scrape Congress.gov bills using the API for chamber, sponsor party, bipartisan, introduced month, and sponsor count.")
    parser.add_argument("--api-key", "-k", required=True, help="Congress.gov API key")
    parser.add_argument("--input", "-i", help="Path to a text file with one Congress.gov URL per line. If omitted, uses built-in list.", default=None)
    parser.add_argument("--output", "-o", help="Output CSV path (use '-' for stdout). Default: '-'", default="-")
    parser.add_argument("--log", help="Log level (DEBUG, INFO, WARNING, ERROR)", default="WARNING")
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log.upper(), logging.WARNING), format="%(levelname)s: %(message)s")

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
    else:
        urls = DEFAULT_URLS

    # Basic validation of URLs
    urls = [u for u in urls if u.startswith("https://www.congress.gov/")]
    if not urls:
        logging.error("No valid Congress.gov URLs provided.")
        sys.exit(1)

    run(args.api_key, urls, args.output)


if __name__ == "__main__":
    main()
