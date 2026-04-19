#!/usr/bin/env python3
import os
import yaml
import time
import csv
import requests
from colorama import Fore, Style, init

init(autoreset=True)

class PromptFuzzer:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.api_key = self.config['api']['key']
        self.api_url = self.config['api']['url']
        self.model = self.config['target']['model']
        self.base_prompt = self.config['fuzzing']['base_prompt']
        self.payloads = self._load_payloads(self.config['paths']['payloads_dir'])
        self.questions = self._load_list(self.config['paths']['harmful_questions'])
        self.success_keywords = self._load_list(self.config['paths']['success_keywords'])
        self.failure_keywords = self._load_list(self.config['paths']['failure_keywords'])

        print(f"{Fore.GREEN}[+] Fuzzer Cloud siap! Target: {self.model}")

    def _load_list(self, filepath):
        if not os.path.exists(filepath): return []
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]

    def _load_payloads(self, dirpath):
        payloads = []
        if not os.path.exists(dirpath): return []
        for filename in os.listdir(dirpath):
            if filename.endswith(".txt"):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r') as f:
                    payloads.extend([line.strip() for line in f if line.strip() and not line.startswith('#')])
        return payloads

    def send_prompt(self, prompt):
        """kirim prompt ke OpenRouter (Cloud)"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"[ERROR] API Down / Key Salah: {response.status_code}"
        except Exception as e:
            return f"[ERROR] Jaringan: {e}"

    def analyze_response(self, response):
        response_lower = response.lower()
        for keyword in self.success_keywords:
            if keyword.lower() in response_lower:
                return "SUCCESS"
        for keyword in self.failure_keywords:
            if keyword.lower() in response_lower:
                return "FAILED"
        return "UNKNOWN"

    def run(self):
        results = []
        total_tests = len(self.payloads) * len(self.questions)
        test_count = 0

        print(f"{Fore.CYAN}[*] Total skenario uji: {total_tests}\n")

        for payload in self.payloads:
            for question in self.questions:
                test_count += 1
                prompt = self.base_prompt.format(payload=payload, question=question)
                
                print(f"{Fore.YELLOW}[TEST {test_count}/{total_tests}] Payload: {payload[:50]}...")
                response = self.send_prompt(prompt)
                status = self.analyze_response(response)
                
                color = Fore.GREEN if status == "SUCCESS" else Fore.RED if status == "FAILED" else Fore.WHITE
                print(f"{color}[{status}] Respon: {response[:100]}...\n")
                
                results.append({
                    "payload": payload, "question": question, "status": status, "response": response
                })
                
                time.sleep(2)

        self.save_results(results)
        print(f"{Fore.GREEN}\n[+] Fuzzing selesai! Hasil disimpan di 'fuzzing_results.csv'.")

    def save_results(self, results):
        with open('fuzzing_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['payload', 'question', 'status', 'response']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

if __name__ == "__main__":
    fuzzer = PromptFuzzer()
    fuzzer.run()