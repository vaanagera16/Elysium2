# Seed db with reports

import json
import logging
import random
from cs50 import SQL
import requests

NUM_REPORTS = 10
WIPE_DB = True


db = SQL("sqlite:///reports.db")
f = open("doggos.json", "r")
photos = json.load(f)
f.close()
# filter photos to only include .jpg, .jpeg, and .png files
photos = list(filter(lambda photo: photo.endswith(
    (".jpg", ".jpeg", ".png")), photos))

# Generate random reports
reports = []

if WIPE_DB:
    db.execute("DELETE FROM reports")
    print("Database wiped")

for i in range(NUM_REPORTS):
    # get random photo of animal
    # fetch from https://random.dog/doggos and get a random photo (ending in .jpg, .jpeg, or .png)
    # save the photo to the reports directory

    randInt = random.randint(0, len(photos) - 1)
    # fetch https://random.dog/{photo}
    hasPhoto = False
    # 50/50 chance of adding a photo to the report
    if random.randint(0, 1) == 0:
        hasPhoto = True
        photo = requests.get("https://random.dog/" + photos[randInt])

    reports.append({
        "landmark": "Landmark " + str(i + 1),
        "exactlocation": "Exact Location " + str(i + 1),
        "notes": "Notes " + str(i + 1),
        "photo_data": photo.content if hasPhoto else None
    })
    print(
        f"Report {i + 1} generated with photo: '{hasPhoto and photos[randInt] or None}'")

# Insert reports into database
for i, report in enumerate(reports):
    db.execute("INSERT INTO reports (landmark, exactlocation, notes, photo) VALUES (:landmark, :exactlocation, :notes, :photo_data)",
               landmark=report["landmark"], exactlocation=report["exactlocation"], notes=report["notes"], photo_data=report["photo_data"])
    print(f"Inserted report {i + 1} into database")
print("Database seeded with reports")
