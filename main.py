import requests , os , random , time , json , unicodedata
RED, GREEN, BLUE, MAGENTA, GRAY, WHITE, RESET, BOLD, YELLOW = "\033[38;5;196m", "\033[38;2;40;230;30m", "\033[1;34m", "\033[38;2;180;0;255m", "\033[1;30m", "\033[1;37m", "\033[0m", "\033[1m", "\033[38;5;11m"
def width(s):
    w = 0
    for c in s:
        e = unicodedata.east_asian_width(c)
        if e in ("W", "F"):
            w += 2
        else:
            w += 1
    return w
def pad(s, w):
    return s + " " * max(0, w - width(s))
def bot(username):
    if ".." in username:
        return True
    if any(c.isupper() for c in username):
        return True
    for c in username:
        if ord(c) > 127:
            return True
    return False
def banner():
    os.system("cls") if os.name == "nt" else os.system("clear")
    print("""
     █████   ██████  ██████     ███    ██ ██    ██ ██   ██ ███████ 
    ██   ██ ██      ██          ████   ██ ██    ██ ██  ██  ██      
    ███████ ██      ██          ██ ██  ██ ██    ██ █████   █████   
    ██   ██ ██      ██          ██  ██ ██ ██    ██ ██  ██  ██      
    ██   ██  ██████  ██████     ██   ████  ██████  ██   ██ ███████ 
                                                               
                                                               
                        <~> Dev : @umw_m - Legend <~>""")
def friend():
    headers = {'Authorization': input(f"{WHITE}Enter Your Token : {RESET}")}
    r = requests.get("https://discord.com/api/v9/users/@me/relationships",headers=headers).json()
    types = {1: "Friend", 2: "Blocked", 3: "Incoming", 4: "Outgoing"}
    colors = {1: GREEN, 2: RED, 3: BLUE, 4: MAGENTA}
    data = []
    for i in r:
        data.append({"type": types.get(i["type"], "Unknown"),"color": colors.get(i["type"], GRAY),"id": i["user"]["id"],"username": i["user"]["username"],"global_name": i["user"]["global_name"] or "-"})
    data.sort(key=lambda d: ({"Friend": 0, "Incoming": 1, "Outgoing": 2, "Blocked": 3}.get(d["type"], 99), d["username"].lower()))
    max_type = max(width(d["type"]) for d in data) if data else 0
    max_id = max(width(d["id"]) for d in data) if data else 0
    max_user = max(width("BOT" if bot(d["username"]) else d["username"]) for d in data) if data else 0
    max_num = max(width(str(i+1)) for i in range(len(data))) if data else 0
    for idx, d in enumerate(data, 1):
        t = pad(d["type"], max_type)
        uid = pad(d["id"], max_id)
        un = pad("BOT" if bot(d["username"]) else d["username"], max_user)
        n = pad(str(idx), max_num)
        c = d["color"]
        print(f"{WHITE}{n} {GRAY}Type     : {c}{t} {WHITE}|{GRAY} ID : {c}{uid} {WHITE}|{GRAY} Username : {c}{un} {WHITE}|{GRAY} Global Name : {c}{d['global_name']}{WHITE}")
    counts = {}
    for d in data:
        counts[d["type"]] = counts.get(d["type"], 0) + 1
    print(f"{GRAY}Total    : {WHITE}{len(r)}")
    for t in ["Friend", "Incoming", "Outgoing", "Blocked"]:
        if t in counts:
            c = {"Friend": GREEN, "Incoming": BLUE, "Outgoing": MAGENTA, "Blocked": RED}[t]
            print(f"{c}{pad(t, 8)} : {WHITE}{counts[t]}")
    type_choice = input(f"{WHITE}Enter type to delete (1=Friend, 2=Incoming, 3=Outgoing, 4=Blocked) : {WHITE}")
    if not type_choice.strip():
        return
    type_map = {"1": "Friend", "2": "Incoming", "3": "Outgoing", "4": "Blocked"}
    selected_type = type_map.get(type_choice.strip())
    if not selected_type:
        print(f"{RED}Invalid type{WHITE}")
        return
    filtered = [d for d in data if d["type"] == selected_type]
    if not filtered:
        print(f"{RED}No {selected_type} found{WHITE}")
        return
    for i, d in enumerate(filtered):
        uid = d["id"]
        resp = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{uid}", headers=headers)
        if resp.status_code == 429:
            retry = resp.json().get("retry_after", 1)
            time.sleep(retry)
            resp = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{uid}", headers=headers)
        if resp.status_code == 204:
            print(f"{GREEN}[{i+1}/{len(filtered)}]{RESET} Deleted : {WHITE}{d['username']}{RESET}")
        else:
            print(f"{RED}[{i+1}/{len(filtered)}]{RESET} Failed : {WHITE}{d['username']} ({resp.status_code}){RESET}")
        if i < len(filtered) - 1:
            time.sleep(0.1)
    print(f"{GREEN}Done{RESET}")
