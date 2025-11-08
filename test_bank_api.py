"""
Тестирование прямой интеграции с API банков
"""
import requests
import json

# Credentials от организаторов хакатона
CLIENT_ID = "team222"
CLIENT_SECRET = "Wl1F0L2aVHOPE20rM0DFeqvP9Qr2pgQT"

# URLs банков
BANKS = {
    "vbank": "https://vbank.open.bankingapi.ru",
    "abank": "https://abank.open.bankingapi.ru",
    "sbank": "https://sbank.open.bankingapi.ru"
}


def print_response(title, response):
    """Красиво выводит ответ"""
    print(f"\n{'='*80}")
    print(f"📍 {title}")
    print(f"{'='*80}")
    print(f"Status: {response.status_code}")
    print(f"URL: {response.url}")
    try:
        data = response.json()
        print(f"Response:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*80}\n")


def test_bank_token(bank_name, bank_url):
    """Тест получения токена от банка"""
    print(f"\n🔑 Тестирование получения токена от {bank_name.upper()}...")
    
    url = f"{bank_url}/auth/bank-token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    try:
        response = requests.post(url, params=params, timeout=10)
        print_response(f"GET TOKEN from {bank_name.upper()}", response)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                print(f"✅ Токен получен: {token[:50]}...")
                return token
            else:
                print(f"❌ Токен не найден в ответе")
        else:
            print(f"❌ Ошибка получения токена: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    return None


def test_create_consent(bank_name, bank_url, token):
    """Тест создания consent"""
    if not token:
        print(f"⚠️  Пропускаем создание consent (нет токена)")
        return None
    
    print(f"\n📝 Создание consent в {bank_name.upper()}...")
    
    url = f"{bank_url}/account-consents/request"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Requesting-Bank": CLIENT_ID,
        "Content-Type": "application/json"
    }
    
    body = {
        "client_id": f"{CLIENT_ID}-1",
        "permissions": ["ReadAccountsDetail", "ReadBalances", "ReadTransactionsDetail"],
        "reason": "Агрегация счетов для Bank Aggregator",
        "requesting_bank": CLIENT_ID,
        "requesting_bank_name": "Team 222 Bank Aggregator"
    }
    
    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        print_response(f"CREATE CONSENT in {bank_name.upper()}", response)
        
        if response.status_code == 200:
            data = response.json()
            consent_id = data.get("consent_id")
            if consent_id:
                print(f"✅ Consent создан: {consent_id}")
                return consent_id
            else:
                print(f"❌ Consent ID не найден в ответе")
        else:
            print(f"❌ Ошибка создания consent: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    return None


def test_get_accounts(bank_name, bank_url, token, consent_id):
    """Тест получения счетов"""
    if not token or not consent_id:
        print(f"⚠️  Пропускаем получение счетов (нет токена или consent)")
        return []
    
    print(f"\n💳 Получение счетов из {bank_name.upper()}...")
    
    url = f"{bank_url}/accounts"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Requesting-Bank": CLIENT_ID,
        "X-Consent-Id": consent_id
    }
    params = {
        "client_id": f"{CLIENT_ID}-1"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print_response(f"GET ACCOUNTS from {bank_name.upper()}", response)
        
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "account" in data["data"]:
                accounts = data["data"]["account"]
                print(f"✅ Получено счетов: {len(accounts)}")
                for acc in accounts:
                    print(f"  - {acc.get('accountId')}: {acc.get('nickname', 'N/A')}")
                return accounts
            else:
                print(f"⚠️  Нет счетов в ответе")
        else:
            print(f"❌ Ошибка получения счетов: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    return []


def main():
    """Главная функция тестирования"""
    print("\n" + "="*80)
    print("🚀 ТЕСТИРОВАНИЕ ИНТЕГРАЦИИ С РЕАЛЬНЫМ API БАНКОВ")
    print("="*80)
    print(f"\n📋 Credentials:")
    print(f"   Client ID: {CLIENT_ID}")
    print(f"   Client Secret: {CLIENT_SECRET[:20]}...")
    
    results = {}
    
    # Тестируем каждый банк
    for bank_name, bank_url in BANKS.items():
        print(f"\n{'▼'*80}")
        print(f"🏦 ТЕСТИРОВАНИЕ БАНКА: {bank_name.upper()}")
        print(f"{'▼'*80}")
        
        # 1. Получаем токен
        token = test_bank_token(bank_name, bank_url)
        
        # 2. Создаём consent
        consent_id = test_create_consent(bank_name, bank_url, token)
        
        # 3. Получаем счета
        accounts = test_get_accounts(bank_name, bank_url, token, consent_id)
        
        results[bank_name] = {
            "token": token is not None,
            "consent": consent_id is not None,
            "accounts": len(accounts)
        }
    
    # Итоговый отчёт
    print(f"\n{'='*80}")
    print("📊 ИТОГОВЫЙ ОТЧЁТ")
    print(f"{'='*80}\n")
    
    for bank_name, result in results.items():
        print(f"🏦 {bank_name.upper()}:")
        print(f"   Токен:    {'✅' if result['token'] else '❌'}")
        print(f"   Consent:  {'✅' if result['consent'] else '❌'}")
        print(f"   Счета:    {result['accounts']} шт.")
        print()
    
    # Проверка успешности
    all_success = all(r['token'] and r['consent'] for r in results.values())
    
    if all_success:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Backend готов к работе с реальными банками!")
    else:
        print("⚠️  Некоторые тесты не прошли. Проверьте credentials или доступность API.")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    main()

