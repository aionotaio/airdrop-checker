import os
import sys
from pathlib import Path


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

FILES_DIR = os.path.join(ROOT_DIR, 'files')
WALLETS_PATH = os.path.join(FILES_DIR, 'wallets.txt')

LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
LOGS_PATH = os.path.join(LOGS_DIR, 'logs.txt')

RESULTS_DIR = os.path.join(ROOT_DIR, 'results')
RESULTS_PATH = os.path.join(RESULTS_DIR, 'results.csv')

class Utils:
    @staticmethod
    def read_strings_from_file(path: str) -> list:
        strings = []
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    strings.append(line)
        return strings