"""Графический интерфейс для Weather Diary"""
import tkinter as tk
from tkinter import ttk, messagebox
from models import WeatherDiaryModel, WeatherRecord
from storage import JSONStorage
from validators import WeatherValidator
from filters import WeatherFilter

class WeatherDiaryGUI:
    """Главный класс GUI приложения"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Weather Diary")
        self.root.geometry("800x600")
        
        # Инициализация сервисов
        self.model = WeatherDiaryModel()
        self.storage = JSONStorage()
        self.validator = WeatherValidator()
        self.filter = WeatherFilter()
        
        # Создание интерфейса
        self._create_input_frame()
        self._create_filter_frame()
        self._create_table()
        self._create_button_frame()
        
        # Отображение записей
        self._refresh_display()
    
    def _create_input_frame(self):
        """Создание формы для ввода"""
        input_frame = tk.LabelFrame(self.root, text="Add Weather Record", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill="x")
        
        # Дата
        tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="e")
        self.date_entry = tk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5)
        
        # Температура
        tk.Label(input_frame, text="Temperature (°C):").grid(row=0, column=2, sticky="e")
        self.temp_entry = tk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5)
        
        # Описание
        tk.Label(input_frame, text="Description:").grid(row=1, column=0, sticky="e")
        self.desc_entry = tk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")
        
        # Осадки
        tk.Label(input_frame, text="Precipitation:").grid(row=1, column=4, sticky="e")
        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(input_frame, variable=self.precip_var).grid(row=1, column=5, sticky="w")
        
        # Кнопка добавления
        tk.Button(input_frame, text="Add Record", command=self._add_record, 
                 bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=6, pady=10)
    
    def _create_filter_frame(self):
        """Создание панели фильтрации"""
        filter_frame = tk.LabelFrame(self.root, text="Filter Records", padx=10, pady=10)
        filter_frame.pack(pady=5, padx=10, fill="x")
        
        # Фильтр по дате
        tk.Label(filter_frame, text="Filter by Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="e")
        self.filter_date_entry = tk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=1, padx=5)
        
        # Фильтр по температуре
        tk.Label(filter_frame, text="Temp > (°C):").grid(row=0, column=2, sticky="e")
        self.filter_temp_entry = tk.Entry(filter_frame, width=10)
        self.filter_temp_entry.grid(row=0, column=3, padx=5)
        
        # Кнопки фильтрации
        tk.Button(filter_frame, text="Apply Filters", command=self._apply_filters, 
                 bg="#2196F3", fg="white").grid(row=0, column=4, padx=10)
        tk.Button(filter_frame, text="Show All", command=self._show_all, 
                 bg="#FF9800", fg="white").grid(row=0, column=5)
    
    def _create_table(self):
        """Создание таблицы для отображения записей"""
        # Создание фрейма с прокруткой
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10, fill="both", expand=True)
        
        # Скроллбары
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        
        # Таблица
        self.tree = ttk.Treeview(table_frame, 
                                 columns=("Date", "Temp", "Description", "Precip"), 
                                 show="headings",
                                 yscrollcommand=scroll_y.set,
                                 xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Настройка колонок
        self.tree.heading("Date", text="Date")
        self.tree.heading("Temp", text="Temp (°C)")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Precip", text="Precipitation")
        
        self.tree.column("Date", width=100)
        self.tree.column("Temp", width=80)
        self.tree.column("Description", width=360)
        self.tree.column("Precip", width=80)
        
        # Размещение
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
    
    def _create_button_frame(self):
        """Создание панели кнопок управления"""
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Save to JSON", command=self._save_to_json,
                 bg="#9C27B0", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Load from JSON", command=self._load_from_json,
                 bg="#9C27B0", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear All Records", command=self._clear_all,
                 bg="#F44336", fg="white").pack(side="left", padx=5)
    
    def _add_record(self):
        """Добавление новой записи"""
        date = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        desc = self.desc_entry.get().strip()
        precip = self.precip_var.get()
        
        # Валидация
        is_valid, error = self.validator.validate_all_fields(date, temp_str, desc)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Получение значения температуры
        _, temp, _ = self.validator.validate_temperature(temp_str)
        
        # Создание и добавление записи
        record = WeatherRecord(date, temp, desc, precip)
        self.model.add_record(record)
        
        # Очистка полей
        self._clear_inputs()
        
        # Обновление отображения
        self._refresh_display()
        messagebox.showinfo("Success", "Record added successfully!")
    
    def _clear_inputs(self):
        """Очистка полей ввода"""
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)
    
    def _apply_filters(self):
        """Применение фильтров"""
        date_filter = self.filter_date_entry.get().strip() or None
        temp_filter_str = self.filter_temp_entry.get().strip()
        
        # Валидация температуры фильтра
        is_valid, temp_filter, error = self.validator.validate_filter_temperature(temp_filter_str)
        if not is_valid:
            messagebox.showerror("Filter Error", error)
            return
        
        # Применение фильтров
        filtered_records = self.filter.apply_filters(
            self.model.get_all_records(),
            date=date_filter,
            min_temp=temp_filter
        )
        
        self._display_records(filtered_records)
    
    def _show_all(self):
        """Показать все записи"""
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self._refresh_display()
    
    def _display_records(self, records):
        """Отображение записей в таблице"""
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Заполнение таблицы
        for rec in records:
            precip_text = "Yes" if rec.precipitation else "No"
            self.tree.insert("", tk.END, values=(
                rec.date,
                f"{rec.temperature:.1f}",
                rec.description,
                precip_text
            ))
    
    def _refresh_display(self):
        """Обновление отображения (без фильтров)"""
        self._display_records(self.model.get_all_records())
    
    def _save_to_json(self):
        """Сохранение в JSON"""
        success, error = self.storage.save(self.model)
        if success:
            messagebox.showinfo("Success", "Data saved to weather_data.json")
        else:
            messagebox.showerror("Error", error)
    
    def _load_from_json(self):
        """Загрузка из JSON"""
        success, error = self.storage.load(self.model)
        if success:
            self._refresh_display()
            messagebox.showinfo("Success", "Data loaded from weather_data.json")
        else:
            messagebox.showerror("Error", error)
    
    def _clear_all(self):
        """Очистка всех записей"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all records?"):
            self.model.clear_records()
            self._refresh_display()
            messagebox.showinfo("Success", "All records cleared")