# Layer2Theme


Layer2Theme is a Qgis plugin facilitates updating layer visibility in existing themes. It added 'Append Layer to theme\s' option to the context menu when right clicking on a specific layer in the layer panel, which  a check-box of available themes and layer visibility status for each that can be toggled.

## Features

- Supports all type of layer that can be displayed in Qgis canvas (map space).
- Provides the option to check or uncheck all a layer from available themes.
- Only uses Qgis standard libraries.

<img src="https://github.com/ohmh/QgisLayer2Theme/blob/main/img/Snapshot.png?raw=true" alt="Snapshot" height="500">

## Known issues and limitations
- If active theme is modified it need to be toggled on and off for effect to take place.
- Modifying groups visibility is not accomodated for in this version of the plugin.

## Installation

### Requirements

- QGIS version 3.18 or higher

### Installation through QGIS

1. Open QGIS.
2. Navigate to `Plugins` > `Manage and Install Plugins`.
3. Search for *Layer2Theme*.
4. Click the `Install` button.

### Installation through GitHub

1. Download the ZIP file from this repository.
2. In QGIS, navigate to `Plugins` > `Manage and Install Plugins`.
3. Click `Install from ZIP` and select the downloaded plugin file.

## Contributing

Please report any bugs or feature requests by creating an issue in this GitHub repository.

## Credits and License

AusMap was developed and is maintained by WMS Engineering and is licensed under the GNU General Public License (GPL) v3.0 or later. You are free to use, modify, and distribute this plugin under the terms of the GNU GPL as published by the Free Software Foundation. This plugin is distributed in the hope that it will be useful, but without any warranty. See the [GNU GPL](https://www.gnu.org/licenses/) for more details.

