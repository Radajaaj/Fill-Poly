from widgets import *





class MainWindow(QMainWindow):
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
        
        
        # Botões para apagar, redesenhar, e reiniciar o programa
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

        LayoutPrincipal.addLayout(LayoutBaixo)
        LayoutPrincipal.setStretch(0, 1)
        LayoutPrincipal.setStretch(1, 20)

        widget = QWidget()
        widget.setLayout(LayoutPrincipal)
        self.setCentralWidget(widget)
        
    
    
    def comboBoxClicada(self):
        
        comboIndex = self.comboBox.currentIndex()
        if 0 <= comboIndex < len(ListaPoligonos):
            poligon = ListaPoligonos[comboIndex]
            #print("Combobox clicada! Current index: ", comboIndex, poligon)

            self.botaoCorArestas.setStyleSheet(f"background-color: {poligon.cor_arestas.name()}; color: {poligon.cor_arestas.name()}")
            self.botaoCorPoligono.setStyleSheet(f"background-color: {poligon.cor_poligono.name()}; color: {poligon.cor_poligono.name()}")
    
    

    def selecionar_cor_poligono(self):
        color = QColorDialog.getColor()  # Abre o seletor de cores
        if color.isValid():
            print(f"Cor do Polígono: {color.name()}")  # Exibe a cor selecionada
            self.botaoCorPoligono.setStyleSheet(f"background-color: {color.name()}; color: {color.name()}")
            
            comboIndex = self.comboBox.currentIndex()
            poligon = ListaPoligonos[comboIndex]
            poligon.cor_poligono = color
            
        #
            

    def selecionar_cor_arestas(self):
        color = QColorDialog.getColor()  # Abre o seletor de cores
        if color.isValid():
            print(f"Cor das arestas: {color.name()}")  # Exibe a cor selecionada
            self.botaoCorArestas.setStyleSheet(f"background-color: {color.name()}; color: {color.name()}")
            
            comboIndex = self.comboBox.currentIndex()
            poligon = ListaPoligonos[comboIndex]
            poligon.cor_arestas = color
        
        #

    def deletar_poligono(self):
        print("Deleta polígono!")
        self.deletarPoligono(self.comboBox.currentIndex())
        

    def redesenhar_poligonos(self):
        print("Redesenha polígonos!")


    def reiniciar(self):
        print("Apaga todos os polígonos e redesenha tudo")
        self.deletarPoligonos()
        self.redesenhar_poligonos()
            
        
    def novoPoligono(self):
        novoPoligono = Poligono(vertices=[])
        ListaPoligonos.append(novoPoligono)
        self.comboBox.atualizarComboBox()  # Atualiza a ComboBox após adicionar um novo polígono
        return len(ListaPoligonos)


    #   Criar a função de deletar o vetor inteiro
    def deletarPoligonos(self):
        for i in range(len(ListaPoligonos)):
            ListaPoligonos.pop()
            #Função de atualizar o drop-down e a lista de cores?
        self.comboBox.atualizarComboBox()


    def deletarPoligono(self, index):     # Recebe um index, e deleta o polígono equivalente.
        if 0 <= index < len(ListaPoligonos):
            ListaPoligonos.pop(index)
                #Função de atualizar o drop-down e a lista de cores?
        self.comboBox.atualizarComboBox()
        
        
    def alterarCorAresta(self, index, cor):
        if 0 <= index < len(ListaPoligonos):
            ListaPoligonos[index].cor_arestas = cor


    def alterarCorPoligono(self, index, cor):
        if 0 <= index < len(ListaPoligonos):
            ListaPoligonos[index].cor_poligono = cor
        
        



