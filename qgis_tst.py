from qgis.core import Qgis, QgsMapLayerStyleManager
from qgis.PyQt.QtWidgets import QAction, QMenu
from qgis.PyQt.QtCore import QEvent
from qgis.PyQt.QtGui import QCursor
from qgis.core import QgsProject, QgsMapLayer, QgsMapLayerType
from qgis.utils import iface
print(Qgis.QGIS_VERSION)

# theme_collection = QgsProject.instance().mapThemeCollection()
# print("Real type:", type(theme_collection))
# print("Has mapThemeRecord:", hasattr(theme_collection, "mapThemeRecord"))
# print("Methods:", dir(theme_collection))


project = QgsProject.instance()
theme_collection = project.mapThemeCollection()
root = QgsProject.instance().layerTreeRoot()
# #record = QgsMapThemeCollection.MapThemeRecord()
# #record = theme_collection.MapThemeRecord('all')
model = iface.layerTreeView().layerTreeModel()
# mvl = theme_collection.masterVisibleLayers()
# themes = theme_collection.mapThemes()
thm = theme_collection.mapThemeState('osm_bound')
# record = theme_collection.mapThemeRecord(themes[0])
#current_theme = iface.mapCanvas().theme()
#theme_collection.applyTheme(name="osm", root=root, model=model)
layout_manager = QgsProject.instance().layoutManager()