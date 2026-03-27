from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib

app = FastAPI()

# 1. Load the new, smarter model
model = joblib.load('advanced_bot_model.pkl')

# 2. Update the Expected Data Structure
class BotStats(BaseModel):
    bot_name: str
    kinetic_energy: int
    armor: int
    ground_clearance: int
    drive_agility: int

@app.post("/predict_survival")
def predict_survival(stats: BotStats):
    # Pass all 4 features into the model in the exact order they were trained
    prediction = model.predict([[
        stats.kinetic_energy, 
        stats.armor, 
        stats.ground_clearance, 
        stats.drive_agility
    ]])
    
    outcome = "Survives & Dominates" if prediction[0] == 1 else "Destroyed in the Arena"
    return {"robot": stats.bot_name, "prediction": outcome}

@app.get("/", response_class=HTMLResponse)
def get_webpage():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pro Combat Robot Predictor</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1a1a1d; color: #fff; display: flex; justify-content: center; padding-top: 40px; }
            .card { background: #2d2d30; padding: 25px 35px; border-radius: 10px; box-shadow: 0 8px 16px rgba(0,0,0,0.5); width: 320px; border: 1px solid #444; }
            h2 { text-align: center; color: #e63946; margin-bottom: 20px; }
            label { font-size: 0.9em; color: #aaa; margin-top: 10px; display: block; }
            input { width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 15px; border: 1px solid #555; border-radius: 5px; background: #1e1e1e; color: #fff; box-sizing: border-box; }
            button { width: 100%; padding: 12px; background-color: #e63946; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; text-transform: uppercase; letter-spacing: 1px; }
            button:hover { background-color: #d62828; }
            #result { margin-top: 20px; font-weight: bold; text-align: center; padding: 12px; border-radius: 5px; display: none; }
            .survives { background-color: #2b9348; color: #fff; box-shadow: 0 0 10px #2b9348; }
            .destroyed { background-color: #9a031e; color: #fff; box-shadow: 0 0 10px #9a031e; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Pro Arena Predictor</h2>
            <form id="botForm">
                <label>Robot Name</label>
                <input type="text" id="botName" value="Angad" required>
                
                <label>Kinetic Energy Weapon (1-10)</label>
                <input type="number" id="weapon" value="8" min="1" max="10" required>
                
                <label>Armor Thickness (1-10)</label>
                <input type="number" id="armor" value="6" min="1" max="10" required>

                <label>Ground Clearance (1 = Scraping, 10 = High)</label>
                <input type="number" id="clearance" value="2" min="1" max="10" required>

                <label>Drive Agility (1-10)</label>
                <input type="number" id="drive" value="9" min="1" max="10" required>

                <button type="submit">Run Simulation</button>
            </form>
            <div id="result"></div>
        </div>

        <script>
            document.getElementById('botForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const payload = {
                    bot_name: document.getElementById('botName').value,
                    kinetic_energy: parseInt(document.getElementById('weapon').value),
                    armor: parseInt(document.getElementById('armor').value),
                    ground_clearance: parseInt(document.getElementById('clearance').value),
                    drive_agility: parseInt(document.getElementById('drive').value)
                };

                const response = await fetch('/predict_survival', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = `${data.robot}: <strong>${data.prediction}</strong>`;
                resultDiv.className = data.prediction === "Survives & Dominates" ? 'survives' : 'destroyed';
            });
        </script>
    </body>
    </html>
    """
    return html_content