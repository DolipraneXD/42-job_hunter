# import required modules
import os
import sys
import pandas as pd
import json

def load_offers(file_path):
	ext = os.path.splitext(file_path)[1]
	if ext == ".csv":
		return pd.read_csv(file_path)
	elif ext == ".json":
		with open(file_path, 'r', encoding='utf-8') as f:
			return pd.DataFrame(json.load(f))
	else:
		raise ValueError("Unsupported file type: " + ext)

def filter_offers(df, offer_type=None, country=None, tech_stack=None):
	if offer_type:
		df = df[df['contract_type'].str.lower().str.contains(offer_type.lower())]
	if country:
		df = df[df['full_address'].str.lower().str.contains(country.lower())]
	if tech_stack:
		tech_stack_lower = tech_stack.lower()
		df = df[df.apply(lambda row: tech_stack_lower in str(row.get('big_description', '')).lower() or tech_stack_lower in str(row.get('title', '')).lower(), axis=1)]
	return df

def to_markdown(df):
	md = "# Filtered Offers\n\n"
	for idx, row in df.iterrows():
		md += f"---\n\n"
		md += f"## Offer {idx+1}: {row['title']}\n\n"
		md += f"**Short Description:**\n{row['little_description']}\n\n"
		md += f"**Full Details:**\n{row['big_description']}\n\n"
		md += f"**Salary:** {row['salary']}\n"
		md += f"**Contract Type:** {row['contract_type']}\n"
		md += f"**Location:** {row['full_address']}\n"
		md += f"**Duration:** {row['min_duration']} - {row['max_duration']} months\n"
		md += f"**Contact Email:** {row['email']}\n"
		md += f"**Offer Link:** {row.get('slug', '')}\n\n"
	md += "---\n"
	return md

def main():
	if len(sys.argv) < 2:
		print("Usage: python filter.py <offers_file> [--type TYPE] [--country COUNTRY] [--tech TECH]")
		sys.exit(1)
	offers_file = sys.argv[1]
	offer_type = None
	country = None
	tech_stack = None
	for i, arg in enumerate(sys.argv):
		if arg == '--type' and i+1 < len(sys.argv):
			offer_type = sys.argv[i+1]
		if arg == '--country' and i+1 < len(sys.argv):
			country = sys.argv[i+1]
		if arg == '--tech' and i+1 < len(sys.argv):
			tech_stack = sys.argv[i+1]
	df = load_offers(offers_file)
	filtered = filter_offers(df, offer_type, country, tech_stack)
	md = to_markdown(filtered)
	with open(os.path.join(os.path.dirname(offers_file), 'offer.md'), 'w', encoding='utf-8') as f:
		f.write(md)
	print(f"Written {len(filtered)} offers to offer.md")

if __name__ == '__main__':
	main()
