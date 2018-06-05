# HEG Anlagendatenkollektor

## Installation (_Windows_)

1. Install Python 3 and Git for Windows and open the MingW
2. Install virtualenv
    ```sh
    pip.exe install virtualenv
    ```
3. Clone the Repo
    ```sh
    git clone https://github.com/morris-frank/heg-plant-monitor
    ```
4. Go into the folder of the repo and init the virtualenv:
    ```sh
    virtualenv.exe .venv
    ``` 
    And activate the virtualenv:
    ```sh
    source .venv/Scripts/activate
    ```
5. Install all dependencies:
    ```sh
    pip install -r requirements.txt
    ```
6. Setup `config.yaml` according to `config.schema.yaml`. An example is given in `config.example.yaml`.

## Running

Run `python collect.py` to collect the newest data.

Run `python process.py` to process the raw data.

Both use the same commmand line options:
- `-v`, `--verbose`: Print all logging information
- `-f`, `--force`, `--overwrite`: Overwrite all data (re-downloads everything)
- `--no-mp`: Don't run in parallel. With this option you can choose which projects to collect/process in the command line.
- `-c`, `--config`: Select a different config file than `config.yaml`