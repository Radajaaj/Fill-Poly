import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.uic import *
from math import *


ListaPoligonos = []     # Lista global que armazena cada polígono, definido por meio de seus vértices


def novoVertice(ponto): # Coloca um novo vértice no último polígono da lista de polígonos, e retorna o número de vértices do polígono atual.
    ListaPoligonos[-1].vertices.append(ponto)   #Tipo QPoint do PyQT6. Uma classe simples para armazenar pontos
    return len(ListaPoligonos[-1].vertices)

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
        
        #


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