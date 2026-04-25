"""Модели данных для Weather Diary"""
from dataclasses import dataclass
from typing import List

@dataclass
class WeatherRecord:
    """Модель одной записи о погоде"""
    date: str
    temperature: float
    description: str
    precipitation: bool
    
    def to_dict(self) -> dict:
        """Конвертация в словарь для JSON"""
        return {
            "date": self.date,
            "temperature": self.temperature,
            "description": self.description,
            "precipitation": self.precipitation
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WeatherRecord':
        """Создание записи из словаря"""
        return cls(
            date=data["date"],
            temperature=data["temperature"],
            description=data["description"],
            precipitation=data["precipitation"]
        )

class WeatherDiaryModel:
    """Модель всего дневника"""
    def __init__(self):
        self.records: List[WeatherRecord] = []
    
    def add_record(self, record: WeatherRecord) -> None:
        """Добавить запись"""
        self.records.append(record)
    
    def get_all_records(self) -> List[WeatherRecord]:
        """Получить все записи"""
        return self.records.copy()
    
    def clear_records(self) -> None:
        """Очистить все записи"""
        self.records.clear()
    
    def load_records(self, records: List[WeatherRecord]) -> None:
        """Загрузить список записей (замена текущих)"""
        self.records = records