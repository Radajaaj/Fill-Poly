import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.uic import *
import math

ListaPoligonos = []     # Lista que armazena cada polígono, definido por meio de seus vértices

# OK, falta:
#   XXCriar o vetor global de pontos de poligonos
#   XX    Vai ser uma lista de vértices. O último se conecta com o primeiro.


def novoVertice(ponto): # Coloca um novo vértice no último polígono da lista de polígonos, e retorna o número de vértices do polígono atual.
    ListaPoligonos[-1].vertices.append(ponto)    # Ponto vai provavelmente ser do tipo "ponto" do PyQT6
    return len(ListaPoligonos[-1].vertices)          # Aparentemente Point() é uma classe. Vamo ve no que dá
    
    #
#   XXFunção de unir o vetor ao drop-down
#   XXFunção de deletar do drop-down
#   Por fim começar a mexer no desenho de linhas e pixels.
#   



class TelaDesenho(QWidget): #QPixmap
    def __init__(self, parent):
        super().__init__()
        self.parent = parent    #Gambiarra sei la se vai funcionar
        
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('white'))
        self.setPalette(palette)






        #
    
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.parent.novoPoligono()
            print(len(ListaPoligonos))
            
            
        if e.button() == Qt.MouseButton.RightButton:
            if len(ListaPoligonos) > 0:
                self.parent.deletarPoligono(len(ListaPoligonos) - 1)
            print(len(ListaPoligonos))
            


class ComboBoxPoligonos(QComboBox):
    def __init__(self):
        super().__init__()
        self.atualizarComboBox
        
        #
        
    def atualizarComboBox(self):
        self.clear()
        i = 0
        for poligono in ListaPoligonos:
            self.addItem(f"Polígono {i + 1}")
            i += 1
    
    #def 






class Titulo1(QLabel):
    def __init__(self, texto):
        super().__init__()
        self.setText(texto)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setFont(QFont("Roboto", 20))
        
        #


class Titulo2(QLabel):
    def __init__(self, texto):
        super().__init__()
        self.setText(texto)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setFont(QFont("Roboto", 8))
        
        #


class Poligono:
    def __init__(self, vertices, cor_arestas = QColor('red'), cor_poligono = QColor('black')):
        self.vertices     = vertices
        self.cor_arestas  = cor_arestas
        self.cor_poligono = cor_poligono