def dm():
    def nuke(channel_id):
        while True:
            deleted = 0
            last_message_id = None
            while True:
                params = {'limit': 100}
                if last_message_id:
                    params['before'] = last_message_id
                r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, params=params)
                if r.status_code == 429:
                    retry = r.json().get('retry_after', 1)
                    time.sleep(retry)
                    continue
                if r.status_code != 200:
                    break
                messages = r.json()
                if not messages:
                    break
                for message in messages:
                    if message['author']['id'] == my_id:
                        del_r = requests.delete(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message["id"]}', headers=headers)
                        if del_r.status_code == 204:
                            deleted += 1
                            print(f"{GREEN}Deleted : {message['id']}{RESET}")
                        elif del_r.status_code == 429:
                            retry = del_r.json().get('retry_after', 1)
                            time.sleep(retry)
                        else:
                            print(f"{RED}Failed : {message['id']} ({del_r.status_code}){RESET}")
                    last_message_id = message['id']
                time.sleep(0.1)
            if deleted == 0:
                break
            time.sleep(1)
        print(f"{GREEN}Done : {channel_id}{RESET}")
    headers = {'Authorization': input(f"{WHITE}Enter Your Token : {RESET}")}
    my_id = requests.get("https://discord.com/api/v9/users/@me",headers=headers).json()["id"]
    channels = requests.get("https://discord.com/api/v9/users/@me/channels",headers=headers).json()
    total = len(channels)
    bots = sum(1 for ch in channels if ch.get("recipients") and ch["recipients"][0].get("bot"))
    humans = total - bots
    print(f"{GREEN}DMs :{humans} {WHITE}\n{RED}Bots : {bots} {WHITE}\n{GRAY}Total : {total}{WHITE}")
    print(f"{WHITE}1- Delete All DMs{RESET}")
    print(f"{WHITE}2- Delete All Bots DMs{RESET}")
    print(f"{WHITE}3- Delete All (DMs + Bots){RESET}")
    print(f"{WHITE}4- Delete By Channel ID{RESET}")
    choice = input(f"{WHITE}Enter Choice : {WHITE}")
    if choice == "1":
        targets = [ch for ch in channels if not (ch.get("recipients") and ch["recipients"][0].get("bot"))]
    elif choice == "2":
        targets = [ch for ch in channels if ch.get("recipients") and ch["recipients"][0].get("bot")]
    elif choice == "3":
        targets = channels
    elif choice == "4":
        cid = input(f"{WHITE}Enter Channel ID : {WHITE}")
        targets = [ch for ch in channels if ch["id"] == cid]
        if not targets:
            print(f"{RED}Channel Not Found{RESET}")
            return
    else:
        return
    for i, ch in enumerate(targets):
        name = ch["recipients"][0]["username"] if ch.get("recipients") else ch["id"]
        print(f"{BLUE}[{i+1}/{len(targets)}]{RESET} Nuking : {WHITE}{name}{RESET}")
        nuke(ch["id"])
    print(f"{GREEN}Done{RESET}")
