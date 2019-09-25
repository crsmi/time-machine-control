import commands
import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter import ttk as ttk

# FUTURE import time as systime


class Application(ttk.Frame):
    """Time Machine Control application."""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # master.report_callback_exception = self.report_callback_exception
        master.title("Time Machine Control")
        master.resizable(0, 0)

        self.tm = commands.TimeMachine()

        self.controls = tk.Frame(self)
        self.controls.pack(side='left')

        """ FUTURE
        self.listen_window = tk.Frame(self)
        self.listen_window.pack(side = 'right')
        """

        self.pack()
        self.add_connection()
        ttk.Separator(self.controls, orient=tk.HORIZONTAL).pack(
            side="top", fill='x', expand=True, padx=2)
        # FUTURE self.create_menu()
        self.add_timeclock()
        ttk.Separator(self.controls, orient=tk.HORIZONTAL).pack(
            side="top", fill='x', expand=True, padx=2)
        self.add_retransmit()
        ttk.Separator(self.controls, orient=tk.HORIZONTAL).pack(
            side="top", fill='x', expand=True, padx=2)
        self.add_set_event()
        ttk.Separator(self.controls, orient=tk.HORIZONTAL).pack(
            side="top", fill='x', expand=True, padx=2)
        self.add_xonxoff()

        # FUTURE self.add_listening_window()

        # Display output from Time TimeMachine
        # while True:
        #     self.output['text'] += self.tm.collect_data()
        #     systime.sleep(1)

    # def report_callback_exception(self, *args):
    #     print(args[1], type(args[1]))
    #     err = traceback.format_exception(*args)
    #     tk.messagebox.showerror('Exception', err)

    def create_menu(self):
        menu = tk.Menu(self.controls)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label='Mode')
        file_menu.add_command(label='Exit', command=self.master.quit)
        menu.add_cascade(label='File', menu=file_menu)
        self.master.config(menu=menu)

    # ADD COM PORT SELECTOR
    def add_connection(self):
        connection = ttk.Frame(self.controls)
        connection.pack(side="top", pady=(0, 5))
        header = ttk.Label(connection, text="Connection")
        header.pack(side="top")

        row1 = ttk.Frame(connection)
        row1.pack(side='top', expand=1, fill='x', padx=5)

        def callback(event=None):
            self.tm.com_port = comport_selection.get()

        comport_list = commands.list_comports()

        comport_label = ttk.Label(row1, text='COM Port:')
        comport_label.pack(side="left")
        comport_selection = ttk.Combobox(row1, values=comport_list, width=11)
        comport_selection.bind("<<ComboboxSelected>>", callback)
        comport_selection.pack(side="right")
        comport_selection.current(0)
        callback()

        """ Future Implementation
        row2 = ttk.Frame(connection)
        row2.pack(side='top',expand=1,fill='x',padx=5)


        def connect():
            print('Connect')
            #self.tm.connect(comport.get())
            self.listen_window.pack()
            self.output = tk.Toplevel(height=10)

        def disconnect():
            print('Disconnect')
            #self.tm.disconnect()
            self.listen_window.pack_forget()
            self.output.withdraw()

        connect_button = ttk.Button(row2, text='Connect')
        connect_button.pack(side='left')
        connect_button['command'] = connect
        disconnect_button = ttk.Button(row2, text='Disconnect')
        disconnect_button.pack(side='left')
        disconnect_button['command'] = disconnect
        """

    # ADD TIMECLOCK
    def add_timeclock(self):
        # TODO: Have hitting send without anything in the TimeEntry fill in the TimeEntry with zeros.
        timeclock = ttk.Frame(self.controls)
        timeclock.pack(side="top", pady=(0, 5))
        header = ttk.Label(timeclock, text="Time Clock")
        header.pack(side="top")

        # Clock action choice
        row1 = ttk.Frame(timeclock)
        row1.pack(side='top', expand=1, fill='x', padx=5)

        clock_action = tk.StringVar()
        clock_action.set('stop_set')
        stop_set = ttk.Radiobutton(row1, text='Stop/Set', value="stop_set", variable=clock_action)
        stop_set.grid(row=0, column=0)
        set_up = ttk.Radiobutton(row1, text='Set ^', value="up", variable=clock_action)
        set_up.grid(row=0, column=1)
        set_down = ttk.Radiobutton(row1, text='Set v', value="down", variable=clock_action)
        set_down.grid(row=0, column=2)

        # CLock time and button
        row2 = ttk.Frame(timeclock)
        row2.pack(side='top', expand=1, fill='x', padx=5)

        time = TimeEntry(row2, text="Time: ")
        time.pack(side='left')
        set_button = ttk.Button(row2, width=7, text='Set')
        set_button.pack(side='right')
        set_button['command'] = lambda: self.tm.clock_set(
            time.get(), clock_action.get())

    # ADD RETRANSMIT
    def add_retransmit(self):
        retransmit = ttk.Frame(self.controls)
        retransmit.pack(side='top', pady=(0, 5))
        header = ttk.Label(retransmit, text='Retransmit')
        header.pack(side="top")

        row1 = ttk.Frame(retransmit)
        row1.pack(side='top')
        event_label = ttk.Label(row1, text='Event')
        event_label.grid(row=0, column=0)
        event_num = ttk.Spinbox(row1, from_=0, to=255, width=5)
        event_num.set(1)
        event_num.grid(row=0, column=1)
        heat_label = ttk.Label(row1, text='Heat')
        heat_label.grid(row=0, column=2)
        heat_num = ttk.Spinbox(row1, from_=0, to=255, width=5)
        heat_num.set(0)
        heat_num.grid(row=0, column=3)

        retransmit_button = ttk.Button(row1, text='Retransmit')
        retransmit_button.grid(row=1, column=0, columnspan=2)
        # TODO include selection of start time for retransmission.
        retransmit_button['command'] = lambda: self.tm.start_retransmit()

        # HALT RETRANSMIT
        halt_retransmit_button = ttk.Button(row1, text='Halt Retransmit')
        halt_retransmit_button.grid(row=1, column=2, columnspan=2)
        halt_retransmit_button['command'] = lambda: self.tm.halt_retransmit()

    # SET EVENT
    def add_set_event(self):
        set_event = ttk.Frame(self.controls)
        set_event.pack(side='top', pady=(0, 5))
        header = ttk.Label(set_event, text="Set Event Heat")
        header.pack(side='top')

        row = ttk.Frame(set_event)
        row.pack(side='top', expand=1, fill='x', padx=5)
        event_num = ttk.Spinbox(row, from_=1, to=255, width=5)
        event_num.set(1)
        event_num.pack(side="left")
        set_button = ttk.Button(row, width=7, text='Set')
        set_button.pack(side='right')
        set_button['command'] = lambda: self.tm.set_event_heat(event_num.get())

    # XON/XOFF
    def add_xonxoff(self):
        xonxoff = ttk.Frame(self.controls)
        xonxoff.pack(side='top', pady=(0, 5))
        header = ttk.Label(xonxoff, text="Time Machine Feed")
        header.pack(side='top')
        row = ttk.Frame(xonxoff)
        row.pack(side='top')
        xon_button = ttk.Button(row, text='XON')
        xon_button.pack(side='left', ipadx=3, padx=2)
        xon_button['command'] = lambda: self.tm.xon()
        xoff_button = ttk.Button(row, text='XOFF')
        xoff_button.pack(side='left', ipadx=2, padx=2)
        xoff_button['command'] = lambda: self.tm.xoff()

    # Listening Window
    ''' Future Implementation
    def add_listening_window(self):
        #self.output = ttk.Label(self)
        output = ttk.Label(self.listen_window, text = 'Output Window')
        output.pack(side='top')
    '''


