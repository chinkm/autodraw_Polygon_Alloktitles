import csv
import datetime
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsProject
from PyQt5.QtCore import QVariant

#Read Coordinate Point retrieved from JTUWMA
with open("E:\xxxxx_Geopackage_Project\GIS_xxxxx_Titles_Project\Land Title QGIS\Group's Land Statement.csv", encoding="utf-8-sig",newline="") as data:
    result=list(csv.reader(data,delimiter=","))
new_result=[]
for i in result:
    new_result.append(list(filter(None, i)))

#Read Land Titles' details based on land titles
with open("E:\xxxxx_Geopackage_Project\GIS_xxxxx_Titles_Project\Land Title QGIS\Group's Land Details.csv", encoding="utf-8-sig",newline="") as data1:
    result1=list(csv.reader(data1, delimiter=","))
new_result1=[]
for j in result1:
    new_result1.append(list(filter(None, j)))


field_names=["Title No","Title Type","Terms","Title Duration","Title Surveyed Area"] 
layer = QgsVectorLayer("Polygon?crs=epsg:4326", "Allok_Polygon_Titles", "memory")
layer.isValid()

fields=[]
fields.append(QgsField("Title No", QVariant.String))
fields.append(QgsField("Title Type", QVariant.String))
fields.append(QgsField("Terms", QVariant.Int))
fields.append(QgsField("Title Expiry", QVariant.String))
fields.append(QgsField("Title Duration", QVariant.Int))
fields.append(QgsField("Title Surveyed Area", QVariant.Double))
fields.append(QgsField("GIS Surveyed Area", QVariant.Double))
fields.append(QgsField("Variance Area", QVariant.Double))

layer.startEditing()
layer.dataProvider().addAttributes(fields)
layer.updateFields()

polygon=[]
geometries=[]

#Create point to draw polygon based on new_result
for row in new_result:
    for i in range(0, len(row)-1,2):
        polygon.append(QgsPointXY(float(row[i]),float(row[i+1])))
    geometries.append(QgsGeometry.fromPolygonXY([polygon]))
        
    polygon.clear()

#Draw polygon to canvasmap
for i, geometry in enumerate(geometries):
    feature=QgsFeature()
    feature.setGeometry(geometry)
    layer.dataProvider().addFeatures([feature])

#Add table attributes with values based on new_result1
n=1   
for row1 in layer.getFeatures():
    row1['Title No']=new_result1[n][0]
    row1['Title Type']=new_result1[n][1]
    row1['Terms']=new_result1[n][2]
    row1['Title Expiry']=new_result1[n][3]
    row1['Title Surveyed Area']=new_result1[n][4]
    
    #Fill Other columns with expressions in attribute table
    expression1= QgsExpression('round($area * 0.000247,2)')
    expression2=QgsExpression('to_int(right("Title Expiry",4))- to_int(left(now(),4))')
    context=QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
    context.setFeature(row1)
    row1['GIS Surveyed Area']=expression1.evaluate(context)
    row1['Title Duration']=expression2.evaluate(context)
    
                        
    layer.updateFeature(row1)
    n+=1
    
layer.commitChanges()

QgsProject.instance().addMapLayer(layer)

#Update/Edit field ["Variance Area"] caused it could not direct input expression from QgsExpression
with edit(layer):
    for row1 in layer.getFeatures():
        row1["Variance Area"]=round(row1["Title Surveyed Area"] - row1["GIS Surveyed Area"],2)
        layer.updateFeature(row1)
        
layer.commitChanges()

QgsProject.instance().addMapLayer(layer)

'''
data_list = []
for field in layer.fields():
    field_name = field.name()
    field_type = field.typeName()

    data = field_name, field_type
    data_list.append(data)    
    
print(data_list)
'''        




    