def authorized():
    headers = {'Authorization': input(f"{WHITE}Enter Your Token : {RESET}")}
    r = requests.get("https://canary.discord.com/api/v9/oauth2/tokens",headers=headers)
    if r.status_code != 200:
        print(f"{RED}Failed :  ({r.status_code}){RESET}")
        return
    data = r.json()
    if not data:
        print(f"{RED}No Authorized Apps{RESET}")
        return
    max_name = max(width(t.get("application",{}).get("name","-")) for t in data) if data else 0
    max_id = max(width(str(t["id"])) for t in data) if data else 0
    for idx, t in enumerate(data, 1):
        app = t.get("application", {})
        name = app.get("name", "-")
        n = pad(str(idx), max_id)
        print(f"{WHITE}{n} {GRAY}|{GRAY} ID : {WHITE}{t['id']} {GRAY}|{GRAY} App : {WHITE}{pad(name, max_name)}")
    print(f"{GRAY}Total : {WHITE}{len(data)}{WHITE}")
    print(f"{WHITE}1- Delete By Number{RESET}")
    print(f"{WHITE}2- Delete All{RESET}")
    print(f"{WHITE}3- Cancel{RESET}")
    choice = input(f"{WHITE}Enter choice : {WHITE}")
    if choice == "1":
        nums = input(f"{WHITE}Enter Numbers (Comma Separated) : {WHITE}")
        targets = []
        for num in nums.split(","):
            num = num.strip()
            if num.isdigit() and 1 <= int(num) <= len(data):
                targets.append(data[int(num) - 1])
            else:
                print(f"{RED}Invalid number : {num}{RESET}")
    elif choice == "2":
        targets = data
    else:
        return
    if not targets:
        print(f"{RED}No targets{RESET}")
        return
    for i, t in enumerate(targets):
        resp = requests.delete(f"https://discord.com/api/v9/oauth2/tokens/{t['id']}",headers=headers)
        if resp.status_code == 429:
            retry = resp.json().get('retry_after', 1)
            time.sleep(retry)
            resp = requests.delete(f"https://discord.com/api/v9/oauth2/tokens/{t['id']}",headers=headers)
        name = t.get("application",{}).get("name","-")
        if resp.status_code == 204:
            print(f"{GREEN}[{i+1}/{len(targets)}]{RESET} Deleted : {WHITE}{name}{RESET}")
        else:
            print(f"{RED}[{i+1}/{len(targets)}]{RESET} Failed : {WHITE}{name} ({resp.status_code}){RESET}")
        if i < len(targets) - 1:
            time.sleep(0.1)
    print(f"{GREEN}Done{RESET}")
def close():
    headers = {'Authorization': input(f"{WHITE}Enter Your Token : {RESET}")}
    channels = requests.get("https://discord.com/api/v9/users/@me/channels",headers=headers).json()
    if not channels:
        print(f"{YELLOW}No DMs found{RESET}")
        return
    total = len(channels)
    bots = sum(1 for ch in channels if ch.get("recipients") and ch["recipients"][0].get("bot"))
    humans = total - bots
    print(f"{GREEN}DMs : {humans} {WHITE}\n{RED}Bots : {bots} {WHITE}\n{GRAY}Total : {total}{WHITE}")
    print(f"{WHITE}1- Close DMs (Users){RESET}")
    print(f"{WHITE}2- Close DMs (Bots){RESET}")
    print(f"{WHITE}3- Close DMs (All){RESET}")
    choice = input(f"{WHITE}Enter choice : {WHITE}")
    if choice == "1":
        targets = [ch for ch in channels if not (ch.get("recipients") and ch["recipients"][0].get("bot"))]
    elif choice == "2":
        targets = [ch for ch in channels if ch.get("recipients") and ch["recipients"][0].get("bot")]
    elif choice == "3":
        targets = channels
    else:
        return
    for i, ch in enumerate(targets):
        name = ch["recipients"][0]["username"] if ch.get("recipients") else ch["id"]
        resp = requests.delete(f"https://discord.com/api/v9/channels/{ch['id']}",headers=headers)
        if resp.status_code == 429:
            retry = resp.json().get('retry_after', 1)
            time.sleep(retry)
            resp = requests.delete(f"https://discord.com/api/v9/channels/{ch['id']}",headers=headers)
        if resp.status_code == 200:
            print(f"{GREEN}[{i+1}/{len(targets)}]{RESET} Closed : {WHITE}{name}{RESET}")
        else:
            print(f"{RED}[{i+1}/{len(targets)}]{RESET} Failed : {WHITE}{name} ({resp.status_code}){RESET}")
        if i < len(targets) - 1:
            time.sleep(0.1)
    print(f"{GREEN}Done{RESET}")
