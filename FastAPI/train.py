from sklearn.ensemble import RandomForestClassifier
import joblib
import random

X = []
y = []

# Generate 500 simulated arena matches
for _ in range(500):
    # Features (1-10 scale)
    kinetic_energy = random.randint(1, 10)
    armor = random.randint(1, 10)
    ground_clearance = random.randint(1, 10) # 1 = scraping the floor, 10 = very high
    drive_agility = random.randint(1, 10)
    
    X.append([kinetic_energy, armor, ground_clearance, drive_agility])
    
    # Advanced Arena Logic:
    # Ground clearance is heavily penalized if it's high. Armor and Drive are highly rewarded.
    survival_score = (armor * 1.5) + (kinetic_energy * 1.0) + (drive_agility * 1.2) - (ground_clearance * 2.0)
    
    # Add the unpredictable chaos of a live arena (lucky hits, driving mistakes)
    survival_score += random.uniform(-4, 4)
    
    # If the combined score passes the threshold, the bot survives
    if survival_score > 12:
        y.append(1)  # Survives
    else:
        y.append(0)  # Destroyed

# Train a more powerful Random Forest model
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

# Dump the upgraded model
joblib.dump(model, 'advanced_bot_model.pkl')
print(f"Advanced model trained on {len(X)} bots and saved as 'advanced_bot_model.pkl'")