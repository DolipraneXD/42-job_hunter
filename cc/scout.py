#!/usr/bin/env python3
"""
Scout Scanner
==================
Author: AccioMo
Date: 11-08-2025

This script fetches job offers from the 42 API, saves them as JSON and CSV files,
and manages authentication using credentials from a .env file.
"""

import requests
import dotenv
import json
import datetime
import time
import os
import csv
import pandas

CLIENT_ID = dotenv.get_key('.env', '42_CLIENT_ID')
CLIENT_SECRET = dotenv.get_key('.env', '42_CLIENT_SECRET')

def get_current_date():
	start_date = datetime.datetime.now()
	if (start_date.day < 28):
		start_date.replace(month=start_date.month-1)
	start_date = start_date.replace(day=28)
	return f"{start_date.strftime('%Y-%m-%d')}T00:00:00.000Z"

def get_access_token():
	response = requests.post('https://api.intra.42.fr/oauth/token', {
	'grant_type': 'client_credentials',
	'client_id': CLIENT_ID,
	'client_secret': CLIENT_SECRET,
	})
	response.raise_for_status()
	return response.json()['access_token']

def get_campus_id(campus_name, access_token):
	response = requests.get(f"https://api.intra.42.fr/v2/campus?filter[name]={campus_name}", 
		headers={"Authorization": "Bearer " + access_token})
	if response.status_code == 200:
		return (response.json()[0]["id"])
	else:
		return (f"Error: {response.status_code}")

def get_user_id(username, access_token):
	response = requests.get(f"https://api.intra.42.fr/v2/users?filter[login]={username}", 
		headers={"Authorization": "Bearer " + access_token})
	if response.status_code == 200:
		return (response.json()[0]["id"])
	else:
		return (f"Error: {response.status_code}")

def write_to_file(log_path, data):
	if ('~' in log_path):
		log_path = os.path.expanduser(log_path)
	if os.path.exists(log_path):
		print("File exists")
		with open(log_path, "a") as f:
			f.write(data + "\n")
	else:
		with open(log_path, "w+") as f:
			f.write(data + "\n")

def write_to_json(log_path, data):
	if ('~' in log_path):
		log_path = os.path.expanduser(log_path)
	with open(log_path, "w+") as f:
			json.dump(data, f, indent=4)

def write_to_csv(log_path, data):
	if ('~' in log_path):
		log_path = os.path.expanduser(log_path)
	with open(log_path, "w+", encoding="utf-8") as f:
		pandas.DataFrame(data).to_csv(f, index=False, quoting=csv.QUOTE_NONNUMERIC)
		

def get_jobs(access_token):
	total_items = []
	for i in range(1, 20):
		response = requests.get(f"https://api.intra.42.fr/v2/offers?page[size]=100&page={i}", 
				headers={"Authorization": "Bearer " + access_token})
		if response.status_code == 200:
			items = response.json()
			total_items.extend(items)
			if len(items) == 0:
				print("reached the end") 
				break
			write_to_json(f"data/part-{i}.json", items)

			print(f"reached page: {i}", end='\r')
			time.sleep(0.5)
		elif response.status_code == 401:
			access_token = get_access_token()
		else:
			print(f"unexpected response: {response.status_code} : {response.text}")

	write_to_json(f"data/offers_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json", total_items)
	write_to_csv(f"data/offers_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv", total_items)

	### DELETE TEMP FILES ###
	for filename in os.listdir("data"):
		if filename.startswith("part-") and filename.endswith(".json"):
			os.remove(os.path.join("data", filename))
	##########################

if __name__ == "__main__":
	try:
		access_token = get_access_token()
		get_jobs(access_token)
	except requests.RequestException as e:
			print(f"request error occurred: {e}")