def leave():
    headers = {'Authorization': input(f"{WHITE}Enter Your Token : {RESET}")}
    guilds = requests.get("https://discord.com/api/v9/users/@me/guilds",headers=headers).json()
    if not guilds:
        print(f"{YELLOW}No servers found{RESET}")
        return
    total = len(guilds)
    owners = sum(1 for g in guilds if g.get("owner"))
    can_leave = total - owners
    print(f"{GREEN}Servers : {can_leave} {WHITE}\n{YELLOW}Owned : {owners} {WHITE}\n{GRAY}Total : {total}{WHITE}")
    print(f"{WHITE}1- Leave All Servers{RESET}")
    print(f"{WHITE}2- Leave By Number{RESET}")
    print(f"{WHITE}3- Cancel{RESET}")
    choice = input(f"{WHITE}Enter Choice : {WHITE}")
    if choice == "1":
        targets = [g for g in guilds if not g.get("owner")]
    elif choice == "2":
        nums = input(f"{WHITE}Enter Numbers (Comma Separated) : {WHITE}")
        targets = []
        for num in nums.split(","):
            num = num.strip()
            if num.isdigit() and 1 <= int(num) <= len(guilds):
                g = guilds[int(num) - 1]
                if g.get("owner"):
                    print(f"{RED}Cannot Leave : {g['name']} (Owned){RESET}")
                else:
                    targets.append(g)
            else:
                print(f"{RED}Invalid Number : {num}{RESET}")
    else:
        return
    for i, g in enumerate(targets):
        resp = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{g['id']}",headers=headers)
        if resp.status_code == 429:
            retry = resp.json().get('retry_after', 1)
            time.sleep(retry)
            resp = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{g['id']}",headers=headers)
        if resp.status_code == 204:
            print(f"{GREEN}[{i+1}/{len(targets)}]{RESET} Left : {WHITE}{g['name']}{RESET}")
        else:
            error = resp.json().get('message', '') if resp.content else ''
            print(f"{RED}[{i+1}/{len(targets)}]{RESET} Failed : {WHITE}{g['name']} ({resp.status_code}){RESET}")
        if i < len(targets) - 1:
            time.sleep(0.1)
    print(f"{GREEN}Done{RESET}")
