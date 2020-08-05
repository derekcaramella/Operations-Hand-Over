import tkinter as tk
from datetime import datetime
from datetime import timedelta
import tkinter.messagebox
import pyodbc

con = pyodbc.connect(Trusted_Connection='no',
                     driver='{SQL Server}',
                     server='192.168.15.32',
                     database='Operator_Hand_Off',
                     UID='pladis_dba',
                     PWD='BigFlats')
cursor = con.cursor()

title_font = ("Times New Roman", 32)
head_font = ("Times New Roman", 24)
body_font = ("Times New Roman", 16)
shifts = ['1', '2', '3', '4']
workstations = ['Alpha Enrobing', 'Alpha Handpack', 'Bravo Enrobing', 'Bravo Packaging', 'Charlie Enrobing',
                'Charlie Packaging', 'Delta Enrobing', 'Delta Packaging', 'Echo Enrobing', 'Echo Packaging', 'Hayssen',
                'Kitchen Chocotech', 'SN', 'Sig 1', 'Sig 2']


class hand_over(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default='Icon.ico')
        tk.Tk.wm_title(self, 'Hand Over Log')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (entry_page, retrieval_page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(entry_page)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class entry_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bg = '#ffcccc'
        self['bg'] = bg
        entry_page_welcome = tk.Label(self, text='Log Page', font=title_font, bg=bg)
        entry_page_welcome.grid(row=0, column=1, columnspan=2, pady=10, padx=10)

        entry_page_timestamp = tk.Label(self, text='Date & Time:', font=head_font, bg=bg)
        entry_page_timestamp.grid(row=1, column=0, pady=10, padx=10, sticky='W')
        entry_page_workstation = tk.Label(self, text='Workstation:', font=head_font, bg=bg)
        entry_page_workstation.grid(row=2, column=0, pady=10, padx=10, sticky='W')
        entry_page_shift = tk.Label(self, text='Shift:', font=head_font, bg=bg)
        entry_page_shift.grid(row=3, column=0, pady=10, padx=10, sticky='W')
        entry_page_name = tk.Label(self, text='Name:', font=head_font, bg=bg)
        entry_page_name.grid(row=4, column=0, pady=10, padx=10, sticky='W')
        entry_page_title = tk.Label(self, text='Title:', font=head_font, bg=bg)
        entry_page_title.grid(row=5, column=0, pady=10, padx=10, sticky='W')
        entry_page_message = tk.Label(self, text='Message:', font=head_font, bg=bg)
        entry_page_message.grid(row=6, column=0, pady=10, padx=10, sticky='NW')

        entry_page_timestamp_entry_var = tk.StringVar()
        entry_page_timestamp_entry_var.set(datetime.now().strftime('%Y-%m-%d %H:%M'))
        entry_page_timestamp_entry = tk.Entry(self, textvariable=entry_page_timestamp_entry_var, font=body_font,
                                              state='readonly', bd=2)
        entry_page_timestamp_entry.grid(row=1, column=1, padx=5)
        entry_page_workstation_entry_var = tk.StringVar()
        entry_page_workstation_entry_var.set(workstations[0])
        entry_page_workstation_entry = tk.OptionMenu(self, entry_page_workstation_entry_var, *workstations)
        entry_page_workstation_entry.config(font=body_font, bd=2)
        entry_page_workstation_entry.grid(row=2, column=1, padx=5, sticky='E')
        entry_page_shift_entry_var = tk.StringVar()
        entry_page_shift_entry_var.set(shifts[0])
        entry_page_shift_entry = tk.OptionMenu(self, entry_page_shift_entry_var, *shifts)
        entry_page_shift_entry.config(font=body_font, bd=2)
        entry_page_shift_entry.grid(row=3, column=1, padx=5, sticky='E')
        entry_page_name_entry_var = tk.StringVar()
        entry_page_name_entry = tk.Entry(self, textvariable=entry_page_name_entry_var, font=body_font, bd=2)
        entry_page_name_entry.grid(row=4, column=1, padx=5)
        entry_page_title_entry_var = tk.StringVar()
        entry_page_title_entry = tk.Entry(self, textvariable=entry_page_title_entry_var, font=body_font, bd=2)
        entry_page_title_entry.grid(row=5, column=1, padx=5)
        entry_page_message_entry = tk.Text(self, height=11, width=20, font=body_font, bd=2)
        entry_page_message_entry.grid(row=6, column=1, columnspan=3, pady=10, padx=5, sticky='W')

        switch_screen_button = tk.Button(self, text='Review Past Entries', font=body_font, bd=2,
                                         command=lambda: controller.show_frame(retrieval_page))
        switch_screen_button.grid(row=0, column=0, pady=10)
        log_button = tk.Button(self, text='Log Hand Over', font=head_font, bd=2, command=lambda: log_hand_over())
        log_button.grid(row=6, column=3, padx=10, pady=10, sticky='S')

        def log_hand_over():
            time_stamp = entry_page_timestamp_entry_var.get()
            workstation = entry_page_workstation_entry_var.get()
            shift = entry_page_shift_entry_var.get()
            name = entry_page_name_entry_var.get()
            title = entry_page_title_entry_var.get()
            message = entry_page_message_entry.get("1.0", 'end-1c')
            if len(title) > 25:
                tk.messagebox.showerror(title='Long Title', message="Please, shorten the title.")
            elif len(message) > 280:
                tk.messagebox.showerror(title='Long Message', message="Please, shorten the message.")
            else:
                instance_tuple = (time_stamp, workstation, shift, name, title, message)
                if all(instance_tuple):
                    cursor.execute('USE [Operator_Hand_Off] INSERT INTO [dbo].Hand_Off VALUES' + str(instance_tuple))
                    con.commit()
                    entry_page_name_entry_var.set('')
                    entry_page_title_entry_var.set('')
                    entry_page_message_entry.delete(1.0, "end")
                else:
                    tk.messagebox.showerror(title='Missing Entries', message="Please, complete your entries.")


class retrieval_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bg = '#ffcccc'
        self['bg'] = bg

        switch_screen_button = tk.Button(self, text='Log an Entry', font=body_font,
                                         command=lambda: controller.show_frame(entry_page))
        switch_screen_button.grid(row=0, column=0, columnspan=2, padx=20, pady=10)
        retrieval_page_welcome = tk.Label(self, text='Historic Entries', font=title_font, bg=bg)
        retrieval_page_welcome.grid(row=0, column=2, columnspan=2, pady=10, padx=10)
        retrieval_page_workstation_entry_var = tk.StringVar()
        retrieval_page_workstation_entry_var.set(workstations[0])
        retrieval_page_workstation_entry = tk.OptionMenu(self, retrieval_page_workstation_entry_var, *workstations)
        retrieval_page_workstation_entry.config(font=body_font, bd=2)
        retrieval_page_workstation_entry.grid(row=1, column=2, columnspan=2, padx=5)
        query_button = tk.Button(self, text='Previous Hand Offs', font=body_font, bd=2,
                                 command=lambda: retrieve_history())
        query_button.grid(row=0, column=4, columnspan=2, padx=20, pady=10)

        def retrieve_history():
            workstation = retrieval_page_workstation_entry_var.get()
            today = datetime.now()
            tomorrow = today + timedelta(days=1)
            yesterday = today - timedelta(days=1)
            cursor.execute(
                "SELECT * FROM [Operator_Hand_Off].[dbo].[Hand_Off] WHERE [Time Stamp] BETWEEN '" + yesterday.strftime(
                    '%Y-%m-%d') + "' AND '" + tomorrow.strftime(
                    '%Y-%m-%d') + "' AND [Workstation] = '" + workstation + "'")
            column = 0
            for row in cursor:
                label = tk.Label(self, text="Shift: " + str(row[2]), font=("Times New Roman", 12), bg=bg)
                label.grid(row=2, column=column, columnspan=2, padx=5, sticky='NSEW')
                label = tk.Label(self, text=row[4], font=("Times New Roman", 12), bg=bg)
                label.grid(row=3, column=column, columnspan=2, padx=5, sticky='NSEW')
                label = tk.Text(self, height=15, width=10, font=("Times New Roman", 12), bd=0, bg=bg)
                label.insert(1.0, row[5])
                label.grid(row=4, column=column, columnspan=2, padx=5, sticky='NSEW')
                column += 2


app = hand_over()
app.mainloop()
