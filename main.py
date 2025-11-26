import matplotlib.pyplot as plt # для побудови графіків
import matplotlib.animation as animation # для анімації графіків
import numpy as np # для математичних операцій
import os # для роботи з файлами

# головні вбудовані функції
def sin_function(x): 
    return np.sin(x)

def cos_function(x): 
    return np.cos(x)

def tg_function(x): 
    return np.tan(x)

def ctg_function(x): 
    return 1/np.tan(x)

def log_function(x): 
    return np.log(x + 1e-6) # додано мале значення для уникнення log(0)

def absolute_function(x): 
    return np.abs(x)

def exponential_function(x): 
    return np.exp(x)

periodic_functions = ['sin', 'cos', 'tg', 'ctg'] # функції періодичні
growth_functions = ['log', 'abs', 'exp'] # функції зростаючі

# словник функцій
functions = {
    "sin": sin_function,
    "cos": cos_function,
    "tg": tg_function,
    "ctg": ctg_function,
    "log": log_function,
    "abs": absolute_function,
    "exp": exponential_function
}

TXT_FILE = "user_choices.txt" # назва TXT файлу

def read_txt(): # функція для читання TXT файлу
    if not os.path.exists(TXT_FILE):
        return []
    try: 
        with open(TXT_FILE, "r", encoding='utf-8') as file:
            lines = file.readlines()
            return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        return []

def get_user_choice(): # функція для отримання вибору користувача
    print("МЕНЮ:")
    print("1. Використати готову функцію (sin, cos, tg, ctg, log, abs, exp)")
    print("2. Ввести власну функцію від x")
    print("3. Обрати функцію з TXT")
    while True:
        choice = input("Введіть 1, 2 або 3: ").strip()
        if choice in ["1","2","3"]:
            return choice 
        else:
            print("Помилка: введіть 1, 2 або 3")

def save_static_plot(func, name, periodic_like=False): # функція для збереження статичного графіка

    fig, ax = plt.subplots(figsize=(10, 6)) 
    
    if periodic_like:
        x = np.linspace(-10, 10, 1000)
        y = func(x)
        y = np.where(np.abs(y) > 50, np.nan, y)
        ax.plot(x, y, linewidth=2)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-3, 3)
    else:
        if name == 'log':
            x = np.linspace(0.01, 10, 500)
        elif name == 'exp':
            x = np.linspace(-2, 5, 500)
        else:
            x = np.linspace(-10, 10, 500)
        
        y = func(x) if callable(func) else eval(func, {"np": np}, {"x": x})
        y = np.where(np.abs(y) > 50, np.nan, y)
        ax.plot(x, y, linewidth=2)
        ax.set_xlim(x[0], x[-1])
        ax.set_ylim(np.nanmin(y)-1, np.nanmax(y)+1)
    
    ax.set_title(f"Графік функції: {name}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    
    # Зберігаємо статичний графік
    filename = f"{name}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Графік збережено як: {filename}")
    plt.close(fig)  # Закриваємо figure для звільнення пам'яті

def animate_graph(func, name, periodic_like=False): # функція для анімації графіка
    if periodic_like:
        fig, ax = plt.subplots()
        x = np.linspace(-10, 10, 2000)
        y = func(x)
        y = np.where(np.abs(y) > 50, np.nan, y)
        line, = ax.plot(x, y)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-5, 5)
        ax.set_title(f"Анімація функції: {name}")
        phase = np.arange(0, 4*np.pi, 0.1)
        def update(frame):
            y_new = func(x + frame)
            y_new = np.where(np.abs(y_new) > 50, np.nan, y_new)
            line.set_ydata(y_new)
            return [line]
        ani = animation.FuncAnimation(fig, update, frames=phase, interval=30, blit=True, repeat=True)
        plt.show()
    else:
        fig, ax = plt.subplots()
        if name == 'log':
            x = np.linspace(0.01, 10, 500)
        elif name == 'exp':
            x = np.linspace(-2, 5, 500)
        else:
            x = np.linspace(-10, 10, 500)
        
        y = func(x) if callable(func) else eval(func, {"np": np}, {"x": x})
        y = np.where(np.abs(y) > 50, np.nan, y)
        line, = ax.plot([], [], lw=2)
        ax.set_xlim(x[0], x[-1])
        ax.set_ylim(np.nanmin(y)-1, np.nanmax(y)+1)
        ax.set_title(f"Анімація функції: {name}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        def update(frame):
            line.set_data(x[:frame], y[:frame])
            return [line]
        ani = animation.FuncAnimation(fig, update, frames=len(x), interval=20, blit=True, repeat=True)
        plt.show()

def main(): # головна функція
    choice_type = get_user_choice() # отримуємо вибір користувача

    if choice_type == "1":
        print("Доступні функції:", ", ".join(functions.keys()))
        while True:
            name = input("Введіть назву функції: ").strip().lower()
            if name in functions:
                # Спочатку зберігаємо статичний графік
                save_static_plot(functions[name], name, periodic_like=(name in periodic_functions))
                # Потім показуємо анімацію
                animate_graph(functions[name], name, periodic_like=(name in periodic_functions))
                break
            else:
                print("Такої функції немає.")
                
    elif choice_type == "2":
        while True:
            formula = input("Введіть формулу функції від x (наприклад: np.sin(x), x**2): ")
            try:
                # Перевіряємо формулу
                test_x = np.linspace(-10, 10, 5)
                test_result = eval(formula, {"np": np}, {"x": test_x})
                
                # Використовуємо саму формулу як ім'я
                name = "custom_function"
                
                # Спочатку зберігаємо статичний графік
                save_static_plot(formula, name, periodic_like=False)
                # Потім показуємо анімацію
                animate_graph(formula, name, periodic_like=False)
                break
                
            except NameError:
                print("Помилка: ви використали невідому функцію чи змінну.")
            except SyntaxError:
                print("Помилка синтаксису у формулі.")
            except ZeroDivisionError:
                print("Помилка: ділення на нуль у формулі.")
            except Exception as e:
                print("Інша помилка у формулі:", e)
                
    else:
        choice = read_txt()
        if not choice:
            print("TXT файл пустий. Повернення в меню.")
            main()
            return
            
        print("Функції з TXT файлу:")
        for idx, item in enumerate(choice, 1):
            print(f"{idx}. {item}")

        while True:
            try:
                sel = int(input(f"Виберіть номер (1-{len(choice)}): "))
                if sel < 1 or sel > len(choice):
                    raise ValueError("Номер поза діапазоном")
                selected = choice[sel-1]
                
                if selected in functions:
                    # Спочатку зберігаємо статичний графік
                    save_static_plot(functions[selected], selected, periodic_like=(selected in periodic_functions))
                    # Потім показуємо анімацію
                    animate_graph(functions[selected], selected, periodic_like=(selected in periodic_functions))
                else:
                    # Для користувацьких функцій з файлу
                    name = f"txt_function_{sel}"
                    # Спочатку зберігаємо статичний графік
                    save_static_plot(selected, name, periodic_like=False)
                    # Потім показуємо анімацію
                    animate_graph(selected, name, periodic_like=False)
                break
                
            except Exception as e:
                print("Помилка:", e)

if __name__ == "__main__":
    main()