def all():
    headers = {'Authorization': input(f"{WHITE}Enter Your Token : {RESET}")}
    my_id = requests.get("https://discord.com/api/v9/users/@me",headers=headers).json()["id"]
    def nuke(channel_id):
        while True:
            deleted = 0
            last_message_id = None
            while True:
                params = {'limit': 100}
                if last_message_id:
                    params['before'] = last_message_id
                r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, params=params)
                if r.status_code == 429:
                    retry = r.json().get('retry_after', 1)
                    time.sleep(retry)
                    continue
                if r.status_code != 200:
                    break
                messages = r.json()
                if not messages:
                    break
                for message in messages:
                    if message['author']['id'] == my_id:
                        del_r = requests.delete(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message["id"]}', headers=headers)
                        if del_r.status_code == 204:
                            deleted += 1
                        elif del_r.status_code == 429:
                            retry = del_r.json().get('retry_after', 1)
                            time.sleep(retry)
                    last_message_id = message['id']
                time.sleep(0.1)
            if deleted == 0:
                break
    print(f"{BLUE}Starting Nuke All{RESET}")
    r = requests.get("https://discord.com/api/v9/users/@me/relationships",headers=headers).json()
    types = {1: "Friend", 2: "Blocked", 3: "Incoming", 4: "Outgoing"}
    skip = {3}
    targets = [d for d in r if d["type"] not in skip]
    if targets:
        print(f"{WHITE}Nuking {len(targets)} Friends{RESET}")
        for i, d in enumerate(targets):
            resp = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{d['user']['id']}", headers=headers)
            if resp.status_code == 429:
                retry = resp.json().get("retry_after", 1)
                time.sleep(retry)
                resp = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{d['user']['id']}", headers=headers)
            t = types.get(d["type"], "?")
            if resp.status_code == 204:
                print(f"{GREEN}[{i+1}/{len(targets)}]{RESET} Deleted {t} : {WHITE}{d['user']['username']}{RESET}")
            else:
                print(f"{RED}[{i+1}/{len(targets)}]{RESET} Failed {t} : {WHITE}{d['user']['username']}{RESET}")
            time.sleep(0.1)
    channels = requests.get("https://discord.com/api/v9/users/@me/channels",headers=headers).json()
    if channels:
        print(f"{WHITE}Nuking {len(channels)} DMs{RESET}")
        for i, ch in enumerate(channels):
            name = ch["recipients"][0]["username"] if ch.get("recipients") else ch["id"]
            print(f"{BLUE}[{i+1}/{len(channels)}]{RESET} Nuking : {WHITE}{name}{RESET}")
            nuke(ch["id"])
        channels = requests.get("https://discord.com/api/v9/users/@me/channels",headers=headers).json()
        for ch in channels:
            r = requests.get(f'https://discord.com/api/v9/channels/{ch["id"]}/messages', headers=headers, params={'limit': 100})
            if r.status_code == 200 and r.json():
                nuke(ch["id"])
        print(f"{WHITE}Closing DMs{RESET}")
        channels = requests.get("https://discord.com/api/v9/users/@me/channels",headers=headers).json()
        for i, ch in enumerate(channels):
            name = ch["recipients"][0]["username"] if ch.get("recipients") else ch["id"]
            resp = requests.delete(f"https://discord.com/api/v9/channels/{ch['id']}",headers=headers)
            if resp.status_code == 429:
                retry = resp.json().get('retry_after', 1)
                time.sleep(retry)
                resp = requests.delete(f"https://discord.com/api/v9/channels/{ch['id']}",headers=headers)
            if resp.status_code == 200:
                print(f"{GREEN}[{i+1}/{len(channels)}]{RESET} Closed : {WHITE}{name}{RESET}")
            else:
                print(f"{RED}[{i+1}/{len(channels)}]{RESET} Failed : {WHITE}{name} ({resp.status_code}){RESET}")
            time.sleep(0.1)
    oauth = requests.get("https://discord.com/api/v9/oauth2/tokens",headers=headers).json()
    if oauth:
        print(f"{WHITE}Nuking {len(oauth)} Authorized Apps{RESET}")
        for i, t in enumerate(oauth):
            resp = requests.delete(f"https://discord.com/api/v9/oauth2/tokens/{t['id']}",headers=headers)
            if resp.status_code == 429:
                retry = resp.json().get('retry_after', 1)
                time.sleep(retry)
                resp = requests.delete(f"https://discord.com/api/v9/oauth2/tokens/{t['id']}",headers=headers)
            name = t.get("application",{}).get("name","-")
            if resp.status_code == 204:
                print(f"{GREEN}[{i+1}/{len(oauth)}]{RESET} Deleted : {WHITE}{name}{RESET}")
            else:
                print(f"{RED}[{i+1}/{len(oauth)}]{RESET} Failed : {WHITE}{name}{RESET}")
            time.sleep(0.1)
    guilds = requests.get("https://discord.com/api/v9/users/@me/guilds",headers=headers).json()
    leave_targets = [g for g in guilds if not g.get("owner")]
    if leave_targets:
        print(f"{WHITE}Nuking {len(leave_targets)} Servers{RESET}")
        for i, g in enumerate(leave_targets):
            resp = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{g['id']}",headers=headers)
            if resp.status_code == 429:
                retry = resp.json().get('retry_after', 1)
                time.sleep(retry)
                resp = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{g['id']}",headers=headers)
            if resp.status_code == 204:
                print(f"{GREEN}[{i+1}/{len(leave_targets)}]{RESET} Left : {WHITE}{g['name']}{RESET}")
            else:
                print(f"{RED}[{i+1}/{len(leave_targets)}]{RESET} Failed : {WHITE}{g['name']}{RESET}")
            time.sleep(0.1)
    print(f"{GREEN}Nuke All Done{RESET}")
