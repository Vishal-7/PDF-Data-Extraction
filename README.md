This project is a demonstration of how we can utilize Azure's Document Client Analysis API to fetch the key-value pairs. This includes a FastAPI code, that interacts with the Azure API and fetches the necessary key-value pairs from the PDF being uploaded by the user.

**Procedure to run**:
1.  Pull the code to the local.
2.  On the `medical_data_test.csv` file, put in the necessary metric values that need to be fetched from the PDF. This will act as the template from which only the necessary       values be picked up from the output from the Azure API.
3.  Create a virtual environment and install the following packages [azure-ai-formrecognizer, fastapi, uvicorn, pandas]. Or the you can try using the venv that is present in       the code repository. This contains all the necessary packages need for the code to run as expected.
4.  In the main directory on your local, open the terminal and type `uvicorn <<file_name>>:<<instance_name>> --reload`. In our case, we can type `uvicorn api_file:app --reload`.
5.  This runs our application on the local port. The terminal will prompt you the link to the local port, which you can click on to visit the page.
6.  After reaching the homepage, click on the browser button and pick the necessary PDF. Also, note that the application does not allow you to pick any file with an extension      other than PDF.
7.  Click on "Upload" button. This takes the file as input and is processed by the Azure API and the result is returned to our application in the form of a JSON block.
8.  The needed metric values are being displayed as a table on the HTML page to the user.

**Testing on Postman/Insomnia**:
1.  Run the extraction code on your local using the command `uvicorn api_file:app --host 0.0.0.0 --port 8000 --reload`. This will ensure that anyone on the same network using a different computer can test out the same on postman.
2.  Open postman/insomnia and create a new request.
3.  Choose post request and set the bodt to `form-data`. Set the key as `file` and pick the type of value as `file`. This will allow you to browse the file from your local computer. Set the url to "https://<<localhost>>:8000/analyse-pdf/"
4.  Once the value is set, click on the send button. This will yield the JSON value to the user on the response section.
