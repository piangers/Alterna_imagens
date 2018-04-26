# -*- coding: utf-8 -*-

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from qgis.core import QgsProject, QgsLayerTreeGroup, QgsMapLayer, QgsMapLayerRegistry

# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
import os.path

class Alterna_imagem:

    def __init__(self,iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.nomeGrupo = ""
        
    def initGui(self):
         
        # cria uma ação que iniciará a configuração do plugin 
        self.actions = []
        pai = self.iface.mainWindow()
        #self.keyAction = QAction(u"Copy the Attributes", self.iface.mainWindow())
        #self.keyAction.triggered.connect(self.run)
        #self.iface.registerMainWindowAction(self.keyAction, "Ctrl+alt+*")
        icon_path = ':/plugins/Alterna_imagens/rumup.png'
        icon_path2 = ':/plugins/Alterna_imagens/rumdown.png'
        self.actionUp = QAction (QIcon (icon_path),'up imagem', pai)
        self.actions.append(self.actionUp)
        self.actionDown = QAction (QIcon (icon_path2),'down imagem', pai)
        self.actions.append(self.actionDown)

        self.toolbar = self.iface.addToolBar('Alterna Imagens')
        # Adicionar o botão da barra de ferramentas e item de menu 
        self.toolbar.addAction(self.actionUp)
        self.toolbar.addAction(self.actionDown)
        
        self.actionUp.triggered.connect(self.alternaUp)
        self.actionDown.triggered.connect(self.alternaDown)
        
    def unload(self):
        for action in self.actions:
            self.toolbar.removeAction(action)
        # remove the toolbar
        del self.toolbar

    def alternaDown(self, grupo):
        root = QgsProject.instance().layerTreeRoot()
        grupo = root.findGroup("Imagens_Dinamicas")
        lista = QgsProject.instance().layerTreeRoot().findLayerIds() # Lista de TODOS os layers (qualquer tipo)
        
        rastersVisiveis = []

        for i in lista:                                  #(id)
            layer = QgsMapLayerRegistry.instance().mapLayer(i)
            layerT = QgsProject.instance().layerTreeRoot().findLayer(i)

            if layer.type() != QgsMapLayer.RasterLayer: # Se a camada nao for raster, tirar o id dela da lista
                lista.remove(i)
            
            else:
                if layerT.isVisible() > 1: # Significa que o item da arvore de camadas esta marcado para ficar visivel
                    rastersVisiveis.append(i) # Incrementar a variavel que guarda o numero de camadas visiveis
        
        if len(rastersVisiveis) > 1 or len(rastersVisiveis) == 0: # Se houver zero ou mais de um layer visivel, desmarcar todos e marcar o primeiro da lista
            for i in lista:
                QgsProject.instance().layerTreeRoot().findLayer(i).setVisible(0) # Desmarca todos
            
            QgsProject.instance().layerTreeRoot().findLayer(lista[0]).setVisible(2) # Marca o primeiro

        else: # Se houver somente um layer visivel, passar para o proximo
            idVisivel = rastersVisiveis[0] # Id do unico raster visivel
            posicao = lista.index(idVisivel) # Posicao do id acima na lista de rasters (preciso para achar o proximo)

            QgsProject.instance().layerTreeRoot().findLayer(idVisivel).setVisible(0) # Desmarca a visualizacao do layer antigo

            # down (proximo)
            if posicao == len(lista)-1:
                posicao = 0
            else:
                posicao = posicao + 1

            idNovo = lista[posicao]
            lyr = QgsProject.instance().layerTreeRoot().findLayer(idNovo)
            lyr.setVisible(2)

    def alternaUp(self):
        root = QgsProject.instance().layerTreeRoot()
        grupo = root.findGroup("Imagens_Dinamicas")
        lista = QgsProject.instance().layerTreeRoot().findLayerIds() # Lista de TODOS os layers (qualquer tipo)
        
        rastersVisiveis = []

        for i in lista:                                  #(id)
            layer = QgsMapLayerRegistry.instance().mapLayer(i)
            layerT = QgsProject.instance().layerTreeRoot().findLayer(i)

            if layer.type() != QgsMapLayer.RasterLayer: # Se a camada nao for raster, tirar o id dela da lista
                lista.remove(i)
            
            else:
                if layerT.isVisible() > 1: # Significa que o item da arvore de camadas esta marcado para ficar visivel
                    rastersVisiveis.append(i) # Incrementar a variavel que guarda o numero de camadas visiveis
        
        if len(rastersVisiveis) > 1 or len(rastersVisiveis) == 0: # Se houver zero ou mais de um layer visivel, desmarcar todos e marcar o primeiro da lista
            for i in lista:
                QgsProject.instance().layerTreeRoot().findLayer(i).setVisible(0) # Desmarca todos
            
            QgsProject.instance().layerTreeRoot().findLayer(lista[0]).setVisible(2) # Marca o primeiro

        else: # Se houver somente um layer visivel, passar para o proximo
            idVisivel = rastersVisiveis[0] # Id do unico raster visivel
            posicao = lista.index(idVisivel) # Posicao do id acima na lista de rasters (preciso para achar o proximo)

            QgsProject.instance().layerTreeRoot().findLayer(idVisivel).setVisible(0) # Desmarca a visualizacao do layer antigo

            # up (anterior)
            if posicao == 0:
                posicao = len(lista)-1
            else:
                posicao = posicao - 1

            idNovo = lista[posicao]
            lyr = QgsProject.instance().layerTreeRoot().findLayer(idNovo)
            lyr.setVisible(2)

