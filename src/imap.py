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
    
    def __check(self, list, other=None) -> str:
        value = len(list)
        values = []
        for num in range(value):
            try:
                if len(list[num]) == 6:
                    if list[num].isnumeric():
                        values.append(list[num])
                if other in list[num]:
                    container = ''
                    for word in list[num]:
                        try:
                            if word.isnumeric():
                                container += word      
                        except:
                            continue
                    
                    values.append(container)
            except:
                continue
        
        return values
    
    def __get_code(self) -> str:
        
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
            
            message = message_from_bytes(data[0][1])
            
            code_2FA_subject = list(message['Subject'].split())
            code_2FA_subject = self.__check(code_2FA_subject)[0]

            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                   bytes = part.get_payload(decode=True)
                   charset = part.get_content_charset('iso-8859-1')
                   chars = bytes.decode(charset, 'replace')
                   code_2FA_content = chars.split()
                   code_2FA_content = self.__check(code_2FA_content, other=code_2FA_subject)[0]
            
            if code_2FA_subject == code_2FA_content:
                code_2FA = code_2FA_content
                
        except IndexError:
            code_2FA = str('No New Code')
        except UnboundLocalError:
            code_2FA = str('Invalid Var')
        
        finally:
            return code_2FA
            
        
    def return_2FA(self):
        self.__select()
        return self.__get_code()
    
