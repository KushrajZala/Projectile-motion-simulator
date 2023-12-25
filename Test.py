import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from matplotlib.widgets import Button
import easygui

def get_user_input():
    msg = "Enter the values for projectile motion:"
    title = "Projectile Motion Simulation"
    field_names = ["Velocity", "Angle"]
    field_values = easygui.multenterbox(msg, title, field_names)
    
    while True:
        if field_values is None:
            break
            
        errmsg = ""
        for i in range(len(field_names)):
            if field_values[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % field_names[i])
                
        if errmsg == "":
            break
            
        field_values = easygui.multenterbox(errmsg, title, field_names, field_values)
    
    return field_values

def animate(i, line, v, theta, time_array):
    line.set_xdata(v * np.cos(theta) * (time_array + i / 100.0))
    line.set_ydata(v * np.sin(theta) * (time_array + i / 100.0) - (0.5) * g * (time_array + i / 100.0)**2)
    

    trail_length = 0.5  
    trail_index = max(0, i - int(trail_length * 100))
    line.set_markerfacecolor('none')
    line.set_markersize(4)
    line.set_markevery(10) 
    line.set_xdata(v * np.cos(theta) * (time_array[trail_index:i + 1] + i / 100.0))
    line.set_ydata(v * np.sin(theta) * (time_array[trail_index:i + 1] + i / 100.0) - (0.5) * g * (time_array[trail_index:i + 1] + i / 100.0)**2)
    
    return line

def on_zoom_in(event):
    ax.set_xlim(ax.get_xlim()[0] * 0.9, ax.get_xlim()[1] * 0.9)
    ax.set_ylim(ax.get_ylim()[0] * 0.9, ax.get_ylim()[1] * 0.9)
    plt.draw()

def on_zoom_out(event):
    ax.set_xlim(ax.get_xlim()[0] * 1.1, ax.get_xlim()[1] * 1.1)
    ax.set_ylim(ax.get_ylim()[0] * 1.1, ax.get_ylim()[1] * 1.1)
    plt.draw()

field_values = get_user_input()
print("Reply was:", field_values)

if field_values is not None:
   
    v = float(field_values[0])
    theta = float(field_values[1])
    

    g = 9.81
    t = 2 * v * np.sin(np.radians(theta)) / g
    r_for_h = v * np.cos(np.radians(theta)) * (t / 2)
    h = ((v**2) * (np.sin(np.radians(theta))**2)) / (2 * g)
    r = (v**2) * np.sin(2 * np.radians(theta)) / g
    
    
    sns.set()
    fig, ax = plt.subplots(figsize=(10, 6))
    time_text = "Flight Time: {:.2f}s".format(t)
    h_point = "Highest Point: {:.2f}m".format(h)
    range_projectile = "Range: {:.2f}m".format(r)
    plt.plot(r, 0, 'go', label='Projectile End')
    plt.plot(r_for_h, h, 'ro', label='Highest Point')  
    plt.text(r_for_h + 1, h + 1, h_point)
    plt.text(r + 1, 1, range_projectile)
    plt.text(r_for_h + 1, h + 2.5, time_text)

   
    time_array = np.arange(0, t, 0.01)
    x = np.arange(0, t, 0.01)

    
    line, = ax.plot(x, v * np.sin(np.radians(theta)) * x - (0.5) * g * x**2, label='Projectile')

    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.xlabel('Distance (x)')
    plt.ylabel('Distance (y)')
    plt.legend()
    plt.title('Projectile Motion Simulation')
    ax.set_autoscale_on(False)


    num_frames = int(t * 100) if t > 0 else 1
    ani = animation.FuncAnimation(fig, animate, frames=np.arange(1, num_frames + 1),
                                  fargs=(line, v, np.radians(theta), time_array), interval=20)


    ax_zoom_in = plt.axes([0.85, 0.01, 0.1, 0.04])
    ax_zoom_out = plt.axes([0.75, 0.01, 0.1, 0.04])
    button_zoom_in = Button(ax_zoom_in, 'Zoom In')
    button_zoom_out = Button(ax_zoom_out, 'Zoom Out')

    button_zoom_in.on_clicked(on_zoom_in)
    button_zoom_out.on_clicked(on_zoom_out)

    plt.show()




