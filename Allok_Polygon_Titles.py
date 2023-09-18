import csv
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsProject
from PyQt5.QtCore import QVariant
with open("I:\Allok_Geopackage_Project\GIS_Allok_Titles_Project\Land Title QGIS\Group's Land Statement.csv", encoding="utf-8-sig",newline="") as data:
    result=list(csv.reader(data,delimiter=","))
new_result=[]
for i in result:
    new_result.append(list(filter(None, i)))

field_names=["fid","Title No","Title Type","Terms","Title Duration","Title Surveyed Area"] 
layer = QgsVectorLayer("Polygon?crs=epsg:4326", "Allok_Polygon_Titles", "memory")
layer.isValid()

fields=[]
fields.append(QgsField("fid", QVariant.Int))
fields.append(QgsField("Title No", QVariant.String))
fields.append(QgsField("Title Type", QVariant.String))
fields.append(QgsField("Terms", QVariant.Int))
fields.append(QgsField("Title Duration", QVariant.DateTime))
fields.append(QgsField("Title Surveyed Area", QVariant.Double))

layer.startEditing()
layer.dataProvider().addAttributes(fields)

    
