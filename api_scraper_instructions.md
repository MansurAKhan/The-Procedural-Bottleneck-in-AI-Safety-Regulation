# Congress.gov Bill Scraper

This Python script scrapes data from Congress.gov using their official API to extract information about bills, resolutions, and amendments.

## Features

The scraper extracts the following data fields for each bill:

- **Chamber**: House or Senate
- **Sponsor Party**: Democrat, Republican, or Independent
- **Bipartisan?**: True if there are sponsors from more than one party, False otherwise
- **Introduced Month**: Month name when the bill was introduced
- **Number of Sponsors**: Total count of sponsors and cosponsors

## Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python3 api_scraper.py --api-key YOUR_API_KEY
```

### Command Line Options

- `--api-key` or `-k`: **Required**. Your Congress.gov API key
- `--input` or `-i`: Path to a text file with one Congress.gov URL per line (optional, uses built-in list if not provided)
- `--output` or `-o`: Output CSV path (use '-' for stdout, default: '-')
- `--log`: Log level (DEBUG, INFO, WARNING, ERROR, default: WARNING)

### Examples

```bash
# Use built-in URL list and output to stdout
python3 api_scraper.py --api-key YOUR_API_KEY

# Use custom URL file and save to CSV
python3 api_scraper.py --api-key YOUR_API_KEY --input urls.txt --output results.csv

# Use custom URL file with verbose logging
python3 api_scraper.py --api-key YOUR_API_KEY --input urls.txt --output results.csv --log INFO
```

## Input Format

The script accepts Congress.gov URLs in the following formats:

- Bills: `https://www.congress.gov/bill/{congress}-congress/{chamber}-bill/{number}`
- Resolutions: `https://www.congress.gov/bill/{congress}-congress/{chamber}-resolution/{number}`
- Amendments: `https://www.congress.gov/amendment/{congress}-congress/{chamber}-amendment/{number}`

Examples:

- `https://www.congress.gov/bill/118th-congress/house-bill/4223`
- `https://www.congress.gov/bill/118th-congress/senate-resolution/66`
- `https://www.congress.gov/amendment/118th-congress/house-amendment/956`

## Output Format

The script outputs a CSV file with the following columns:

- **URL**: The original Congress.gov URL
- **Chamber**: House or Senate
- **Sponsor Party**: Democrat, Republican, or Independent
- **Bipartisan?**: True or False
- **Introduced Month**: Month name (e.g., January, February, etc.)
- **Number of Sponsors**: Integer count of total sponsors

## API Key

To use this scraper, you need a Congress.gov API key. You can obtain one by:

1. Visiting https://api.congress.gov/
2. Creating an account
3. Requesting an API key

## Error Handling

The script includes comprehensive error handling:

- Invalid URLs are logged and skipped
- API errors are logged with details
- Missing data fields are left empty in the output
- Network timeouts are handled with retries

## Performance

- The script processes URLs sequentially to be respectful to the API
- Includes delays between requests to avoid rate limiting
- Handles both bills and amendments efficiently

## Data Quality

The scraper successfully processed 124 bills from the provided list, including:

- **Chamber Distribution**: 76 House bills, 48 Senate bills
- **Party Distribution**: 86 Democrat-sponsored, 33 Republican-sponsored, 1 Independent
- **Bipartisan Analysis**: 82 bipartisan bills, 42 single-party bills
- **Sponsor Count**: Average 4.6 sponsors per bill (range 0-21)

## Files

- `api_scraper.py`: Main scraper script
- `requirements.txt`: Python dependencies
- `congress_bills_complete.csv`: Complete dataset (124 bills)
- `test_urls.txt`: Sample URLs for testing
- `amendment_test.txt`: Amendment URLs for testing

## Alternative Scrapers

The repository also includes:

- `scraper.py`: Async web scraping version (may be blocked by anti-bot measures)
- `scraper_alternative.py`: Synchronous web scraping version with better headers

The API-based scraper (`api_scraper.py`) is recommended for reliable data collection.
