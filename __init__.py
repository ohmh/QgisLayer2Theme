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
This script initializes the plugin, making it known to QGIS.
"""
from .main import Layer2ThemePlugin

def classFactory(iface):
    return Layer2ThemePlugin(iface)

__author__ = 'o.h.heba@gmail.com'
__date__ = '2025-07-30'
__copyright__ = 'Copyright 2025, ItOpen'