# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class CarbonCreditsRequest(BaseModel):
    data: str  # Example input data if your Python script needs any input

@app.post("/run-script/")
def run_script(request: CarbonCreditsRequest):
    try:
        # Run the script and capture the output
        result = subprocess.run(
            ["python", "tonyalgo.py"], capture_output=True, text=True
        )
        if result.returncode != 0:
            return {"error": result.stderr}

        return {"output": result.stdout}
    except Exception as e:
        return {"error": str(e)}
