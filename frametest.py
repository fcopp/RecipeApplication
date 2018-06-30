from tkinter import *
from PIL import Image, ImageTk

def main(root):
    cons = Frame(root)
    cons.grid()

    frameDict = setup_frames(cons)
    populate_frames(frameDict)

def setup_frames(cons):
    frame = {}
    # Parental Frames
    frame['a'] = Frame(cons, borderwidth=2, relief='groove')
    frame['b'] = Frame(cons, borderwidth=2, relief='groove')
    frame['c'] = Frame(cons, borderwidth=2, relief='groove')

    frame['a'].grid(row=0, column=0, sticky=N+S+E+W)
    frame['b'].grid(row=0, column=1, sticky=N+S+E+W)
    frame['c'].grid(row=1, column=0, columnspan=2)

    # Progeny 0 Frames:
    frame['b1'] = Frame(frame['b'], borderwidth=2, relief='groove')
    frame['b2'] = Frame(frame['b'], borderwidth=2, relief='groove')

    frame['b1'].grid(row=0, column=0, sticky=N+S+E+W)
    frame['b2'].grid(row=1, column=0, sticky=N+S+E+W)

    # Progeny 1 Frames:

    frame['b2a'] = Frame(frame['b2'], borderwidth=2, relief='groove',
                         background='green')
    frame['b2b'] = Frame(frame['b2'], borderwidth=2, relief='groove',
                         background='red')

    frame['b2a'].grid(row=0, column=0, sticky=S)
    frame['b2b'].grid(row=0, column=1, sticky=SW)

    # Weighting
    frame['b'].grid_rowconfigure(0, weight=1)
    frame['b'].grid_columnconfigure(0, weight=1)

    return frame

def populate_frames(fr):

    # Populating 'a' frame
    aLab = Label(fr['a'], image=img[0])
    aLab.grid()

    # Populating b2a & b2b frames
    bLab = Label(fr['b2a'], image=img[1])
    bLab.grid(row=0, column=0)

    bLab = Label(fr['b2b'], image=img[2])
    bLab.grid(row=0, column=1)

    # Populating c1 frame
    cLab = Label(fr['c'], image=img[3])
    cLab.grid()

if __name__ == '__main__':
    root = Tk()
    img = []
    w = [40,  160, 80, 480]
    h = [180, 60,  60, 60]
    for i in range(4):
        a = Image.new('RGBA', (w[i], h[i]))
        b = ImageTk.PhotoImage(a)
        img.append(b)
    main(root)