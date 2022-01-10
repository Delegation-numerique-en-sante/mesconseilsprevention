# POC

## Install

1. Create a Python virtualenv and activate it
2. Install pip-tools: `python3 -m pip install pip-tools`
3. Install dependencies: `pip-sync`


## Run

1. Transform the source: `make preprocess xlsx-file=path/to/file.xlsx > transformed.csv`
2. Run the database creation command: `make load csv-file=transformed.csv`
3. Run the datasette server against it: `make serve`
4. Open http://127.0.0.1:8001


## Test

1. Install Hurl: https://hurl.dev/docs/installation.html
2. Install dev dependencies: `pip-sync requirements.txt requirements-dev.txt`
3. Launch datasette (see Run → 3. above)
4. Run tests: `make test`


## Check types

1. Install dev dependencies: `pip-sync requirements.txt requirements-dev.txt`
2. Run tests: `make check`
