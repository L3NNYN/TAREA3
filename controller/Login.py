import sys
import shutil
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QTableWidgetItem
from PyQt5.uic import loadUi
import json
import os
import os.path
import errno

usu='' 
estado = True
class Login(QDialog):

    def __init__(self):
        super(Login,self).__init__()
        loadUi("view/principal.ui",self)
        self.btningresar.clicked.connect(self.btningresarfunction) 
        self.txtcontrasenia.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btnregistrarse.clicked.connect(self.ventanaregistrarse)
       
    def btningresarfunction(self):
        global usu
        usuario = self.txtusuario.text()
        contrasenia = self.txtcontrasenia.text()
        if self.auth(usuario, contrasenia):
            priview = Principal()
            widget.addWidget(priview)
            widget.setCurrentIndex(widget.currentIndex()+1)
            usu=usuario
            print("Sesion iniciada con exito con el usuario: ",usuario, "y contraseña: ",contrasenia)
        else:
            self.lblAuth.setText('Credenciales no encontradas')

    #se abre el archivo y se recorre los usuarios
    def auth(self, user, password):
        with open('usuarios.txt') as json_file:
            data = json.load(json_file)
            for item in data['usuarios']: 
                if item['usuario'] == user and item['password'] == password:
                    print('Encontrado')
                    return True
            print('No encontrado')
            return False #no lo encuentra

    def ventanaregistrarse(self):
        cuenta = funcion()
        widget.addWidget(cuenta)
        widget.setCurrentIndex(widget.currentIndex()+1)

class funcion(QDialog):
    def __init__(self):
        super(funcion,self).__init__()
        loadUi("view/registrarse.ui",self)
        self.btnagregar.clicked.connect(self.crearfuncion)

    def addjson(self, user, password):
        #se crea el objeto del usuario
        usuario = {'usuario':user, 'password':password}
        
        aux = {}
        aux['usuarios'] = []
        
        #se abre el archivo y se obtiene el array de usuarios
        with open('usuarios.txt') as json_file:
            data = json.load(json_file)
            aux['usuarios'] = data['usuarios']

        #se agrega el nuevo usuario y se guarda en el archivo
        aux['usuarios'].append(usuario)
        with open('usuarios.txt', 'w') as outfile:
            json.dump(aux, outfile)

    def crearfuncion(self):
        if self.txtpass.text() != '' and self.txtnombre.text() != '':
            usuario = self.txtnombre.text()
            password = self.txtpass.text() #password
            self.addjson(usuario, password)
            print("Se creo la cuenta con el usuario: ",usuario, "y contraseña: ",password)
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
            try:
                os.mkdir('CarpetasRepositorio/'+ usuario)
                os.mkdir('CarpetasRepositorio/'+ usuario+'/perm')
                os.mkdir('CarpetasRepositorio/'+ usuario+'/temp')
                os.mkdir('CarpetasRepositorio/'+usuario+'/version')
                self.versionNuevo(usuario, 0)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

    def versionNuevo(self,usuario, p):
        try:
            if p == 1:
                cont = 0
                data = {}
                with open('CarpetasRepositorio/'+usuario+'/version/v.txt') as version_file:
                    data = json.load(version_file)
                    cont = data['conteo']
                
                os.mkdir('CarpetasRepositorio/'+usuario+'/version/'+str(cont))

                with open('CarpetasRepositorio/'+usuario+'/version/v.txt','w') as version_file:
                    json.dump({'conteo': cont+1}, version_file)
                
                return cont
            else:    
                with open('CarpetasRepositorio/'+usuario+'/version/v.txt', 'w') as version_file:
                    json.dump({'conteo':1}, version_file)
        except Exception as e:
            print(e)

    def agregarVersion(self, usu, cont):
        try:
                target = 'CarpetasRepositorio/'+usu+'/version/'+str(cont)
                user_perm = 'CarpetasRepositorio/'+usu+'/perm/'
                perm_count = os.listdir(user_perm)
                aux=''
                for aux in perm_count:
                    source = user_perm = 'CarpetasRepositorio/'+usu+'/perm/'+aux
                    shutil.copy(source, target)
        except Exception as e:
            print(e)

