import tkinter as tk
from tkinter import messagebox
import random
import time
from pynput.mouse import Button, Controller
import threading
import keyboard
import webbrowser

# Инициализация мыши
mouse = Controller()

# Список валидных ключей (можно добавлять свои ключи сюда)
VALID_KEYS = [
    "GHJHJ-LDKSLF-EFWEDW",
    # Добавляйте свои ключи в таком формате:
    # "XXXXX-XXXXX-XXXXX",
    # "YYYYY-YYYYY-YYYYY",
]

# Глобальные переменные
clicking = False
key_binds = {"left_toggle": "f1", "right_toggle": "f2"}

# Глобальные переменные для управления
cps = None
mouse_button = None
hold_mode = None
anti_ban = None
left_button = None
right_button = None
status_label = None
cps_entry = None
cps_label = None
apply_button = None
cps_frame = None
change_button = None

# Цветовая палитра
BG_COLOR = "#1E1E2F"
CARD_COLOR = "#2A2A3D"
ACCENT_COLOR = "#6B5B95"
TEXT_COLOR = "#F5F5F5"
SECONDARY_TEXT = "#A0A0B0"
HOVER_COLOR = "#8874A3"

def toggle_clicking(side):
    global clicking
    if side == "left":
        if not clicking:
            clicking = True
            mouse_button.set("left")
            left_button.config(text="СТОП", bg="#FF6B6B")
            right_button.config(text="ПРАВАЯ", bg=ACCENT_COLOR)
            status_label.config(text="Кнопка: Left")
            threading.Thread(target=click_loop, daemon=True).start()
        else:
            clicking = False
            left_button.config(text="ЛЕВАЯ", bg=ACCENT_COLOR)
    elif side == "right":
        if not clicking:
            clicking = True
            mouse_button.set("right")
            right_button.config(text="СТОП", bg="#FF6B6B")
            left_button.config(text="ЛЕВАЯ", bg=ACCENT_COLOR)
            status_label.config(text="Кнопка: Right")
            threading.Thread(target=click_loop, daemon=True).start()
        else:
            clicking = False
            right_button.config(text="ПРАВАЯ", bg=ACCENT_COLOR)

def click_loop():
    if mouse_button is None or cps is None or hold_mode is None or anti_ban is None:
        return
    button_map = {"left": Button.left, "right": Button.right}
    selected_button = button_map[mouse_button.get()]
    base_delay = 1.0 / cps.get()

    if hold_mode.get():
        while clicking:
            mouse.press(selected_button)
            time.sleep(0.001)
            mouse.release(selected_button)
            delay = base_delay if not anti_ban.get() else base_delay * random.uniform(0.9, 1.1)
            time.sleep(max(0, delay - 0.001))
    else:
        while clicking:
            start_time = time.perf_counter()
            mouse.click(selected_button, 1)
            elapsed = time.perf_counter() - start_time
            delay = base_delay if not anti_ban.get() else base_delay * random.uniform(0.9, 1.1)
            time.sleep(max(0, delay - elapsed))

def check_key():
    entered_key = key_entry.get()
    if entered_key in VALID_KEYS:
        key_window.destroy()
        show_animation()
    else:
        messagebox.showerror("Ошибка", "Неверный ключ!")

def show_animation():
    anim_window = tk.Tk()
    anim_window.title("Загрузка")
    anim_window.geometry("350x200")
    anim_window.configure(bg=BG_COLOR)
    anim_window.overrideredirect(True)
    
    screen_width = anim_window.winfo_screenwidth()
    screen_height = anim_window.winfo_screenheight()
    x = (screen_width - 350) // 2
    y = (screen_height - 200) // 2
    anim_window.geometry(f"350x200+{x}+{y}")

    label = tk.Label(anim_window, text="DLLClicker\nby @dllhosts", font=("Arial", 16, "bold"), 
                    fg=ACCENT_COLOR, bg=BG_COLOR)
    label.pack(expand=True)

    def fade_out():
        alpha = 1.0
        while alpha > 0:
            alpha -= 0.05
            anim_window.attributes("-alpha", alpha)
            anim_window.update()
            time.sleep(0.05)
        anim_window.destroy()
        show_clicker()

    anim_window.after(1500, fade_out)
    anim_window.mainloop()

def check_updates():
    update_window = tk.Tk()
    update_window.overrideredirect(True)
    update_window.attributes("-alpha", 0.8)
    update_window.configure(bg="#000000")
    
    screen_width = update_window.winfo_screenwidth()
    screen_height = update_window.winfo_screenheight()
    window_width, window_height = 300, 150
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    update_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Фрейм для центрирования
    content_frame = tk.Frame(update_window, bg="#000000")
    content_frame.pack(expand=True)

    label = tk.Label(content_frame, text="Проверка обновлений", 
                    font=("Arial", 12), fg=TEXT_COLOR, bg="#000000")
    label.pack(pady=10)

    # Индикатор загрузки
    loading_label = tk.Label(content_frame, text="⠋", font=("Arial", 20), 
                           fg=ACCENT_COLOR, bg="#000000")
    loading_label.pack()

    def update_loading():
        symbols = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        while update_window.winfo_exists():
            loading_label.config(text=symbols[i % len(symbols)])
            update_window.update()
            time.sleep(0.1)
            i += 1

    def redirect():
        time.sleep(2)
        if update_window.winfo_exists():
            webbrowser.open("https://github.com/Erorrpython/DLLClicker-")
            update_window.destroy()

    threading.Thread(target=update_loading, daemon=True).start()
    update_window.after(0, redirect)
    update_window.mainloop()

