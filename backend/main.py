from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

import requests

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)

NASA_API_KEY = "FXZ8qsbEB8AfVyOmUpveQ1UYklrTZGYbN42YZb0e"
cache = {}

def parse_asteroids(near_earth_objects):
	result = []
	for date in near_earth_objects.keys():
		for asteroid in near_earth_objects[date]:
			clean_asteroid = {
				"id": asteroid["id"],
				"name": asteroid["name"],
				"nasa_jpl_url": asteroid["nasa_jpl_url"],
				"absolute_magnitude_h": asteroid["absolute_magnitude_h"],
				"is_dangerous": asteroid["is_potentially_hazardous_asteroid"],
				"is_sentry_object": asteroid["is_sentry_object"],
				"close_approach_date": date,
				"diameter_min_km": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
				"diameter_max_km": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
				"close_approach_date_full": asteroid["close_approach_data"][0]["close_approach_date_full"],
				"velocity_kmh": asteroid["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"],
				"miss_distance_km": asteroid["close_approach_data"][0]["miss_distance"]["kilometers"],
				"miss_distance_lunar": asteroid["close_approach_data"][0]["miss_distance"]["lunar"],
			}
			result.append(clean_asteroid)
	return result

@app.get("/asteroids")
def get_asteroids(start_date: str, end_date: str):
	cache_key = f"{start_date}_{end_date}"
	
	if cache_key in cache:
		return cache[cache_key]
	
	asteroids = fetch_asteroids_range(start_date, end_date)
	cache[cache_key] = asteroids
	return asteroids

def fetch_asteroids_range(start_date: str, end_date: str):
	start = datetime.strptime(start_date, "%Y-%m-%d")
	end = datetime.strptime(end_date, "%Y-%m-%d")
	
	all_asteroids = []
	current_start = start

	while current_start < end:
		current_end = current_start + timedelta(days=7)
		
		if current_end > end:
			current_end = end

		url = "https://api.nasa.gov/neo/rest/v1/feed"
		params = {
			"start_date": current_start.strftime("%Y-%m-%d"),
			"end_date": current_end.strftime("%Y-%m-%d"),
			"api_key": NASA_API_KEY
		}

		response = requests.get(url, params=params)
		data = response.json()

		chunk = parse_asteroids(data["near_earth_objects"])
		all_asteroids.extend(chunk)

		current_start = current_end + timedelta(days=1)
	
	return all_asteroids