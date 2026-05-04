from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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