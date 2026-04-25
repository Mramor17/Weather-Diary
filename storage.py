"""Модуль для сохранения и загрузки данных в JSON"""
import json
from typing import List, Tuple, Optional
from models import WeatherRecord, WeatherDiaryModel

class JSONStorage:
    """Класс для работы с JSON файлом"""
    
    def __init__(self, filename: str = "weather_data.json"):
        self.filename = filename
    
    def save(self, model: WeatherDiaryModel) -> Tuple[bool, Optional[str]]:
        """
        Сохранить все записи в JSON файл
        Возвращает: (успех, сообщение об ошибке)
        """
        try:
            data = [record.to_dict() for record in model.get_all_records()]
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True, None
        except Exception as e:
            return False, f"Ошибка сохранения: {str(e)}"
    
    def load(self, model: WeatherDiaryModel) -> Tuple[bool, Optional[str]]:
        """
        Загрузить записи из JSON файла
        Возвращает: (успех, сообщение об ошибке)
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            records = [WeatherRecord.from_dict(item) for item in data]
            model.load_records(records)
            return True, None
        except FileNotFoundError:
            return False, "Файл не найден. Сначала сохраните данные."
        except json.JSONDecodeError:
            return False, "Ошибка формата JSON файла"
        except Exception as e:
            return False, f"Ошибка загрузки: {str(e)}"