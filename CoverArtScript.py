#!/usr/bin/python3

import os
import fnmatch
import shutil
import tkinter
import pickle
import urllib.request, json
from tkinter import messagebox,filedialog
from tkinter.filedialog import askdirectory

class BoxArtApplication:
    steamid = 0
    apikey = 0
    target_path = ""

    def __init__(self, master):
        self.master = master
        master.title("Box Art App")
        self.master.geometry("202x125")
        
        #GUI Configurations
        self.settingsFrame = tkinter.Frame(master,bg="#21242a")
        self.settingsFrame.pack(side=tkinter.TOP,fill=tkinter.BOTH, expand=1)

        self.settingsBtn = tkinter.Button(self.settingsFrame,command=self.settings, fg="white", text="Settings", bg="#3e444e")
        self.settingsBtn.pack(padx=5,side=tkinter.RIGHT,fill=tkinter.Y)

        self.midFrame = tkinter.Frame(master,bg="#21242a")
        self.midFrame.pack(side=tkinter.TOP,fill=tkinter.BOTH, expand=1)

        self.refreshBtn = tkinter.Button(self.midFrame,bg="#3f444e" ,fg="white",text="Get Currently \nPlayed Game",command=self.refresh)   
        self.refreshBtn.pack(padx=5,pady=5,side=tkinter.LEFT,fill=tkinter.BOTH, expand=1)
        
        self.bottomframe = tkinter.Frame(master,bg="#21242a")
        self.bottomframe.pack(side=tkinter.BOTTOM,fill=tkinter.BOTH, expand=1)
  
        self.runBtn = tkinter.Button(self.bottomframe ,bg="#1db34c",fg="white",text="Run",command=self.getgame)
        self.runBtn.pack(padx=5,pady=5,side=tkinter.LEFT,fill=tkinter.BOTH, expand=1)

        #Load pickle variables
        try:
            with open("var.pickle", "rb") as f:
                data = pickle.load(f)
            BoxArtApplication.steamid = data["steamid"]
            BoxArtApplication.apikey = data["apikey"]
            BoxArtApplication.target_path = data["target_path"]
        except (OSError, IOError):
            data = {"steamid": 0, "apikey": 0, "target_path": ""}
            with open("var.pickle", "wb") as f:
                pickle.dump(data, f)
    
    def settings(self):
        top = tkinter.Toplevel()
        Settings(top)

    def refresh(self):
        try:
            with urllib.request.urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + BoxArtApplication.apikey  + "&steamids=" + BoxArtApplication.steamid) as k:
                jdata = json.loads(k.read().decode())
                self.variable = int(jdata["response"]["players"][0]["gameid"])
                print(int(jdata["response"]["players"][0]["gameid"]))
        except KeyError:
            tkinter.messagebox.showerror(title="Error",message="You need to be currently running a game on steam for this to work")

    def getgame(self):
        id = 0
        with urllib.request.urlopen("https://api.steampowered.com/ISteamApps/GetAppList/v2/") as url:
            data = json.loads(url.read().decode())
        
        for key in data["applist"]["apps"]:
            if key["appid"] == self.variable:
                id = str(key["appid"])
                break
        if id != 0:
            for file in os.listdir('/Program Files (x86)/Steam/appcache/librarycache'):
                if fnmatch.fnmatch(file, id + '*600x900.jpg'):
                    if len(os.listdir(BoxArtApplication.target_path)) == 1:
                        for f in os.listdir(BoxArtApplication.target_path):
                            os.remove(os.path.join(BoxArtApplication.target_path,f))
                            
                        print("File Removed")
                        shutil.copy(r'C:/Program Files (x86)/Steam/appcache/librarycache/'+file, BoxArtApplication.target_path)
                        for f in os.listdir(BoxArtApplication.target_path):
                            os.rename(os.path.join(BoxArtApplication.target_path,f),os.path.join(BoxArtApplication.target_path,'boxart.jpg'))
                        
                    else:
                        print("No file needed to remove")
                        shutil.copy(r'C:/Program Files (x86)/Steam/appcache/librarycache/'+file, BoxArtApplication.target_path)
                        for f in os.listdir(BoxArtApplication.target_path):
                            os.rename(os.path.join(BoxArtApplication.target_path,f),os.path.join(BoxArtApplication.target_path,'boxart.jpg'))
                        
                    break
        else:
            tkinter.messagebox.showerror(title="Error",message="The program you selected is either not steam supported or you aren't currently playing a game")

    def exists_steamid(self):
        return False if BoxArtApplication.steamid == 0 else True
    
    def exists_apikey(self):
        return False if BoxArtApplication.apikey == 0 else True

    def exists_target_path(self):
        return False if BoxArtApplication.target_path == "" else True

