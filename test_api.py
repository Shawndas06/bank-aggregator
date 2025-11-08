"""
Скрипт тестирования API
"""
import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000"

def print_response(response):
    """Красиво выводит ответ"""
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print("-" * 80)


def test_auth_flow():
    """Тестирует flow авторизации"""
    print("\n🔐 ТЕСТИРОВАНИЕ АУТЕНТИФИКАЦИИ\n")
    
    # 1. Регистрация
    print("1. Регистрация пользователя...")
    signup_data = {
        "email": "test@example.com",
        "password": "Test123456",
        "name": "Тестовый Пользователь",
        "birth_date": "2000-01-01"
    }
    response = requests.post(f"{BASE_URL}/api/auth/sign-up", json=signup_data)
    print_response(response)
    
    if response.status_code == 201:
        otp_code = response.json().get("data", {}).get("otpCode")
        print(f"📧 OTP код: {otp_code}")
        
        # 2. Подтверждение email
        print("\n2. Подтверждение email...")
        verify_data = {
            "email": "test@example.com",
            "code": otp_code
        }
        response = requests.post(f"{BASE_URL}/api/auth/verify-email", json=verify_data)
        print_response(response)
        
        # Сохраняем cookie
        session_cookie = response.cookies.get("session-id")
        
        if session_cookie:
            cookies = {"session-id": session_cookie}
            
            # 3. Получение данных пользователя
            print("\n3. Получение данных пользователя (GET /me)...")
            response = requests.get(f"{BASE_URL}/api/auth/me", cookies=cookies)
            print_response(response)
            
            # 4. Выход
            print("\n4. Выход из системы...")
            response = requests.post(f"{BASE_URL}/api/auth/logout", cookies=cookies)
            print_response(response)
            
            # 5. Вход
            print("\n5. Повторный вход...")
            signin_data = {
                "email": "test@example.com",
                "password": "Test123456"
            }
            response = requests.post(f"{BASE_URL}/api/auth/sign-in", json=signin_data)
            print_response(response)
            
            return response.cookies.get("session-id")
    
    return None


def test_accounts_flow(session_cookie):
    """Тестирует flow работы со счетами"""
    if not session_cookie:
        print("❌ Нет сессии для тестирования счетов")
        return
    
    print("\n💳 ТЕСТИРОВАНИЕ СЧЕТОВ\n")
    cookies = {"session-id": session_cookie}
    
    # 1. Создание счёта
    print("1. Создание счёта...")
    create_data = {
        "client_id": 1
    }
    response = requests.post(f"{BASE_URL}/api/accounts", json=create_data, cookies=cookies)
    print_response(response)
    
    if response.status_code == 201:
        account_id = response.json().get("data", {}).get("account", {}).get("accountId")
        
        # 2. Список счетов
        print("\n2. Получение списка счетов...")
        response = requests.get(f"{BASE_URL}/api/accounts", cookies=cookies)
        print_response(response)
        
        # 3. Информация о счёте
        if account_id:
            print(f"\n3. Получение информации о счёте {account_id}...")
            response = requests.get(
                f"{BASE_URL}/api/accounts/{account_id}?client_id=1",
                cookies=cookies
            )
            print_response(response)
            
            # 4. Баланс счёта
            print(f"\n4. Получение баланса счёта {account_id}...")
            response = requests.get(
                f"{BASE_URL}/api/accounts/{account_id}/balances?client_id=1",
                cookies=cookies
            )
            print_response(response)
            
            # 5. Транзакции
            print(f"\n5. Получение транзакций счёта {account_id}...")
            response = requests.get(
                f"{BASE_URL}/api/accounts/{account_id}/transactions?client_id=1",
                cookies=cookies
            )
            print_response(response)


def test_groups_flow(session_cookie):
    """Тестирует flow работы с группами"""
    if not session_cookie:
        print("❌ Нет сессии для тестирования групп")
        return
    
    print("\n👥 ТЕСТИРОВАНИЕ ГРУПП\n")
    cookies = {"session-id": session_cookie}
    
    # 1. Настройки групп
    print("1. Получение настроек групп...")
    response = requests.get(f"{BASE_URL}/api/groups/settings")
    print_response(response)
    
    # 2. Создание группы
    print("\n2. Создание группы...")
    create_data = {
        "name": "Моя семья"
    }
    response = requests.post(f"{BASE_URL}/api/groups", json=create_data, cookies=cookies)
    print_response(response)
    
    if response.status_code == 201:
        group_id = response.json().get("data", {}).get("id")
        
        # 3. Список групп
        print("\n3. Получение списка групп...")
        response = requests.get(f"{BASE_URL}/api/groups", cookies=cookies)
        print_response(response)
        
        # 4. Счета группы
        if group_id:
            print(f"\n4. Получение счетов группы {group_id}...")
            response = requests.get(
                f"{BASE_URL}/api/groups/{group_id}/accounts",
                cookies=cookies
            )
            print_response(response)
            
            # 5. Балансы группы
            print(f"\n5. Получение балансов группы {group_id}...")
            response = requests.get(
                f"{BASE_URL}/api/groups/{group_id}/accounts/balances",
                cookies=cookies
            )
            print_response(response)


def main():
    """Главная функция"""
    print("=" * 80)
    print("🚀 ЗАПУСК ТЕСТОВ API")
    print("=" * 80)
    
    # Проверка доступности API
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ API доступен: {response.status_code}")
    except Exception as e:
        print(f"❌ API недоступен: {e}")
        return
    
    # Тестирование
    session_cookie = test_auth_flow()
    
    if session_cookie:
        test_accounts_flow(session_cookie)
        test_groups_flow(session_cookie)
    
    print("\n" + "=" * 80)
    print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 80)


if __name__ == "__main__":
    main()

