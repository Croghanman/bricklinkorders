from PyQt5.QtWidgets import QDialog, QApplication, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore
import pyodbc



class Window(QDialog):
    def __init__(self):
        super(Window,self).__init__()
        loadUi("main.ui",self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged() 
        self.saveButton.clicked.connect(self.saveChanges) 
        self.addButton.clicked.connect(self.addNewTask)
    
    def calendarDateChanged(self):
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print("Date Selected",dateSelected)
        self.updateTaskList(dateSelected)

    def updateTaskList(self,date):
        self.tasksListWidget.clear()
        
        conn = pyodbc.connect('Driver=ODBC Driver 17 for SQL Server;'
                      'Server=192.168.1.163,1433;'
                      'Database=UserForms;'
                      'UID=admin;'
                      'PWD=password;')
        cursor = conn.cursor()

        query = "SELECT DISTINCT task, completed FROM TaskList Where date = ?"
        row = (date,)
        results =cursor.execute(query,row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags()| QtCore.Qt.ItemIsUserCheckable)
            print (result[1])
            
            if 'Y' in result[1] :
                item.setCheckState(QtCore.Qt.Checked)
                print('Working')
            else:
                item.setCheckState(QtCore.Qt.Unchecked)      
            self.tasksListWidget.addItem(item)

    def saveChanges(self):
        conn = pyodbc.connect('Driver=ODBC Driver 17 for SQL Server;'
                      'Server=MacGyver;'
                      'Database=UserForms;'
                      'Trusted_Connection=yes;')
        cursor = conn.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()

        for i in range(self.tasksListWidget.count()):
            item = self.tasksListWidget.item(i)
            task = item.text()
            
            if item.checkState() == QtCore.Qt.Checked:
                query = "Update tasklist Set completed = 'Yes' WHERE task = ? AND date = ?"
            else:
                query = "Update tasklist Set completed = 'No' WHERE task = ? AND date = ?"
            row = (task,date,)
            cursor.execute(query,row)

        cursor.commit()
        messagebox = QMessageBox()
        messagebox.setText("Changes Saved.")
        messagebox.setStandardButtons(QMessageBox.Ok)
        messagebox.exec()

        
    def addNewTask(self):
        newTask = str(self.taskLineEdit.text())
        conn = pyodbc.connect('Driver=ODBC Driver 17 for SQL Server;'
                      'Server=MacGyver;'
                      'Database=UserForms;'
                      'Trusted_Connection=yes;')
        cursor = conn.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()
        query = "INSERT INTO TaskList(task,completed,date) VALUES(?,?,?)"
        row = (newTask,"NO",date,)
        cursor.execute(query,row)
        cursor.commit()
        self.updateTaskList(date)
        self.taskLineEdit.clear()

if __name__== "__main__":
    
    app= QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
