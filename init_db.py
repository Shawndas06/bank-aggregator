"""
Скрипт инициализации базы данных
"""
from src.database import Base, engine
from src.models import User, BankAccount, Group, GroupMember, Invitation, OTPCode

def init_database():
    """Создаёт все таблицы в базе данных"""
    print("🔧 Создание таблиц в базе данных...")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы успешно созданы!")
        
        # Выводим список созданных таблиц
        print("\n📋 Созданные таблицы:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
            
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")
        raise

if __name__ == "__main__":
    init_database()

