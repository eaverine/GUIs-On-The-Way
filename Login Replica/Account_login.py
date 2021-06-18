def ben():
    import tkinter as tk
    from tkinter.messagebox import showinfo, showerror

    def open_newuser():
        root1.destroy()
        from new_user import new_userpage
        new_userpage()

    def open_forgotpswd():
        root1.destroy()
        from forgot_pswd import forgot
        forgot()

    def check_validity():
        user = user_entry.get()
        pswd = pswd_entry.get()
        file = open('Ben.txt', 'r')
        

    root1 = tk.Tk()

    root1.title('Account Login')

    user_label = tk.Label(text = 'Enter your username: ')
    pswd_label = tk.Label(text= 'Enter your password: ')

    login_button = tk.Button(text = 'Login', command  = check_validity)

    user_entry = tk.Entry(font = ('Verdana', 16), width = 16)
    pswd_entry = tk.Entry(font = ('Verdana', 16), width = 16)

    forgot_pswd = tk.Button(text = 'Forgot Password?', command = open_forgotpswd)

    show_pswd = tk.IntVar()
    show = tk.Checkbutton(text = 'Show Password?', var = show_pswd)

    new = tk.Button(text = 'Create An Account', command = open_newuser)

    user_label.grid(row = 0, column = 0)
    pswd_label.grid(row = 1, column = 0)
    login_button.grid(row = 3, column=1)
    user_entry.grid(row=0, column = 1)
    pswd_entry.grid(row = 1, column = 1)
    forgot_pswd.grid(row = 1, column = 2)
    show.grid(row = 2, column = 1)
    new.grid(row = 2, column = 2, columnspan = 2)

    tk.mainloop()

if __name__ == '__main__':
    ben()
