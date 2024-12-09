import csv

import requests
from fake_useragent import UserAgent
from tabulate import tabulate
from loguru import logger

from src.utils import PROJECTS_NAMES


class Client:
    def __init__(self, address: str) -> None:
        self.address = address
        self.user_agent = UserAgent().random

    def make_request(self) -> dict:
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i',
            'referer': f'https://checkdrop.byzantine.fi/?address={self.address}',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
        }

        params = {
            'address': self.address,
        }

        response = requests.get('https://checkdrop.byzantine.fi/api/getDatas', params=params, headers=headers)
        if response.status_code == 200:
            res = response.json()
            result_dict = {key: value for key, value in res.items() if key != 'count'}
            return result_dict
        else:
            logger.error(f'Request failed with status: {response.status_code}.')
            return None
    
    def get_claim_link(self, project: str) -> str:
        claim_links = {
            'eigenlayer': 'https://checkeigen.byzantine.fi/',
            'optimism': 'https://app.optimism.io/airdrops/5',
            'scroll': 'https://claim.scroll.io/',
            'swell': 'https://app.swellnetwork.io/dao/voyage',
            'puffer': 'https://claims.puffer.fi/',
            'zora': 'N/A',
            'initia': 'N/A',
            'debridge': 'https://app.debridge.finance/r/482',
            'layerzero': 'https://www.layerzero.foundation/',
            'mode': 'https://app.hedgey.finance/claim/1878e884-40b3-4d87-87ca-5c16a0ce66d0',
            'p2p': 'https://app.p2p.org/claim',
            'zircuitFairdrop': 'https://app.zircuit.com/fairdrop',
            'zircuitS1S2': 'N/A',
            'usual': 'N/A'
        }
        return claim_links.get(project, 'N/A')
    
    def get_tickers(self) -> dict:
        return {
            'eigenlayer': '$EIGEN',
            'optimism': '$OP',
            'scroll': '$SCR',
            'swell': '$SWELL',
            'puffer': '$PUFFER',
            'zora': '$ZORA',
            'initia': '$INT',
            'debridge': '$DBR',
            'layerzero': '$ZRO',
            'mode': '$MODE',
            'p2p': '$ETH',
            'zircuitFairdrop': '$ZRC',
            'zircuitS1S2': '$ZRC',
            'usual': '$USUAL'
        }
    
    def format_tokens(self, tokens: str, ticker: str) -> str:
        return f"{tokens} {ticker}" if tokens != 'N/A' else 'N/A'

    def check_eligibility(self, tokens: str) -> bool:
        return tokens != 'N/A' and float(tokens) > 0
    
    def print_table(self, data: dict) -> list:
        logger.info(f"Data for wallet {self.address}:")
        tickers = self.get_tickers()

        table_data = []
        csv_data = []
        eligible_messages = []

        for project, details in data.items():
            project_name = PROJECTS_NAMES[project]
            points = details['points'] if details['points'] != '-' and details['points'] != -1 else 'N/A'
            tokens = details['tokens'] if details['tokens'] != '-' and details['tokens'] != -1 else 'N/A'
            if isinstance(points, float):
                points = f"{points:.2f}"
            if isinstance(tokens, float):
                tokens = f"{tokens:.2f}"
            ticker = tickers.get(project, 'N/A')
            tokens_with_ticker = self.format_tokens(tokens, ticker)
            eligibility = self.check_eligibility(tokens)
            claim_link = self.get_claim_link(project) if eligibility else 'N/A'

            table_data.append([project_name, points, tokens_with_ticker])
            if eligibility:
                eligible_messages.append(f'{self.address} eligible for {tokens} {ticker}. Claim: {claim_link}.')
            csv_data.append([self.address, project_name, points, tokens_with_ticker, eligibility, claim_link])
        
        print(tabulate(table_data, headers=['Project', 'Points', 'Tokens'], tablefmt='pretty', stralign='left'))
        
        for message in eligible_messages:
            logger.success(message)

        return csv_data

    def write_to_csv(self, csv_data: list, csv_path: str):
        with open(csv_path, 'a', newline='', encoding='utf-8-sig') as output_file:
            csv_writer = csv.writer(output_file, delimiter=';')
            if output_file.tell() == 0:
                csv_writer.writerow(['Address', 'Project', 'Points', 'Tokens', 'Eligibility', 'Claim Link'])
            csv_writer.writerows(csv_data)

    def write_eligible_to_csv(self, csv_data: list, csv_path: str):
        eligible_data = [row for row in csv_data if row[4]]
        with open(csv_path, 'a', newline='', encoding='utf-8-sig') as output_file:
            csv_writer = csv.writer(output_file, delimiter=';')
            if output_file.tell() == 0:
                csv_writer.writerow(['Address', 'Project', 'Points', 'Tokens', 'Eligibility', 'Claim Link'])
            csv_writer.writerows(eligible_data)
