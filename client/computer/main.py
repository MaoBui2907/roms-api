
import tkinter as tk

from tkinter import filedialog
import math
import os
import urllib.parse
from tkinter import ttk
import json
import requests
from PIL import Image, ImageTk
from io import BytesIO

class RomsBrowser:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Emulator roms browser")
        self.window.geometry('645x580')
        self.window.resizable(False, False)

        self.control_frame = tk.LabelFrame(self.window, text="Search")
        self.control_frame.grid(row=0, sticky='WE', padx=10, pady=10, ipadx=10, ipady=10)


        self.categories = []
        self.categories_title = []
        self.categories_id = []

        self.api_host = "http://localhost:2020"

        try:
            self.categories_url = self.api_host + "/categories/0/10000"
            res = requests.get(self.categories_url)
            self.categories = json.loads(res.text).get("data")
            self.categories_title = [c.get("title") for c in self.categories]
            self.categories_id = [c.get("id") for c in self.categories]
        except:
            print("Network error")

        self.categories_var = tk.StringVar(self.control_frame)
        self.categories_var.set(self.categories_title[0] if self.categories_title else '')
        self.categories_dropdown = ttk.Combobox(self.control_frame, textvariable=self.categories_var, values=self.categories_title)
        self.categories_dropdown.grid(column=0, row=0, sticky="WE", padx=10, pady=10)
        
        
        self.regions = []
        self.regions_title = []
        self.regions_id = []
        try:
            self.regions_url = self.api_host + "/regions"
            res = requests.get(self.regions_url)
            self.regions = json.loads(res.text).get("data")
            self.regions_title = [r.get("title") for r in self.regions]
            self.regions_id = [r.get("id") for r in self.regions]
        except requests.exceptions.ConnectionError:
            print("Network error")

        self.regions_var = tk.StringVar(self.control_frame)
        self.regions_var.set(self.regions_title[0] if self.regions_title else '')
        self.regions_dropdown = ttk.Combobox(self.control_frame, textvariable=self.regions_var, values=self.regions_title)
        self.regions_dropdown.grid(column=1, row=0, sticky="WE", padx=10, pady=10)


        self.search_box = tk.Entry(self.control_frame, text="search...")
        self.search_box.grid(column=2, row=0, stick="WE", padx=10, pady=10)

        
        self.search_button = tk.Button(self.control_frame,text='search', command=self.search_button_click)
        self.search_button.grid(column=3, row=0, stick="WE", padx=10, pady=10)

        self.result_frame = tk.LabelFrame(self.window, text="Result")
        self.result_frame.grid(row=1, sticky='WE', padx=10, pady=10, ipadx=10, ipady=10)

        self.search_url = self.api_host + "/search"

        self.result_list = tk.ttk.Treeview(self.result_frame, selectmode="browse", height=7)
        self.result_list['columns'] = ('one', 'two')
        self.result_list.column("#0", width=60, minwidth=50, stretch=tk.YES)
        self.result_list.column("one", width=300, minwidth=200, stretch=tk.YES)
        self.result_list.column("two", width=80, minwidth=80, stretch=tk.YES)
        self.result_list.heading("#0", text="Number", anchor=tk.W)
        self.result_list.heading("one", text="Title", anchor=tk.W)
        self.result_list.heading("two", text="Region", anchor=tk.W)
        self.result_list.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.result_list.grid(row=0, column=0, padx=10, pady=5)
        self.search_roms = []
        self.selected_rom = None
        self.download_queue = []

        self.page = 1
        self.item_per_page = 20

        self.logo_label = tk.Label(self.result_frame)
        self.logo_label.grid(row=0, column=1, padx=5, pady=5, sticky='WE')

        self.search_control = tk.Frame(self.result_frame, width=95)
        self.search_control.grid(row=1, column=0, sticky='WENS', padx=5, pady=5)
        self.prev_page_button = tk.Button(self.search_control, state="disable", text="<", command=self.prev_page)
        self.prev_page_button.pack(side=tk.LEFT)
        self.cur_page_show = tk.Button(self.search_control, state="disable", text=self.page)
        self.cur_page_show.pack(side=tk.LEFT)
        self.next_page_button = tk.Button(self.search_control, text=">", command=self.next_page)
        self.next_page_button.pack(side=tk.LEFT)

        self.add_queue_button = tk.Button(self.search_control, text="add queue", command=self.add_to_download_list)
        self.add_queue_button.pack(side=tk.RIGHT)

        self.action_frame = tk.LabelFrame(self.window, text="Download")
        self.action_frame.grid(row=2,sticky='WE', padx=10, pady=10, ipadx=10, ipady=10)
        self.download_queue_list = tk.ttk.Treeview(self.action_frame, selectmode="browse", height=5)
        self.download_queue_list['columns'] = ('one', 'two', 'three')
        self.download_queue_list.column("#0", width=60, minwidth=50, stretch=tk.YES)
        self.download_queue_list.column("one", width=250, minwidth=200, stretch=tk.YES)
        self.download_queue_list.column("two", width=80, minwidth=80, stretch=tk.YES)
        self.download_queue_list.column("three", width=50, minwidth=50, stretch=tk.YES)
        self.download_queue_list.heading("#0", text="Number", anchor=tk.W)
        self.download_queue_list.heading("one", text="Title", anchor=tk.W)
        self.download_queue_list.heading("two", text="Category", anchor=tk.W)
        self.download_queue_list.heading("three", text="Region", anchor=tk.W)
        self.download_roms_selected = None
        self.download_queue_list.bind("<<TreeviewSelect>>", self.on_download_tree_select)
        self.download_queue_list.grid(row=0, column=0, padx=10, pady=5)

        self.download_location_control = tk.Frame(self.action_frame)
        self.download_location_control.grid(row=0, column=1, padx=10, pady=5)

        self.save_location_button = tk.Button(self.download_location_control, text="save as..", command=self.browser_save_location)
        self.save_location_button.pack(side=tk.TOP, fill='x')
        self.start_download_button = tk.Button(self.download_location_control, text="start", command=self.start_download_roms)
        self.start_download_button.pack(side=tk.TOP, fill='x')
        self.download_progress_bar = tk.ttk.Progressbar(self.download_location_control, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.download_progress_bar.pack(side=tk.TOP, fill='x') 

        self.download_control_frame = tk.Frame(self.action_frame, width=95)
        self.download_control_frame.grid(row=1, column=0, sticky="we", padx=10, pady=5)

        self.remove_from_queue = tk.Button(self.download_control_frame, text="del", command=self.remove_queue_roms)
        self.remove_from_queue.pack(side=tk.RIGHT)
        self.tempdir=os.getcwd()


    def on_download_tree_select(self, event):
        for item in self.download_queue_list.selection():
            item_text = self.download_queue_list.item(item,"text")
            self.download_roms_selected = self.download_queue[int(item_text) - 1]

    def remove_queue_roms(self):
        del self.download_queue[self.download_queue.index(self.download_roms_selected)]
        self.update_download_list()

    def browser_save_location(self):
        self.tempdir = filedialog.askdirectory(parent=self.window, initialdir=self.tempdir, title="Save location")
        

    def start_download_roms(self):
        for i in range(len(self.download_queue)):
            url = self.download_queue[i].get('file')[0]
            res = requests.get(url)
            file_name = urllib.parse.urlparse(url)[2].rpartition('/')[-1]
            with open(os.path.join(self.tempdir, file_name), 'wb') as fb:
                fb.write(res.content)
            self.download_progress_bar['value'] = math.floor((i +1)*100/len(self.download_queue))
        pass

    def update_button_state(self):
        if self.page <=1:
            self.prev_page_button['state'] = "disable"
        else:
            self.prev_page_button['state'] = 'normal'
        self.cur_page_show['text']=self.page

    def next_page(self):
        self.page += 1
        self.update_button_state()
        self.update_search_list()

    def prev_page(self):
        self.page -= 1
        self.update_button_state()
        self.update_search_list()

    def add_to_result_list(self, i:int, target:tuple):
        self.result_list.insert("", "end", text=i, values=target)

    def add_to_download_list(self):
        if self.selected_rom not in self.download_queue:
            self.download_queue.append(self.selected_rom)
            self.update_download_list()

    def update_download_list(self):
        self.download_queue_list.delete(*self.download_queue_list.get_children())
        for i in range(len(self.download_queue)):
            item = self.download_queue[i]
            tit = item.get('title')
            cate = self.categories_title[self.categories_id.index(item.get('category'))]
            reg = self.regions_title[self.regions_id.index(item.get('region'))]
            self.download_queue_list.insert("", "end", text=i + 1, values=(tit, cate, reg))

    def clear_result_list(self):
        for i in self.result_list.get_children():
            self.result_list.delete(i)

    def on_tree_select(self, event):
        for item in self.result_list.selection():
            item_text = self.result_list.item(item,"text")
            self.selected_rom = self.search_roms[int(item_text) - 1]
            res = requests.get(self.selected_rom.get('logo')[0])
            logo = Image.open(BytesIO(res.content)).resize((120, 120))
            img_tk = ImageTk.PhotoImage(logo)
            self.show_logo(img_tk)

    def show_logo(self, img):
        self.logo_label.configure(image=img)
        self.logo_label.image = img

    def update_search_list(self):
        cate_tit = self.categories_var.get()
        category_id = self.categories_id[self.categories_title.index(cate_tit)]
        reg_tit = self.regions_var.get()
        region_id = self.regions_id[self.regions_title.index(reg_tit)]
        keyword = self.search_box.get()
        dataform = {
            "category": category_id,
            "region": region_id,
            "keyword": keyword,
            "offset": (self.page - 1) * self.item_per_page,
            "limit": self.item_per_page
        }
        res = requests.post(self.search_url, data=dataform)
        data = json.loads(res.text).get("data")
        self.search_roms = data
        self.clear_result_list()
        for i in range(len(data)):
            target = (data[i].get('title'), data[i].get('region'))
            self.add_to_result_list(i + 1, target)

    def search_button_click(self):
        self.page = 1
        self.update_button_state()
        self.update_search_list()

if __name__ == "__main__":
    app = RomsBrowser()
    app.window.mainloop()