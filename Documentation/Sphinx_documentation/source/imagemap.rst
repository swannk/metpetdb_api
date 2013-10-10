====================
MetPetDB Image Map
====================

The MetPetDB Image Map is used to display petrologic image samples with slice and data overlays. It is built on the OpenLayers framework. 

***************
Key Terms
***************
.. image:: http://micmoo.org/uiexample.jpg

Map
	The main canvas that the images are displayed on. Contains the BaseLayer.

ImageLayer
	Contains Individual Images. Properties: opacity, z-index, bounds, size, name, scale, data, zoomLevels

BaseLayer
	Main image that all other images are displayed relative to. Of type ImageLayer

ZoomLevel
	Maximum zooms. It is possible for the BaseLayer can have a different number than other Images.

Opacity
	(float) 0.0 (not visible) to 1.0 (fully visible).

Z-index
	(int) Stacking order. The ImageLayer with the highest z-index is displayed on top.

Bounds/Extent
	(float left, float bottom, float right, float left) Distance from the origin. Bounds is dependent on the BaseLayer size. The bounds of the BaseLayer are (-0.5 * width, -0.5 * height, 0.5 * width, 0.5 * height)

Size
	(float width, float height) Size of image when all the way zoomed out.

Scale
	(float) Real-world size of image. Displayed in the scale marker on bottom left. 

Lon/Lat
	Position Left/Bottom on the BaseLayer

Data
	Data about a specified image. Includes notes/descriptions etc

LayerSwitcher
	Turn on and off specific layers. Drag layers up and down to change z-index. Also can be used to adjust opacity

Feature
	Instead of preloading and displaying a grouping of images that would be too small to see at the current zoom level and feature can be used instead. It is the equivalent of a thumbnail for a layer or group of layers. When clicked, the map loads and zooms directly to the images. The feature is then removed and the layers are added to the layerSwitcher

Marker
	The user clicks on a point on the map and is able to mark it with a point to store data about that point. Position is stored as bounds. Of type Feature.

Polygon
	User drawable polygon. Used to associate data with a particular region of the Map. Of type feature.

***************
Functions
***************

Pan/Zoom
	The default action is to pan across the map by clicking and dragging. A double click zooms in. Scroll Wheel and the bottoms on the top left can also be used to zoom.

Add Image
	To add an image, the user first selects the add image tool and then draws a shape on the Map. They are then prompted to upload an image or supply a URL along with a name for the layer. Optional parameters include opacity, z-index, data, scale. 

Delete Image
	Deletes Image from map. Users must select the delete tool.
Move
	Allows user to move and drag images, shapes and data points freely on the map. 

Add Feature
	First click on the add feature tool. Then chooses a shape for the feature. The user is then prompted to upload a thumbnail and it is placed at the specified location. When the user adds an image, as long as he is within the bounds of the feature, he is given the option to “add to feature” and choose the feature from the list. When the user clicks the feature, he is then brought to the maximum zoom level that can accommodate all of the images in the feature. Note the following example:User Bob has three high resolution samples of a very small portion of the very large BaseImage. They are too small to be seen at the default zoom level and he does not want them to be loaded every time the ImageMap is loaded. He therefore draws a box around the small area that the sample is taken from and uploads a thumbnail. He then zooms as far as he desires into this box and uses the Add Image tool to upload a photo. Since he is in the feature bounds, he is prompted to add the image to the feature. If he chooses yes, the image will not be loaded until the feature is clicked on. Once the feature is clicked on the map zooms directly to the sample and the sample is added to the LayerSwitcher.Right 

Click
	Opacity, z-index and Data editing. Brings up popup to change layer settings. Right click works on ImageLayers, Features, Data Points and Polygons. 

LayerSwitcher
	Turn on and off specific layers. Drag layers up and down to change z-index. Also can be used to adjust opacity. 

Save
	Saves ImageMap state either locally or to the database.



***************
Data Model
***************

The data is saved in GeoJSON format. This allows easy handling via Javascript and easy storage in a database as well as simple state restoring. 

ImageLayer
 ``{"type":"Image","zIndex":4,"visibility":true,"name":"moo","opacity":0.9,"metadata":{"data1":"mydata"},"isBaseLayer":false,"extent":{"left":90,"bottom":-104,"right":224,"top":10},"size":{"w":134,"h":114},"numZoomLevels":16}``

If isBaseLayer = true, then this is the BaseLayer. Thus the extent stored here is the extent of the whole map. 

Feature
 ``{"type":"Feature","properties":{"data":"awesomeData","data2":"awesomerdata","sublayers":["a","b","c"],"externalGraphic":"img/small.jpg","graphicHeight":21,"graphicWidth":16},"geometry":{"type":"Point","coordinates":[0,0]},"crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}}}`` 

This allows custom data fields, which are specified in the first “properties” field. Included in this is the name of the sublayers that will be loaded when the feature is clicked. The coordinates are the lon/lat of the image. The externalGraphic is a link to the thumbnail, along with it’s size.


**Data Point**
	``{"type":"Feature","properties":{"data":"somedata"},"geometry":{"type":"Point","coordinates":[17,-64]},"crs":{"type":"name","":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}}}``	

Polygon
 ``{“type":"Feature","properties":{"data":"somedata"},"geometry":{"type":"Polygon","coordinates":[[[77,86],[-72,-3],[105,-64],[248,32],[77,86]]]},"crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}}}``