import getpass
import json
from time import sleep
import colorama
import requests
from colorama import Fore, Style
import colors

colorama.init()

class InstagramUnfollow:
    print(Fore.BLUE+"""
       _______  ____________  ___   ________________  ____ 
      / ____/ |/ /_  __/ __ \/   | / ____/_  __/ __ \/ __ \\
     / __/  |   / / / / /_/ / /| |/ /     / / / / / / /_/ /
    / /___ /   | / / / _, _/ ___ / /___  / / / /_/ / _, _/ 
   /_____//_/|_|/_/ /_/ |_/_/  |_\____/ /_/  \____/_/ |_|                     
    
    
    """+Fore.RESET)
    def __init__(self):
        self.headers = {
		"Accept": "*/*",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "en-US",
		"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 123.1.0.26.115 (iPhone11,8; iOS 13_3; en_US; en-US; scale=2.00; 828x1792; 190542906)",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"X-IG-Capabilities": "3brTvw==",
		"X-IG-Connection-Type": "WIFI",
		}
        self.session = requests.session()
        self.url = "https://i.instagram.com"
        self.API = "/api/v1"
    def Start(self):
        
        self.get_csrf()
        self.Login()

    def get_csrf(self):
        try:
            self.session.headers = self.headers
            self.session.headers.update({'Referer': self.url})
            getcsrf = self.session.get(self.url)
            self.csrf = getcsrf.cookies['csrftoken']
            self.session.headers.update({'X-CSRFToken': self.csrf})
        except Exception as e:
            print(Fore.RED + '\r                         Unknown Error.',e)
        except KeyboardInterrupt:
            print(Fore.RED + '\r                         Process has been cancelled')

    def Login(self):
        ASK = True
        try:
            while ASK:
                self.account = self.session.post(self.url + "/accounts/login/ajax/", data={"username":'',"password":''}, allow_redirects=True)
                self.LoginData = self.account.json()
                if self.LoginData['authenticated'] == True:
                    break
                elif self.LoginData['authenticated'] == False:
                    print(f"{Fore.RED}         username or password is wrong.")
            self.GetUsersInfo()
        except Exception as e:
            print(Fore.RED + '\r                         Unknown Error.', e)
        except KeyboardInterrupt:
            print(Fore.RED + '\r                         Process has been cancelled.')
    
    def status(self):
        print(f"{Fore.BLUE}Emails:                         {Fore.BLUE}{len(self.EMAILS)}{Fore.RESET}")
        print(f"{Fore.BLUE}Users :                         {Fore.BLUE}{len(self.users)}{Fore.RESET}")

    def GetUsersInfo(self):
        try:
            self.get_csrf()
            self.EMAILS = []
            with open('list.txt','r') as f:
                i = 1
                lines = [x.rstrip('\n') for x in f]
                print(Fore.LIGHTWHITE_EX+'                         Downloading...\n')
                self.publicEmail = ''
                num = 0
                self.users = []
                for line in lines:
                    self.r = self.session.get(self.url + self.API + '/users/' + line + '/usernameinfo/').json()
                    if  self.r["status"] == "fail":
                        self.username = line + 'was not found'

                    elif self.r["status"] == "ok":
                        self.username = self.r["user"]["username"]
                        self.users.append(self.username)
                        if 'public_email' in self.r["user"]:
                            if self.r["user"]["public_email"] == '':
                                self.publicEmail = "Email not found"
                                COLOR = Fore.YELLOW
                                num += 1
                            else:
                                self.publicEmail = self.r["user"]["public_email"]
                                COLOR = Fore.LIGHTYELLOW_EX
                                self.EMAILS.append(self.publicEmail)
                                num +=1
                            print(f'    {Fore.GREEN}{num}. {self.username}{Fore.RESET} | {COLOR}{self.publicEmail}{Fore.RESET}    ')
                self.status()
        except KeyboardInterrupt:
            print(Fore.RED + '\n                  Process has been cancelled by user.\n'+Fore.RESET)
            self.status()



if __name__ == "__main__":
    InstagramBot = InstagramUnfollow()
    InstagramBot.Start()