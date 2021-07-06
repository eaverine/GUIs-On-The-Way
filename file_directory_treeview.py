import tkinter as tk
from tkinter import ttk
from pathlib import Path

root = tk.Tk()

paths = Path('.').glob('**/*')

tv = ttk.Treeview(root, columns = ['size', 'modified'], selectmode = 'browse')
tv.heading('#0', text = 'Name', command = lambda: sort(tv, '#0') )
tv.heading('size', text = 'Size', anchor = 'center', command = lambda: sort(tv, 'size') )
tv.heading('modified', text = 'Modified', anchor = 'e', command = lambda: sort(tv, 'modified') )

tv.column('#0', stretch = True)
tv.column('size', width = 200)

tv.pack(expand = True, fill = 'both')

# mytreeview.insert(parent, 'end', iid = 'item1', text = 'My Item 1', values = ['12', '42'] )

for path in paths:
    meta = path.stat()
    parent = str(path.parent)

    if parent == '.':
        parent = ''

    tv.insert(parent, 'end', iid = str(path), text = str(path.name), values = [meta.st_size, meta.st_mtime] )
                  
def sort(tv,col):
    itemlist = list(tv.get_children(''))
    itemlist.sort(key = lambda x: tv.set(x,col))
    for index, iid in enumerate(itemlist):
        tv.move(iid, tv.parent(iid), index)


root.mainloop()
