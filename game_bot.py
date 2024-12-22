import requests
import time
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import re
import threading

from colorama import Fore, Style, init

API_URL = "https://nodewars.nodepay.ai"
HEADER = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, ztsd",
    "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
    "Priority": "u=1, i",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Origin": "https://minigame-nw.nodepay.ai",
    "Referer": "https://minigame-nw.nodepay.ai/",
    "Sec-CH-Ua": 'Microsoft Edge";v="131", "Chromium";v="131", "Not_A_Brand";v="24", "Microsoft Edge WebView2";v="131',
    "Sec-CH-Ua-Mobile": "?0",
    "Sec-CH-Ua-Platform": "Windows",
}

# 从文件中读取代理
def read_proxies_from_file(file_path: str = 'proxie.txt') -> list:
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}未找到代理文件 {file_path}！程序将不使用代理。{Fore.RESET}")
        return []

# 从查询字符串中提取用户名
def extract_username_from_query(query_string: str) -> str:
    try:
        match = re.search(r'username%22%3A%22([^%"]+)', query_string)
        username = match.group(1) if match else query_string[:15]
        if len(username) > 15:
            username = username[:15]
        elif len(username) < 15:
            padding = 15 - len(username)
            left_pad = padding // 2
            right_pad = padding - left_pad
            username = ' ' * left_pad + username + ' ' * right_pad
        return username
    except Exception:
        return ' ' * 15

# 设置日志记录
def setup_logging(username: str) -> logging.Logger:
    logger = logging.getLogger(username)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter(
        f'{Fore.GREEN}%(asctime)s{Fore.RESET} - {Fore.CYAN}[{username}]{Fore.RESET} - %(levelname)s: %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

# 生成动作日志
def generate_action_logs(base_prefix: str = '10') -> list:
    action_logs = []
    current_timestamp = int(time.time() * 1000000)
    possible_prefixes = ['10', '31', '53', '43', '10', '10', '10']
    for _ in range(24):
        prefix = random.choice(possible_prefixes)
        unique_number = random.randint(1000, 9999)
        current_timestamp += random.randint(100, 1000)
        action_log = f"{prefix}{unique_number}{current_timestamp}"
        action_logs.append(action_log)
    return action_logs

# 生成随机代币
def generate_random_tokens(tokens: list) -> Dict[str, int]:
    return {token: random.randint(1, 3) for token in tokens}

# 从文件中读取查询字符串
def read_query_strings_from_file(file_path: str = 'data.txt') -> list:
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}未找到文件 {file_path}！{Fore.RESET}")
        return []

# 使用查询字符串登录
def login_with_query_string(query_string: str, logger: logging.Logger, proxy: str = None) -> Optional[Dict[str, Any]]:
    url = f"{API_URL}/users/profile"
    headers = {**HEADER, "Authorization": f"Bearer {query_string}"}
    proxies = {'http': proxy, 'https': proxy} if proxy else {}
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        response.raise_for_status()
        logger.info(f"{Fore.GREEN}登录成功！{Fore.RESET}")
        logger.info(f"{Fore.YELLOW}使用代理: {proxy or '直接连接'}{Fore.RESET}")
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        logger.error(f"{Fore.RED}登录失败: {e}{Fore.RESET}")
        return None

# 领取每日奖励
def claim_daily(query_string: str, logger: logging.Logger, proxy: str = None, last_claim: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
    if last_claim and datetime.now() - last_claim < timedelta(hours=24):
        logger.info(f"{Fore.YELLOW}距离下次领取时间不足 24 小时，请稍后重试。{Fore.RESET}")
        return None
    url = f"{API_URL}/missions/daily/claim"
    headers = {**HEADER, "Authorization": f"Bearer {query_string}"}
    mission_id = "66c4b006c767c2cee0afe806"
    payload = {"missionId": mission_id}
    proxies = {'http': proxy, 'https': proxy} if proxy else {}
    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxies, timeout=30)
        if response.status_code == 200:
            logger.info(f"{Fore.GREEN}每日奖励领取成功！{Fore.RESET}")
            return response.json()
        elif response.status_code == 400:
            logger.warning(f"{Fore.YELLOW}每日奖励已领取！{Fore.RESET}")
            return None
        else:
            logger.error(f"{Fore.RED}意外响应: {response.status_code}{Fore.RESET}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"{Fore.RED}每日奖励领取失败: {e}{Fore.RESET}")
        return None

# 开始游戏
def start_game(level: int, query_string: str, logger: logging.Logger, proxy: str = None) -> Optional[Dict[str, Any]]:
    url = f"{API_URL}/game/start"
    headers = {**HEADER, "Authorization": f"Bearer {query_string}"}
    payload = {"level": level}
    proxies = {'http': proxy, 'https': proxy} if proxy else {}
    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxies, timeout=30)
        response.raise_for_status()
        logger.info(f"{Fore.GREEN}游戏已开始，当前等级：{level}！{Fore.RESET}")
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        logger.error(f"{Fore.RED}游戏启动失败: {e}{Fore.RESET}")
        return None

