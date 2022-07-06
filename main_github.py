import requests,time,colorama,os,sys,threading,win32api, multiprocessing,psutil
colorama.init()

username = 'justalghamdi'
xtbanner = '''     ____    ___  _____   ________ 
  __/ / /_  / _ \/ __/ | / /  _/ / 
 /_  . __/ / // / _/ | |/ // // /__
/_    __/ /____/___/ |___/___/____/
 /_/_/'''
txtbanner = ''.join(('', xtbanner))

attempt = 0
spam = 0
error = 0
rs = 0
profileInfo = None
kill_threads = False
global_target = None
class WEBs:
    headers = {}
    cookies = {}
    def __init__(self,username,password) -> None:
        self.username = username
        self.password = password
        self.headers = self.make_headers()
    
    def make_headers(self):
        headers:dict = {}
        headers['accept'] = '*/*'
        headers['user-agent'] = 'justa1lghamdi/1.1'
        headers['Connection'] = 'close'
        security = requests.get('https://www.instagram.com/accounts/login/ajax/',headers=headers)
        headers['x-csrftoken'] = security.cookies.get_dict()['csrftoken']
        self.csrftoken = security.cookies.get_dict()['csrftoken'] 
        headers['x-requested-with'] = 'XMLHttpRequest'
        return headers

    
    def SendRequest(self, method = "GET" ,path = "/", isproxies = False, proxies = {} , data = {} , headers = {}, cookies = {},timeout = 5,server="www.instagram.com") -> requests.Response :
        endpoint = f"https://{server}{path}"
        reqeust = None
        request_headers = {}
        request_data = {}
        request_cookies = {}
        request_prxy = {}
        if len(headers) == 0:
            request_headers = self.headers
        else:
            request_headers = headers
        
        if len(cookies) == 0:
            request_cookies = self.cookies
        else:
            request_cookies = cookies
        
        if len(proxies) != 0:
            request_prxy = proxies
        try:
            if method == "GET": 
                if not isproxies:
                    reqeust = requests.get(endpoint,headers=request_headers,cookies=request_cookies)
                else:
                    reqeust = requests.get(endpoint,headers=request_headers,cookies=request_cookies,proxies=request_prxy,timeout=timeout)
            
            elif method == "POST":
                
                request_data = data
                if not isproxies:
                    reqeust = requests.post(endpoint,data=request_data,headers=request_headers,cookies=request_cookies)
                else:
                    reqeust = requests.post(endpoint,data=request_data,headers=request_headers,cookies=request_cookies,proxies=request_prxy,timeout=timeout)      
            
            return reqeust
        except :
            return None
    
    
    
    def login(self) -> requests.Response:
        data = {}
        data['username'] = self.username
        data['enc_password'] = f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{self.password}"
        request = self.SendRequest(method="POST", path="/accounts/login/ajax/",data=data)
        if request != None:
            self.cookies = request.cookies.get_dict()
        return request
    
    def get_profile(self) -> requests.Response:
        return self.SendRequest(method="GET",path='/accounts/edit/?__a=1')
    
    def edit_profile_username(self,username) -> requests.Response:
        global profileInfo
        profiledata = profileInfo
        data = {}
        self.headers['x-csrftoken'] = self.cookies['csrftoken']
        if profiledata:
            data['first_name'] = profiledata['first_name']
            data['email'] = profiledata['email']
            data['username'] = username
            data['biography'] = profiledata['biography']
            data['external_url'] = profiledata['external_url']
            data['chaining_enabled'] = 'on'
        return self.SendRequest(method="POST", path='/accounts/edit/',data=data,cookies=self.cookies,headers=self.headers)
        
    
def banner():
    os.system('cls')
    print(colorama.Fore.RED)
    print(f"{txtbanner} @{username}")
    print(colorama.Fore.RESET)
    

def zerors():
    global rs,kill_threads
    while 1:
        if kill_threads:
            break
        rs = 0
        time.sleep(1)

    
def webhook(target:str,attempts:int, rs:int):
    return requests.post('https://discord.com/api/webhooks/{}/{}',headers={'Content-Type':'application/json'},json={
        "embeds": [
            {
                "description": f"**Swapped Successfully -> [ [@{target}](https://www.instagram.com/{target}/) ] .**\n**Attempts: {attempts} | r/s: {rs}**\n**By DEvil [@{username}](https://www.instagram.com/{username}/)**", 
                "title": "**- New Swapped ! -**", 
                "image": {"url": "https://cdn.discordapp.com/attachments/{}/{}/idk.jpg"},
                "color": 5814783
            }
        ],
        "username": f"#{username}"})
   

