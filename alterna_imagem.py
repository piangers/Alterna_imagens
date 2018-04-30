# -*- coding: utf-8 -*-

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from qgis.core import QgsProject, QgsLayerTreeGroup, QgsMapLayer, QgsMapLayerRegistry
import resources_rc
from qgis.gui import QgsMessageBar
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
        icon_path = ':/plugins/Alterna_imagens/runup.png'
        icon_path2 = ':/plugins/Alterna_imagens/rundown.png'
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

    def alternaUp(self):
        self.alterna('Up')

    def alternaDown(self, grupo):
        self.alterna('Down')

    
    def alterna(self, tipo):
        root = QgsProject.instance().layerTreeRoot()
        grupo = root.findGroup("Imagens Dinamicas")
        if grupo:
            lista = [x for x in grupo.findLayerIds() if QgsMapLayerRegistry.instance().mapLayer(x).type() == QgsMapLayer.RasterLayer]
            if len(lista) > 0:
                rastersVisiveis = [x for x in lista if grupo.findLayer(x).isVisible() > 1]

                if len(rastersVisiveis) > 1 or len(rastersVisiveis) == 0: # Se houver zero ou mais de um layer visivel, desmarcar todos e marcar o primeiro da lista
                    for i in lista:
                        grupo.findLayer(i).setVisible(0) # Desmarca todos
                    
                    grupo.findLayer(lista[0]).setVisible(2) # Marca o primeiro

                else: # Se houver somente um layer visivel, passar para o proximo
                    idVisivel = rastersVisiveis[0] # Id do unico raster visivel
                    posicao = lista.index(idVisivel) # Posicao do id acima na lista de rasters (preciso para achar o proximo)

                    grupo.findLayer(idVisivel).setVisible(0) # Desmarca a visualizacao do layer antigo

                    if tipo == 'Down':
                        # down (proximo)
                        if posicao == len(lista)-1:
                            posicao = 0
                        else:
                            posicao = posicao + 1

                    if tipo == 'Up':
                        # up (anterior)
                        if posicao == 0:
                            posicao = len(lista)-1
                        else:
                            posicao = posicao - 1

                    lyr = grupo.findLayer(lista[posicao])
                    lyr.setVisible(2)
            else:
                
                self.iface.messageBar().pushMessage(u'O Grupo deve conter pelo menos uma camada.', level=QgsMessageBar.INFO, duration=5)
        else:
            
            self.iface.messageBar().pushMessage(u'Deve haver um GRUPO com o nome: Imagens Dinamicas.', level=QgsMessageBar.INFO, duration=5)


