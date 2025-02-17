import os

app_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(app_dir, "json")

provinces_file = os.path.join(data_dir, "provinces.json")
cities_file = os.path.join(data_dir, "cities.json")

print("مسیر پوشه data:", data_dir)
print("مسیر فایل provinces.json:", provinces_file)
print("مسیر فایل cities.json:", cities_file)
