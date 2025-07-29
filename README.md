# Publication Map

A comprehensive tool for analyzing academic publications and creating geographic visualizations of research collaboration patterns. This system crawls Google Scholar citations, extracts author affiliations from journal articles, and generates country-based publication statistics.

## Overview

The Publication Map system consists of several interconnected Python scripts that work together to:

1. **Extract citation URLs** from Google Scholar profiles
2. **Crawl journal articles** to collect author information
3. **Extract author affiliations** from various journal platforms (ScienceDirect, Springer, MDPI, IEEE)
4. **Process and analyze** geographic data using AI
5. **Generate statistics** for publication mapping

## Prerequisites

Before using this system, ensure you have the following installed:

- **Python 3.7+**
- **Chrome WebDriver** (for Selenium automation)
- **Required Python packages** (see Installation section)

### Required Python Packages

```bash
pip install selenium
pip install beautifulsoup4
pip install requests
pip install fake-useragent
pip install google-generativeai
pip install python-dotenv
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd publication-map
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```
   API_KEY=your_gemini_api_key_here
   ```

4. **Download Chrome WebDriver:**
   - Download ChromeDriver from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)
   - Ensure it's in your system PATH or in the same directory as the scripts

## Usage Guide

### Step 1: Generate Google Scholar Citation URLs

**File:** `googleUrlGetter.py`

This script extracts citation URLs from Google Scholar profiles.

```bash
python googleUrlGetter.py
```

**What it does:**
- Fetches citation URLs from specified Google Scholar profiles
- Saves URLs to `files/google-scholar-pages.txt`
- Uses rotating user agents to avoid detection

**Configuration:**
- Modify the `prof_urls` list in the script to target different Google Scholar profiles
- Adjust the `alternate_headers` list to use different user agents

### Step 2: Extract Journal URLs from Citations

**File:** `journalUrlGetter.py`

This script crawls through citation pages to extract journal article URLs.

```bash
python journalUrlGetter.py
```

**What it does:**
- Reads citation URLs from `files/google-scholar-pages.txt`
- Visits each citation page and extracts journal article links
- Saves journal URLs to individual files in `files/citations/`
- Handles pagination automatically
- Includes captcha detection and handling

**Features:**
- Automatic pagination through all citation results
- Captcha detection and waiting
- Progress tracking with batch processing
- Error handling for failed requests

### Step 3: Extract Author Information from Journals

**File:** `journalCrawler.py`

This script extracts author affiliations from journal articles.

```bash
python journalCrawler.py
```

**What it does:**
- Reads journal URLs from `files/citations/`
- Visits each journal article and extracts author information
- Supports multiple journal platforms:
  - **ScienceDirect** (`sciencedirect.com`)
  - **Springer** (`link.springer.com`)
  - **MDPI** (`mdpi.com`)
  - **IEEE** (`ieee.org`)
- Saves author data to `files/author_data.csv`

**Output Format:**
```csv
Journal Url,Corresponding Journal Id,Authors,Locations
https://example.com/article,12345,"Author Name","Affiliation, Country"
```

**Supported Platforms:**
- **ScienceDirect:** Extracts author names and affiliations from popup modals
- **Springer:** Handles author popup windows and affiliation data
- **MDPI:** Processes author spans and affiliation divs
- **IEEE:** Extracts author information from IEEE article pages

### Step 4: Process Geographic Data with AI

**File:** `countryCounter.py`

This script uses Google Gemini AI to analyze affiliations and extract country information.

```bash
python countryCounter.py
```

**What it does:**
- Reads author affiliations from `files/author_data.csv`
- Uses Google Gemini AI to:
  - Identify countries from affiliation strings
  - Handle inconsistent formatting (abbreviations, full names, inferred locations)
  - Count publications per country
- Saves results to `mapData.txt`

**AI Processing:**
- Processes affiliations in batches to avoid API limits
- Handles various affiliation formats:
  - Full country names: "United States"
  - Abbreviations: "USA"
  - Inferred locations: "MIT" → "United States"
- Outputs JSON format with country counts

### Step 5: Reformat Data for Visualization

**File:** `mapDataReformatter.py`

This script converts the AI-processed data into a clean CSV format.

```bash
python mapDataReformatter.py
```

**What it does:**
- Reads raw data from `mapData.txt`
- Aggregates country counts across all batches
- Creates a clean CSV file: `files/mapDataReformatted.csv`
- Normalizes country names and removes duplicates

**Output Format:**
```csv
Country,Count
China,1719
United States,876
India,324
...
```

## File Structure

```
publication-map/
├── README.md                 # This user manual
├── googleUrlGetter.py        # Extract Google Scholar citation URLs
├── journalUrlGetter.py       # Extract journal URLs from citations
├── journalCrawler.py         # Extract author data from journals
├── countryCounter.py         # AI-powered country analysis
├── mapDataReformatter.py     # Data formatting for visualization
├── proxy.py                  # Proxy configuration (if needed)
├── mapData.txt              # Raw AI-processed data
├── files/
│   ├── citations/           # Individual citation files
│   ├── author_data.csv      # Extracted author information
│   ├── mapDataReformatted.csv # Final formatted data
│   ├── journalCounts.txt    # Journal URL statistics
│   └── google-scholar-pages.txt # Google Scholar URLs
└── .env                     # Environment variables (create this)
```

## Configuration Options

### Google Scholar Profile URLs

Edit `googleUrlGetter.py` to target different profiles:

```python
prof_urls = [
    "https://scholar.google.com/citations?user=YOUR_USER_ID&hl=en&cstart=0&pagesize=100",
    # Add more profile URLs as needed
]
```

### Batch Processing

In `countryCounter.py`, adjust batch processing:

```python
batch_size = 50  # Number of affiliations per API call
batch_start = 1  # Start from specific batch (useful for resuming)
```

### Supported Journal Platforms

The system automatically detects and handles these platforms:
- ScienceDirect (`sciencedirect.com`)
- Springer (`link.springer.com`)
- MDPI (`mdpi.com`)
- IEEE (`ieee.org`)

## Troubleshooting

### Common Issues

1. **Chrome WebDriver Errors:**
   - Ensure ChromeDriver is installed and in PATH
   - Update ChromeDriver to match your Chrome version

2. **API Rate Limiting:**
   - The system includes delays between requests
   - If you encounter rate limits, increase delays in the scripts

3. **Captcha Detection:**
   - The system includes captcha detection and waiting
   - If captchas persist, try using different user agents

4. **Missing API Key:**
   - Ensure your `.env` file contains the `API_KEY` variable
   - Verify your Google Gemini API key is valid

### Error Handling

The system includes comprehensive error handling for:
- Network timeouts
- Missing elements on web pages
- API failures
- File I/O errors
- Captcha challenges

## Output Files

### Primary Outputs

- **`files/author_data.csv`**: Complete author and affiliation data
- **`files/mapDataReformatted.csv`**: Final country statistics for mapping
- **`mapData.txt`**: Raw AI processing results

### Intermediate Files

- **`files/citations/`**: Individual citation files
- **`files/journalCounts.txt`**: Journal URL statistics
- **`files/google-scholar-pages.txt`**: Google Scholar URLs

## Data Visualization

The final output file `files/mapDataReformatted.csv` can be used with various mapping tools:

- **Tableau**: Import CSV and create geographic visualizations
- **Python libraries**: Use `folium`, `plotly`, or `matplotlib` for maps
- **Online tools**: Upload to Google My Maps, Carto, or similar platforms

## Performance Considerations

- **Processing time**: Large datasets may take several hours
- **API costs**: Google Gemini API usage incurs costs
- **Storage**: Ensure sufficient disk space for intermediate files
- **Memory**: Large CSV files may require significant RAM

## Contributing

To extend the system:

1. **Add new journal platforms**: Modify `journalCrawler.py` with new platform handlers
2. **Improve AI prompts**: Update prompts in `countryCounter.py` for better accuracy
3. **Add visualization**: Create scripts to generate maps from the final CSV data

## License

[Add your license information here]

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Ensure all prerequisites are properly installed