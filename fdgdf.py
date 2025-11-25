import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Створення фігури
fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 400)
line, = ax.plot(x, np.sin(x))

ax.set_title("Анімація синусоїди (Animation)")
ax.set_xlabel("x")
ax.set_ylabel("sin(x)")
ax.set_ylim(-1.2, 1.2)
ax.grid(True)

# Функція оновлення кадрів
def update(frame):
    line.set_ydata(np.sin(x + frame / 10))
    return line,

# Створення анімації
ani = FuncAnimation(fig, update, frames=200, interval=30, blit=True)

plt.show()