def counters(t,a,s,e,r):
    print(f'[{colorama.Fore.GREEN}${colorama.Fore.RESET}] @{t} - ::Attempt -> {a} - ::Spam -> {s} - ::Error -> {e} - ::r/s -> {r}  \r',end='')
    sys.stdout.flush()
     
def print_log():
    global kill_threads, attempt,error,rs,spam,global_target 
    banner()
    while True:
        if not kill_threads:
            counters(global_target ,attempt,spam,error,rs)
        else:
            kill_threads = True
            banner()
            banner()
            print(f'[{colorama.Fore.GREEN}+{colorama.Fore.RESET}] Username Swapped Successfully @{global_target}!')
            print(f'[{colorama.Fore.GREEN}+{colorama.Fore.RESET}] By DEvil | @{username}',end='')
            webhook(global_target,attempt,rs)    
            MessageBox("!!! New Swap !!!",f"Username => {global_target}\nBy DEvil @{username}")
            psutil.Process(os.getpid()).terminate()

def MessageBox(title,message):
    win32api.MessageBox(None, message, title,0x0000)

def swap(web: WEBs, target):
    global kill_threads, attempt,error,rs,spam,global_target
    global_target = target
    while 1:
        if kill_threads:
            break
        else:
            request = web.edit_profile_username(target)
            if request == None:
                error += 1
            else:
                rs+=1
                if request.text == '{"status":"ok"}' and request.status_code == 200:
                    kill_threads = True
                    break
                elif request.status_code == 429:      
                    spam += 1
                elif request.status_code == 400:
                    attempt += 1
                else:
                    error += 1
        
def update_title():
    global kill_threads, attempt,error,rs,spam,global_target 

    while 1:
        if kill_threads:
            break
        win32api.SetConsoleTitle(f"#DEvil Swapper | Attempt {attempt} - Spam {spam} - Error {error} - r/s {rs}")
        time.sleep(0.3)
def main():
    global profileInfo
    banner()
    threading.Thread(target=update_title).start()
    print(f'[{colorama.Fore.RED}1{colorama.Fore.RESET}]- Swapper')
    print(f'[{colorama.Fore.YELLOW}2{colorama.Fore.RESET}]- Credits')
    sys.stdout.flush()
    if int(sys.stdin.readline()[:-1]) == 2:
        banner()
        sys.stdin.flush()
        print('This tools is free and programmed by insta @justalghamdi')
        print('press any key to return to main page')
        os.system('pause > nul')
        return main()
    
    banner()
    print(f'[{colorama.Fore.MAGENTA}*{colorama.Fore.RESET}] Target: ',end='')
    target = sys.stdin.readline()[:-1]
    print(f'[{colorama.Fore.MAGENTA}*{colorama.Fore.RESET}] Username: ',end='')
    username = sys.stdin.readline()[:-1]
    print(f'[{colorama.Fore.MAGENTA}*{colorama.Fore.RESET}] Password: ',end='')
    password = sys.stdin.readline()[:-1]
    web = WEBs(username,password)
    login_res = web.login()
    if login_res != None:
        banner()
        if login_res.text.__contains__('"authenticated":true'):
            profileInfo = web.get_profile().json()['form_data']
            print(f'[{colorama.Fore.CYAN}~{colorama.Fore.RESET}] Threads:',end='')
            sys.stdout.flush()
            threads = int(sys.stdin.readline()[:-1])
            
            MessageBox("#DEvil Swapper",f"Ready?")
            
            threading.Thread(target=zerors).start()
            threading.Thread(target=print_log).start()
            for _ in range(threads):
                threading.Thread(target=swap,args=(web,target,)).start()
            
        elif login_res.text.__contains__('{"user":true,"authenticated":false,"status":"ok"}'):
            print(f'[{colorama.Fore.RED}-{colorama.Fore.RESET}] Your password is Wrong')
            print('press any key to return main page')
            os.system('pause > nul')  
            return main() 
        elif login_res.text.__contains__('{"user":false,"authenticated":false,"status":"ok"}'):
            print(f'[{colorama.Fore.RED}-{colorama.Fore.RESET}] Your info is Wrong')
            print('press any key to return main page')
            os.system('pause > nul')   
            return main()
        elif login_res.text.__contains__('challenge'):
            print(f'[{colorama.Fore.RED}-{colorama.Fore.RESET}] Secure Error')
            print('press any key to return main page')
            os.system('pause > nul')   
            return main()
        else:
            print(f'[{colorama.Fore.RED}-{colorama.Fore.RESET}] Check your inputs !')
            print('press any key to return main page')
            os.system('pause > nul')   
            return main()
    else:
        banner()
        print('Error in login')    
        print('press any key to return main page')
        os.system('pause > nul')   
        return main()
if __name__ == '__main__':
    main()