# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Layer2ThemePlugin
                                 A QGIS plugin
 This plugin allows users to append layers to existing themes in QGIS.
                             -------------------
        begin                : 2025-07-30
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Osama Heba
        email                : o.h.heba@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtWidgets import QAction, QMenu
from qgis.PyQt.QtCore import QEvent
from qgis.PyQt.QtGui import QCursor
from qgis.core import Qgis, QgsProject, QgsMapLayer, QgsMapThemeCollection
from qgis.utils import iface

# Custom QMenu that stays open when clicking checkable actions.
class StayOpenMenu(QMenu):
    def mouseReleaseEvent(self, event):
        action = self.actionAt(event.pos())
        if action and action.isCheckable():
            # Toggle the action manually without closing the menu.
            action.toggle()
            event.accept()
        else:
            super().mouseReleaseEvent(event)

class Layer2ThemePlugin:
    def __init__(self, iface):
        self.iface =  iface
        self.actions =  []


    def initGui(self):
        for layer_type in QgsMapLayer.LayerType:
            action = QAction("Append layer to theme/s", self.iface.mainWindow())
            menu = StayOpenMenu()
            menu.aboutToShow.connect(lambda m=menu: self.updateMenu(m))
            action.setMenu(menu)
            self.iface.addCustomActionForLayerType(action, None, layer_type, True)
            self.actions.append(action)

    def updateMenu(self, menu):
        menu.clear()

        self.project =                  QgsProject.instance()
        self.theme_collection =         self.project.mapThemeCollection()
        self.themes =                   self.theme_collection.mapThemes()
        layer =                         iface.activeLayer()
        #self.layers =                  self.project.mapLayers()                        # To be removed, not used in the plugin.
        #self.root =                    self.project.layerTreeRoot()                    #These items are not used in the plugin, but are kept for further development.
        #self.model =                   iface.layerTreeView().layerTreeModel()          #These items are not used in the plugin, but are kept for further development.
        if not layer:
            return

        # Create a checkable action per theme.
        for theme in self.themes:
            act = QAction(theme, menu)
            act.setCheckable(True)
            visible_ids = self.theme_collection.mapThemeVisibleLayerIds(theme)
            act.setChecked(layer.id() in visible_ids)
            act.toggled.connect(lambda checked, t=theme, lyr=layer: self.toggleThemeVisibility(theme_name=t, layer=lyr, visible=checked))
            menu.addAction(act)

        menu.addSeparator()

        check_all = QAction("Check all", menu)
        check_all.triggered.connect(lambda _, lyr=layer: self.setAllThemes(layer=lyr, visible=True))
        menu.addAction(check_all)

        uncheck_all = QAction("Uncheck all", menu)
        uncheck_all.triggered.connect(lambda _, lyr=layer: self.setAllThemes(layer=lyr, visible=False))
        menu.addAction(uncheck_all)

    def toggleThemeVisibility(self, theme_name, layer, visible):  
        theme_collection = self.theme_collection
        layer_record = QgsMapThemeCollection.MapThemeLayerRecord(layer)
        theme_record = theme_collection.mapThemeState(theme_name)
        current_ids = list(theme_collection.mapThemeVisibleLayerIds(theme_name))
        if visible and layer.id() not in current_ids:
            theme_record.addLayerRecord(layer_record)
            theme_collection.update(theme_name, theme_record)
            current_ids.append(layer.id())
        elif not visible and layer.id() in current_ids:
            theme_record.removeLayerRecord(layer)
            theme_collection.update(theme_name, theme_record)
            current_ids.remove(layer.id())
        
        iface.mapCanvas().refresh()  # Refresh the map canvas to reflect changes
        # iface.mapCanvas().refreshAllLayers()


    def setAllThemes(self, layer, visible):
        for theme in self.themes:
            self.toggleThemeVisibility(theme_name=theme, layer=layer, visible=visible)
        #self.theme_collection.applyTheme(name=*active theme*, root=root, model=model)           # This should make changes update automatically to active theme, I just couldn't find away to grab the active theme name.
        '''I difintly need to apply this eleswhere, toggleThemeVisibility is a candidate\
            but it will repeat applying the theme for as many themes there are.'''  

    def unload(self):
        # Remove the custom actions when the plugin is unloaded.
        for action in self.actions:
            self.iface.removeCustomActionForLayerType(action)
        self.actions = []