from _TelaDesenho import *


class MainWindow(QMainWindow):
    corArestaChanged = pyqtSignal(QColor)           # Signals que vão transmitir as trocas de cores feitas pelos usuários
    corPoligonoChanged = pyqtSignal(QColor)         
    
        
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("FillPoly")
        
        # Obtenha a geometria da tela
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = int(screen_geometry.width() * 0.8)
        screen_height = int(screen_geometry.height() * 0.8)

        # Defina o tamanho fixo da janela para a resolução da tela
        self.setFixedSize(QSize(screen_width, screen_height))
        
        # Mostre a janela maximizada
        self.showMaximized()
        


        # Definição do layout principal
        LayoutPrincipal = QVBoxLayout()
        self.titulo1 = Titulo1("Algoritmo FillPoly")
        LayoutPrincipal.addWidget(self.titulo1)
        
        
        # Definição da barra de ferramentas da esquerda
        LayoutBarraEsquerda = QVBoxLayout()
        self.titulo2 = Titulo2("Selecionar Polígono:")
        LayoutBarraEsquerda.addWidget(self.titulo2)
        self.comboBox = ComboBoxPoligonos()
    
        self.comboBox.currentIndexChanged.connect(self.comboBoxClicada)
        
        LayoutBarraEsquerda.addWidget(self.comboBox)  # Checkbox para selecionar polígonos
        LayoutBarraEsquerda.addWidget(QWidget())
        self.titulo3 = Titulo2("Selecionar Cores:")
        LayoutBarraEsquerda.addWidget(self.titulo3)
        
        
        # Grid 2x2 com os seletores de cores
        gridCores = QGridLayout()
        
        gridCores.addWidget(QLabel("Cor do Polígono:"), 0, 0)
        self.botaoCorPoligono = QPushButton()
        self.botaoCorPoligono.setStyleSheet(f"background-color: yellow; color: yellow")
        self.botaoCorPoligono.clicked.connect(self.selecionar_cor_poligono)
        gridCores.addWidget(self.botaoCorPoligono, 0, 1)
        
        gridCores.addWidget(QLabel("Cor das Arestas:"), 1, 0)
        self.botaoCorArestas = QPushButton()
        self.botaoCorArestas.setStyleSheet(f"background-color: black; color: black")
        self.botaoCorArestas.clicked.connect(self.selecionar_cor_arestas)
        gridCores.addWidget(self.botaoCorArestas, 1, 1)
        
        LayoutBarraEsquerda.addLayout(gridCores)
        
        LayoutBarraEsquerda.addWidget(QWidget())
        
        
        # Botões para apagar, redesenhar, e reiniciar o programa. E iniciar processo de criação de um novo polígono.
        
        
        self.botaoNovo = QPushButton("Adicionar Polígono")
        self.botaoNovo.clicked.connect(self.adicionar_poligono)
        LayoutBarraEsquerda.addWidget(self.botaoNovo)
        
        self.botaoDeletar = QPushButton("Deletar Polígono")
        self.botaoDeletar.clicked.connect(self.deletar_poligono)
        LayoutBarraEsquerda.addWidget(self.botaoDeletar)
        
        self.botaoRedesenhar = QPushButton("Redesenhar Polígonos")
        self.botaoRedesenhar.clicked.connect(self.redesenhar_poligonos)
        LayoutBarraEsquerda.addWidget(self.botaoRedesenhar)
        
        self.botaoReiniciar = QPushButton("Reiniciar")
        self.botaoReiniciar.clicked.connect(self.reiniciar)
        LayoutBarraEsquerda.addWidget(self.botaoReiniciar)
        
        LayoutBarraEsquerda.setStretch(2, 10)
        LayoutBarraEsquerda.setStretch(5, 50)
        
        LayoutBaixo = QHBoxLayout()
        LayoutBaixo.addLayout(LayoutBarraEsquerda)
        self.telaDesenho = TelaDesenho(self)
        LayoutBaixo.addWidget(self.telaDesenho)
        LayoutBaixo.setStretch(0, 1)
        LayoutBaixo.setStretch(1, 8)
        
        

        self.corArestaChanged.connect(self.telaDesenho.updateCorAresta)     #Conectamos os sinais de trocas de cores com
        self.corPoligonoChanged.connect(self.telaDesenho.updateCorPoligono)     #as funç~eos do widget filho.
                                                                                #agora, basta usar signal.emit() de forma dinâmica!

        LayoutPrincipal.addLayout(LayoutBaixo)
        LayoutPrincipal.setStretch(0, 1)
        LayoutPrincipal.setStretch(1, 20)

        widget = QWidget()
        widget.setLayout(LayoutPrincipal)
        self.setCentralWidget(widget)
        
        self.testx, self.testy, = 0, 0
    
    def comboBoxClicada(self):
        
        comboIndex = self.comboBox.currentIndex()
        
        if comboIndex == 0:  # This is the "None" option
            #print("Novo polígono selecionado na combobox")
            return
        
        
        if 1 <= comboIndex < len(ListaPoligonos) + 1:
            poligon = ListaPoligonos[comboIndex - 1]
            #print("Combobox clicada! Current index: ", comboIndex, poligon)

            self.botaoCorArestas.setStyleSheet(f"background-color: {poligon.cor_arestas.name()}; color: {poligon.cor_arestas.name()}")
            self.botaoCorPoligono.setStyleSheet(f"background-color: {poligon.cor_poligono.name()}; color: {poligon.cor_poligono.name()}")
            
            self.corArestaChanged.emit(poligon.cor_arestas)
            self.corPoligonoChanged.emit(poligon.cor_poligono)
            
    
    

    def selecionar_cor_poligono(self):
        color = QColorDialog.getColor()  # Abre o seletor de cores
        if color.isValid():
            print(f"Cor do Polígono: {color.name()}")  # Exibe a cor selecionada
            self.botaoCorPoligono.setStyleSheet(f"background-color: {color.name()}; color: {color.name()}")
            
            self.corPoligonoChanged.emit(color)
            
            comboIndex = self.comboBox.currentIndex() - 1
            if 0 <= comboIndex < len(ListaPoligonos):
                poligon = ListaPoligonos[comboIndex]
                poligon.cor_poligono = color
            corPoligono = color
        #
            

    def selecionar_cor_arestas(self):
        color = QColorDialog.getColor()  # Abre o seletor de cores
        if color.isValid():
            print(f"Cor das arestas: {color.name()}")  # Exibe a cor selecionada
            self.botaoCorArestas.setStyleSheet(f"background-color: {color.name()}; color: {color.name()}")
            
            self.corArestaChanged.emit(color)
            
            comboIndex = self.comboBox.currentIndex() - 1
            if 0 <= comboIndex < len(ListaPoligonos):
                poligon = ListaPoligonos[comboIndex]
                poligon.cor_arestas = color
            
        #



    def adicionar_poligono(self):
        print("Pontos liberados!")
        
        self.telaDesenho.setUI(False)
        self.telaDesenho.startFlag = True
        self.telaDesenho.lineFlag  = False


    def deletar_poligono(self):
        print("Deleta polígono!")
        self.deletarPoligono(self.comboBox.currentIndex() - 1)
        

    def redesenhar_poligonos(self):
        print("Redesenha polígonos!")
        self.telaDesenho.scene.blockSignals(True)   #Pausa a renderização da tela
        i = 0
        for poligono in ListaPoligonos:
            for item in poligono.itensGraficos.childItems():
                self.telaDesenho.scene.removeItem(item)         #Primeiro retiramos o polígono da tela
            
            #Agora desenhamos todos as suas linhas
            
            self.telaDesenho.updateCorAresta(poligono.cor_arestas)
            self.telaDesenho.updateCorPoligono(poligono.cor_poligono)
            
            self.telaDesenho.fillpoly(i, poligono)  
              
            verticeAnt = poligono.vertices[-1]
            for vertice in poligono.vertices:
                self.telaDesenho.desenharReta(verticeAnt, vertice, i)
                verticeAnt = vertice   
                
            
        
            i += 1

        self.telaDesenho.scene.blockSignals(False)  #Despausa a renderização da tela. +eficiente
        self.comboBox.atualizarComboBox()   #Função de atualizar o drop-down e a lista de cores
        
        

    def reiniciar(self):
        print("Apaga todos os polígonos!")
        self.deletarPoligonos()
        self.redesenhar_poligonos()
            
        
    def novoPoligono(self, parent):
        novoPoligono = Poligono(parent, [], self.telaDesenho.corAresta, self.telaDesenho.corPoligono) 
        ListaPoligonos.append(novoPoligono)
        #self.comboBox.atualizarComboBox()  # Atualiza a ComboBox após adicionar um novo polígono
        return len(ListaPoligonos)



    #   Criar a função de deletar o vetor inteiro
    def deletarPoligonos(self):
        for i in range(len(ListaPoligonos)):
            self.deletarPoligono(0)
            
        self.comboBox.atualizarComboBox()   #Função de atualizar o drop-down e a lista de cores


    def deletarPoligono(self, index):       # Recebe um index, e deleta o polígono equivalente.
        if 0 <= index < len(ListaPoligonos):
            poligono = ListaPoligonos[index]
            
            #Removemos os itens gráficos da cena
            for item in poligono.itensGraficos.childItems():
                self.telaDesenho.scene.removeItem(item)
                
            self.telaDesenho.scene.removeItem(poligono.itensGraficos)   #Removemos o grupo de itens gráficos
            
            ListaPoligonos.pop(index)
            self.comboBox.atualizarComboBox()
                
        
        
        
    def alterarCorAresta(self, index, cor):
        if 0 <= index < len(ListaPoligonos):
            ListaPoligonos[index].cor_arestas = cor


    def alterarCorPoligono(self, index, cor):
        if 0 <= index < len(ListaPoligonos):
            ListaPoligonos[index].cor_poligono = cor
        
        



