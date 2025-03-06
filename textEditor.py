from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import showerror ,askyesnocancel
fileName = None
is_dark_mode = False  # Track the current theme state
font_size = 12  # Default font size

def newFile():
    global fileName
    fileName = "Untitled"
    text.delete(0.0, END)
    
def saveFile():
    global fileName
    if fileName is None:
        # If no filename yet, call saveAs() instead
        saveAs()
    else:
        # We have a filename, proceed with saving
        t = text.get(0.0, END)
        f = open(fileName, 'w')
        f.write(t)
        f.close()

def saveAs():
    global fileName
    file_types = [
        ('Text files', '*.txt'),
        ('Python files', '*.py'),
        ('HTML files', '*.html'),
        ('All files', '*.*')
    ]
    f = asksaveasfile(mode='w', defaultextension='.txt', filetypes=file_types)
    if f is not None:  # Only proceed if user didn't cancel
        t = text.get(0.0, END)
        try: 
            f.write(t.rstrip())
            fileName = f.name  # Update the global fileName
            f.close()
        except:
            showerror(title="Oops!", message="Unable to save file")

def openFile():
    file_types = [
        ('Text files', '*.txt'),
        ('Python files', '*.py'),
        ('HTML files', '*.html'),
        ('All files', '*.*')
    ]
    f = askopenfile(mode='r', filetypes=file_types)
    if f is not None:  # Only proceed if user didn't cancel
        t = f.read()
        text.delete(0.0, END)
        text.insert(0.0, t)
        fileName = f.name  # Update the global fileName
        
def exitApp():
    """Properly terminate the application after asking to save changes"""
    global fileName
    # Check if there's content in the editor
    if text.get(0.0, END).strip():
        # Get the title for the unsaved file
        title = fileName if fileName else "Untitled"
        # Ask user if they want to save changes
        response = askyesnocancel("Save Changes", f"Save changes to {title}?")
        
        # User selected Yes - save the file
        if response:
            saveFile()
        # User selected Cancel - abort exit
        elif response is None:
            return
        
    # Destroy the root window and terminate the program
    root.destroy()

# Add dark mode functions
def toggle_dark_mode():
    """Toggle between dark and light mode"""
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    apply_theme()

def apply_theme():
    """Apply the current theme to the UI elements"""
    if is_dark_mode:
        # Dark mode: black background, white text
        text.config(bg="black", fg="white", insertbackground="white")
        root.config(bg="black")
        text_frame.config(bg="black")
    else:
        # Light mode: white background, black text (default)
        text.config(bg="white", fg="black", insertbackground="black")
        root.config(bg="SystemButtonFace")
        text_frame.config(bg="SystemButtonFace")

# Add font size functions
def increase_font_size():
    """Increase the font size by 2 points"""
    global font_size
    font_size += 2
    apply_font_size()

def decrease_font_size():
    """Decrease the font size by 2 points but not below 8"""
    global font_size
    font_size = max(8, font_size - 2)  # Don't go below 8pt
    apply_font_size()

def reset_font_size():
    """Reset font size to default (12pt)"""
    global font_size
    font_size = 12
    apply_font_size()

def apply_font_size():
    """Apply the current font size to the text widget"""
    current_font = ("TkDefaultFont", font_size)
    text.config(font=current_font)
    
root = Tk()
root.title("Text Editor")
# Remove size restrictions to allow resizing
root.geometry("600x400")  # Set initial size instead of fixed size

# Create a frame for text widget and scrollbars
text_frame = Frame(root)
text_frame.pack(fill=BOTH, expand=True)

# Add scrollbars
scrollbar_y = Scrollbar(text_frame)
scrollbar_y.pack(side=RIGHT, fill=Y)

scrollbar_x = Scrollbar(text_frame, orient=HORIZONTAL)
scrollbar_x.pack(side=BOTTOM, fill=X)

# Configure text widget with scrollbars
text = Text(text_frame, wrap=NONE, font=("TkDefaultFont", font_size))
text.pack(side=LEFT, fill=BOTH, expand=True)

# Connect scrollbars to text widget
text.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
scrollbar_y.config(command=text.yview)
scrollbar_x.config(command=text.xview)

menubar = Menu(root)
filemenu = Menu(menubar)
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As", command=saveAs)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=exitApp)  # Changed to exitApp instead of root.quit
menubar.add_cascade(label="File", menu=filemenu)

# Add View menu for dark mode and font size
viewmenu = Menu(menubar)
viewmenu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)
viewmenu.add_separator()
viewmenu.add_command(label="Increase Font Size", command=increase_font_size)
viewmenu.add_command(label="Decrease Font Size", command=decrease_font_size)
viewmenu.add_command(label="Reset Font Size", command=reset_font_size)
menubar.add_cascade(label="View", menu=viewmenu)

# key binds

root.bind("<Control-n>", lambda e: newFile())
root.bind("<Control-o>", lambda e: openFile())
root.bind("<Control-s>", lambda e: saveFile())
root.bind("<Control-Shift-S>", lambda e: saveAs())
root.bind("<Control-q>", lambda e: exitApp())
root.bind("<Control-d>", lambda e: toggle_dark_mode())  # Add dark mode shortcut
# Font size shortcuts
root.bind("<Control-plus>", lambda e: increase_font_size())
root.bind("<Control-equal>", lambda e: increase_font_size())  # Alternative for plus
root.bind("<Control-minus>", lambda e: decrease_font_size())
root.bind("<Control-0>", lambda e: reset_font_size())

root.config(menu=menubar)
apply_theme()  # Apply the initial theme
# Initial font size is already set when creating the text widget
root.mainloop()
