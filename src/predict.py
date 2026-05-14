import joblib
import pandas as pd
import os

print("\n===== AI HOUSE PRICE PREDICTOR =====\n")

# Load trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "models", "house_price_model.pkl")
model = joblib.load(model_path)

# STEP 1 — Ask Buy or Rent
print("What are you looking for?")
print("1 - Buy Property")
print("2 - Rent Property")

transaction_type = int(input("Enter option: "))


# STEP 2 — Ask house type
print("\nSelect House Type:")
print("1 - Flat")
print("2 - Studio Flat")
print("3 - PG")
print("4 - Bungalow")

house_type = int(input("Enter option: "))


# Default feature values
area = 0
bedrooms = 0
bathrooms = 0
floors = 0
parking = 0
garden = 0
sharing = 0
meal_included = 0
building_age = 0


# FLAT
if house_type == 1:
    area = float(input("Area (sq ft): "))
    bedrooms = int(input("Bedrooms: "))
    bathrooms = int(input("Bathrooms: "))
    floors = int(input("Floor number: "))
    parking = int(input("Parking spaces: "))


# STUDIO FLAT
elif house_type == 2:
    area = float(input("Area (sq ft): "))
    bathrooms = int(input("Bathrooms: "))
    floors = int(input("Floor number: "))
    building_age = int(input("Building age (years): "))


# PG
elif house_type == 3:
    area = float(input("Room area (sq ft): "))
    bathrooms = int(input("Bathrooms available: "))
    sharing = int(input("Sharing capacity (1/2/3): "))
    meal_included = int(input("Meal included? (1 Yes / 0 No): "))


# BUNGALOW
elif house_type == 4:
    area = float(input("Area (sq ft): "))
    bedrooms = int(input("Bedrooms: "))
    bathrooms = int(input("Bathrooms: "))
    floors = int(input("Floors: "))
    parking = int(input("Parking spaces: "))
    garden = int(input("Garden available? (1 Yes / 0 No): "))

else:
    print("Invalid house type selected")
    exit()


# Create dataframe with same features as training
input_data = pd.DataFrame({
    "area":[area],
    "bedrooms":[bedrooms],
    "bathrooms":[bathrooms],
    "floors":[floors],
    "parking":[parking],
    "garden":[garden],
    "sharing":[sharing],
    "meal_included":[meal_included],
    "building_age":[building_age],
    "house_type":[house_type]
})


# Predict price
prediction = model.predict(input_data)[0]


# Rent approximation
if transaction_type == 2:
    prediction = prediction * 0.005


# Output result
if transaction_type == 1:
    print("\nEstimated Property Price: ₹", round(prediction,2))
else:
    print("\nEstimated Monthly Rent: ₹", round(prediction,2))