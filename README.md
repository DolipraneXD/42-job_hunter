# Job Hunter

A simple tool for scouting and filtering job offers.

## Structure

- `cc/scout.py`: Collects job offers and saves them to data files.
- `cc/filter.py`: Filters job offers based on criteria.
- `cc/data/`: Contains offer data in CSV, JSON, and Markdown formats.

## Usage

1. Run `scout.py` to gather offers:
   ```bash
   python3 cc/scout.py
   ```
2. Use `filter.py` to filter offers as needed.
   To use it, run:
      python3 filter.py offers_2026-02-26-15-26-56.csv --type stage --country France --tech React
   For internships: use --type stage
   For country: use --country France or --country French Polynesia
   For tech: use --tech React

## Requirements

- Python 3
- Install dependencies:
  ```bash
  pip install -r cc/requirements.txt
  ```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
42_CLIENT_ID=your_client_id
42_CLIENT_SECRET=your_client_secret
```

## Author

DolipraneXD
