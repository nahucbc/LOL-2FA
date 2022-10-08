from imaplib import IMAP4_SSL 
from email import message_from_bytes

class Mail:
    
    def __init__(self,
                 host=str,
                 port=int,
                 user=str,
                 password=str) -> None:
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__server()
        self.__login()

    def __server(self) -> None:
        self.__mail = IMAP4_SSL(host=str(self.__host), port=int(self.__port)) # connect to imap server
        return
    
    def __login(self) -> None:
        self.__mail.login(user=self.__user, password=self.__password) # login with user and password
        return
    
    def __select(self) -> None:
        self.__mail.select('INBOX') # select inbox
        return
    
    def __get_code(self) -> int:
        
        _, msgnums = self.__mail.search(None, 
                                 'UNSEEN', 
                                 'FROM', 
                                 '<noreply@mail.accounts.riotgames.com>') # search message from riot games
        
        latest_number = (list(  # convert it to list
            reversed( # reverse all 
                msgnums[0] # number zero of the reversed list 
                .split() # split it 
                )))
        
        try:
            
            _, data = self.__mail.fetch(latest_number[0],
                             '(RFC822)') # get message from latest_number
            
            code_2FA = (message_from_bytes(data[0][1]) # convert
                .get('Subject')# get subject From Message
                .split() # split it 
                [1] # get part two of split where is the code-2FA
                )
            
        except IndexError:
            code_2FA = str('no new code')
        except UnboundLocalError:
            code_2FA = str('invalid var')
        
        return code_2FA 
    
    def return_2FA(self):
        self.__select()
        return self.__get_code()
    
