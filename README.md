# BTC-note-on-chain

## ABOUT
This project is web application allowing user to write a note or message into transaction.\
However due to various reasons I am not able to sign the bitcoin transaction with any of the \
methods mentioned in the bitcoin-core documentation.

## Requirements
- Python 3
- Poetry

## Installation
1. Install Poetry by following the instructions on their [official website](https://python-poetry.org/docs/#installation).
2. Clone this repository:

   ```bash
   git clone https://github.com/szymonsztreja/BTC-note-on-chain.git
   cd BTC-note-on-chain

3. Have virtual environment (can be skipped)
   ```bash
   poetry config virtualenvs.in-project

4. Install dependencies
   ```bash
   poetry install
   
## Run the app

1. Spawn the shell
   
   ```bash
   poetry shell

3. Run the flask application
   
   ```bash
   flask --app flaskr run --debug --host=0.0.0.0
