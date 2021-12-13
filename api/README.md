# POC

## Install

1. Create a Python virtualenv and activate it
2. Install pip-tools: `pip install pip-tools`
3. Install dependencies: `pip-sync`


## Run

1. Run the database creation command: `make load csv-file=paht/to/file.csv`
2. Run the datasette server against it: `make serve`
3. Open http://127.0.0.1:8001
