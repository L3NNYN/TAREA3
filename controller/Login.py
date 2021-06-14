import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import json

class Login(QDialog):

    def __init__(self):
        super(Login,self).__init__()
        loadUi("view/principal.ui",self)
        self.btningresar.clicked.connect(self.btningresarfunction) 
        self.txtcontrasenia.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btnregistrarse.clicked.connect(self.ventanaregistrarse)
       
       

    def btningresarfunction(self):
        priview = Principal()
        widget.addWidget(priview)
        widget.setCurrentIndex(widget.currentIndex()+1)
        usuario = self.txtusuario.text()
        contrasenia = self.txtcontrasenia.text()
        print("Sesion iniciada con exito con el usuario: ",usuario, "y contraseña: ",contrasenia)


    def ventanaregistrarse(self):
        cuenta = funcion()
        widget.addWidget(cuenta)
        widget.setCurrentIndex(widget.currentIndex()+1)

class funcion(QDialog):
    def __init__(self):
        super(funcion,self).__init__()
        loadUi("view/registrarse.ui",self)
        self.btnagregar.clicked.connect(self.crearfuncion)
        self.cbcuenta.addItems(["Administrador", "Usuario"])
        self.cbcuenta.setCurrentIndex(-1)

    def crearfuncion(self):
         nombre = self.txtnombre.text()
         if self.txtpass.text() == self.txtpasscon.text():
             contra = self.txtpass.text()
             print("Se creo la cuenta con el usuario: ",nombre, "y contraseña: ",contra)
             login = Login()
             widget.addWidget(login)
             widget.setCurrentIndex(widget.currentIndex()+1)

class Principal(QDialog):
    def __init__(self):
        super(Principal,self).__init__()
        loadUi("view/git.ui",self)
    
    def principalview(self):
        log = Login()
        widget.addWidget(log)
        widget.setCurrentIndex(widget.currentIndex()+1)


app = QApplication(sys.argv)
mainwindows = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindows)
widget.setFixedWidth(601)
widget.setFixedHeight(618)
widget.show()
app.exec_()      