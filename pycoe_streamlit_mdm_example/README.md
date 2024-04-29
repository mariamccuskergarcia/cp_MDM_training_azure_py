
# MDM Training Tool

This tool is designed for training consultants in the basic's of master data management - namely learning how to match and merge different datasets to create master records.

In addition, it is also designed to be a real-life example of what a well set up and documented python project should look like.

## How to use this repo

1. Clone the repo
2. Install poetry and install dependencies
```
poetry install
```
3. Run the app locally:
```
poetry run streamlit run app.py
```

#### Always make a working branch before making any changes to the code. NEVER MERGE DIRECTLY TO THE MAIN.

## How to run locally

1. Create a virtual environent in the root of the folder: 
```
python -m venv .venv
```

2. Create a requirements.txt file for all the packages required (Already created, no need to create again):

- poetry >= 1.8.0
- streamlit >= 1.31.1
- pandas == 2.2.1
- faker == 24.0.0
- numpy == 1.26.4
- recordlinkage == 0.16
- timedelta == 2020.12.3

3. Activate virtual environment:
```
source .venv/Scripts/activate Bash
```

4. Install all the necessary requirments on virtual environment:
```
python -m  pip install -r requirements.txt
```

5. Run the the app locally: 
- To run on Powershell, first set execution policy to bypass and activate the virtual environment and then run the app using the following commands:
  ```
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

  .venv\Scripts\activate

  python -m poetry run streamlit run '.\MDM Tool Intro.py'
  ```
- To run on Bash, ensure the virtual environment is activated and run the following command:
  ```
  python -m poetry run streamlit run MDM\ Tool\ Intro.py 
  ```
  If that does not work try:
  ```
  python -m streamlit run MDM\ Tool\ Intro.py 
  ```

6. Access the interactive webpage through the localhost.

## How to test CI locally

1. Ensure that there is a test folder which contains a CI folder holding all the tests in python code. Also ensure that there is a requirements.txt for both the CI and UX which contains packages required in order to run the tests locally. 

2. Activate the virtual environment again and cd into the CI folder, and run the tests by simultaneously installing the requirements.txt and running the tests using the commands below:
```
cd tests/ci/

python -m pip install -r requirements.txt && pytest
```

## How to test UX locally

1. Ensure that there is a test folder which contains a UX folder holding all the selenium tests in python code. Also ensure that there is a requirements.txt for both the CI and UX which contains packages required in order to run the tests locally. 
   
2. Open two Bash terminals and activate the virtual environment again in both terminals ensuring that you are in the root of the folder. 
```
source .venv/Scripts/activate
```

3. On one terminal, continuously run the app on a localhost matching the localhost server in the test_selenium.py. This will need to be run continuopusly to allow the UX tests to run.
```
python -m poetry run streamlit run MDM\ Tool\ Intro.py 
```
   
4. In the other terminal, direct into the UX folder, and run the tests by installing the requirements.txt and running the tests simultaneously using the commands below:
```
cd tests/ux/

python -m pip install -r requirements.txt && pytest
```
5. After the test has successfully completed, there will be web captures of each page in the UX folder of the explorer and use the ctrl C function of the keyboard to terminate the server. 

