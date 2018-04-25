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
        
    def initGui(self):
         
        # cria uma ação que iniciará a configuração do plugin 
        self.actions = []
        pai = self.iface.mainWindow()
        #self.keyAction = QAction(u"Copy the Attributes", self.iface.mainWindow())
        #self.keyAction.triggered.connect(self.run)
        #self.iface.registerMainWindowAction(self.keyAction, "Ctrl+alt+*")
        icon_path = ':/plugins/Alterna_imagens/rup.png'
        icon_path2 = ':/plugins/Alterna_imagens/rdown.png'
        self.action = QAction (QIcon (icon_path),'up imagem', pai)
        self.actions.append(self.action)
        self.action2 = QAction (QIcon (icon_path2),'down imagem', pai)
        self.action.setObjectName ('Alterna imagens')
        self.actions.append(self.action2)

        self.toolbar = self.iface.addToolBar('Alterna Imagens')
        # Adicionar o botão da barra de ferramentas e item de menu 
        self.toolbar.addAction(self.action)
        self.toolbar.addAction(self.action2)
        
        #self.action.triggered.connect()
        #self.action2.triggered.connect()
        
    def unload(self):
        for action in self.actions:
            self.toolbar.removeAction(action)
        # remove the toolbar
        del self.toolbar

    def alterna(self):
        root = QgsProject.instance().layerTreeRoot()
        grupo = root.findGroup("Imagens_Dinamicas")
        parentes = grupo.parent()
        

        for child in root.children():
            if isinstance(child, QgsLayerTreeGroup):
                if child.name() == grupo: #testa os subgrupos de grupo
                    for subChild in child.children():
                        if isinstance(subChild, QgsLayerTreeGroup) and subChild.type() == QgsMapLayer.RasterLayer:
                            subChild.name()
            
            

            ''' elif(layer.type() == QgsMapLayer.RasterLayer):
                layers_ativados = self.iface.mapCanvas().layers()
                todos_os_layers = QgsMapLayerRegistry.instance().mapLayers()
            for layer in layers_ativados:
                if  layer.connect:
                   pass
 '''

                
   
