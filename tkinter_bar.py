import tkinter as tk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import(FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

root = tk.Tk()
root.wm_title('Monthly Visual Data Representation')

figure = Figure(figsize = (6,4), dpi = 100)
canvas = FigureCanvasTkAgg(figure, master = root)

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack(fill = 'both', expand = True)

axes = figure.add_subplot(1,1,1)
axes.set_xlabel('Destinations')
axes.set_ylabel('Number of Visits')

numbers = (1,2,3,4,5,6,7,8,8,2,1)
places = ('ABV','LOS','DXB','LHR','LON','TKY','JAP','ABC','UAE','SAU','OPO')

axes.bar(places, numbers, align = 'center')

tk.mainloop()
