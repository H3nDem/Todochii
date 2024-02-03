from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
from threading import Thread
from time import sleep
import json

from classes.Tamagotchi import *
from classes.ListOfTodolists import *
from classes.Todolist import *


global APP_WIN_WIDTH, APP_WIN_HEIGHT, RUNNING, time
APP_WIN_WIDTH = 1280
APP_WIN_HEIGHT = 720


class TodochiiApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.load("database/data.json")
        self.init_font()
        self.init_Tamagotchi()
        self.init_Todolist()
        self.init_points_system()
        self.run_internal_clock()
        self.init_frames()
        self.bind_keys()
        
    
# =============================================================================
#   INTERNAL CLOCK
# =============================================================================
    # Starts the internal clock, useful for various reasons
    def run_internal_clock(self):
        self.internalClock = Thread(target=self.myClock, args=(self.AllData['Time'],))
        self.internalClock.start()

    # Function called when the internal clock starts running
    def myClock(self, seconds):
        self.is_running = True
        self.time = seconds
        while (self.is_running):
            if (self.time % 10 == 0): # every 10 sec
                self.Tamagotchi.reduce_hunger()
            self.time += 1
            sleep(1) # Ticking every seconds
        self.notify() 

    # Function called when the internal clock stops
    def notify(self):
        print("APP CLOSED")
      
    

# =============================================================================
#   SAVE/LOAD DATA               
# =============================================================================
    # Save the app data
    def save(self, path):
        self.AllData["Points"] = self.points
        self.AllData["Time"] = self.time
        self.AllData["Hunger"] = self.Tamagotchi.get_hunger()

        l = []
        for t in self.Todolist.get_Todos():
            l.append(t.get_Tasks())
        self.AllData["Todolists"] = l

        f = open(path, 'w')
        json.dump(self.AllData, f)
        f.close()

    #load the app data
    def load(self, path): 
        f = open(path, 'r')
        self.AllData = json.load(f)
        f.close()
    
    
    
# =============================================================================
#   FRAME HANDLERS
# =============================================================================
    # I'm not sure how it works and why but i noted this a long time ago about it (so prolly wrong): Container contains all the elements on one page
    def init_container(self):
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    # Loads all the pages to navigate through them
    def init_frames(self):
        self.init_container()
        
        self.frames = {} # GamesMenu, ShopMenu
        for F in (MainMenu, HomeMenu, TamagotchiMenu, ToolsMenu, TodolistMenu, ShopMenu, SettingsMenu, CreditsMenu):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MainMenu")
         
    # Show the frame with the given page name
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()  



# =============================================================================
#   POINTS SYSTEM
# =============================================================================
    # Starts the system of point
    def init_points_system(self):
        self.points = self.AllData["Points"]
        self.points_display = StringVar()
        self.update_point_display()
        
    # Increment the number of points
    def increment_points(self, event):
        self.points += 1
        self.update_point_display()
        
    # Decrement the number of points    
    def decrement_points(self, event):
        if (self.points > 0):
            self.points -= 1
        self.update_point_display()

    # Each time we change the points value we also have to update the display
    def update_point_display(self):
        self.points_display.set("Points: {0}".format(self.points))



# =============================================================================
#   TAMAGOTCHI
# =============================================================================
    def init_Tamagotchi(self):
        self.Tamagotchi = Tamagotchi()
        self.Tamagotchi.set_hunger(self.AllData['Hunger'])
        


# =============================================================================
#   TODOLIST
# =============================================================================
    def init_Todolist(self):
        self.Todolist = ListOfTodolists()
        self.todolists = self.AllData['Todolists']



# =============================================================================
#   FONT HANDLERS
# =============================================================================  
    # Prepares all the fonts needed for the app
    def init_font(self):
        self.init_fontsizes()
        self.title_font = Font(family='MS Gothic', size=self.title_fontsize)
        self.main_button_font = Font(family='Modern', size=self.main_button_fontsize, weight="bold")
        self.buttons_font = Font(family='Modern', size=self.buttons_fontsize, weight="bold")
        self.points_font = Font(family='MS Gothic', size=self.points_fontsize)
        self.version_font = Font(family='Helvetica', size=self.version_fontsize)
        self.todolists_font = Font(family='MS Gothic', size=self.todolists_fontsize, weight="bold")
        
    # Initialize the fontsizes
    def init_fontsizes(self):
        self.title_fontsize = 24
        self.main_button_fontsize = 20
        self.buttons_fontsize = 18
        self.todolists_fontsize = 26
        self.points_fontsize = 20
        self.version_fontsize = 10
        


# =============================================================================
#   APP CLOSURE
# =============================================================================
    def quit_app(self):
        if messagebox.askokcancel("Quit", "Close the app?"):
            self.save("database/data.json")
            self.is_running = False
            app.destroy()



