import cv2
import numpy as np
import pyautogui
import win32gui

# Define the name of the window to capture
window_name = "Knight OnLine Client"

hwnd = win32gui.FindWindow(None, window_name)
window_rect = win32gui.GetWindowRect(hwnd)
screen_width = window_rect[2]
screen_height = window_rect[3]

SKILL_RANGE_LIMIT = 280  # 60 Nova.

# Define the center and radius of the circular area
center_x = screen_width / 2
center_y = screen_height / 2

# Define the color of the circle (in BGR format)
circle_color = (0, 255, 0)  # Green

while True:
    # Get the current mouse position
    mouse_x, mouse_y = pyautogui.position()

    # Get the caster position (it's actually the center of the screen).
    caster_x, caster_y = screen_width // 2, screen_height // 2

    # Calculate the distance between the caster and the target
    distance = np.sqrt((mouse_x - caster_x) ** 2 + (mouse_y - caster_y) ** 2)

    # Check if the distance is within the skill range limit
    if distance <= SKILL_RANGE_LIMIT:
        # Print "Inside" if the distance is within the limit
        print("Inside")

        pyautogui.moveTo(mouse_x, mouse_y)
    else:
        # Print "Outside" if the distance is outside the limit
        print("Outside")

        # Calculate the normalized direction vector from the caster to the target
        dx = mouse_x - caster_x
        dy = mouse_y - caster_y
        direction = np.array([dx, dy]) / distance

        # Calculate the new mouse position at the edge of the limit
        new_x = int(caster_x + direction[0] * SKILL_RANGE_LIMIT)
        new_y = int(caster_y + direction[1] * SKILL_RANGE_LIMIT)

        # Move the mouse to the new position
        pyautogui.moveTo(new_x, new_y)

    screenshot = np.array(pyautogui.screenshot(region=window_rect))

    # Draw the skill range limit ellipse
    img = cv2.ellipse(screenshot, (caster_x, caster_y), (SKILL_RANGE_LIMIT, SKILL_RANGE_LIMIT), 0, 0, 360, (0, 255, 0),
                      2)

    cv2.imshow(window_name, img)

    # Wait for a key press to exit the script
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Clean up the window
cv2.destroyAllWindows()
