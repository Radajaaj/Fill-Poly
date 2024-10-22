from _widgets import *

class TelaDesenho(QGraphicsView):                               #QGraphicsView. Widget usado para criar e manipular elementos gráficos.
    
    lineFlag  = False    #Variável que acompanha se existe algum polígono que ainda não foi finalizado pelo usuário
    startFlag = False    #Habilita ou edsabilita o uso da tela de desenho
    
    itemSelecionado = pyqtSignal(QGraphicsItem)                 #Sinal pra quando o user escolher um poligono com o mouse
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent                                    #Ponteiro para fácil acesso ao widget pai
        
                                                                #Aqui criamos um retângulo branco para cobrir todo o fundo da cena.
        self.setBackgroundBrush(QBrush(QColor("white")))
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setBackgroundBrush(QBrush(QColor("white")))
        self.scene.setBackgroundBrush(QBrush(QColor("white")))
        self.scene.setSceneRect(0, 0, self.width(), self.height())


        self.corAresta = QColor('yellow')
        self.corPoligono = QColor('black')

        #

    def mousePressEvent(self, e):
        
        if self.startFlag == True:
            
            if e.button() == Qt.MouseButton.LeftButton:

                if self.lineFlag == False:                      # Se não tiver nenhum polígono inicializado na tela...
                    #print(len(ListaPoligonos))                 # Criamos um novo polígono, e começamos a armazenar os pontos dele.
                    self.parent.novoPoligono(self)
                    self.scene.addItem(ListaPoligonos[-1].itensGraficos)
                    self.lineFlag = True
                    ListaPoligonos[-1].itensGraficos.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

                # pos = self.mapToScene(QPoint(int(e.position().x()), int(e.position().y())))
                pos = self.mapToScene(e.position().toPoint())
                
                #Posição do clique do mouse convertido da posição global (em relação ao app) para a posição relativa (em relação ao widget)

                #TODO self.vetorPontos.append(pos)
                ListaPoligonos[-1].vertices.append(pos.toPoint())   #Definimos a posição do mouse como um dos vértices.     

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
                    self.lineFlag = False                       #Finalizamos o polígono, então viramos a flag.
                    self.setUI(not(self.lineFlag))
                    self.startFlag = False

                    #pos = self.mapToScene(QPoint(int(e.position().x()), int(e.position().y())))
                    pos = self.mapToScene(e.position().toPoint())
                    
                    ListaPoligonos[-1].vertices.append(pos.toPoint())

                    print("----------------\nTamanho: ", len(ListaPoligonos[-1].vertices))
                    print("Posição: ", ListaPoligonos[-1].vertices[-1])

                    # Desenhamos as 2 últimas retas
                    self.desenharReta(ListaPoligonos[-1].vertices[-1], ListaPoligonos[-1].vertices[-2], -1)
                    self.desenharReta(ListaPoligonos[-1].vertices[-1], ListaPoligonos[-1].vertices[0], -1)

                #print("\n-------------------\nVETOR FINAL\n", self.vetorPontos, "\n----------------\n")
                #self.vetorPontos.clear()

                    print("\n-------------------\nVETOR FINAL\n", ListaPoligonos[-1].vertices, "\n----------------\n")
                    print("Len ListaPoli: ", len(ListaPoligonos))
                    
                    self.parent.comboBox.atualizarComboBox()    #Função de atualizar o drop-down e a lista de cores

        else:
            super().mousePressEvent(e)
            items = self.scene.selectedItems()
            if len(items) != 0:
                item = items[0]
                                                                #Loop for para ir comparando com cada item de ListaPoligonos
                for i in range(len(ListaPoligonos)):
                    
                    if item == ListaPoligonos[i].itensGraficos:
                       self.parent.comboBox.setCurrentIndex(i + 1)
                       break
                                                                #Dai muda o index pro index do item encontrado
    #
        
    def desenharPonto(self, x, y, index, cor, size=1):
        # Cria um ponto 1x1 na posição (x, y)
        pontinho = QGraphicsRectItem(x, y, size, size)
        pontinho.setBrush(QBrush(cor))  # Define a cor do ponto

        pontinho.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        # Adiciona o ponto ao grupo de itens gráficos do polígono
        ListaPoligonos[index].itensGraficos.addToGroup(pontinho)

    # TODO: self.scene.addItem(pontinho)
    
    def desenharReta(self, ponto1, ponto2, index, size = 3):
        
        if self.parent.flagBordas == True:
        
            reta = QGraphicsLineItem(ponto1.x(), ponto1.y(), ponto2.x(), ponto2.y())

            reta.setPen(QPen(self.corAresta, size))

            reta.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

            ListaPoligonos[index].itensGraficos.addToGroup(reta)
            #TODO self.scene.addItem(reta)
    
    #
    
    def updateCorAresta(self, nova_cor):
        self.corAresta = nova_cor                               # Atualiza o atributo da instância
        print(f"Cor das arestas atualizada para: {self.corAresta.name()}")  # Debug
    
    #
    
    def updateCorPoligono(self, nova_cor):
        self.corPoligono = nova_cor                             # Atualiza o atributo da instância
        print(f"Cor dos poligonos atualizada para: {self.corAresta.name()}")  # Debug

    #

    def setUI(self, flag):                                      #Vamos desativar a UI sempre que a lineFlag for verdadeira.
        self.parent.comboBox.setEnabled(flag)
        self.parent.botaoCorPoligono.setEnabled(flag)
        self.parent.botaoCorArestas.setEnabled(flag)
        self.parent.botaoDeletar.setEnabled(flag)
        self.parent.botaoRedesenhar.setEnabled(flag)
        self.parent.botaoReiniciar.setEnabled(flag)

    #
                        
    def fillpoly(self, indexPoly, poligono):
            Ymin = 999999
            Ymax = 0
            vetorPoly = []

            for i in poligono.vertices:                         # Primeiro, percorremos por todos os vértices, para obter o Ymin e o Ymax
                if i.y() < Ymin:
                    Ymin = int(i.y())
                if i.y() > Ymax:
                    Ymax = int(i.y())

            #print("\n")
            #print("Ymin Sistema: ", Ymin)
            #print("Ymax Sistema: ", Ymax)

            #Ns = (Ymax - 1) - Ymin                             # Define-se o número de scanlines
            Ns = Ymax - Ymin + 1                                # Det Acho que é -1 em vez de +1

            #print("Ns é: ", Ns)


            for i in range(Ns):                                 # Preparamos um array de listas vazias, com Ns posições
                vetorPoly.append([])


            for i in range(-1, len(poligono.vertices) - 1):     #Acho que vai ter que fazer len(poligono.vertices) - 1
                vertCima    = poligono.vertices[i]
                vertBaixo   = poligono.vertices[i + 1]

                if vertCima.y() > vertBaixo.y():                #Vertcima sempre terá o menor valor de Y
                    vertCima, vertBaixo = vertBaixo, vertCima

                if vertCima.y() == vertBaixo.y():               # Arestas horizontais não precisam ser processadas
                    pass
                
                #print("\nVertCima: ", vertCima)
                #print("VertBaixo: ", vertBaixo)

                YminReta = int(min(vertCima.y(), vertBaixo.y()))
                YmaxReta = int(max(vertCima.y(), vertBaixo.y()))

                try:
                    Tx = (vertBaixo.x() - vertCima.x())/(vertBaixo.y() - vertCima.y())      #1/m
                except ZeroDivisionError as e:
                    Tx = (vertBaixo.x() - vertCima.x())/ 0.0001

                #print("YminReta: ", YminReta)
                #print("YmaxReta: ", YmaxReta)
                #print("Tx is ", Tx)

                vetorPoly[YminReta - Ymin].append(vertCima)     #O primeiro elemento sempre é o vertCima
                #print("vetorPoly len is: ", len(vetorPoly))
                
                for j in range(YminReta + 1 - Ymin, YmaxReta - Ymin): #Começamos a partir da segunda scanline então
                    pontoAnterior = vetorPoly[j-1][-1]
                    
                    pontoNovo     = QPointF(pontoAnterior.x() + Tx, pontoAnterior.y() + 1)   #Incremental -> feito com base no valor   anterior

                    vetorPoly[j].append(pontoNovo)
                    #print("Pontoanterior: ", pontoAnterior, " | PontoNovo: ", pontoNovo)

                    #Loop pronto! Dai ele vai ir fazendo isso para todas as retas, teoricamente.
    
            #Loop terminou! Agora, fazemos um sorting em cada vetor de vetorPoly, com base nos valores de X
            #print("Before sorting:")
            #for i in range(len(vetorPoly)):
                #print("Vetor ", i, ": ", vetorPoly[i])

            for i in range(len(vetorPoly)):
                vetorPoly[i].sort(key=lambda point: point.x())  # é

            #print("After sorting:")
            #for i in range(len(vetorPoly)):
                #print("Vetor ", i, ": ", vetorPoly[i])

            #Pronto. Temos tudo feito, e o vetorPoly foi criado e populado. Agora, vamos printando ponto por ponto.
    
            for scanline in vetorPoly:
                if len(scanline) == 1:
                    self.desenharPonto(int(scanline[-1].x()), int(scanline[-1].y()), indexPoly, poligono.cor_poligono)
            
                if len(scanline) % 2 != 0:
                    print("Quantia impar de pontos. Checar terminal")

                #Agora pintamos entre cada par de pontos
                
                for i in range(0, len(scanline) - 1, 2):
                    primeiro = scanline[i]
                    segundo  = scanline[i + 1]

                    for j in range(int(primeiro.x()), int(segundo.x())):
                        self.desenharPonto(floor(j), ceil(primeiro.y()), indexPoly, poligono.cor_poligono)

    #