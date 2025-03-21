from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import io
from pandas import read_csv
import cred

# Fetching the api credentials and connecting to the Azure's Document Analysis Client API
endpoint = cred.api_endpoint
api_key = cred.api_key
client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

# Reading the metric values from the csv template to display only the necessary values
analysis_data = read_csv("medical_data_test.csv")
metric_list = analysis_data['Metrics'].to_list()

# Creating the FastAPI instance and setting up the templates to display the UI
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

# The GET function to direct the user to the base html page to upload the PDF for analysis
@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# POST function to upload the PDF to the Azure API for processing
@app.post("/analyze-pdf/")
async def analyze_pdf(file: UploadFile = File(...)):

    file_content = await file.read()
    analysis_res = []

    # poller variable fetches the result from the analysis using the "prebuilt model" used
    poller = client.begin_analyze_document('prebuilt-document', io.BytesIO(file_content))
    result = poller.result()

    # Displaying the key-value part to the user and storing in a list for further use
    print("----Key-value pairs found in document----")
    for kv_pair in result.key_value_pairs:
        if kv_pair.key and kv_pair.value:
            if kv_pair.key.content in metric_list: # Checking if the metric key from the template is present in the processed PDF
                analysis_res.append({"key": kv_pair.key.content, "value": kv_pair.value.content})
        else:
            if kv_pair.key.content in metric_list:
                analysis_res.append({"key": kv_pair.key.content, "value": ""})

    print("----------------------------------------")
    print(analysis_res)

    # Returing the JSON response back to the HTML page for display
    return JSONResponse(content={"kv_pairs": analysis_res})