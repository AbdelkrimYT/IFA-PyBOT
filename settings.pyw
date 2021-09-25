from tkinter import Tk, LabelFrame, messagebox, StringVar, IntVar, BooleanVar
from tkinter.ttk import Label, Entry, Checkbutton, Combobox, Spinbox, Button, Radiobutton, Separator
from os.path import exists
import json


MODEL = {
    "email": "",
    "password": "",
    "regions": ["1"],
    "tcf-exams": ['TCF SO'],
    "motivation": "Etudes en France",
    "max-month": 2,
    "date": 0,
    "period": -1,
    "cpu": 2
}


class REGIONS:
    ALGER = '1'
    ORAN = '2'
    ANNABA = '3'
    CONSTANTINE = '4'
    TLEMCEN = '5'


class TCF_EXAMS:
    TCF_SO = 'TCF SO'
    TCF_CANADA = 'TCF Canada'
    TCF_DAP = 'TCF dans le cadre de la DAP'


class Window(Tk):
    
    def __init__(self):
        super().__init__()
        self.title('IFA Paramètres')
        self.resizable(False, False) 

        if not exists('settings.json'):
            with open('settings.json', 'w') as f:
                json.dump(MODEL, f)
        
        with open('settings.json', 'r') as f:
            self.config = json.load(f)
        
        self.email = StringVar()
        self.password = StringVar()
        self.email.set(self.config['email'])
        self.password.set(self.config['password'])
        self.emailLabel = Label(self, text='Email:')
        self.emailEntry = Entry(self, textvariable=self.email, width=50)
        self.passwordLabel = Label(self, text='Mot de passe:')
        self.passwordEntry = Entry(self, textvariable=self.password, width=50)
        self.emailLabel.pack(fill='both', expand='yes', padx=2)
        self.emailEntry.pack(fill='both', expand='yes', padx=2)
        self.passwordLabel.pack(fill='both', expand='yes', padx=2)
        self.passwordEntry.pack(fill='both', expand='yes', padx=2)
        
        self.regionsFrame = LabelFrame(text='Sélectionnez les régions')

        self.alger       = BooleanVar()
        self.oran        = BooleanVar()
        self.annaba      = BooleanVar()
        self.constantine = BooleanVar()
        self.tlemcen     = BooleanVar()

        self.alger.set(REGIONS.ALGER in self.config['regions'])
        self.oran.set(REGIONS.ORAN in self.config['regions'])
        self.annaba.set(REGIONS.ANNABA in self.config['regions'])
        self.constantine.set(REGIONS.CONSTANTINE in self.config['regions'])
        self.tlemcen.set(REGIONS.TLEMCEN in self.config['regions'])

        self.region_alger       = Checkbutton(self.regionsFrame, text='Alger', variable=self.alger)
        self.region_oran        = Checkbutton(self.regionsFrame, text='Oran', variable=self.oran)
        self.region_annaba      = Checkbutton(self.regionsFrame, text='Annaba', variable=self.annaba)
        self.region_constantine = Checkbutton(self.regionsFrame, text='Constantine', variable=self.constantine)
        self.region_tlemcen     = Checkbutton(self.regionsFrame, text='Tlemcen', variable=self.tlemcen)

        self.region_alger.pack(fill='both', expand='yes', padx=2)
        self.region_oran.pack(fill='both', expand='yes', padx=2)
        self.region_annaba.pack(fill='both', expand='yes', padx=2)
        self.region_constantine.pack(fill='both', expand='yes', padx=2)
        self.region_tlemcen.pack(fill='both', expand='yes', padx=2)
        self.regionsFrame.pack(fill='both', expand='yes', padx=2)
        
        self.tcfExamsFrame = LabelFrame(text='Sélectionnez TCF Exams')
        self.tcf_so        = BooleanVar()
        self.tcf_canada    = BooleanVar()
        self.tcf_dap       = BooleanVar()

        self.tcf_so.set(TCF_EXAMS.TCF_SO in self.config['tcf-exams'])
        self.tcf_canada.set(TCF_EXAMS.TCF_CANADA in self.config['tcf-exams'])
        self.tcf_dap.set(TCF_EXAMS.TCF_DAP in self.config['tcf-exams'])

        self.tcfSo     = Checkbutton(self.tcfExamsFrame, text='TCF SO', variable=self.tcf_so,)
        self.tcfCanada = Checkbutton(self.tcfExamsFrame, text='TCF Canada', variable=self.tcf_canada)
        self.tcfDap    = Checkbutton(self.tcfExamsFrame, text='TCF dans le cadre de la DAP', variable=self.tcf_dap,)
        
        self.tcfSo.pack(fill='both', expand='yes', padx=2)
        self.tcfCanada.pack(fill='both', expand='yes', padx=2)
        self.tcfDap.pack(fill='both', expand='yes', padx=2)
        self.tcfExamsFrame.pack(fill='both', expand='yes', padx=2)
        
        self.motivation = StringVar()
        Label(text="Le motivation:").pack(fill='both', expand='yes', padx=2)
        self.motivation.set(self.config['motivation'])

        self.motivationCombobox = Combobox(self, textvariable=self.motivation, state='readonly')
        self.motivationCombobox['values'] = ('Etudes en France', 'Immigration au Canada', 'Procédure de naturalisation', 'Autre')
        
        self.motivation.set(self.config['motivation'])
        self.motivationCombobox.pack(fill='both', expand='yes', padx=2)
        
        self.dateFrame = LabelFrame(text='Décidez comment choisir le jour de paiement')
        self.date = IntVar()
        self.date.set(self.config['date'])
        self.dateFirst = Radiobutton(self.dateFrame, text="Premier jour disponible", variable=self.date, value=0)
        self.dateLast = Radiobutton(self.dateFrame, text="Dernier jour disponible", variable=self.date, value=-1)
        self.dateRandom = Radiobutton(self.dateFrame, text="Choisissez le jour au hasard", variable=self.date, value=1)
        self.dateFirst.pack(fill='both', expand='yes', padx=2)
        self.dateLast.pack(fill='both', expand='yes', padx=2)
        self.dateRandom.pack(fill='both', expand='yes', padx=2)
        self.dateFrame.pack(fill='both', expand='yes', padx=2)

        self.periodFrame = LabelFrame(text='Décidez comment choisir la période de paiement')
        self.period = IntVar()
        self.period.set(self.config['period'])

        self.periodFirst  = Radiobutton(self.periodFrame, text="Première période disponible", variable=self.period, value=0)
        self.periodLast   = Radiobutton(self.periodFrame, text="Dernier période disponible", variable=self.period, value=-1)
        self.periodRandom = Radiobutton(self.periodFrame, text="Choisissez la période au hasard", variable=self.period, value=1)
        
        self.periodFirst.pack(fill='both', expand='yes', padx=2)
        self.periodLast.pack(fill='both', expand='yes', padx=2)
        self.periodRandom.pack(fill='both', expand='yes', padx=2)
        self.periodFrame.pack(fill='both', expand='yes', padx=2)

        self.maxMonth = IntVar()
        Label(text='Spécifiez la plage de recherche en mois: ').pack(fill='both', expand='yes', padx=2)
        self.maxMonth.set(self.config['max-month'])
        self.maxMonthSpinbox = Spinbox(self, textvariable=self.maxMonth, from_=1, to=12)
        self.maxMonthSpinbox.pack(fill='both', expand='yes', padx=2)
        
        self.cpu = IntVar()
        Label(text='Déterminer le nombre des processus (CPU): ').pack(fill='both', expand='yes', padx=2)
        self.cpu.set(self.config['cpu'])
        self.cpuSpinbox = Spinbox(self, textvariable=self.cpu, from_=1, to=64)
        self.cpuSpinbox.pack(fill='both', expand='yes', padx=2)
        
        self.saveButton = Button(text='Sauvegarder', command=self.save)
        self.saveButton.pack(fill='both', expand='yes', padx=4, pady=4)
        self.eval('tk::PlaceWindow  . center')
    
    def save(self):
        self.config['email'] = self.email.get()
        # REGIONS
        for v, s in [
            (REGIONS.ALGER, self.alger.get()),
            (REGIONS.ORAN, self.oran.get()),
            (REGIONS.ANNABA, self.annaba.get()),
            (REGIONS.CONSTANTINE, self.constantine.get()),
            (REGIONS.TLEMCEN, self.tlemcen.get())]:
            if s:
                if v not in self.config['regions']:
                    self.config['regions'].append(v)
            else:
                if v in self.config['regions']:
                    self.config['regions'].remove(v)
        # TCF_EXAMS
        for v, s in [
            (TCF_EXAMS.TCF_SO, self.tcf_so.get()),
            (TCF_EXAMS.TCF_CANADA, self.tcf_canada.get()),
            (TCF_EXAMS.TCF_DAP, self.tcf_dap.get())]:
            if s:
                if v not in self.config['tcf-exams']:
                    self.config['tcf-exams'].append(v)
            else:
                if v in self.config['tcf-exams']:
                    self.config['tcf-exams'].remove(v)
        
        self.config['password']   = self.password.get()
        self.config['date']       = self.date.get()
        self.config['period']     = self.period.get()
        self.config['motivation'] = self.motivation.get()
        self.config['max-month']  = self.maxMonth.get()
        self.config['cpu']        = self.cpu.get()

        with open('settings.json', 'w') as f:
            json.dump(self.config, f)
        
        messagebox.showinfo(parent=self, title='', message='Sauvegardé avec succès')


if __name__ == '__main__':
    w = Window()
    w.mainloop()
