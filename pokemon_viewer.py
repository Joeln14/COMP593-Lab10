import ctypes
import os 
from tkinter import *
from tkinter import ttk
import poke_api
import image_lib
from PIL import ImageTk 

# Set the script path and directory as variables 
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# Create the image cache directory if it does not exist
image_cache_dir = os.path.join(script_dir, 'images')
if not os.path.isdir(image_cache_dir):
    os.makedirs(image_cache_dir)


# Create the GUI window
root = Tk()
root.title("Pokemon Image Viewer")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.minsize(500, 600)

# Seth the GUI icon and task bar icon to a Poke ball
icon_path = os.path.join(script_dir, 'Poké_Ball_icon.svg.ico')
app_id = 'COMP593.PokeImageViewer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
root.iconbitmap(icon_path)


# Make gui frame
frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky=NSEW)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

# Add image into frame
image_path = os.path.join(script_dir, 'poke_logo.png')
img_poke = PhotoImage(file=image_path)

lbl_image = ttk.Label(frame, image=img_poke)
lbl_image.grid(padx=10, pady=10)

# Add the pull-down of pokemon names in the frame and handle event
poke_name_list = sorted(poke_api.get_pokemon_names())
cbox_poke_names = ttk.Combobox(frame, values=poke_name_list, state='readonly')
cbox_poke_names.set("Select a Pokémon")
cbox_poke_names.grid(padx=10, pady=10)

def handle_poke_sel(event):

    btn_set_desktop.state(['!disabled'])
    sel_pokemon = cbox_poke_names.get()
    global image_path
    image_path = poke_api.download_poke_artwork(sel_pokemon, image_cache_dir)
    img_poke['file'] = image_path

    return

cbox_poke_names.bind('<<ComboboxSelected>>', handle_poke_sel)


#Put 'Set desktop' button in frame and disable the button

def handle_set_desktop():
    image_lib.set_desktop_background_image(image_path)


btn_set_desktop = ttk.Button(frame, text='Set as Desktop Image', command=handle_set_desktop)
btn_set_desktop.grid(padx=10, pady=10)
btn_set_desktop.state(['disabled'])




root.mainloop()