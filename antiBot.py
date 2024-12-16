from screeninfo import get_monitors
import pyautogui
import random as rand
import time

# Point of reference
# X: 828, Y: 757

# ReCapture Box
# DIMENSIONS: 35 by 35
# X: 820, Y: 755 Top Left
# X: 820, Y: 790 Bottom Left
# X: 855, Y: 790 Bottom Right
# X: 855, Y: 755 Top Right

monitors = get_monitors()
driverMonitor = monitors[0] # 1 for second monitor

mouseSpeed = (0.5, 1)

def debugMonitors():
    for i, info in enumerate(monitors):
        print(info)
        print(f"{monitors[i].width}x{monitors[i].height}")

def goToBox():
    boxPos = {"TL":(820, 755), "BR":(855, 790)}
    x = rand.randint(boxPos["TL"][0], boxPos["BR"][0])
    y = rand.randint(boxPos["TL"][1], boxPos["BR"][1])
    return x, y

def addnoise(max_pos, max_range):
    for i in range(rand.randint(1, max_range)):
        x, y = pyautogui.position()
        #print("current:", x, y)
        x_rand = x + rand.randint(0, max_pos)
        y_rand = y + rand.randint(0, max_pos)
        pyautogui.moveTo(driverMonitor.x+x_rand, driverMonitor.y+y_rand, duration=rand.uniform(*mouseSpeed))

def confirm():
    x, y = pyautogui.position()
    new_y = y + 110
    pyautogui.moveTo(driverMonitor.x+x, driverMonitor.y+new_y, duration=rand.uniform(*mouseSpeed))
    pyautogui.click()


def passReCapture():
    #debugMonitors()
    x_pos, y_pos = goToBox()
    print(x_pos, y_pos)
    addnoise(250, 3)
    pyautogui.moveTo(driverMonitor.x+x_pos, driverMonitor.y+y_pos, duration=rand.uniform(*mouseSpeed))
    time.sleep(rand.uniform(0, 1))
    pyautogui.click()
    confirm()
    addnoise(1000, 1)

# while True:
#     time.sleep(3)
#     passReCapture()