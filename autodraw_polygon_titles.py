import csv
import datetime
import os
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsProject, QgsExpression, QgsExpressionContext, QgsExpressionContextUtils
from PyQt5.QtCore import QVariant

# Uses clean project-relative asset indexing paths instead of rigid drive names
base_data_path = os.path.join("data")
statement_csv = os.path.join(base_data_path, "Land_Statement.csv")
details_csv = os.path.join(base_data_path, "Land_Details.csv")

if not os.path.exists(statement_csv) or not os.path.exists(details_csv):
    print("Please place the target CSV source sheets inside the relative /data folder path container.")
    sys.exit(1)

with open(statement_csv, encoding="utf-8-sig", newline="") as data:
    result = list(csv.reader(data, delimiter=","))

new_result = []
for i in result:
    new_result.append(list(filter(None, i)))

with open(details_csv, encoding="utf-8-sig", newline="") as data1:
    result1 = list(csv.reader(data1, delimiter=","))
    
new_result1 = []
for j in result1:
    new_result1.append(list(filter(None, j)))

field_names = ["Title No", "Title Type", "Terms", "Title Duration", "Title Surveyed Area"] 
layer = QgsVectorLayer("Polygon?crs=epsg:4326", "Operational_Polygon_Title_Layer", "memory")

fields = [
    QgsField("Title No", QVariant.String),
    QgsField("Title Type", QVariant.String),
    QgsField("Terms", QVariant.Int),
    QgsField("Title Expiry", QVariant.String),
    QgsField("Title Duration", QVariant.Int),
    QgsField("Title Surveyed Area", QVariant.Double),
    QgsField("GIS Surveyed Area", QVariant.Double),
    QgsField("Variance Area", QVariant.Double)
]

layer.startEditing()
layer.dataProvider().addAttributes(fields)
layer.updateFields()

polygon = []
geometries = []

for row in new_result:
    for i in range(0, len(row) - 1, 2):
        polygon.append(QgsPointXY(float(row[i]), float(row[i+1])))
    geometries.append(QgsGeometry.fromPolygonXY([polygon]))
    polygon.clear()

for geometry in geometries:
    feature = QgsFeature()
    feature.setGeometry(geometry)
    layer.dataProvider().addFeatures([feature])

n = 1   
for row1 in layer.getFeatures():
    row1['Title No'] = new_result1[n][0]
    row1['Title Type'] = new_result1[n][1]
    row1['Terms'] = new_result1[n][2]
    row1['Title Expiry'] = new_result1[n][3]
    row1['Title Surveyed Area'] = new_result1[n][4]
    
    expression1 = QgsExpression('round($area * 0.000247,2)')
    expression2 = QgsExpression('to_int(right("Title Expiry",4))- to_int(left(now(),4))')
    
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
    context.setFeature(row1)
    
    row1['GIS Surveyed Area'] = expression1.evaluate(context)
    row1['Title Duration'] = expression2.evaluate(context)
    
    layer.updateFeature(row1)
    n += 1
    
layer.commitChanges()
QgsProject.instance().addMapLayer(layer)

layer.startEditing()
for row1 in layer.getFeatures():
    row1["Variance Area"] = round(row1["Title Surveyed Area"] - row1["GIS Surveyed Area"], 2)
    layer.updateFeature(row1)
        
layer.commitChanges()
QgsProject.instance().addMapLayer(layer)
