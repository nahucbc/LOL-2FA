from imap import Mail
from tkinter import DISABLED, NORMAL, Tk, messagebox, Toplevel
from tkinter import ttk
from PIL import Image
from pystray import MenuItem as item
import pystray
import pyperclip

class Interface():
    def __init__(self) -> None:
        self.__root = Tk()
        self.__config()
        self.__widgets()
        self.__grid()
        self.__root.mainloop()
        
    def __config(self) -> None:
        self.__root.resizable(False, False)
        self.__root.title('2FA')
        self.__root.protocol('WM_DELETE_WINDOW', self.__hide)
        self.__any_account = False
        
    def __widgets(self):
        self.__host_label = ttk.Label(text='Server')
        self.__port_label = ttk.Label(text='Port')
        self.__email_label = ttk.Label(text='Email')
        self.__password_label = ttk.Label(text='Password Third-Party')
        
        self.__host_entry = ttk.Entry()
        self.__port_entry = ttk.Entry()
        self.__email_entry = ttk.Entry()
        self.__password_entry = ttk.Entry()
        
        self.__add = ttk.Button(text='Add', state=NORMAL, command=self.__add_set)
        self.__check = ttk.Button(text='Check', state=DISABLED, command=self.__check_get)
    
    def __grid(self):
        self.__host_label.grid(column=0, row=0)
        self.__host_entry.grid(column=0, row=1)
        self.__port_label.grid(column=0, row=2)
        self.__port_entry.grid(column=0, row=3)
        
        self.__email_label.grid(column=1, row=0)
        self.__email_entry.grid(column=1, row=1)
        self.__password_label.grid(column=1, row=2)
        self.__password_entry.grid(column=1, row=3)
        
        self.__add.grid(column=2, row=1)
        self.__check.grid(column=2, row=3)
        
    def __add_set(self):
        self.__source = Mail(host=self.__host_entry.get(),
                      port=self.__port_entry.get(),
                      user=self.__email_entry.get(),
                      password=self.__password_entry.get())
        self.__check['state'] = NORMAL
        self.__any_account = True
        
    def __check_get(self, dialog=None):
        if self.__any_account == True:
            self.__code = self.__source.return_2FA()
            if  dialog == None:
                messagebox.showinfo(title='Code', message=self.__code)
            if self.__source.is_code(self.__code):
                pyperclip.copy(self.__code)
                
        elif self.__any_account == False:
            messagebox.showinfo(title='Code', message='There are not any account, add any')

            
    #System Tray
    def __hide(self):
        self.__root.withdraw()
        menu=(item('Check', self.__check_get), item('Show', self.__show), item('Quit', self.__quit))
        self.__icon =  pystray.Icon(name='LOL-2FA' ,title='LOL-2FA', icon=Image.open('hide.ico'), menu=menu)
        self.__icon.run()
    
    def __show(self):
        self.__icon.stop()
        self.__root.after(0, self.__root.deiconify())
    
    def __quit(self):
        self.__icon.stop()
        self.__root.destroy()

    
if __name__ == '__main__':
    desktop = Interface()