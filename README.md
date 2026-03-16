# Job Hunter
This script fetches job offers from the 42 API, saves them as JSON and CSV files,
and manages authentication using credentials from a .env file.

## Structure
- `cc/scout.py`: Collects job offers and saves them to data files.
- `cc/filter.py`: Filters job offers based on criteria.
- `cc/data/`: Contains offer data in CSV, JSON, and Markdown formats.

## Requirements
- Python 3
- Install dependencies:
  ```bash
  pip install requests python-dotenv pandas
  ```
  OR
  ```bash
  pip install -r cc/requirements.txt
  ```
  OR inside a virtual environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate        # On Windows: venv\Scripts\activate
  pip install requests python-dotenv pandas
  ```

## Environment Variables
Create a `.env` file in the project root with the following variables:
```
42_CLIENT_ID=your_client_id
42_CLIENT_SECRET=your_client_secret
```

## Usage

### 1. Collect offers
Run `scout.py` to gather offers. The `data/` directory will be created automatically if it doesn't exist:
```bash
python3 cc/scout.py
```

### 2. Filter offers
Use `filter.py` to filter the collected offers by type, country, or tech stack:
```bash
python3 cc/filter.py <offers_file> [--type TYPE] [--country COUNTRY] [--tech TECH]
```

**Example:**
```bash
python3 cc/filter.py cc/data/offers_2026-02-26-15-26-56.csv --type stage --country France --tech React
```

**Options:**
| Flag | Description | Example |
|------|-------------|---------|
| `--type` | Contract type | `--type stage` for internships |
| `--country` | Country or region | `--country France`, `--country "French Polynesia"` |
| `--tech` | Tech stack keyword | `--tech React`, `--tech Python` |

The filtered results are saved as `offer.md` in the same directory as the input file.

## Authors
DolipraneXD acciomo