row=0
class Principal(QDialog):
    def __init__(self):
        super(Principal,self).__init__()
        loadUi("view/git.ui",self)
        self.btnarchivo.clicked.connect(self.archivos)
        self.btnlog.clicked.connect(self.volver)
        self.btnversion.clicked.connect(self.ventanaexplorar)
        self.tbarchivo.setColumnWidth(0,571)
        self.btnborrar.clicked.connect(self.borrar)
        self.btnpush.clicked.connect(self.push)
        self.btnpull.clicked.connect(self.pull)


    def principalview(self):
        log = Login()
        widget.addWidget(log)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def archivos(self):
      global row, usu
      filename = QFileDialog.getOpenFileName()
      nom = filename[0]
      self.tbarchivo.setRowCount(row+1)
      self.tbarchivo.setItem(row, 0, QtWidgets.QTableWidgetItem(os.path.basename(nom)))
      
      row=row+1
      target='CarpetasRepositorio/'+usu+'/temp/'+os.path.basename(nom)
      shutil.copyfile(nom, target)
    
    def volver(self):
      login = Login()
      widget.addWidget(login)
      widget.setCurrentIndex(widget.currentIndex()+1)
    
    def ventanaexplorar(self):
       ex = Explorador()
       widget.addWidget(ex)
       widget.setCurrentIndex(widget.currentIndex()+1)

    def borrar(self):
        global row
        self.tbarchivo.removeRow(self.tbarchivo.currentRow())
        row=row-1
        self.tbarchivo.setRowCount(row)

    def push(self):
        global row, usu
        x=0
        for x in range(row):
            print(self.tbarchivo.item(x, 0).data(0))
            target='CarpetasRepositorio/'+usu+'/perm/'+str(self.tbarchivo.item(x, 0).data(0))
            source='CarpetasRepositorio/'+usu+'/temp/'+str(self.tbarchivo.item(x, 0).data(0))
            shutil.copyfile(source, target)
            os.remove(source)
        row = 0
        self.tbarchivo.clearContents()
        self.tbarchivo.setRowCount(0)
        #primero se crea la carpeta con el numero de vesion correspondiente
        cont = funcion.versionNuevo(self, usu, 1)
        #luego se agregan los archivos en perm a la carpeta creada
        funcion.agregarVersion(self, usu, cont)

    def pull(self):
        global row, usu

        
        user_temp = 'CarpetasRepositorio/'+usu+'/temp/'
        temp_count = os.listdir(user_temp)
        
        aux=''
        for aux in temp_count:
            source = user_perm = 'CarpetasRepositorio/'+usu+'/temp/'+aux
            os.remove(source)
        row = 0
        self.tbarchivo.clearContents()
        self.tbarchivo.setRowCount(0)

        user_perm = 'CarpetasRepositorio/'+usu+'/perm/'
        perm_count = os.listdir(user_perm)

        aux2=''
        self.tbarchivo.setRowCount(len(perm_count))
        for aux2 in perm_count:
            source = 'CarpetasRepositorio/'+usu+'/perm/'+aux2
            self.tbarchivo.setItem(row, 0, QtWidgets.QTableWidgetItem(aux2))

            row=row+1
            target='CarpetasRepositorio/'+usu+'/temp/'+aux2
            shutil.copyfile(source, target)

class Explorador(QDialog):
    def __init__(self):
        super(Explorador,self).__init__()
        loadUi("view/explorador.ui",self)
        self.tbexplorar.setColumnWidth(0,271)
        self.tbexplorar2.setColumnWidth(0,271)
        self.btnselect.clicked.connect(self.load)
        self.btncancelar.clicked.connect(self.cancelar)
        self.btnrecuperar.clicked.connect(self.recuperar)
        self.version()
        
        global estado

        estado = True

    def load(self):
        global row, usu, estado
        col = self.tbexplorar.currentRow()+1

        self.tbexplorar2.clearContents()
        self.tbexplorar2.setRowCount(0)

        dirname = 'CarpetasRepositorio/'+usu+'/version/'+str(col)+'/'
        dirfile = os.listdir(dirname)
        print(dirfile)

        aux2=''
        self.tbexplorar2.setRowCount(len(dirfile))
        for aux2 in dirfile:
            self.tbexplorar2.setItem(row, 0, QtWidgets.QTableWidgetItem(aux2)) 
            row=row+1
            print(aux2)

        estado = False

    def version(self):
        global row, usu
        dirname = 'CarpetasRepositorio/'+usu+'/version/'
        dirfile = os.listdir(dirname)

        aux2=''
        self.tbexplorar.setRowCount(len(dirfile)-1)
        for aux2 in dirfile:
           if aux2 != 'v.txt':
               self.tbexplorar.setItem(row, 0, QtWidgets.QTableWidgetItem(aux2)) 
               row=row+1
   
    def cancelar(self):
        git = Principal()
        widget.addWidget(git)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def recuperar(self):
        global row, usu, estado

        if estado == True:

            user_temp = 'CarpetasRepositorio/'+usu+'/perm/'
            temp_count = os.listdir(user_temp)

            aux=''
            for aux in temp_count:
                source = user_perm = 'CarpetasRepositorio/'+usu+'/perm/'+aux
                os.remove(source)
            row = 0

            user_perm = 'CarpetasRepositorio/'+usu+'/version/'+str(self.tbexplorar.currentRow()+1)+'/'
            perm_count = os.listdir(user_perm)

            aux2=''
            for aux2 in perm_count:
                source = user_perm + aux2

                row=row+1
                target='CarpetasRepositorio/'+usu+'/perm/'+aux2
                shutil.copyfile(source, target)
        else:
            print()


app = QApplication(sys.argv)
mainwindows = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindows)
widget.setWindowTitle("Control de Versiones")
widget.setWindowIcon(QIcon("resources/icono.png"))
widget.setFixedWidth(601)
widget.setFixedHeight(618)
widget.show()
app.exec_()      