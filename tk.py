# this file builds the GUI
# it also acts at the entrypoint for the rest of the program

from tkinter import *
import customtkinter as ctk # we use a fork of TK called customTK. it looks much nicer and has more features such as the progressbar
from tkinter import filedialog # this is the file selection GUI. we can borrow it from vanilla TK
import threading
import webbrowser

ctk.set_appearance_mode('light')

root = ctk.CTk()

github = 'https://github.com/notnotmelon/conocophillips'
discord = 'https://discord.gg/3jRh2W25ZE' # acm discord

# add newlines every 80 characters after spaces
def make_readable(text):
    result = ''
    i = 0
    while i < len(text):
        result += text[i:i+80] + '\n'
        i += 80
    return result

def format_percentage(unsearchable_urls, percent):
    percent = round(percent * 1000) / 10
    return f'{percent}%' if len(unsearchable_urls) == 0 else f'>{percent}%'

class ResultsWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x600")
        # create scrollable frame
        self.scroll = ctk.CTkScrollableFrame(self, label_text='Results', width=3000, height=600, corner_radius=0)
        self.scroll.pack()

    # build the 2ed window that shows the search results
    def process_results(self, plagiarisized_substrings, unsearchable_urls, percent):
        if len(plagiarisized_substrings) == 0:
            switch = ctk.CTkLabel(self.scroll, text='100% original!')
            switch.pack(padx=20, pady=20)
            switch = ctk.CTkLabel(self.scroll, text='We searched far and wide, but could not find any plagiarized text!')
            switch.pack(padx=20, pady=0)
        else:
            switch = ctk.CTkLabel(self.scroll, text=f'{format_percentage(unsearchable_urls, percent)} plagiarized')
            switch.pack(padx=20, pady=20)
            switch = ctk.CTkLabel(self.scroll, text='We found the following plagiarized text:')
            switch.pack(padx=20, pady=0)
        for substring, url in plagiarisized_substrings:
            print(f'"{substring}" was plagiarized from {url}')
            switch = ctk.CTkLabel(self.scroll, text=f'{make_readable(substring)}\n\nwas plagiarized from')
            switch.pack(padx=20, pady=20)
            switch = ctk.CTkButton(self.scroll, text=url, command=lambda url=url: webbrowser.open(url), fg_color='transparent', border_width=0, text_color='blue')
            switch.pack(padx=20, pady=0)
        if len(unsearchable_urls) != 0:
            switch = ctk.CTkLabel(self.scroll, text='Our webcrawler could not search the following websites.\nPlease ensure that the text you entered is not plagiarized from any of these websites.')
            switch.pack(padx=20, pady=20)
        for url in unsearchable_urls:
            print('Could not search ' + url)
            switch = ctk.CTkButton(self.scroll, text=url, command=lambda url=url: webbrowser.open(url), fg_color='transparent', border_width=0, text_color='blue')
            switch.pack(padx=20, pady=0)
        return self

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Hawkathon 2023 Plagiarism Detection Software')
        self.geometry(f'{1100}x{580}')
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text='Conocomellon', font=ctk.CTkFont(size=20, weight='bold'))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, command=lambda: webbrowser.open(github), text='Github')
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, command=lambda: webbrowser.open(discord), text='Discord')
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text='Appearance Mode', anchor='w')
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=['Light', 'Dark', 'System'],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text='UI Scale', anchor='w')
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=['80%', '90%', '100%', '110%', '120%'],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.set('Light')
        self.scaling_optionemenu.set('100%')

        # create main entry and button
        self.entry = ctk.CTkEntry(self, placeholder_text='CTkEntry')
        self.entry.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky='nsew')
        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.grid(row=3, column=1, padx=(20, 00), pady=(20, 20), sticky='nsew')
        self.progressbar.set(1)

        self.main_button = ctk.CTkButton(master=self, fg_color='transparent', border_width=2, text_color=('gray10', '#DCE4EE'), text='Create Map', command=self.create_map)
        self.main_button.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky='nsew')

        # create textbox
        self.textbox = ctk.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, rowspan=2, padx=(20, 0), pady=(20, 0), sticky='nsew')
        self.textbox.insert('0.0', 'Enter suspicious text here...')

    # handles dark mode, light mode, or system mode
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    # handles changing the GUI scale
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace('%', '')) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print('sidebar_button click')

    def on_closing(self):
        self.destroy()
        exit()


    def create_map(self):
        print('qqqqq')

    
    action_queue = [] # list of functions to run on a 1 tick delay. for some reason we cannot run the .focus() command on the 2ed window until after 1 tick
    def duqueue(self):
        while len(self.action_queue) != 0:
            self.action_queue[0]()
            del self.action_queue[0]

    def finish_check_plagiarism(self, event):
        if event is not None:
            event.wait()
        print('Finished checking plagiarism')
        self.progressbar.configure(mode='determinnate')
        self.progressbar.set(1)
        self.progressbar.stop()
        plagiarisized_substrings, unsearchable_urls, percent = plagiarism_checker.results()
        self.action_queue.append(lambda: ResultsWindow(self).process_results(plagiarisized_substrings, unsearchable_urls, percent).focus())
        self.after(1, self.duqueue)

if __name__ == '__main__':
    app = App()
    app.mainloop()