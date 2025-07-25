from qgis.PyQt.QtWidgets import QAction, QMenu
from qgis.PyQt.QtCore import QEvent
from qgis.PyQt.QtGui import QCursor
from qgis.core import QgsProject, QgsMapLayer
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
        self.theme_collection = self.project.mapThemeCollection()
        self.themes = self.theme_collection.mapThemes()

    def initGui(self):
        # For Vector Layers
        action_vector = QAction("Append layer to theme/s", self.iface.mainWindow())
        # Use StayOpenMenu instead of QMenu.
        menu_vector = StayOpenMenu()
        # Rebuild the menu each time it's about to show.
        menu_vector.aboutToShow.connect(lambda: self.updateMenu(menu_vector))
        # Set to pop up on hover.
        action_vector.setMenu(menu_vector)
        self.iface.addCustomActionForLayerType(action_vector, None, QgsMapLayer.VectorLayer, True)
        self.actions.append(action_vector)

        # For Raster Layers (repeat same process)
        action_raster = QAction("Append layer to theme/s", self.iface.mainWindow())
        menu_raster = StayOpenMenu()
        menu_raster.aboutToShow.connect(lambda: self.updateMenu(menu_raster))
        action_raster.setMenu(menu_raster)
        self.iface.addCustomActionForLayerType(action_raster, None, QgsMapLayer.RasterLayer, True)
        self.actions.append(action_raster)

    def updateMenu(self, menu):
        menu.clear()
        layer = iface.activeLayer()
        if not layer:
            return

        themes = self.themes
        # Create a checkable action per theme.
        for theme in themes:
            act = QAction(theme, menu)
            act.setCheckable(True)
            visible_ids = self.theme_collection.mapThemeVisibleLayerIds(theme)
            act.setChecked(layer.id() in visible_ids)
            act.toggled.connect(lambda checked, t=theme, lyr=layer: self.toggleThemeVisibility(t, layer=lyr, visible=checked))
            menu.addAction(act)

        menu.addSeparator()

        check_all = QAction("Check all", menu)
        check_all.triggered.connect(lambda lyr=layer: self.setAllThemes(layer=lyr, visible=True))
        menu.addAction(check_all)

        uncheck_all = QAction("Uncheck all", menu)
        uncheck_all.triggered.connect(lambda lyr=layer: self.setAllThemes(layer=lyr, visible=False))
        menu.addAction(uncheck_all)

    def toggleThemeVisibility(self, theme_name, layer, visible):
        theme_collection = self.theme_collection
        layer_record = theme_collection.MapThemeLayerRecord(layer)
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


    def setAllThemes(self, layer, visible):
        for theme in self.theme_collection.mapThemes():
            self.toggleThemeVisibility(theme, layer, visible)

    def unload(self):
        # Remove the custom actions when the plugin is unloaded.
        for action in self.actions:
            self.iface.removeCustomActionForLayerType(action)
        self.actions = []