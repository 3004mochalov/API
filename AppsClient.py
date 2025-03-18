import pygame
import sys
import requests

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont('Arial', 24)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Калькулятор Клиент')

# Переменные для ввода и результата
input_num1 = ''
input_num2 = ''
result = ''
operation = 'add'

# Кнопки навигации
nav_buttons = [
    {'text': 'Калькулятор', 'x': 10, 'y': 10, 'visible': True},
    {'text': 'Пинболл (в разработке)', 'x': 10, 'y': 50, 'visible': True},
    {'text': 'Меню', 'x': 10, 'y': 90, 'visible': False}  # Кнопка меню
]

# Кнопки цифр и операций
buttons = [
    {'text': '7', 'x': 100, 'y': 100},
    {'text': '8', 'x': 160, 'y': 100},
    {'text': '9', 'x': 220, 'y': 100},
    {'text': '/', 'x': 280, 'y': 100},
    {'text': '4', 'x': 100, 'y': 150},
    {'text': '5', 'x': 160, 'y': 150},
    {'text': '6', 'x': 220, 'y': 150},
    {'text': '*', 'x': 280, 'y': 150},
    {'text': '1', 'x': 100, 'y': 200},
    {'text': '2', 'x': 160, 'y': 200},
    {'text': '3', 'x': 220, 'y': 200},
    {'text': '-', 'x': 280, 'y': 200},
    {'text': '0', 'x': 100, 'y': 250},
    {'text': '.', 'x': 160, 'y': 250},
    {'text': '=', 'x': 220, 'y': 250},
    {'text': '+', 'x': 280, 'y': 250},
    {'text': 'C', 'x': 340, 'y': 250}  # Кнопка для стирания
]

# Флаги для переключения между калькулятором и пинболлом
show_calculator = False
show_pinball = False
show_menu = True

# Функция для отображения кнопок навигации
def draw_nav_buttons():
    for button in nav_buttons:
        if button['visible']:
            pygame.draw.rect(screen, BLACK, (button['x'], button['y'], 100, 30), 1)
            button_text = FONT.render(button['text'], True, BLACK)
            screen.blit(button_text, (button['x'] + 10, button['y'] + 5))

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Обработка кнопок навигации
            for button in nav_buttons:
                if (button['visible'] and
                        button['x'] <= mouse_pos[0] <= button['x'] + 100 and
                        button['y'] <= mouse_pos[1] <= button['y'] + 30):
                    if button['text'] == 'Калькулятор':
                        show_calculator = True
                        show_pinball = False
                        show_menu = False
                    elif button['text'] == 'Пинболл (в разработке)':
                        show_calculator = False
                        show_pinball = True
                        show_menu = False
                    elif button['text'] == 'Меню':
                        show_calculator = False
                        show_pinball = False
                        show_menu = True
                    for btn in nav_buttons:
                        if btn['text'] != 'Меню':
                            btn['visible'] = show_menu  # Скрытие/отображение кнопок
                        else:
                            btn['visible'] = not show_menu

            # Обработка кнопок калькулятора
            if show_calculator:
                for button in buttons:
                    if (button['x'] <= mouse_pos[0] <= button['x'] + 50 and
                            button['y'] <= mouse_pos[1] <= button['y'] + 40):
                        if button['text'] == '=':
                            try:
                                data = {
                                    "num1": float(input_num1),
                                    "num2": float(input_num2),
                                    "operation": operation
                                }
                                response = requests.post('http://localhost:5000/calculate', json=data)
                                if response.status_code == 200:
                                    result = "{:.2f}".format(response.json().get('result'))  # Две цифры после запятой
                                else:
                                    result = 'Ошибка'
                            except Exception as e:
                                result = 'Ошибка соединения'
                        elif button['text'] == 'C':
                            input_num1 = ''
                            input_num2 = ''
                            result = ''
                            operation = 'add'
                        elif button['text'] in ['+', '-', '*', '/']:
                            operation = button['text']
                        else:
                            if input_num1 == '':
                                input_num1 += button['text']
                            else:
                                input_num2 += button['text']

    # Очистка экрана
    screen.fill(WHITE)

    # Рисование элементов интерфейса
    if show_menu:
        draw_nav_buttons()
        for btn in nav_buttons:
            if btn['text'] == 'Меню':
                btn['visible'] = False
            else:
                btn['visible'] = True
    elif show_calculator:
        # Скрываем кнопки навигации
        for btn in nav_buttons:
            btn['visible'] = False
        nav_buttons[2]['visible'] = True # Отображаем кнопку меню

        # Рисование калькулятора
        input_num1_text = FONT.render(input_num1, True, BLACK)
        screen.blit(input_num1_text, (100, 50))
        input_num2_text = FONT.render(input_num2, True, BLACK)
        screen.blit(input_num2_text, (100, 80))
        operation_text = FONT.render(operation, True, BLACK)
        screen.blit(operation_text, (100, 110))
        result_text = FONT.render(f"Результат: {result}", True, BLACK)
        screen.blit(result_text, (100, 500))  # Отображение результата внизу

        for button in buttons:
            pygame.draw.rect(screen, BLACK, (button['x'], button['y'], 50, 40), 1)
            button_text = FONT.render(button['text'], True, BLACK)
            screen.blit(button_text, (button['x'] + 15, button['y'] + 10))
        #Рисуем кнопку меню
        draw_nav_buttons()

    elif show_pinball:
        # Скрываем кнопки навигации
        for btn in nav_buttons:
            btn['visible'] = False
        nav_buttons[2]['visible'] = True  # Отображаем кнопку меню

        # Рисование пинболла
        pinball_text = FONT.render('Пинболл находится в разработке', True, BLACK)
        screen.blit(pinball_text, (100, 100))
        #Рисуем кнопку меню
        draw_nav_buttons()

    # Обновление экрана
    pygame.display.flip()

    # Ограничение частоты кадров
    pygame.time.Clock().tick(60)
