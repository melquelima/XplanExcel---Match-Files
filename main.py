import os
import pandas as pd
from sql import create_connection
from PyQt5 import QtCore, QtGui, QtWidgets
from tela import Ui_tela
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QFileDialog, QCheckBox
from iniLib import *
from datetime import datetime as dt
import openpyxl

class processar_dados(QDialog):
    def __init__(self, *args, **argvs):
        super(processar_dados, self).__init__(*args, **argvs)
        self.ui = Ui_tela()
        self.ui.setupUi(self)
        self.ui.Selecionar_arquivo1.clicked.connect(self.seleciona_arquivos1)
        self.ui.Selecionar_arquivo2.clicked.connect(self.seleciona_arquivos2)
        self.ui.selecionar_output_path.clicked.connect(self.output_path)
        self.ui.upload_1.clicked.connect(self.processar1)
        self.ui.upload_2.clicked.connect(self.processar2)
        self.ui.pushButton.clicked.connect(self.clear_db)
        self.ui.go_button.clicked.connect(self.output)
        self.conn = create_connection(os.getcwd() + '\\dados_db.db')
        self.pasta1,self.pasta2 = None,None
        self.ini = IniFile(os.getcwd() + "\\config.ini")
        self.check_previously_addresses()
        self.logFile = lambda:dt.now().strftime("%d%m%y_%H%M%S") + ".txt"
        print(self.logFile())
    
    def clear_db(self):
            try:
                c = self.conn.cursor()
                c.execute(f"drop table if exists A1")
                c.execute(f"drop table if exists A2")
                self.ui.campo_de_status.setText("DROP Sucess")
            except:
                open(self.logFile(),'w').write(str(sys.exc_info()[1]))
                QMessageBox.warning(QMessageBox(),"Error", "Program Error")

    def check_previously_addresses(self):
        try:
            value   = self.ini.read("CONFIG","pasta1")
            value2  = self.ini.read("CONFIG","pasta2")
            value3  = self.ini.read("CONFIG","pastaoutput")
            if value[0]:
                self.pasta1 = value[1]
                self.ui.arquivo1_entrada.setText(self.pasta1)

            if value2[0]:
                self.pasta2 = value2[1]
                self.ui.arquivo2_entrada.setText(self.pasta2)

            if value3[0]:
                self.pastaoutput = value3[1]
                self.ui.output_path.setText(self.pastaoutput)
        except:
            open(self.logFile(),'w').write(str(sys.exc_info()[1]))
            QMessageBox.warning(QMessageBox(),"Error", "Program Error")

    # Função do botão de selecionar pasta1
    def seleciona_arquivos1(self):
        try:
            self.pasta1 = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', 'C:\\', QtWidgets.QFileDialog.ShowDirsOnly)
            self.ui.arquivo1_entrada.setText(self.pasta1)
            self.ui.campo_de_status.setText(f'Folder 1 path: {self.pasta1}')
            self.ini.write("CONFIG","pasta1",self.pasta1)
        except:
            open(self.logFile(),'w').write(str(sys.exc_info()[1]))
            QMessageBox.warning(QMessageBox(),"Error", "Program Error")
        
 # Função do botão de selecionar pasta2
 
    def seleciona_arquivos2(self):
        try:
            self.pasta2 = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', 'C:\\', QtWidgets.QFileDialog.ShowDirsOnly)
            self.ui.arquivo2_entrada.setText(self.pasta2)
            self.ui.campo_de_status.setText(f'Folder 2 path: {self.pasta2}')
            self.ini.write("CONFIG","pasta2",self.pasta2)
        except:
            open(self.logFile(),'w').write(str(sys.exc_info()[1]))
            QMessageBox.warning(QMessageBox(),"Error", "Program Error")

     # Função do botão upload1
    def subir_arquivo1(self,tabela):
        try:
            for diretorio, subpastas, arquivos in os.walk(self.pasta1):
                for arquivo in arquivos:
                    df = pd.read_excel(os.path.join(diretorio, arquivo))
                    df.to_sql(tabela, con=self.conn, if_exists='append', index= False,dtype={col_name: "TEXT" for col_name in df})
            self.ui.campo_de_status.setText(f'{self.pasta1} ok')
            QMessageBox.warning(QMessageBox(),"Sucess", "Folder 1 data uploaded successfully")
        except:
            open(self.logFile(),'w').write(str(sys.exc_info()[1]))
            QMessageBox.warning(QMessageBox(),"Error", "Program Error")
            
    # Função do botão upload2
    def subir_arquivo2(self,tabela):
        try:

            for diretorio, subpastas, arquivos in os.walk(self.pasta2):
                for arquivo in arquivos:
                    df = pd.read_excel(os.path.join(diretorio, arquivo))
                    df.to_sql(tabela, con=self.conn, if_exists='append', index= False,dtype={col_name: "TEXT" for col_name in df})
            self.ui.campo_de_status.setText(f'{self.pasta2} ok')
            QMessageBox.warning(QMessageBox(),"Sucess", "Folder 2 data uploaded successfully")
        
        except:
            open(self.logFile(),'w').write(str(sys.exc_info()[1]))
            QMessageBox.warning(QMessageBox(),"Error", "Program Error")
    
    def output(self):

        # processando a Query
        try:
            self.ui.campo_de_status.setText(f"Processing...!")
            self.query = 'select * from A1 Inner join A2 on A1.CPF = A2.CPF'
            self.conn.cursor()
            self.df = pd.read_sql_query(self.query, self.conn)
            self.df.to_excel(f'{self.pastaoutput}/output.xlsx', index= False)
            self.ui.campo_de_status.setText(f'Output data uploaded successfully.')
        except:
            open(self.logFile(),'w').write(str(sys.exc_info()[1]))
            QMessageBox.warning(QMessageBox(),"Error", "Program Error")
            

    def output_path(self):
        try:
            # Selecionando a pasta de saída
            self.pastaoutput = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', 'C:\\', QtWidgets.QFileDialog.ShowDirsOnly)
            self.ui.output_path.setText(self.pastaoutput)
            self.ui.campo_de_status.setText(f'Selected output folder: {self.pastaoutput}')
            self.ini.write("CONFIG","pastaoutput",self.pastaoutput)
            self.output_path = self.pastaoutput
        except:
            open(self.logFile(),'w').write(str(sys.exc_info()[1]))
            QMessageBox.warning(QMessageBox(),"Error", "Program Error")
        

    def processar1(self):
        self.subir_arquivo1("A1")
    
    def processar2(self):
        self.subir_arquivo2("A2")


app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    window = processar_dados()
    window.show()
sys.exit(app.exec_())