def owner():
    headers = {'Authorization': input(f"{WHITE}Enter Your Token : {RESET}")}
    guilds = requests.get("https://discord.com/api/v9/users/@me/guilds",headers=headers).json()
    owned = [g for g in guilds if g.get("owner")]
    if not owned:
        print(f"{YELLOW}No owned servers{RESET}")
        return
    max_name = max(width(g["name"]) for g in owned) if owned else 0
    max_id = max(width(g["id"]) for g in owned) if owned else 0
    for idx, g in enumerate(owned, 1):
        print(f"{WHITE}{idx}- {GRAY}|{GRAY} ID : {WHITE}{g['id']} {GRAY}|{GRAY} Name : {WHITE}{pad(g['name'], max_name)}{WHITE}")
    print(f"{GRAY}Total : {WHITE}{len(owned)}{WHITE}")
    print(f"{WHITE}1- Delete All{RESET}")
    print(f"{WHITE}2- Delete By Number{RESET}")
    print(f"{WHITE}3- Cancel{RESET}")
    choice = input(f"{WHITE}Enter choice : {WHITE}")
    if choice == "1":
        targets = owned
    elif choice == "2":
        nums = input(f"{WHITE}Enter Numbers (Comma Separated) : {WHITE}")
        targets = []
        for num in nums.split(","):
            num = num.strip()
            if num.isdigit() and 1 <= int(num) <= len(owned):
                targets.append(owned[int(num) - 1])
            else:
                print(f"{RED}Invalid number : {num}{RESET}")
    else:
        return
    for i, g in enumerate(targets):
        resp = requests.post(f"https://discord.com/api/v9/guilds/{g['id']}/delete",headers=headers)
        if resp.status_code == 429:
            retry = resp.json().get('retry_after', 1)
            time.sleep(retry)
            resp = requests.post(f"https://discord.com/api/v9/guilds/{g['id']}/delete",headers=headers)
        if resp.status_code == 204 or resp.status_code == 200:
            print(f"{GREEN}[{i+1}/{len(targets)}]{RESET} Deleted : {WHITE}{g['name']}{RESET}")
        else:
            print(f"{RED}[{i+1}/{len(targets)}]{RESET} Failed : {WHITE}{g['name']} ({resp.status_code}){RESET}")
        if i < len(targets) - 1:
            time.sleep(0.1)
    print(f"{GREEN}Done{RESET}")
def tool():
    banner()
    print(f"{WHITE}1- Friend{RESET}")
    print(f"{WHITE}2- DM{RESET}")
    print(f"{WHITE}3- Authorized Apps{RESET}")
    print(f"{WHITE}4- Close DMs{RESET}")
    print(f"{WHITE}5- Leave Servers{RESET}")
    print(f"{WHITE}6- Delete Owner Servers{RESET}")
    print(f"{WHITE}7- Nuke All{RESET}")
    print(f"{WHITE}8- Exit{RESET}")
    choice = input(f"{WHITE}Enter Your Choice : {RESET}")
    if choice == "1":
        friend()
    elif choice == "2":
        dm()
    elif choice == "3":
        authorized()
    elif choice == "4":
        close()
    elif choice == "5":
        leave()
    elif choice == "6":
        owner()
    elif choice == "7":
        all()
    else:
        exit()
tool()