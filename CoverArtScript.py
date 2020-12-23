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
                    else:
                        print("No file needed to remove")
                        shutil.copy(r'C:/Program Files (x86)/Steam/appcache/librarycache/'+file, BoxArtApplication.target_path)
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
         self.top.geometry("275x120")

         top.columnconfigure(1, weight=1)
         top.rowconfigure(1,weight=1)
         top.columnconfigure(2, weight=1)
         top.rowconfigure(2,weight=1)
         top.columnconfigure(3, weight=1)
         top.rowconfigure(3,weight=1)

         with open("var.pickle", "rb") as f:
             data = pickle.load(f)

         
         

         tkinter.Label(top, text="SteamID64").grid(row=0)
         tkinter.Label(top, text="Steam API Key").grid(row=1)
         tkinter.Label(top, text=data["target_path"][0:25],bg="white" ).grid(row=2, column=1)

         self.steamID = tkinter.Entry(top)
         self.steamID.insert(0, data["steamid"])
         self.apiKey = tkinter.Entry(top)
         self.apiKey.insert(0,data["apikey"])

         self.steamID.grid(row=0, column=1)
         self.apiKey.grid(row=1, column=1)

         tkinter.Button(top, text="Apply", command=self.submit).grid(row=3, column=1,sticky="nsew")
         tkinter.Button(top,text="Set Target \nDirectory",command=self.selectdirectory).grid(row=2,sticky="nsew")
         
     def submit(self):
         with open("var.pickle", "rb") as f:
            data = pickle.load(f)
         data["steamid"] = self.steamID.get()
         data["apikey"] = self.apiKey.get()
         with open("var.pickle", "wb") as f:
            pickle.dump(data, f)

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

        

        

        

        
