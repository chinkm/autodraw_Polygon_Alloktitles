import csv
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsProject
from PyQt5.QtCore import QVariant

#Read Coordinate Point retrieved from JTUWMA
with open("I:\Allok_Geopackage_Project\GIS_Allok_Titles_Project\Land Title QGIS\Group's Land Statement.csv", encoding="utf-8-sig",newline="") as data:
    result=list(csv.reader(data,delimiter=","))
new_result=[]
for i in result:
    new_result.append(list(filter(None, i)))

#Read Land Titles' details 
with open("I:\Allok_Geopackage_Project\GIS_Allok_Titles_Project\Land Title QGIS\Group's Land Details.csv", encoding="utf-8-sig",newline="") as data1:
    result1=list(csv.reader(data, delimiter=","))
new_result1=[]
for j in result1:
    new_result1.append(list(filter(None, j)))


field_names=["fid","Title No","Title Type","Terms","Title Duration","Title Surveyed Area"] 
layer = QgsVectorLayer("Polygon?crs=epsg:4326", "Allok_Polygon_Titles", "memory")
layer.isValid()

fields=[]
fields.append(QgsField("Title No", QVariant.String))
fields.append(QgsField("Title Type", QVariant.String))
fields.append(QgsField("Terms", QVariant.Int))
fields.append(QgsField("Title Duration", QVariant.DateTime))
fields.append(QgsField("Title Surveyed Area", QVariant.Double))

layer.startEditing()
layer.dataProvider().addAttributes(fields)
layer.updateFields()

polygon=[]
geometries=[]

for row in new_result:
    for i in range(0, len(row)-1,2):
        polygon.append(QgsPointXY(float(row[i]),float(row[i+1])))
    geometries.append(QgsGeometry.fromPolygonXY([polygon]))
        
    polygon.clear()
    
    
for i, geometry in enumerate(geometries):
    feature=QgsFeature()
    feature.setGeometry(geometry)
    layer.dataProvider().addFeatures([feature])

layer.commitChanges()

QgsProject.instance().addMapLayer(layer)

    
        




    