# 游戏完成
def finish_game(session_id: str, game_log_id: str, query_string: str, logger: logging.Logger, proxy: str = None) -> Optional[Dict[str, Any]]:
    url = f"{API_URL}/game/finish"
    headers = {**HEADER, "Authorization": f"Bearer {query_string}"}
    token_list = [
        "nodewars", "shiba", "nodepay", "pepe", "polkadot", 
        "babydoge", "bnb", "avax", "eth", "usdt", "solana", 
        "aptos", "ton", "bonk", "bomb", "doge", "floki", 
        "chainlink", "uniswap", "trx", "lido", "xrp", "ltc", 
        "ada", "sui", "dogwifhat", "near", "bitcoin"
    ]
    collected_tokens = generate_random_tokens(token_list)
    action_logs = generate_action_logs()
    score = random.randint(45, 60)
    time_spent = random.randint(25000, 30000)
    payload = {
        "sessionId": session_id,
        "gameLogId": game_log_id,
        "isCompleted": True,
        "timeSpent": time_spent,
        "actionLogs": action_logs,
        "score": score,
        "collectedTokens": collected_tokens
    }
    proxies = {'http': proxy, 'https': proxy} if proxy else {}
    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxies, timeout=30)
        response.raise_for_status()
        response_data = response.json()
        response_score = response_data.get('data', {}).get('score', score)
        logger.info(f"{Fore.GREEN}游戏完成！得分: {response_score}{Fore.RESET}")
        return response_data
    except requests.exceptions.RequestException as e:
        logger.error(f"{Fore.RED}游戏完成失败: {e}{Fore.RESET}")
        return None

# 处理单个账号
def process_account(query_string: str, proxies: list):
    username = extract_username_from_query(query_string)
    logger = setup_logging(username)
    last_claim_time = None
    delay = random.randint(30, 60)
    proxy = random.choice(proxies) if proxies else None
    logger.info(f"{Fore.YELLOW}使用代理: {proxy or '无代理'}{Fore.RESET}")
    while True:
        try:
            user_data = login_with_query_string(query_string, logger, proxy)
            if not user_data:
                break
            logger.info(f"{Fore.LIGHTMAGENTA_EX}用户ID: {user_data.get('userId')}{Fore.RESET}")
            claim_response = claim_daily(query_string, logger, proxy, last_claim_time)
            if claim_response:
                last_claim_time = datetime.now()
            while True:
                user_level = user_data.get("level", 1)
                game_data = start_game(user_level, query_string, logger, proxy)
                if not game_data:
                    break
                session_id = game_data["sessionId"]
                game_log_id = game_data["gameLogId"]
                time.sleep(delay)
                finish_response = finish_game(session_id, game_log_id, query_string, logger, proxy)
                if finish_response and finish_response.get("data", {}).get("isLevelUp"):
                    user_data["level"] += 1
        except Exception as e:
            logger.error(f"{Fore.RED}账号处理失败: {e}{Fore.RESET}")
            time.sleep(delay)

# 主程序入口
def main():
    init(autoreset=True)
    print(f"{Fore.YELLOW}NODEWARS 自动机器人启动中...{Fore.RESET}")
    query_strings = read_query_strings_from_file()
    proxies = read_proxies_from_file()
    threads = []
    for query_string in query_strings:
        thread = threading.Thread(target=process_account, args=(query_string, proxies))
        thread.start()
        threads.append(thread)
        time.sleep(5)
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
