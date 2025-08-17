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


from functools import partial
from qgis.PyQt.QtWidgets import QAction, QMenu
from qgis.core import QgsProject, QgsMapLayer, QgsMapThemeCollection
from qgis.utils import iface


class StayOpenMenu(QMenu):
    """QMenu that stays open when clicking checkable actions."""
    def mouseReleaseEvent(self, event):
        action = self.actionAt(event.pos())
        if action and action.isCheckable():
            action.toggle()
            event.accept()
        else:
            super().mouseReleaseEvent(event)


class Layer2ThemePlugin:
    def __init__(self, iface):
        self.iface = iface
        self.actions = []

    def initGui(self):
        """Create context menu actions for all layer types."""
        for layer_type in QgsMapLayer.LayerType:
            action = QAction("Toggle layer visibility in theme(s)", self.iface.mainWindow())
            menu = StayOpenMenu()
            menu.aboutToShow.connect(partial(self.updateMenu, menu))
            action.setMenu(menu)
            self.iface.addCustomActionForLayerType(action, None, layer_type, True)
            self.actions.append(action)

    def unload(self):
        """Remove actions when plugin is unloaded."""
        for action in self.actions:
            self.iface.removeCustomActionForLayerType(action)
        self.actions.clear()

    # --------------------
    # Helpers
    # --------------------
    def themeCollection(self):
        return QgsProject.instance().mapThemeCollection()

    # --------------------
    # Menu handling
    # --------------------
    def updateMenu(self, menu):
        menu.clear()
        theme_collection = self.themeCollection()
        themes = theme_collection.mapThemes() if theme_collection else []
        layer = iface.activeLayer()

        if not layer:
            msg = QAction("No active layer selected", menu)
            msg.setEnabled(False)
            menu.addAction(msg)
            return

        if not themes:
            msg = QAction("Create a theme to activate", menu)
            msg.setEnabled(False)
            menu.addAction(msg)
            return

        # Theme toggles
        for theme in themes:
            act = QAction(theme, menu, checkable=True)
            visible_ids = theme_collection.mapThemeVisibleLayerIds(theme)
            act.setChecked(layer.id() in visible_ids)
            act.toggled.connect(partial(self.toggleThemeVisibility, theme, layer))
            menu.addAction(act)

        menu.addSeparator()

        # Batch toggles
        check_all = QAction("Check all", menu)
        check_all.triggered.connect(partial(self.setAllThemes, layer, True))
        menu.addAction(check_all)

        uncheck_all = QAction("Uncheck all", menu)
        uncheck_all.triggered.connect(partial(self.setAllThemes, layer, False))
        menu.addAction(uncheck_all)

    # --------------------
    # Theme operations
    # --------------------
    def toggleThemeVisibility(self, theme_name, layer, visible):
        theme_collection = self.themeCollection()
        if not theme_collection:
            return

        theme_record = theme_collection.mapThemeState(theme_name)
        layer_record = QgsMapThemeCollection.MapThemeLayerRecord(layer)

        if visible:
            theme_record.addLayerRecord(layer_record)
        else:
            theme_record.removeLayerRecord(layer)

        theme_collection.update(theme_name, theme_record)
        iface.mapCanvas().refresh()

    def setAllThemes(self, layer, visible):
        theme_collection = self.themeCollection()
        if not theme_collection:
            return

        for theme in theme_collection.mapThemes():
            self.toggleThemeVisibility(theme, layer, visible)

        iface.mapCanvas().refresh()  # Refresh once at the end
