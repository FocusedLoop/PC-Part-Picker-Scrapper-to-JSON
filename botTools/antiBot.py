from screeninfo import get_monitors
import pyautogui
import random as rand
import time
from config.botSettings import BOT_SETTING

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

# Print monitor details
def debugMonitors():
    for i, info in enumerate(monitors):
        print(info)
        print(f"{monitors[i].width}x{monitors[i].height}")

# Send mouse to box position
def goToBox(boxPos):
    x = rand.randint(boxPos["TL"][0], boxPos["BR"][0])
    y = rand.randint(boxPos["TL"][1], boxPos["BR"][1])
    return x, y

# Send mouse to random postions on the screen
def addnoise(max_pos, max_range):
    for i in range(rand.randint(1, max_range)):
        x, y = pyautogui.position()
        #print("current:", x, y)
        x_rand = x + rand.randint(0, max_pos)
        y_rand = y + rand.randint(0, max_pos)
        pyautogui.moveTo(driverMonitor.x+x_rand, driverMonitor.y+y_rand, duration=rand.uniform(*BOT_SETTING['mouse_speed']))

# Press confirm box for ReCapture
def confirm():
    x, y = pyautogui.position()
    new_y = y + 110
    pyautogui.moveTo(driverMonitor.x+x, driverMonitor.y+new_y, duration=rand.uniform(*BOT_SETTING['mouse_speed']))
    pyautogui.click()

# Move mouse
def driveMouse(boxPos):
    x_pos, y_pos = goToBox(boxPos)
    #print(x_pos, y_pos)
    addnoise(250, 3)
    pyautogui.moveTo(driverMonitor.x+x_pos, driverMonitor.y+y_pos, duration=rand.uniform(*BOT_SETTING['mouse_speed']))
    time.sleep(rand.uniform(0, 1))
    pyautogui.click()

def passReCapture():
    #debugMonitors()
    boxPos = {"TL":BOT_SETTING['Re_box_position'][0], "BR":BOT_SETTING['Re_box_position'][1]}
    driveMouse(boxPos)
    confirm()
    addnoise(500, 1)

def passCloudFlare():
    boxPos = {"TL":BOT_SETTING['Cloud_box_position'][0], "BR":BOT_SETTING['Cloud_box_position'][1]}
    driveMouse(boxPos)
    addnoise(500, 1)

def testReCapture():
    while True:
        time.sleep(3)
        #passReCapture()
        passCloudFlare()

#testReCapture()