"""Модуль валидации данных для Weather Diary"""
from datetime import datetime
from typing import Tuple, Optional

class WeatherValidator:
    """Валидатор для записей погоды"""
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, Optional[str]]:
        """
        Проверка формата даты
        Возвращает: (валидность, сообщение об ошибке)
        """
        if not date_str:
            return False, "Дата не может быть пустой"
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, None
        except ValueError:
            return False, "Неверный формат даты. Используйте ГГГГ-ММ-ДД"
    
    @staticmethod
    def validate_temperature(temp_str: str) -> Tuple[bool, Optional[float], Optional[str]]:
        """
        Проверка температуры
        Возвращает: (валидность, значение, сообщение об ошибке)
        """
        if not temp_str:
            return False, None, "Температура не может быть пустой"
        
        try:
            temp = float(temp_str)
            return True, temp, None
        except ValueError:
            return False, None, "Температура должна быть числом"
    
    @staticmethod
    def validate_description(desc: str) -> Tuple[bool, Optional[str]]:
        """
        Проверка описания
        Возвращает: (валидность, сообщение об ошибке)
        """
        if not desc or not desc.strip():
            return False, "Описание не может быть пустым"
        
        if len(desc) > 200:
            return False, "Описание не должно превышать 200 символов"
        
        return True, None
    
    @staticmethod
    def validate_filter_temperature(temp_str: str) -> Tuple[bool, Optional[float], Optional[str]]:
        """Проверка температуры фильтра (может быть пустой)"""
        if not temp_str:
            return True, None, None
        
        try:
            temp = float(temp_str)
            return True, temp, None
        except ValueError:
            return False, None, "Температура фильтра должна быть числом"
    
    @staticmethod
    def validate_all_fields(date: str, temp: str, desc: str) -> Tuple[bool, Optional[str]]:
        """
        Комплексная проверка всех полей
        Возвращает: (валидность, сообщение об ошибке)
        """
        # Проверка даты
        is_valid, error = WeatherValidator.validate_date(date)
        if not is_valid:
            return False, error
        
        # Проверка температуры
        is_valid, _, error = WeatherValidator.validate_temperature(temp)
        if not is_valid:
            return False, error
        
        # Проверка описания
        is_valid, error = WeatherValidator.validate_description(desc)
        if not is_valid:
            return False, error
        
        return True, None