from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)
app = FastAPI()
MAIN_MODEL_SERVER_BASE_URL=os.getenv("MAIN_MODEL_SERVER_BASE_URL")



main_model_server_base_url = MAIN_MODEL_SERVER_BASE_URL

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/classify")
async def classify(request: Request):
    try:
        # Accept any JSON body
        data = await request.json()
        response = requests.post(f"{main_model_server_base_url}/classify", json=data)
        json_response = response.json()
        json_response["reasoning"] ="" 
        return json_response

        # testing perpose hard coded data
        # {
        #     "success": true,
        #     "probability": 75,
        #     "classification": "Warm",
        #     "reasoning": "The email clearly identifies a healthcare clinic in Sri Lanka (80 staff), aligning with Test1's target industry. The request for procurement and reporting tools indicates a need for the ERP system. While not explicitly stating a budget or pain points, the size of the clinic and location are positive indicators. The sender's title (Admin) suggests a decision-maker is involved.  A 'Warm' classification is appropriate as the fit is strong, but further qualification is needed to assess budget and specific requirements.",
        #     "error": null
        # }
        # return {
        #     "success": True,
        #     "probability": 75,
        #     "classification": "Warm",
        #     "reasoning": "The email clearly identifies a healthcare clinic in Sri Lanka (80 staff), aligning with Test1's target industry. The request for procurement and reporting tools indicates a need for the ERP system. While not explicitly stating a budget or pain points, the size of the clinic and location are positive indicators. The sender's title (Admin) suggests a decision-maker is involved.  A 'Warm' classification is appropriate as the fit is strong, but further qualification is needed to assess budget and specific requirements.",
        #     "error": None
        # }
    except Exception as e:
        print("error ------", e)
        return {
            "status": "error",
            "message": "something went wrong"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fast_server:app", host="0.0.0.0", port=4111, reload=True)