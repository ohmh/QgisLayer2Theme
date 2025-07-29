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
        self.iface = iface
        self.actions = []
        self.project = QgsProject.instance()
        self.layers = self.project.mapLayers()
        self.layer = iface.activeLayer()
        self.theme_collection = self.project.mapThemeCollection()
        self.themes = self.theme_collection.mapThemes()

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
        layer = self.layer
        if not layer:
            return

        themes = self.themes
        # Create a checkable action per theme.
        for theme in themes:
            act = QAction(theme, menu)
            act.setCheckable(True)
            visible_ids = self.theme_collection.mapThemeVisibleLayerIds(theme)
            act.setChecked(layer.id() in visible_ids)
            act.toggled.connect(lambda checked, t=theme: self.toggleThemeVisibility(t, visible=checked))
            menu.addAction(act)

        menu.addSeparator()

        check_all = QAction("Check all", menu)
        check_all.triggered.connect(lambda _: self.setAllThemes(visible=True))
        menu.addAction(check_all)

        uncheck_all = QAction("Uncheck all", menu)
        uncheck_all.triggered.connect(lambda _: self.setAllThemes(visible= False))
        menu.addAction(uncheck_all)

    def toggleThemeVisibility(self, theme_name, visible):
        iface.messageBar().pushMessage("Visibility", str(visible ), level=Qgis.Info)   
        layer = self.layer
        theme_collection = self.theme_collection
        layer_record = QgsMapThemeCollection.MapThemeLayerRecord(self.layer)
        theme_record = theme_collection.mapThemeState(theme_name)
        current_ids = list(theme_collection.mapThemeVisibleLayerIds(theme_name))
        if visible and layer.id() not in current_ids:
            theme_record.addLayerRecord(layer_record)
            theme_collection.update(theme_name, theme_record)
            theme_collection.mapThemesChanged
            iface.mapCanvas().refresh()  # Refresh the map canvas to reflect changes
            # iface.mapCanvas().refreshAllLayers()
            current_ids.append(layer.id())
        elif not visible and layer.id() in current_ids:
            theme_record.removeLayerRecord(layer)
            theme_collection.update(theme_name, theme_record)
            theme_collection.mapThemesChanged
            iface.mapCanvas().refresh()  # Refresh the map canvas to reflect changes
            # iface.mapCanvas().refreshAllLayers()
            current_ids.remove(layer.id())
        #theme_collection.setMapThemeVisibleLayerIds(theme_name, current_ids) # There is no setMapThemeVisibleLayer method in QGIS API, and this is a method that returns a list so we can't equate it to a list to resolve the issue


    def setAllThemes(self, visible):
        for theme in self.themes:
            self.toggleThemeVisibility(theme_name=theme, visible=visible)

    def unload(self):
        # Remove the custom actions when the plugin is unloaded.
        for action in self.actions:
            self.iface.removeCustomActionForLayerType(action)
        self.actions = []