# =============================================================================
#   KEY BINDINGS       
# =============================================================================
    def bind_keys(self):
        self.bind("<Control-Button-1>", self.increment_points) # Ctrl + L Click
        self.bind("<Control-Button-3>", self.decrement_points) # Ctrl + R Click



class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.load_Todochii_image()
        self.init_MainMenu_buttons()
        self.place_app_version()
        
    # Loads the image of the app (and the title at the same time)
    def load_Todochii_image(self):
        self.MainMenu_title = Label(self, text="Todochii", font=self.controller.title_font).pack(side="top", fill="x", pady=20)
        self.Todochii_canvas = Canvas(self, width=150, height=150)
        self.Todochii_icon = ImageTk.PhotoImage(Image.open("ressources/todochiiT.png").resize((150, 150), Image.LANCZOS))
        self.Todochii_image = self.Todochii_canvas.create_image(0,0,image=self.Todochii_icon, anchor="nw")
        self.Todochii_canvas.pack()
    
    # Places all the buttons on the main menu
    def init_MainMenu_buttons(self):
        self.MainMenu_buttons = Frame(self, borderwidth=1, relief='solid', bg="white")
        self.start_button = Button(self.MainMenu_buttons, text="Start", bg="white", width=15, font=self.controller.main_button_font, borderwidth=0, command=lambda: self.controller.show_frame("HomeMenu"))
        self.credits_button = Button(self.MainMenu_buttons, text="Credits", bg="white", width=15, font=self.controller.main_button_font, borderwidth=0, command=lambda: self.controller.show_frame("CreditsMenu"))
        self.quit_button = Button(self.MainMenu_buttons, text="Quit", bg="white", width=15, font=self.controller.main_button_font, borderwidth=0, command=lambda:self.controller.quit_app())
        
        self.start_button.pack()
        self.credits_button.pack(pady=5)
        self.quit_button.pack(pady=30)
        self.MainMenu_buttons.pack(pady=50)

    def place_app_version(self):
        self.version = Label(self, text="v1.0", font=self.controller.version_font)
        self.version.pack()
        self.version.place(x=APP_WIN_WIDTH/50*48, y=APP_WIN_HEIGHT/50*48)
        


class HomeMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.HomeMenu_title = Label(self, text="Home Menu", font=self.controller.title_font).pack(side="top", fill="x", pady=20)
        self.init_HomeMenu_buttons()
        self.show_points()
    
    def init_HomeMenu_buttons(self):
        self.HomeMenu_buttons = Frame(self, borderwidth=1, relief='solid', bg="white")
        self.tamagotchi_button = Button(self.HomeMenu_buttons, text="Tamagotchi", bg="white", width=15, font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.show_frame("TamagotchiMenu"))
        self.tools_button = Button(self.HomeMenu_buttons, text="Tools", bg="white", width=15, font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.show_frame("ToolsMenu"))
        #self.games_button = Button(self.HomeMenu_buttons, text="Games", width=15, font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.show_frame("GamesMenu"))
        self.shop_button = Button(self.HomeMenu_buttons, text="Shop", bg="white", width=15, font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.show_frame("ShopMenu"))
        self.settings_button = Button(self.HomeMenu_buttons, bg="white", text="Settings", width=15, font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.show_frame("SettingsMenu"))
        self.main_menu_button = Button(self.HomeMenu_buttons, bg="white", text="Main Menu", width=15, font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.show_frame("MainMenu"))
        
        self.tamagotchi_button.pack()
        self.tools_button.pack(pady=10)
        # self.games_button.pack()
        self.shop_button.pack()
        self.settings_button.pack(pady=10)
        self.main_menu_button.pack(pady=20)
        self.HomeMenu_buttons.pack(pady=30)

    def show_points(self):
        self.label = Label(self, textvariable=self.controller.points_display, font=self.controller.points_font)
        self.label.pack(pady=30)



class TamagotchiMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.Tamagotchi_title = Label(self, text="Tamagotchi", font=self.controller.title_font).pack(side="top", fill="x", pady=20)
        self.init_GUI()
        self.init_Tamagotchi_buttons()
        
    def init_Tamagotchi_buttons(self):
        self.Tamagotchi_buttons = Frame(self, borderwidth=0, relief='solid')
        self.home_menu_button = Button(self.Tamagotchi_buttons, text="Home Menu", width=15, font=self.controller.buttons_font, borderwidth=3, command=lambda: self.controller.show_frame("HomeMenu"))
        self.home_menu_button.grid(row=0, column=0, padx=30)
        self.shop_menu_button = Button(self.Tamagotchi_buttons, text="Shop", width=15, font=self.controller.buttons_font, borderwidth=3, command=lambda: self.controller.show_frame("ShopMenu"))
        self.shop_menu_button.grid(row=0, column=1)
        self.Tamagotchi_buttons.pack(pady=15)

    def init_GUI(self):
        graphic_size = (int(APP_WIN_WIDTH/10*7), int(APP_WIN_HEIGHT/20*15))
        infos_size = (int(APP_WIN_WIDTH/10*3), int(APP_WIN_HEIGHT/20*15))
        self.GUI = Frame(self, width=graphic_size[0]-40, height=graphic_size[1], bd=0, relief="solid")
        self.graphic_frame = Frame(self.GUI, bg="black", width=graphic_size[0]-20, height=graphic_size[1], bd=2, relief="solid")
        self.infos_frame = Frame(self.GUI, bg="white", width=infos_size[0]-20, height=infos_size[1], bd=2, relief="solid")
        self.graphic_canvas = Canvas(self.graphic_frame, width=graphic_size[0]-20, height=graphic_size[1])

        self.graphic_frame.pack(side=LEFT)
        self.infos_frame.pack(side=RIGHT, fill='both')
        self.graphic_canvas.pack()
        self.GUI.pack(padx=40)
        
        self.__load_graphics()
        self.__load_infos()
        
    def __load_graphics(self):
        graphic_size = (int(APP_WIN_WIDTH/10*7), int(APP_WIN_HEIGHT/20*15))
        self.wall_img = ImageTk.PhotoImage(Image.open("ressources/" + self.controller.AllData["Equiped_W"] + ".png").resize((graphic_size[0], int(graphic_size[1]/15*12)+5), Image.LANCZOS))
        self.ground_img = ImageTk.PhotoImage(Image.open("ressources/" + self.controller.AllData["Equiped_G"] + ".png").resize((graphic_size[0],int(graphic_size[1]/15*3)), Image.LANCZOS))
        self.furniture_img = ImageTk.PhotoImage(Image.open("ressources/" + self.controller.AllData["Equiped_F"] + ".png").resize((int(graphic_size[0]/7), int(graphic_size[1]/15*5)), Image.LANCZOS))
        self.pet_img = ImageTk.PhotoImage(Image.open("ressources/" + self.controller.AllData["Equiped_P"] + ".png").resize((int(graphic_size[0]/7*1.15), int(graphic_size[1]/15*4)), Image.LANCZOS))
    
        self.wall_canvas = self.graphic_canvas.create_image(0,0,image=self.wall_img, anchor="nw")
        self.ground_canvas = self.graphic_canvas.create_image(0,int(graphic_size[1]/15*12)+5,image=self.ground_img, anchor="nw")
        self.furniture_canvas = self.graphic_canvas.create_image(int(graphic_size[0]/7*5), int(graphic_size[1]/15*7)+5, image=self.furniture_img, anchor="nw")
        self.pet_canvas = self.graphic_canvas.create_image(int(graphic_size[0]/7*3), int(graphic_size[1]/15*9), image=self.pet_img, anchor="nw")
        
    def __load_infos(self):
        self.show_points()
        self.show_pet_hunger()
        
        self.actions_frame = Frame(self.infos_frame, bg="black")
        self.feed_button = Button(self.actions_frame, text="Feed", width=13, bg='white', font=self.controller.buttons_font, borderwidth=1, command=lambda: self.feed())
        self.edit_button = Button(self.actions_frame, text="Edit", width=13, bg='white', font=self.controller.buttons_font, borderwidth=1, command=lambda: self.edit_background())
        self.feed_button.pack(padx=1, pady=3, side='left')
        self.edit_button.pack(padx=1, pady=3, side='right')
        self.actions_frame.pack(side='bottom', fill='both')

    def show_points(self):
        self.label = Label(self.infos_frame, width=22, textvariable=self.controller.points_display, font=self.controller.points_font)
        self.label.pack(pady=20)
          
    def show_pet_hunger(self):
        self.label = Label(self.infos_frame, width=22, textvariable=self.controller.Tamagotchi.get_hunger_display(), font=self.controller.points_font)
        self.label.pack()   
            
    def feed(self):
        if (self.controller.points > 0):
            self.controller.Tamagotchi.feed()
            self.controller.points -= 1
        else :
            print("Not enough points")
        self.controller.update_point_display()    

    def edit_background(self):
        self.edit_frame = Frame(self, bg='lightgray', width=int(APP_WIN_WIDTH/10*3), height=int(APP_WIN_HEIGHT/20*15), bd=0, relief="solid", padx=8, pady=0)
        self.edit_listbox = Listbox(self.edit_frame, width=21, height=12, font=('MS Gothic', 21), bg="white", fg="black", highlightthickness=0, selectbackground="#a6a6a6", activestyle="none")
        self.edit_scrollbar = Scrollbar(self.edit_frame)
        
        self.edit_buttons_frame = Frame(self.edit_frame, bg='lightgray', width=100, height=50, bd=0, relief="solid")
        
        self.close_edit = Button(self.edit_buttons_frame, text="Close", width=7, font=self.controller.buttons_font, borderwidth=2, command=lambda:self.close_edit_menu()).grid(row=2, column=1, pady=10)
        self.walls_load = Button(self.edit_buttons_frame, text="Walls",  width=7, font=self.controller.buttons_font, borderwidth=1, command=lambda:self.show_elements("Walls")).grid(row=0, column=0, pady=2, padx=18)
        self.grounds_load = Button(self.edit_buttons_frame, text="Grounds", width=7, font=self.controller.buttons_font, borderwidth=1, command=lambda:self.show_elements("Grounds")).grid(row=0, column=1, padx=18, pady=5)
        self.furnitures_load = Button(self.edit_buttons_frame, text="Furnitures", width=8, font=self.controller.buttons_font, borderwidth=1, command=lambda:self.show_elements("Furnitures")).grid(row=1, column=0, padx=10, pady=5)
        self.pets_load = Button(self.edit_buttons_frame, text="Pets", width=7, font=self.controller.buttons_font, borderwidth=1, command=lambda:self.show_elements("Pets")).grid(row=1, column=1, padx=5)
        
        self.edit_listbox.bind('<Double-1>', self.change_background)
        
        self.edit_frame.pack(side=RIGHT)
        self.edit_frame.place(x=int(APP_WIN_WIDTH/10*7)+30,y=79)
        self.edit_listbox.pack(pady=5)
        
        self.edit_buttons_frame.pack(pady=5, side=BOTTOM)     

    def show_elements(self, element_type:str):
        self.edit_listbox.delete(0,END)
        for element in self.controller.AllData[element_type]:
            self.edit_listbox.insert(END, element)
     
    def change_background(self, event):
        try:
            element_pos = self.edit_listbox.curselection()[0]
        except IndexError:
            print("CHANGE BACKGROUND: No element has been selected")
            return -1
        
        element_str = self.edit_listbox.get(element_pos)
        self.change_element(element_str)
    
    def change_element(self, element:str):
        element_img = "ressources/" + element + ".png"
        graphic_size = (int(APP_WIN_WIDTH/10*7), int(APP_WIN_HEIGHT/20*15))
        if (element[0:1] == "w"):
            self.wall_img = ImageTk.PhotoImage(Image.open(element_img).resize((graphic_size[0], int(graphic_size[1]/15*12)+5), Image.LANCZOS))
            self.wall_canvas = self.graphic_canvas.create_image(0,0, image=self.wall_img, anchor="nw")
            self.graphic_canvas.lift(self.pet_canvas)
            self.graphic_canvas.lift(self.furniture_canvas)
            self.controller.AllData["Equiped_W"] = element
        elif (element[0:1] == "g"):
            self.ground_img = ImageTk.PhotoImage(Image.open(element_img).resize((graphic_size[0],int(graphic_size[1]/15*3)), Image.LANCZOS))
            self.ground_canvas = self.graphic_canvas.create_image(0,int(graphic_size[1]/15*12)+5, image=self.ground_img, anchor="nw")
            self.graphic_canvas.lift(self.pet_canvas)
            self.graphic_canvas.lift(self.furniture_canvas)
            self.controller.AllData["Equiped_G"] = element
        elif (element[0:1] == "f"):
            self.furniture_img = ImageTk.PhotoImage(Image.open(element_img).resize((int(graphic_size[0]/7), int(graphic_size[1]/15*5)), Image.LANCZOS))
            self.furniture_canvas = self.graphic_canvas.create_image(int(graphic_size[0]/7*5), int(graphic_size[1]/15*7)+5, image=self.furniture_img, anchor="nw")
            self.graphic_canvas.lift(self.pet_canvas)
            self.graphic_canvas.lift(self.furniture_canvas)
            self.controller.AllData["Equiped_F"] = element
        elif (element[0:1] == "p"):
            self.pet_img = ImageTk.PhotoImage(Image.open(element_img).resize((int(graphic_size[0]/7*1.15), int(graphic_size[1]/15*4)), Image.LANCZOS))
            self.pet_canvas = self.graphic_canvas.create_image(int(graphic_size[0]/7*3), int(graphic_size[1]/15*9), image=self.pet_img, anchor="nw")
            self.graphic_canvas.lift(self.pet_canvas)
            self.graphic_canvas.lift(self.furniture_canvas) 
            self.controller.AllData["Equiped_P"] = element
        else:
            print("unknown file, maybe file isn't .png or isn't any of these elements")

    def close_edit_menu(self):
        self.edit_frame.destroy()
        self.edit_listbox.destroy()
        self.edit_scrollbar.destroy()



class ToolsMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.Tools_title = Label(self, text="Tools", font=self.controller.title_font).pack(side="top", fill="x", pady=20)
        self.init_Tools_buttons()       
        
    def init_Tools_buttons(self):
        self.Tools_buttons = Frame(self, borderwidth=1, bg="white", relief='solid')
        self.home_menu_button = Button(self.Tools_buttons, text="Home Menu", width=15, bg="white", font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.show_frame("HomeMenu"))
        self.todolist_button = Button(self.Tools_buttons, text="Todolist", bg="white", width=15, font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.show_frame("TodolistMenu"))
        
        self.todolist_button.pack()
        self.home_menu_button.pack(pady=20)
        self.Tools_buttons.pack(pady=30)
        


class ShopMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.shop_font = ('MS Gothic', 20)
        self.shop_items = self.controller.AllData['Shop_items']
        self.Tools_title = Label(self, text="Shop", font=self.controller.title_font).pack(side="top", fill="x", pady=20)
        
        self.init_points_display()
        self.init_shop_GUI()
        self.init_shop_item()
        self.init_buttons()
    
    def init_shop_GUI(self):
        self.shop_frame = Frame(self, width=700, height=40, bd=1, relief="solid")
        self.shop_frame.pack(pady=30)
        self.shop_listbox = Listbox(self.shop_frame, width=22, height=14, font=self.shop_font, bg="white", highlightthickness=0, selectbackground="#a6a6a6", activestyle="none") # fg="#464646"
        self.shop_listbox.bind('<Double-1>', self.load_infos) # detecte le double click()
        
        self.shop_scrollbar = Scrollbar(self.shop_frame)
        self.shop_listbox.config(yscrollcommand=self.shop_scrollbar.set)  # Hide scrollbar until there is too many items...
        self.shop_scrollbar.config(command=self.shop_listbox.yview)
        self.shop_scrollbar.pack(side='left', fill=Y)
        self.shop_listbox.pack(side=LEFT, padx=3, pady=5)

        self.item_infos_frame = Frame(self.shop_frame, width=400, height=400, bd=1, relief="solid", bg="white").pack(side=RIGHT, padx=2, pady=2)
        self.item_infos_name = None          
        self.item_infos_price = None 
        self.item_infos_type = None 
        self.item_infos_description = None 
        self.item_infos_image = None 
        
    def load_infos(self, event):
        if (self.item_infos_name != None):
            self.item_infos_name.destroy()
            self.item_infos_price.destroy()
            
        cs = self.shop_listbox.curselection()
        item_name = "Name: " + self.shop_items[cs[0]][0]
        item_price = "Price: " + str(self.shop_items[cs[0]][1]) + " points"
        
        self.item_infos_name = Label(self.item_infos_frame, text=item_name, font=('MS Gothic', 18), bg="white")
        self.item_infos_name.pack()
        self.item_infos_name.place(x=APP_WIN_WIDTH/4*2-30, y=APP_WIN_HEIGHT/4*2-240)
        
        self.item_infos_price = Label(self.item_infos_frame, text=item_price, font=('MS Gothic', 18), bg="white")
        self.item_infos_price.pack()
        self.item_infos_price.place(x=APP_WIN_WIDTH/4*2-30, y=APP_WIN_HEIGHT/4*2-200)

    def init_shop_item(self):
        for item in self.shop_items:
            self.shop_listbox.insert(END, item[0])

    def init_points_display(self):
        self.point_frame = Frame(self, width=100, height=40, bd=0, relief="solid")
        self.label = Label(self.point_frame, width=22, textvariable=self.controller.points_display, font=self.controller.points_font)
        self.label.pack(pady=20)
        self.point_frame.pack()
        self.point_frame.place(x=APP_WIN_WIDTH/7*5,y=10)
        
    def init_buttons(self):
        self.buttons_frame = Frame(self, width=700, height=50, bd=0, relief="solid", pady=10)
        self.go_back_button = Button(self.buttons_frame, text="Home Menu", font=self.controller.buttons_font, borderwidth=3, command=lambda:self.hide_before_changing_page("HomeMenu")).grid(row=0, column=0, padx=40)
        self.go_to_shop_button = Button(self.buttons_frame, text="Tamagotchi",font=self.controller.buttons_font, borderwidth=3, command=lambda:self.hide_before_changing_page("TamagotchiMenu")).grid(row=0, column=3, padx=40)
        self.buy_button = Button(self.buttons_frame, font=self.controller.buttons_font, borderwidth=3, width=5, text="Buy", command=lambda:self.buy()).grid(row=0, column=2, padx=40)
        self.buttons_frame.pack()

    def hide_before_changing_page(self, pagename):
        if (self.item_infos_name != None):
            self.item_infos_name.destroy()
            self.item_infos_price.destroy()
        self.controller.show_frame(pagename)

    def buy(self):
        try:
            cs = self.shop_listbox.curselection()
        except IndexError:
            print("No item has been selected")
            return
        
        item = self.shop_items[cs[0]]
        if (self.controller.points < item[1]): # if we have enough money to buy the item
            print("You don't have enough points :(")
        else:
            self.controller.points -= item[1]
            self.controller.update_point_display()  

            if item[2] == 'w':
                self.controller.AllData['Walls'].append(item[0])
                self.controller.AllData['Shop_items'].remove(item)
            if item[2] == 'g':
                self.controller.AllData['Grounds'].append(item[0])
            if item[2] == 'f':
                self.controller.AllData['Furnitures'].append(item[0])
            if item[2] == 'p':
                self.controller.AllData['Pets'].append(item[0])
            print("New item bought !")
            self.shop_listbox.delete(cs[0])
            self.shop_items.remove(item)
            self.item_infos_name.destroy()
            self.item_infos_price.destroy()
            
      

class TodolistMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.todolist_font = self.controller.todolists_font
        self.Todolist_title = Label(self, text="Todolist", font=self.controller.title_font).pack(side="top", fill="x", pady=20)
            
        self.init_Todolist_GUI()
        self.init_Todolist_buttons()
        self.bind_keys()

        for todo in self.controller.todolists:
            todolist = Todolist()
            todolist_name = "todo" + str(todolist.get_ID())
            if todo == []:
                pass
            else:
                for task in todo:
                    todolist.add_task(task[0], task[1])

            self.controller.Todolist.add_todolist(todolist)
            self.todos_listbox.insert(END, todolist_name)

        self.point_frame = Frame(self, width=100, height=40, bd=0, relief="solid")
        self.label = Label(self.point_frame, width=22, textvariable=self.controller.points_display, font=self.controller.points_font)
        self.label.pack(pady=20)
        self.point_frame.pack()
        self.point_frame.place(x=APP_WIN_WIDTH/7*5,y=10)
        
 
# =============================================================================
#         SET TODOLIST GUI
# =============================================================================
    def init_Todolist_buttons(self):
        self.Todolist_buttons = Frame(self, borderwidth=0, relief='solid')
        self.tools_button = Button(self.Todolist_buttons, text="Tools", width=10, font=self.controller.buttons_font, borderwidth=3, command=lambda: self.controller.show_frame("ToolsMenu"))
        self.tamagotchi_button = Button(self.Todolist_buttons, text="Tamagotchi", width=10, font=self.controller.buttons_font, borderwidth=3, command=lambda: self.controller.show_frame("TamagotchiMenu"))
        self.create_todo_button = Button(self.Todolist_buttons, text="New TODO",bg="white", width=15, font=self.controller.buttons_font, borderwidth=3, command=self.create_TODO)

        self.tools_button.grid(row=0, column=0)
        self.create_todo_button.grid(row=0, column=1, padx=150)
        self.tamagotchi_button.grid(row=0, column=2)
        self.Todolist_buttons.pack()
        
        
    def init_Todolist_GUI(self):
        self.Todolist_frame = Frame(self, width=700, height=350, bd=2, relief="solid")
        
        self.todos_frame = Frame(self.Todolist_frame, width=200, height=350, bd=0, relief="solid")
        self.todos_listbox_frame = Frame(self.todos_frame, width=180, height=350, bd=0, relief="solid")
        self.todos_listbox = Listbox(self.todos_listbox_frame, width=25, height=9, font=self.todolist_font, bg="white", fg="#464646", highlightthickness=0, selectbackground="#a6a6a6", activestyle="none")
        self.todos_scrollbar = Scrollbar(self.todos_listbox_frame)
        self.todos_listbox.config(yscrollcommand=self.todos_scrollbar.set)  # Hide scrollbar until there is too many items...
        self.todos_scrollbar.config(command=self.todos_listbox.yview)

        self.tasks_frame = Frame(self.Todolist_frame, width=500, height=350, bd=0, relief="solid")
        self.tasks_listbox_frame = Frame(self.tasks_frame, width=480, height=400, bd=0, relief="solid")
        self.tasks_listbox = Listbox(self.tasks_listbox_frame, width=30, height=9, font=self.todolist_font, bg="white", fg="#464646", highlightthickness=0, selectbackground="#a6a6a6", activestyle="none")
        self.tasks_scrollbar = Scrollbar(self.tasks_listbox_frame)
        self.tasks_listbox.config(yscrollcommand=self.tasks_scrollbar.set)  # Hide scrollbar until there is too many items...
        self.tasks_scrollbar.config(command=self.tasks_listbox.yview)

        self.point_frame = Frame(self, width=100, height=40, bd=0, relief="solid")
        self.controller.points_display.set("Points: {0}".format(self.controller.points)) 
        self.entry = Entry(self, font=self.todolist_font, width=35) # Entry to write new tasks to do

        self.Todolist_frame.pack(pady=20)
        
        self.todos_frame.pack(side='left')
        self.todos_listbox_frame.pack()
        self.todos_listbox.pack(side='right')
        self.todos_scrollbar.pack(side='left', fill=Y)
        
        self.tasks_frame.pack(side='right')
        self.tasks_listbox_frame.pack()
        self.tasks_listbox.pack(side='left')
        self.tasks_scrollbar.pack(side='right', fill=Y)

        
        self.entry.pack()
        self.point_frame.pack()
        
    
   

    # Creates a todolist
    def create_TODO(self):
        todolist = Todolist()           # creates a new todolist
        todolist_name = "todo" + str(todolist.get_ID())
        self.controller.Todolist.add_todolist(todolist)    # adds the todolist in the list of todolists
        self.todos_listbox.insert(END, todolist_name)   # adds in the listbox the todolist, allowing to do some actions (load/delete todos)


    def delete_TODO(self, event):
        self.todos_listbox.selection_clear(0,END)
        self.todos_listbox.selection_set(self.todos_listbox.nearest(event.y))
        self.todos_listbox.activate(self.todos_listbox.nearest(event.y))
        
        todolist_pos = self.get_Listbox_click(self.todos_listbox,"DELETE TODO: No Todo-List has been selected") # checks if we selected a todolist
        if (todolist_pos == -1): return            # if nothing is selected, we do nothing
            
        if (todolist_pos == self.controller.Todolist.get_Loaded()):   # if the selected one is also the loaded one (printed on screen)...
            self.controller.Todolist.delete_selected_todolist()        # deletes this todolist and its tasks from the list of todolists
            self.todos_listbox.delete(todolist_pos)         # removes the todolist from display
            self.tasks_listbox.delete(0,END)                # removes its belonging tasks from display
            self.controller.Todolist.select_todolist(None)             # stops selecting this todolist (since it doesn't exist anymore)               
        else:                                      # else, e.g. if the selected one is NOT the loaded one OR no todolists are loaded...
            self.controller.Todolist.delete_todolist(todolist_pos)     # deletes the selected todolist and its tasks from the list of todolists
            self.todos_listbox.delete(todolist_pos)         # removes the todolist from display
                
            if (self.controller.Todolist.get_Loaded() == None): return             # if no list was loaded... there is nothing to do
            elif (self.controller.Todolist.get_Loaded() > todolist_pos):           # if the deleted todolist was before the loaded one, then the position of the loaded one is now wrong
                self.controller.Todolist.select_todolist(self.controller.Todolist.get_Loaded()-1)  # so we replace the pointer of the loaded todolist to the correct position to adress this issue
        
    def load_TODO(self, event):
        todolist_pos = self.get_Listbox_click(self.todos_listbox, "LOAD TODO: No Todo-List has been selected") # checks if we selected a todolist
        if (todolist_pos == -1): return # if nothing is selected, we do nothing
        self.tasks_listbox.delete(0,END)        # removes the tasks from display
            
        self.controller.Todolist.select_todolist(todolist_pos)               # places the pointer on the selected todolist
        selected_todolist = self.controller.Todolist.get_selected_todolist() # gets the selected todolist
        tasks_list = selected_todolist.get_Tasks()        # gets its belonging tasks
        #self.time_left = selected_todolist.get_time_left()
        #self.time_string.set("Timer: {0} s".format(self.time_left))
        
        index = 0
        for task in tasks_list:
            if (task[1]):                                 # if the task is marked...
                task_completed = task[0] + " ✔"            # adds the checked mark
                self.tasks_listbox.insert(END,task_completed)       # adds task to display
                self.tasks_listbox.itemconfig(index,fg="#dedede")   # colors the task in lightgray
            else:                                         # if the task is unmarked...
                self.tasks_listbox.insert(END,task[0])              # adds task to display
            index += 1
        self.color_loaded_TODO() # colors the selected todolist finally loaded in red
            
    # Colors the loaded todolist, for aesthetic purposes
    def color_loaded_TODO(self):
        for i in range (0,self.todos_listbox.size()):
            if (self.controller.Todolist.get_Loaded() == i):               # if this todolist is loaded...
                self.todos_listbox.itemconfig(i,fg="#de0000")    # colors this todolist in red
            else:                                       # else (e.g. not loaded todolist)...
                self.todos_listbox.itemconfig(i,fg="#464646")    # colors this todolist in black
               
    def get_Listbox_click(self, listbox:Listbox, error_message:str):
        try:
            pos = listbox.curselection()[0] # Position de l'element selectioné dans la liste
        except IndexError:
            print(error_message)
            return -1
        return pos           
       
    def add_task(self, event):
        if (self.controller.Todolist.get_Loaded() == None):    # if none of the todolists has been loaded
            print("ADD TASK: No Todo-lists has been loaded")
            self.entry.delete(0,END)        # removes the written task from the entry, for ergonomic purposes
            return
            
        if (self.entry.get() != ""):                              # if our entry isn't empty
            if not (self.entry.get().isspace()):                   # if our entry isn't just spaces
                self.tasks_listbox.insert(END, self.entry.get())            # adds the written task to display
                selected_todolist = self.controller.Todolist.get_selected_todolist()   # gets the loaded todolist
                selected_todolist.add_task(self.entry.get())        # adds the written task in the loaded todolist
            else: # else the text is just spaces
                print("ADD TASK: You can't see a task with only spaces !")
        else:     # else the text is empty
            print("ADD TASK: You can't add nothing !")
        self.entry.delete(0,END)                                  # removes the written task from the entry, for ergonomic purposes
            
    # Deletes a task in the selected todolist
    def delete_task(self, event):
        self.tasks_listbox.selection_clear(0,END)
        self.tasks_listbox.selection_set(self.tasks_listbox.nearest(event.y))
        self.tasks_listbox.activate(self.tasks_listbox.nearest(event.y))
        task_pos = self.get_Listbox_click(self.tasks_listbox, "DELETE TASK: No task has been selected") # checks if we selected a task
        if (task_pos == -1): return                       # if nothing is selected, we do nothing
        selected_todolist = self.controller.Todolist.get_selected_todolist() # else...
        selected_todolist.remove_task(task_pos)           # deletes the task from the todolist
        self.tasks_listbox.delete(task_pos)                       # removes the selected task from display
        
    # Marks a task down or unmark one in the selected todolist
    def mark_unmark_task(self, event):
        self.tasks_listbox.selection_clear(0,END)
        self.tasks_listbox.selection_set(self.tasks_listbox.nearest(event.y))
        self.tasks_listbox.activate(self.tasks_listbox.nearest(event.y))
        
        task_pos = self.get_Listbox_click(self.tasks_listbox, "MARK/UNMARK TASK: No task has been selected") # checks if we selected a task
        if (task_pos == -1): return  # if nothing is selected, we do nothing
        """ To emulate the mark down/unmark* :
        Step 1: Copy the selected task and add/remove* the ✔ to it,
        Step 2: Delete the one without/with* a ✔ in the display
        Step 3: Replace the copied one in the display at the same place
        """
        task_string = self.tasks_listbox.get(task_pos)
        if (task_string[len(task_string)-1] == "✔"): # if the task is marked
            task_string = task_string[0:len(task_string)-2] # update the text of the task
            self.tasks_listbox.delete(task_pos)
            self.tasks_listbox.insert(task_pos,task_string)
            self.tasks_listbox.itemconfig(task_pos,fg="#464646")
            self.controller.Todolist.get_selected_todolist().unmark_completed_task(task_pos)
            self.controller.decrement_points(event=event)
        else: # Else, if the task is unmarked
            task_string = task_string + " ✔"
            self.tasks_listbox.delete(task_pos)
            self.tasks_listbox.insert(task_pos,task_string)
            self.tasks_listbox.itemconfig(task_pos,fg="#dedede")
            self.controller.Todolist.get_selected_todolist().mark_task_as_completed(task_pos)
            self.controller.increment_points(event=event)

    def bind_keys(self):
        self.todos_listbox.bind('<Double-1>', self.load_TODO)        # double click to load the todo list
        self.todos_listbox.bind('<Button-3>', self.delete_TODO)      # right click after selected a list to delete it
        self.tasks_listbox.bind('<Double-1>', self.mark_unmark_task) # double click to mark/unmark a task
        self.tasks_listbox.bind("<Button-3>", self.delete_task)      # right click after selected a task to delete it
        self.entry.bind("<Return>", self.add_task)
        
 

class SettingsMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.Settings_title = Label(self, text="Settings", font=self.controller.title_font).pack(side="top", fill="x", pady=20)
        self.init_Settings_buttons()

    def init_Settings_buttons(self):
        self.Settings_buttons = Frame(self, borderwidth=1, bg="white", relief='solid')
        self.home_menu_button = Button(self.Settings_buttons, bg="white", text="Home Menu", width=15, font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.show_frame("HomeMenu"))
        #self.size1024x768 = Button(self.Settings_buttons, text="1024x768", width=15, font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.resize_window(1024,768))
        #self.size800x600 = Button(self.Settings_buttons, text="800x600", width=15, font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.resize_window(800,600))
        
        self.home_menu_button.pack()
        #self.size1024x768.pack()
        #self.size800x600.pack()
        self.Settings_buttons.pack()



class CreditsMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.Credits_title = Label(self, text="Credits", font=self.controller.title_font).pack(side="top", fill="x", pady=20)
        self.Credits_text = Label(self, text="Realised by Henrique D.M.M\n", font=self.controller.buttons_font).pack(fill="x", pady=50)
        self.init_Credits_buttons()

    def init_Credits_buttons(self):
        self.Credits_buttons = Frame(self, borderwidth=1, bg="white", relief='solid')
        self.main_menu_button = Button(self.Credits_buttons, bg="white", text="Main Menu", width=15, font=self.controller.buttons_font, borderwidth=0, command=lambda: self.controller.show_frame("MainMenu"))
    
        self.main_menu_button.pack()
        self.Credits_buttons.pack()




app = TodochiiApp()
app.title("Todochii")
app.geometry(str(APP_WIN_WIDTH) + 'x' + str(APP_WIN_HEIGHT)) # 1280x720
app.minsize(APP_WIN_WIDTH, APP_WIN_HEIGHT)
app.maxsize(APP_WIN_WIDTH, APP_WIN_HEIGHT)
app.iconbitmap("ressources/todochii icon.ico")
app.protocol("WM_DELETE_WINDOW", app.quit_app)
app.mainloop()  
