def new_userpage():
    import tkinter as tk
    from tkinter.messagebox import showinfo,showerror

    def creation():
        add_file()
        showinfo(title = 'New user', message = 'New account created successfully!')
        back_ben()

    def update():
        root2.after(1000, update)
        if user_entry.get() != '' and pswd_entry.get() != '' and pswdc_entry.get() != '':
            create.configure(state = tk.NORMAL)

    def back_ben():
        root2.destroy()
        from Ben_Project import ben
        ben()

    def add_file():
        if pswd_entry.get() == pswdc_entry.get() != '':
            f = open('Ben.txt', 'a')
            print(user_entry.get(), file = f)
            print(pswd_entry.get(), file = f)
            f.close()
                       
    root2 = tk.Tk()

    root2.title('Create New User Account')

    user_label = tk.Label(text = 'Create a new username: ')
    pswd_label = tk.Label(text = 'Password: ')
    pswdc_label = tk.Label(text = 'Confirm Password: ')
    create_label = tk.Label(font = ('Verdana', 16))

    user_entry = tk.Entry(font = ('Verdana', 16), width = 16)
    pswd_entry = tk.Entry(font = ('Verdana', 16), width = 16)
    pswdc_entry = tk.Entry(font = ('Verdana', 16), width = 16)

    create = tk.Button(text = 'Create',state = tk.DISABLED, command = creation)

    user_label.grid(row = 2, column = 0)
    user_entry.grid(row = 2, column = 1)
    pswd_label.grid(row = 3, column = 0)
    pswd_entry.grid(row = 3, column = 1)
    pswdc_label.grid(row = 4, column = 0)
    pswdc_entry.grid(row = 4, column = 1)
    create_label.grid(row = 6, column = 1)
    create.grid(row = 5, column = 1)

    update()

    tk.mainloop()

if __name__ == '__main__':
    new_userpage()
