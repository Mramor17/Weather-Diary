"""Модуль для фильтрации записей о погоде"""
from typing import List, Optional
from models import WeatherRecord

class WeatherFilter:
    """Класс для фильтрации записей"""
    
    @staticmethod
    def filter_by_date(records: List[WeatherRecord], date: Optional[str]) -> List[WeatherRecord]:
        """Фильтрация по точной дате"""
        if not date:
            return records
        return [r for r in records if r.date == date]
    
    @staticmethod
    def filter_by_min_temperature(records: List[WeatherRecord], min_temp: Optional[float]) -> List[WeatherRecord]:
        """Фильтрация по минимальной температуре"""
        if min_temp is None:
            return records
        return [r for r in records if r.temperature > min_temp]
    
    @staticmethod
    def apply_filters(records: List[WeatherRecord], 
                     date: Optional[str] = None, 
                     min_temp: Optional[float] = None) -> List[WeatherRecord]:
        """Применить все фильтры"""
        result = records
        
        # Фильтр по дате
        result = WeatherFilter.filter_by_date(result, date)
        
        # Фильтр по температуре
        result = WeatherFilter.filter_by_min_temperature(result, min_temp)
        
        return result