def bind_key(action, label):
    def wait_for_key():
        keyboard.unhook_all()
        key = keyboard.read_key()
        key_binds[action] = key
        label.config(text=key.upper())
        update_binds()
    threading.Thread(target=wait_for_key, daemon=True).start()

def update_binds():
    keyboard.unhook_all()
    keyboard.on_press_key(key_binds["left_toggle"], lambda e: toggle_clicking("left"))
    keyboard.on_press_key(key_binds["right_toggle"], lambda e: toggle_clicking("right"))

def button_hover(event, button, enter=True):
    button.config(bg=HOVER_COLOR if enter else ACCENT_COLOR)

def show_clicker():
    global clicking, cps, mouse_button, hold_mode, anti_ban, left_button, right_button, status_label
    global cps_entry, cps_label, apply_button, cps_frame, change_button
    
    window = tk.Tk()
    window.title("DLLClicker")
    window.geometry("400x600")
    window.configure(bg=BG_COLOR)
    window.resizable(False, False)

    # Переменные
    cps = tk.DoubleVar(value=10.0)
    mouse_button = tk.StringVar(value="left")
    hold_mode = tk.BooleanVar(value=False)
    anti_ban = tk.BooleanVar(value=False)

    def update_cps():
        try:
            value = float(cps_entry.get())
            if 1 <= value <= 1000:
                cps.set(value)
                cps_label.config(text=f"{cps.get():.1f} CPS")
                cps_entry.pack_forget()
                apply_button.pack_forget()
                change_button.pack(side=tk.LEFT, padx=5)
            else:
                messagebox.showwarning("Ошибка", "CPS должен быть от 1 до 1000")
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите число")

    def show_cps_input():
        change_button.pack_forget()
        cps_entry.pack(side=tk.LEFT, padx=5)
        apply_button.pack(side=tk.LEFT, padx=5)

    # Заголовок
    header = tk.Label(window, text="DLLClicker", font=("Arial", 26, "bold"), 
                     fg=ACCENT_COLOR, bg=BG_COLOR)
    header.pack(pady=20)

    # Основной контейнер
    main_frame = tk.Frame(window, bg=BG_COLOR)
    main_frame.pack(padx=20, pady=10, fill="both")

    # CPS настройка
    cps_card = tk.Frame(main_frame, bg=CARD_COLOR, bd=0, relief="flat")
    cps_card.pack(fill="x", pady=5)
    
    tk.Label(cps_card, text="Скорость кликов", font=("Arial", 12, "bold"), 
            fg=TEXT_COLOR, bg=CARD_COLOR).pack(pady=5)
    
    cps_frame = tk.Frame(cps_card, bg=CARD_COLOR)
    cps_frame.pack(pady=5)
    
    cps_entry = tk.Entry(cps_frame, width=8, font=("Arial", 12), 
                        bg="#363650", fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                        relief="flat", justify="center")
    cps_entry.insert(0, "10.0")
    cps_entry.pack(side=tk.LEFT, padx=5)
    
    apply_button = tk.Button(cps_frame, text="✓", command=update_cps, 
                           bg=ACCENT_COLOR, fg=TEXT_COLOR, 
                           font=("Arial", 12, "bold"), relief="flat", width=3)
    apply_button.pack(side=tk.LEFT, padx=5)
    
    change_button = tk.Button(cps_frame, text="✎", command=show_cps_input,
                            bg="#363650", fg=TEXT_COLOR, font=("Arial", 12),
                            relief="flat", width=3)
    
    cps_label = tk.Label(cps_card, text="10.0 CPS", font=("Arial", 12), 
                        fg=SECONDARY_TEXT, bg=CARD_COLOR)
    cps_label.pack(pady=5)

    # Настройки
    settings_card = tk.Frame(main_frame, bg=CARD_COLOR, bd=0, relief="flat")
    settings_card.pack(fill="x", pady=5)
    
    tk.Checkbutton(settings_card, text="Режим удержания", variable=hold_mode,
                  font=("Arial", 11), fg=TEXT_COLOR, bg=CARD_COLOR,
                  selectcolor="#363650", activebackground=CARD_COLOR).pack(pady=5, padx=10, anchor="w")
    
    tk.Checkbutton(settings_card, text="Анти-бан", variable=anti_ban,
                  font=("Arial", 11), fg=TEXT_COLOR, bg=CARD_COLOR,
                  selectcolor="#363650", activebackground=CARD_COLOR).pack(pady=5, padx=10, anchor="w")

    # Кнопки управления
    buttons_frame = tk.Frame(main_frame, bg=BG_COLOR)
    buttons_frame.pack(pady=15)
    
    left_button = tk.Button(buttons_frame, text="ЛЕВАЯ", command=lambda: toggle_clicking("left"),
                           font=("Arial", 12, "bold"), bg=ACCENT_COLOR,
                           fg=TEXT_COLOR, relief="flat", width=10)
    left_button.pack(side=tk.LEFT, padx=5)
    left_button.bind("<Enter>", lambda e: button_hover(e, left_button, True))
    left_button.bind("<Leave>", lambda e: button_hover(e, left_button, False))
    
    right_button = tk.Button(buttons_frame, text="ПРАВАЯ", command=lambda: toggle_clicking("right"),
                            font=("Arial", 12, "bold"), bg=ACCENT_COLOR,
                            fg=TEXT_COLOR, relief="flat", width=10)
    right_button.pack(side=tk.LEFT, padx=5)
    right_button.bind("<Enter>", lambda e: button_hover(e, right_button, True))
    right_button.bind("<Leave>", lambda e: button_hover(e, right_button, False))

    # Статус
    status_label = tk.Label(main_frame, text="Кнопка: Left", font=("Arial", 10),
                          fg=SECONDARY_TEXT, bg=BG_COLOR)
    status_label.pack(pady=5)

    # Горячие клавиши
    binds_card = tk.Frame(main_frame, bg=CARD_COLOR, bd=0, relief="flat")
    binds_card.pack(fill="x", pady=5)
    
    tk.Label(binds_card, text="Горячие клавиши", font=("Arial", 12, "bold"),
            fg=TEXT_COLOR, bg=CARD_COLOR).pack(pady=5)
    
    # Левый бинд
    left_bind_frame = tk.Frame(binds_card, bg=CARD_COLOR)
    left_bind_frame.pack(pady=2)
    
    tk.Label(left_bind_frame, text="Левая:", font=("Arial", 11),
            fg=TEXT_COLOR, bg=CARD_COLOR, width=8).pack(side=tk.LEFT)
    
    left_key_label = tk.Label(left_bind_frame, text="F1", font=("Arial", 11),
                            fg=TEXT_COLOR, bg=CARD_COLOR, width=8)
    left_key_label.pack(side=tk.LEFT, padx=5)
    
    tk.Button(left_bind_frame, text="✎", 
             command=lambda: bind_key("left_toggle", left_key_label),
             bg="#363650", fg=TEXT_COLOR, font=("Arial", 12), relief="flat", width=3).pack(side=tk.LEFT)

    # Правый бинд
    right_bind_frame = tk.Frame(binds_card, bg=CARD_COLOR)
    right_bind_frame.pack(pady=2)
    
    tk.Label(right_bind_frame, text="Правая:", font=("Arial", 11),
            fg=TEXT_COLOR, bg=CARD_COLOR, width=8).pack(side=tk.LEFT)
    
    right_key_label = tk.Label(right_bind_frame, text="F2", font=("Arial", 11),
                              fg=TEXT_COLOR, bg=CARD_COLOR, width=8)
    right_key_label.pack(side=tk.LEFT, padx=5)
    
    tk.Button(right_bind_frame, text="✎", 
             command=lambda: bind_key("right_toggle", right_key_label),
             bg="#363650", fg=TEXT_COLOR, font=("Arial", 12), relief="flat", width=3).pack(side=tk.LEFT)

    # Кнопка проверки обновлений
    update_button = tk.Button(window, text="Проверить обновления",
                            font=("Arial", 10), bg=ACCENT_COLOR, fg=TEXT_COLOR,
                            relief="flat", command=check_updates)
    update_button.pack(pady=5)
    update_button.bind("<Enter>", lambda e: button_hover(e, update_button, True))
    update_button.bind("<Leave>", lambda e: button_hover(e, update_button, False))

    # Подпись
    tk.Label(window, text="Created by @dllhosts", font=("Arial", 9),
            fg=SECONDARY_TEXT, bg=BG_COLOR).pack(pady=10)

    update_binds()
    window.mainloop()

# Окно ввода ключа
key_window = tk.Tk()
key_window.title("Активация")
key_window.geometry("350x200")
key_window.configure(bg=BG_COLOR)
key_window.resizable(False, False)

tk.Label(key_window, text="DLLClicker", font=("Arial", 20, "bold"),
        fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=10)

entry_frame = tk.Frame(key_window, bg=BG_COLOR)
entry_frame.pack(pady=10)

key_entry = tk.Entry(entry_frame, font=("Arial", 12), width=25,
                    bg="#363650", fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                    relief="flat", justify="center")
key_entry.pack(pady=5)

tk.Button(entry_frame, text="Активировать", command=check_key,
         font=("Arial", 12), bg=ACCENT_COLOR, fg=TEXT_COLOR,
         relief="flat", width=15).pack(pady=10)

tk.Label(key_window, text="Ключ у @dllhosts", font=("Arial", 10),
        fg=SECONDARY_TEXT, bg=BG_COLOR).pack()

key_window.mainloop()