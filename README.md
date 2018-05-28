# HEG Anlagendatenkollektor

## Installation

1. Set up a Python virtual enviroment
2. Activate the Virtual enviroment
3. ```sh
    pip install -r requirements.txt
    ```
4. Setup `config.yaml` according to `config.schema.yaml`. An example is given in `config.example.yaml`.

## Running

Run `python collect.py` to collect the newest data.

Run `python process.py` to process the raw data.

Both use the same commmand line options:
- `-v`, `--verbose`: Print all logging information
- `-f`, `--force`, `--overwrite`: Overwrite all data (re-downloads everything)
- `--no-mp`: Don't run in parallel. With this option you can choose which projects to collect/process in the command line.
- `-c`, `--config`: Select a different config file than `config.yaml`