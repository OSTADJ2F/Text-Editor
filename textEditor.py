from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import showerror

fileName = None

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
    
root = Tk()
root.title("Text Editor")
root.minsize(width=400, height=400)
root.maxsize(width=400, height=400)

text = Text(root, width=400, height=400)
text.pack()

menubar = Menu(root)
filemenu = Menu(menubar)
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As", command=saveAs)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


root.config(menu=menubar)
root.mainloop()
