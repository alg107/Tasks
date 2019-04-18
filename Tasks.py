import gspread
from oauth2client.service_account import ServiceAccountCredentials
import hashlib

# Deal with problem of identical hashes
# Maybe check if a hash exists before adding something
# Or come up with a new hash system

class Task:
    def __init__(self, title, description, due):
        self.title = title
        self.description = description
        self.due = due
    def to_list(self):
        return [self.title, self.description, self.due] 
    
    def gen_hash(self):
        return hashlib.md5(self.title+self.description+self.due).hexdigest()

class Worksheet:
    def __init__(self, key):
        self.key = key

    def initialise(self, cred):

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(cred, scope)

        gc = gspread.authorize(credentials)

        self.wks = gc.open_by_key(self.key).sheet1

    def new_task(self, task):
        hsh = task.gen_hash()
        self.wks.insert_row([task.title, task.description, task.due, hsh],2)
        return hsh

    def delete_task(self, hsh):
        try:
            row = self.wks.findall(hsh)[0].row
            self.wks.delete_row(row)
            return 0
        except IndexError:
            return 1
    
    def get_task(self, hsh):
        try:
            row = self.wks.findall(hsh)[0].row
            vals = self.wks.row_values(row)
            tsk = Task(vals[0], vals[1], vals[2])
            tsk.hsh = vals[3] 
            return tsk
        except IndexError:
            return 1

    def update_task(self, tskt, hsh):
        try:
            row = self.wks.findall(hsh)[0].row
            tsk = Task(tskt.title,tskt.description, tskt.due)
            rng = "A{0}:D{0}".format(row)
            cell_list = self.wks.range(rng)
            cell_list[0].value = tsk.title
            cell_list[1].value = tsk.description
            cell_list[2].value = tsk.due
            new_hsh = tskt.gen_hash()
            cell_list[3].value = new_hsh
            self.wks.update_cells(cell_list)
            return new_hsh
            
        except IndexError:
            return 1
        
    def get_all_tasks(self):
        allvals = self.wks.get_all_values()
        tsks = []
        for row in allvals[1:]:
            tskt = Task(row[0], row[1], row[2])
            tskt.hsh = row[3]
            tsks.append(tskt)
        return tsks


if __name__ == '__main__':
    key = "1h8J9DHD8ZPgKU6g5uUZcOcVnkwtUUTBRDBrPkDFiv14"
    credsfile = 'Goodenbour-4447ab141b22.json'

    data = Worksheet(key)
    data.initialise(credsfile)

    for i in  data.get_all_tasks():
        print i.title
        print i.description
        print i.due
        print "%%%%%%%%%"