class TimeEntry(ttk.Frame):
    """Define a Time Entry Widget.

    TODO: init variable for starting values."""

    def __init__(self, master, text="", frame_look={}):
        args = dict(relief=tk.FLAT, border=1)
        args.update(frame_look)
        ttk.Frame.__init__(self, master, **args)

        ttk.Style().configure("t.TLabel", relief=tk.FLAT)
        ttk.Style().configure("t.TEntry", relief=tk.FLAT)

        args = {'relief': tk.FLAT}
        # args.update(look)

        vcmd = (self.register(self.onValidate), '%S')

        self.text_label = ttk.Label(self, text=text, style="t.TLabel")
        self.entry_1 = ttk.Entry(self, width=2, style="t.TEntry",
                                 validate='key', validatecommand=vcmd)
        self.label_1 = ttk.Label(self, text=':', style="t.TLabel")
        self.entry_2 = ttk.Entry(self, width=2, style="t.TEntry",
                                 validate='key', validatecommand=vcmd)
        self.label_2 = ttk.Label(self, text=':', style="t.TLabel")
        self.entry_3 = ttk.Entry(self, width=2, style="t.TEntry",
                                 validate='key', validatecommand=vcmd)

        self.text_label.pack(side=tk.LEFT)
        self.entry_1.pack(side=tk.LEFT)
        self.label_1.pack(side=tk.LEFT)
        self.entry_2.pack(side=tk.LEFT)
        self.label_2.pack(side=tk.LEFT)
        self.entry_3.pack(side=tk.LEFT)

        self.entries = [self.entry_1, self.entry_2, self.entry_3]

        self.entry_1.bind('<Key>', self._check)
        self.entry_2.bind('<Key>', self._check)
        self.entry_3.bind('<Key>', self._check)

        self.entry_1.bind('<FocusOut>', self.zerofill)
        self.entry_2.bind('<FocusOut>', self.zerofill)
        self.entry_3.bind('<FocusOut>', self.zerofill)

    def zerofill(self, event):
        entry = event.widget
        while len(entry.get()) < entry['width']:
            entry.insert(0, '0')

    def onValidate(self, S):
        # Disallow anything but numbers
        if S.isdigit():
            return True
        else:
            self.bell()
            return False

    def _check(self, event):
        entry = event.widget
        index = self.entries.index(entry)
        size = entry['width']
        next_index = index + 1
        next_entry = self.entries[next_index] if next_index < len(
            self.entries) else None

        # Overtype
        if event.char.isdigit():
            entry.delete(entry.index(tk.INSERT))
        # Jump to next entry
        if entry.index(tk.INSERT) == size - 1:
            if next_entry:
                next_entry.focus()
                next_entry.icursor(0)
                next_entry.selection_clear()
            else:
                entry.tk_focusNext().focus()

    def get(self):
        return [e.get() for e in self.entries]


class Catcher:
    def __init__(self, func, subst, widget):
        self.func = func
        self.subst = subst
        self.widget = widget

    def __call__(self, *args):
        try:
            if self.subst:
                args = self.subst(*args)
            return self.func(*args)
        except SystemExit as msg:
            raise SystemExit(msg)
        except commands.TimeMachineError as e:
            tk.messagebox.showerror('Time Machine Error', e.message)
        except:
            traceback.print_exc()


if __name__ == "__main__":
    root = tk.Tk()
    tk.CallWrapper = Catcher
    app = Application(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
