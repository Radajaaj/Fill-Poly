import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.uic import *
from math import *

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
    

class ComboBoxPoligonos(QComboBox):
    def __init__(self):
        super().__init__()
        self.atualizarComboBox
        
        #
        
    def atualizarComboBox(self):
        self.clear()
        self.addItem("Novo Polígono")
        i = 0
        for poligono in ListaPoligonos:
            self.addItem(f"Polígono {i + 1}")
            i += 1
        self.setCurrentIndex(-1)
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
    def __init__(self, parent, vertices, cor_arestas, cor_poligono):
        self.vertices       = vertices
        self.cor_arestas    = cor_arestas
        self.cor_poligono   = cor_poligono
        self.itensGraficos  = QGraphicsItemGroup()

        self.itensGraficos.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        #


