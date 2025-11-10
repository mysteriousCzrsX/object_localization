import tkinter as tk
import math
import serial
import random
import time

# Configuration parameters
PORT = "COM3"   # serial port
BAUD = 9600     # baud rate
DIST = 22       # distance between sensors in cm
HEIGHT = 27     # height of sensors from the ground in cm

CALIB_P1 = (125, 480, 90, 0)   # (Vmin, Vmax, alfa_min, alfa_max) 
CALIB_P2 = (100, 835, 0, 180)    

# Scale value to angle
def map_to_angle(_value, _Vmin, _Vmax, _Amin, _Amax):
    return (_Amin + (_value - _Vmin) * (_Amax - _Amin) / (_Vmax - _Vmin))

# Calculate object position based on angles and distance
def calc_position(a1_deg, a2_deg, d = DIST):
    a1 = math.radians(a1_deg)
    a2 = math.radians(a2_deg)
    a3_deg = 180 - a1_deg - a2_deg
    a3 = math.radians(a3_deg)

    # Check if angles form a valid triangle
    if a3_deg <= 0 or math.isclose(math.sin(a1 + a2), 0, abs_tol=1e-9):
        print("Invalid triangle: angles do not form a triangle.")
        return None, None
    
    # Distances from sensors to object
    a = d * math.sin(a1) / math.sin(a3) # Distance from sensor 2 (right) to object
    b = d * math.sin(a2) / math.sin(a3) # Distance from sensor 1 (left) to object

    # Check if distances can form a triangle
    if a + b <= d or abs(a - b) >= d:
        print("Invalid triangle: sides cannot form a triangle.")
        return None, None
    
    x = (b**2 - a**2 + d**2) / (2 * d)
    y_sq = a**2 - x**2
    if y_sq < 0:
        print("Invalid triangle: computed y^2 is negative.")
        return None, None
    y = math.sqrt(y_sq)
    return x, y

#Canvas functions
def clear_canvas():
    canvas.delete("all")
    global obj
    obj = canvas.create_oval(0, 0, 10, 10, fill="red")

def start_drawing():
    global drawing
    drawing = True

def stop_drawing():
    global drawing
    drawing = False

# Update function to read serial data and update position
def update():
    global last_x, last_y
    #testing = 1
    if ser and ser.in_waiting: # testing:
        try:
            line = ser.readline().decode().strip()
            v1, v2 = map(int, line.split(','))

            # For testing without serial input      
            # v1 = random.randint(125, 480)
            # v2 = random.randint(100, 835)

            a1 = map_to_angle(v1, *CALIB_P1)
            a2 = map_to_angle(v2, *CALIB_P2)

            x, y = calc_position(a1, a2)

            if x is not None:
                # Scale coordinates to fit canvas
                xscale = canvas_width / DIST
                cx = x * xscale
                #Tkinter canvas has its origin at the top-left and y increases downward, so invert y
                yscale = canvas_height / HEIGHT
                cy = canvas_height - y * yscale

                # Update object position
                # +/-5 makes a 10x10 pixel dot with center at (cx,cy).
                canvas.coords(obj, cx-5, cy-5, cx+5, cy+5)

                # Draw line if drawing is enabled
                if drawing and last_x is not None:
                    canvas.create_line(last_x, last_y, cx, cy, fill="blue", width=2)

                last_x, last_y = cx, cy

        except Exception as e:
            print("Error occurred:", e)

    root.after(100, update)

# Setup GUI
def setup_gui():
    global root, canvas, canvas_width, canvas_height, obj, drawing, last_x, last_y

    root = tk.Tk()
    root.title("Object Localization Visualization")

    canvas_width = 500
    canvas_height = 400

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack(padx=10, pady=10)

    obj = canvas.create_oval(0, 0, 10, 10, fill="red")
    last_x, last_y = None, None
    drawing = False

    frame = tk.Frame(root)
    frame.pack()
   
    btn_clear = tk.Button(frame, text="Clear", command=clear_canvas)
    btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

    btn_start = tk.Button(frame, text="Start Drawing", command=start_drawing)
    btn_start.pack(side=tk.LEFT, padx=5, pady=5)

    btn_stop = tk.Button(frame, text="Stop Drawing", command=stop_drawing)
    btn_stop.pack(side=tk.LEFT, padx=5, pady=5)

# Setup serial connection
def setup_serial():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        print(f" Connected to {PORT} at {BAUD} baud.")
    except Exception as e:
        print("Error during connection:", e)
        ser = None
    return ser

# Main execution
if __name__ == "__main__":
    setup_gui()
    ser = setup_serial()
    update()
    root.mainloop()