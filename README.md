# Airdrop Checker Tool

## Functionality

- Checking allocation for:
    - EigenLayer S2 airdrop
    - Optimism S5 airdrop
    - Scroll airdrop
    - Swell airdrop
    - Puffer airdrop
    - Zora airdrop (when it will be available)
    - Initia airdrop (when it will be available)
    - deBridge airdrop
    - LayerZero S2 airdrop
    - Mode S2 airdrop
    - P2P Eigen S2 airdrop
    - Zircuit Fairdrop

### Follow: https://t.me/touchingcode

## Settings
- `files/wallets.txt` - Wallet addresses. 1 line = 1 address, NOT PRIVATE KEYS!!!

## Run

- Python version: 3.10+

- Installing virtual env: \
`pip install virtualenv` \
`cd <project_dir>` \
`python -m venv venv`


- Activating: 
    - Mac/Linux - `source venv/bin/activate` 
    - Windows - `.\venv\Scripts\activate` 

- Installing dependencies: \
`pip install -r requirements.txt`

- Run main script: \
`python main.py`

## Results
- `logs/logs.txt` - Logs
- `results/results.csv` - Results
- `results/eligible.csv` - Results with only eligible wallets