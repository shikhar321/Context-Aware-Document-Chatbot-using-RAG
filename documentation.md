### .venv file to separate requirement from global python (only first time before starting project)

python -m venv .venv
.\.venv\Scripts\Activate.ps1

### rq.txt file contains all the libraries needed to run the project
# We can install all the libraries in one go
# Install libraries from text file
pip install -r requirements.txt

# If working with python notebook ipynb file, make sure kernel is set to .venv interpreter
# choose this by clicking on right corner

# To run streamlit application command

streamlit run .\main.py

# To cancel current cmd
ctrl+c

# To run python rfrom terminal 
python main.py

# How to use Gemini inside VS Code (2 Methods)

# Method 1 
1. Press ctrl + I
2. prompt - "/Debug this code"

# Method 2
1. add a comment - // Function to create a Cloud Storage bucket.
2. Press Ctrl+Enter
3. Press Tab to accept

# Upgrading PIP
python.exe -m pip install --upgrade pip

## To call API through postman (2 Methods)
# Method 1 (Requires installing Postman)
1. Select API router code and open gemini code assist
or give 3 inputs - function name, method, input manually to chatgpt 
2. Prompt - "Give curl command"
3. click on + (create new request) and paste the curl command
4. Click on send and the request ouput will be displayed in postman terminal
5. Always keep curl command to call the API through postman in future in comments

# Method 2 (Requires VS Code Extension: REST Client (by Huachao Mao))
1. Create a file with extension - .http or .rest
2. Create the code by pasting 3 inputs in chatgpt
3. Paste the code in .http/.rest file and click 'send request' button
4. To run multiple JSON separate them by ###

