# Land Title Polygon Auto-Drawing Tool

Tech Stack: Python, QGIS API, PyQt5, CSV

Overview

This project automates the creation of polygon layers in QGIS based on land title coordinates and metadata. It reads CSV files containing land title coordinates and details, generates polygons, and enriches them with calculated attributes such as surveyed area, GIS area, duration, and variance.

Features

CSV Integration: Reads coordinate points and land title details from external CSV files.

Polygon Generation: Automatically constructs polygons in QGIS using QgsGeometry and adds them to the project canvas.

Attribute Enrichment: Populates fields such as Title No, Title Type, Terms, Expiry, Surveyed Area, GIS Area, Duration, and Variance.

Automated Calculations:

Computes GIS surveyed area using QGIS expressions.

Calculates title duration based on expiry year.

Determines variance between official surveyed area and GIS‑calculated area.

Layer Management: Adds the generated polygon layer to the QGIS project for visualization and analysis.

Problem Solved

Previously, estate staff had to manually draw polygons and calculate land title attributes in QGIS. This script automates the process, ensuring accuracy and saving significant time.

Impact

Reduced manual GIS work by automating polygon creation.

Improved accuracy in land title area calculations.

Provided clear variance analysis between surveyed and GIS areas.

Enabled faster visualization and reporting for estate land management.
