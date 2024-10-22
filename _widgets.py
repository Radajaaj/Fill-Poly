import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtCore import pyqtSignal, QObject
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



class TelaDesenho(QGraphicsView):   #QGraphicsView. Widget usado para criar e manipular elementos gráficos.
    
    lineFlag  = False    #Variável que acompanha se existe algum polígono que ainda não foi finalizado pelo usuário
    startFlag = False    #Habilita ou edsabilita o uso da tela de desenho
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent    #Ponteiro para fácil acesso ao widget pai
        
        #Aqui criamos um retângulo branco para cobrir todo o fundo da cena.
        self.setBackgroundBrush(QBrush(QColor("white")))
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setBackgroundBrush(QBrush(QColor("white")))
        self.scene.setBackgroundBrush(QBrush(QColor("white")))
        self.scene.setSceneRect(0, 0, self.width(), self.height())


        self.corAresta = QColor('black')
        self.corPoligono = QColor('yellow')




        #
    
    
    
    def mousePressEvent(self, e):
        
        if self.startFlag == True:
            
            if e.button() == Qt.MouseButton.LeftButton:

                if self.lineFlag == False:              # Se não tiver nenhum polígono inicializado na tela...
                    print(len(ListaPoligonos))              # Criamos um novo polígono, e começamos a armazenar os pontos dele.
                    self.parent.novoPoligono(self)
                    self.scene.addItem(ListaPoligonos[-1].itensGraficos)
                    self.lineFlag = True
                    ListaPoligonos[-1].itensGraficos.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

                    

                pos = self.mapToScene(QPoint(int(e.position().x()), int(e.position().y())))
                #Posição do clique do mouse convertido da posição global (em relação ao app) para a posição relativa (em relação ao widget)

                #TODO self.vetorPontos.append(pos)
                ListaPoligonos[-1].vertices.append(pos) # Definimos a posição do mouse como um dos vértices.     

                #TODO print("----------------\nTamanho: ", len(self.vetorPontos))
                #TODO print("Posição: ", self.vetorPontos[-1])

                print("----------------\nTamanho: ", len(ListaPoligonos[-1].vertices))
                print("Posição: ", ListaPoligonos[-1].vertices[-1])


                #Agora checamos se tem no minimo 2 pontos, e desenhamos a reta:
                if len(ListaPoligonos[-1].vertices) > 1:
                    self.desenharReta(ListaPoligonos[-1].vertices[-1], ListaPoligonos[-1].vertices[-2], -1)
                else:
                    self.desenharPonto(int(pos.x()), int(pos.y()), -1, self.corAresta)  #  Desenhar o primeiro ponto definido
                #TODO

            if e.button() == Qt.MouseButton.RightButton:
                if not ListaPoligonos or len(ListaPoligonos[-1].vertices) < 2 or self.lineFlag == False:
                    print("Erro! Selecione ao menos 2 vértices.")
                    telaErro = QMessageBox(self)
                    telaErro.setWindowTitle("Atenção!")
                    telaErro.setText("Atenção! Selecione ao menos 2 vértices antes de finalizar um polígono.")
                    telaErro.exec()
                else:
                    self.lineFlag = False   #Finalizamos o polígono, então viramos a flag.
                    self.setUI(not(self.lineFlag))
                    self.startFlag = False

                    pos = self.mapToScene(QPoint(int(e.position().x()), int(e.position().y())))
                    ListaPoligonos[-1].vertices.append(pos)

                    print("----------------\nTamanho: ", len(ListaPoligonos[-1].vertices))
                    print("Posição: ", ListaPoligonos[-1].vertices[-1])

                    # Desenhamos as 2 últimas retas
                    self.desenharReta(ListaPoligonos[-1].vertices[-1], ListaPoligonos[-1].vertices[-2], -1)
                    self.desenharReta(ListaPoligonos[-1].vertices[-1], ListaPoligonos[-1].vertices[0], -1)

                #print("\n-------------------\nVETOR FINAL\n", self.vetorPontos, "\n----------------\n")
                #self.vetorPontos.clear()

                    print("\n-------------------\nVETOR FINAL\n", ListaPoligonos[-1].vertices, "\n----------------\n")
                    print("Len ListaPoli: ", len(ListaPoligonos))
                    
                    self.parent.comboBox.atualizarComboBox()   #Função de atualizar o drop-down e a lista de cores

        else:
            super().mousePressEvent(e)
        #
        
    def desenharPonto(self, x, y, index, cor, size = 1):
        print("cor do ponto eh ", cor.name())
        pontinho = QGraphicsEllipseItem(QRectF(x - size / 2, y - size / 2, size, size))
        pontinho.setBrush(QBrush(cor))
        pontinho.setPen(QPen(cor))
        
        pontinho.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        
        ListaPoligonos[index].itensGraficos.addToGroup(pontinho)
        #TODO self.scene.addItem(pontinho)
        
    
    def desenharReta(self, ponto1, ponto2, index, size = 3):
        reta = QGraphicsLineItem(ponto1.x(), ponto1.y(), ponto2.x(), ponto2.y())
        
        reta.setPen(QPen(self.corAresta, size))
        
        reta.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        
        ListaPoligonos[index].itensGraficos.addToGroup(reta)
        #TODO self.scene.addItem(reta)
    
    
    def updateCorAresta(self, nova_cor):
        self.corAresta = nova_cor  # Atualiza o atributo da instância
        print(f"Cor das arestas atualizada para: {self.corAresta.name()}")  # Debug
    
    
    def updateCorPoligono(self, nova_cor):
        self.corPoligono = nova_cor  # Atualiza o atributo da instância
        print(f"Cor dos poligonos atualizada para: {self.corAresta.name()}")  # Debug


    def setUI(self, flag):    #Vamos desativar a UI sempre que a lineFlag for verdadeira.
        self.parent.comboBox.setEnabled(flag)
        self.parent.botaoCorPoligono.setEnabled(flag)
        self.parent.botaoCorArestas.setEnabled(flag)
        self.parent.botaoDeletar.setEnabled(flag)
        self.parent.botaoRedesenhar.setEnabled(flag)
        self.parent.botaoReiniciar.setEnabled(flag)

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

        #


