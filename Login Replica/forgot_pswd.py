def forgot():
    import tkinter as tk
    from tkinter.messagebox import showinfo

    def reset():
        showinfo(title = 'Password Reset', message = 'Password Reset Link has been sent to your mail!')
        back_ben()
    
    def update():
        root3.after(1000, update)
        if email_entry.get() != '':
            send.configure(state = tk.NORMAL)

    def back_ben():
        root3.destroy()
        from Ben_Project import ben
        ben()

    root3 = tk.Tk()

    root3.title('Password Reset')

    email_label = tk.Label(text = 'Type in your email address: ')
    email_entry = tk.Entry()

    send = tk.Button(text = 'Send',state = tk.DISABLED, command = reset)
    email_entry.cget('text')

    email_label.grid(row = 1, column = 0)
    email_entry.grid(row = 1, column = 1)
    send.grid(row = 2, column = 1)

    update()

    tk.mainloop()

if __name__ == '__main__':
    forgot()
