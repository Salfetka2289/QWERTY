import tkinter as tk
from tkinter import scrolledtext
import random
import re

class SimpleChatBot:
    def __init__(self):
        # База знаний с шаблонами вопросов и ответов
        self.knowledge_base = {
            # Математические вопросы
            r'\b2\+2\b|\bдва плюс два\b': "2 + 2 = 4",
            r'\bсколько будет 2\*2\b|\b2 умножить на 2\b': "2 × 2 = 4",
            r'\b5\+7\b|\bпять плюс семь\b': "5 + 7 = 12",
            r'\b10-3\b|\bдесять минус три\b': "10 - 3 = 7",
            
            # Общие вопросы о животных
            r'\bкто такая кошка\b|\bчто такое кошка\b': "Кошка - это домашнее животное, млекопитающее семейства кошачьих.",
            r'\bкто такая собака\b|\bчто такое собака\b': "Собака - это домашнее животное, друг человека, относится к семейству псовых.",
            r'\bчто такое нейросеть\b': "Нейросеть - это математическая модель, работающая по принципу нейронов мозга.",
            
            # Приветствия
            r'\bпривет\b|\bздравствуй\b|\bдобрый день\b': "Привет! Как дела?",
            r'\bкак дела\b|\bкак ты\b': "У меня всё отлично! А у вас?",
            
            # Прощания
            r'\bпока\b|\bдо свидания\b|\bпрощай\b': "До свидания! Было приятно пообщаться!",
            
            # Вопросы о боте
            r'\bкто ты\b|\bкак тебя зовут\b': "Я простой чат-бот, созданный на Python.",
            r'\bчто ты умеешь\b': "Я могу отвечать на простые вопросы по математике и о животных.",
        }
        
        # Общие ответы для неизвестных вопросов
        self.default_responses = [
            "Извините, я не знаю ответ на этот вопрос.",
            "Пока я не могу ответить на это. Спросите что-то другое!",
            "Интересный вопрос! Но мои знания ограничены.",
            "Я ещё учусь. Можете задать другой вопрос?",
        ]

    def get_response(self, user_input):
        """Получить ответ на вопрос пользователя"""
        user_input = user_input.lower().strip()
        
        # Проверяем все шаблоны в базе знаний
        for pattern, response in self.knowledge_base.items():
            if re.search(pattern, user_input):
                return response
        
        # Если не нашли подходящего ответа, возвращаем случайный из default_responses
        return random.choice(self.default_responses)

class ChatGUI:
    def __init__(self, root):  # Добавляем параметр root
        self.root = root
        self.root.title("Простой Чат-Бот")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        self.bot = SimpleChatBot()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text="Простой Чат-Бот", 
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=10)
        
        # Область для отображения диалога
        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Arial", 11),
            bg='white',
            fg='#333'
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        # Приветственное сообщение
        self.display_message("Бот", "Привет! Я простой чат-бот. Задайте мне вопрос!\nНапример: '2+2=?' или 'Кто такая кошка?'")
        
        # Фрейм для ввода сообщения
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Поле ввода
        self.input_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=50
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind('<Return>', lambda event: self.send_message())
        
        # Кнопка отправки
        send_button = tk.Button(
            input_frame,
            text="Отправить",
            command=self.send_message,
            font=("Arial", 10),
            bg='#4CAF50',
            fg='white',
            padx=20
        )
        send_button.pack(side=tk.RIGHT)
        
        # Подсказка
        hint_label = tk.Label(
            self.root,
            text="Примеры вопросов: '2+2=?', 'Кто такая кошка?', 'Как дела?'",
            font=("Arial", 9),
            bg='#f0f0f0',
            fg='#666'
        )
        hint_label.pack(pady=5)
    
    def display_message(self, sender, message):
        """Отобразить сообщение в области чата"""
        self.chat_area.config(state=tk.NORMAL)
        
        if sender == "Вы":
            self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        else:
            self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)  # Прокрутка вниз
    
    def send_message(self):
        """Отправить сообщение и получить ответ"""
        user_input = self.input_entry.get().strip()
        
        if user_input:
            # Отображаем сообщение пользователя
            self.display_message("Вы", user_input)
            
            # Очищаем поле ввода
            self.input_entry.delete(0, tk.END)
            
            # Получаем ответ от бота
            response = self.bot.get_response(user_input)
            
            # Отображаем ответ бота
            self.display_message("Бот", response)

def main():
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()

main()