class Settings:
     
     def __init__(self, top):
         self.top = top 
         self.top.title("Settings")
         self.top.configure(bg="#21242a")
         self.top.columnconfigure(0, weight=1)
         self.top.columnconfigure(1, weight=4)

         self.top.rowconfigure(0,weight=1)
         self.top.rowconfigure(1,weight=1)
         self.top.rowconfigure(2,weight=1)
         self.top.rowconfigure(3,weight=1)
         
    
         with open("var.pickle", "rb") as f:
             data = pickle.load(f)

         
         self.steam_id_label = tkinter.Label(top, text="SteamID64", fg="white",bg="#21242a")
         self.steam_id_label.grid(row=0, column=0, sticky="W", ipadx=10, ipady=10,padx=10, pady=10)

         self.steamID = tkinter.Entry(top, bg="#21242a", fg="white", justify='center' )
         self.steamID.insert(0, data["steamid"])
         self.steamID.grid(row=0, column=1, ipadx=10, ipady=10, sticky="NSEW", padx=10, pady=10)
         self.steamID.config(highlightbackground="white")

         self.api_key_label = tkinter.Label(top, text="Steam API Key", fg="white", bg="#21242a")
         self.api_key_label.grid(row=1, column=0, sticky="W", ipadx=10, ipady=10,padx=10, pady=10)
         
         
         self.apiKey = tkinter.Entry(top, bg="#21242a", fg="white", justify='center')
         self.apiKey.insert(0,data["apikey"])
         self.apiKey.grid(row=1, column=1, ipadx=10, ipady=10, sticky="NSEW", padx=10, pady=10)
         self.apiKey.config(highlightbackground="white")
              
         self.frame = tkinter.Frame(top)
         self.frame.grid(column=0, columnspan=2, row=2,sticky="NSEW")
         
         self.target_path_label = tkinter.Label(self.frame, text="   " + data["target_path"][0:50] + "...",bg="#21242a", anchor="w", fg="white")
         self.target_path_label.grid(column=0, row=0, ipadx=15, ipady=10, sticky="NSEW", padx=10, pady=10)
         self.target_path_label.config(highlightbackground="white")
         
         self.set_directory_btn = tkinter.Button(self.frame,text="Set Directory",command=self.selectdirectory, bg="#393f47", fg="white")
         self.set_directory_btn.grid(column=1, row=0, ipadx=10, ipady=10, sticky="NSEW", padx=10, pady=10)
         
         self.frame.columnconfigure(0,weight=4)
         self.frame.columnconfigure(1,weight=1)
         self.frame.configure(bg="#21242a")
         self.frame.rowconfigure(0,weight=1)

         self.frame2 = tkinter.Frame(top, bg="#21242a")
         self.frame2.grid(column=0, columnspan=2, row=3 , ipadx=10, ipady=10, sticky="NSEW",padx=10)

         tkinter.Button(self.frame2, text="Saved", command=self.submit, width="12", height="2", bg="#393f47", fg="white").pack(side=tkinter.RIGHT)
         self.visible = tkinter.Label(self.frame2, text="Applied", width="12", height="2", bg="#21242a", fg="white")
         
         

         
     def submit(self):
         with open("var.pickle", "rb") as f:
            data = pickle.load(f)
         data["steamid"] = self.steamID.get()
         data["apikey"] = self.apiKey.get()
         with open("var.pickle", "wb") as f:
            pickle.dump(data, f)
         self.visible.pack(side=tkinter.RIGHT, padx=10)

     def selectdirectory(self):
         with open("var.pickle", "rb") as f:
             data = pickle.load(f)
        
         data["target_path"] = filedialog.askdirectory()
         BoxArtApplication.target_path = data["target_path"]

         with open("var.pickle", "wb")as f:
            pickle.dump(data, f)


root = tkinter.Tk()

app = BoxArtApplication(root)

root.mainloop()
