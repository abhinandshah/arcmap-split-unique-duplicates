# ArcMap Split Unique & Duplicates Toolbox

A simple **ArcMap Python Script Tool** that automatically identifies unique and duplicate values in a selected attribute field and exports them into separate shapefiles.

This tool is useful for **GIS data cleaning, UID validation, cadastral data processing, parcel management, house numbering, and quality control workflows** where duplicate attribute values need to be identified quickly.

---

## ✨ Features

* 🔍 Check any attribute field for repeated values
* 🟢 Extract features with **unique values**
* 🔴 Extract features with **duplicate values**
* 📁 Automatically create the output folder if it does not exist
* 🗂️ Export results as separate Shapefiles
* ⚡ Uses `arcpy.da.SearchCursor` for efficient attribute counting
* 🛡️ Handles text values containing single quotes
* 💻 Designed for **ArcMap / ArcGIS Desktop**

---

## 🛠️ How It Works

The tool follows a simple workflow:

```text
Input Feature Layer
        │
        ▼
Select Attribute Field
        │
        ▼
Count Field Values
        │
        ├───────────────┐
        ▼               ▼
Count = 1          Count > 1
        │               │
        ▼               ▼
Unique Values    Duplicate Values
        │               │
        ▼               ▼
unique_UID.shp   duplicate_UID.shp
```

The script reads the selected field and counts how many times each value appears. Values occurring exactly once are classified as **unique**, while values occurring more than once are classified as **duplicates**.

---

## 📋 Requirements

* **ArcGIS Desktop / ArcMap**
* Python environment compatible with your ArcMap installation
* `arcpy`

The script uses ArcPy functions including:

* `arcpy.GetParameterAsText()`
* `arcpy.da.SearchCursor()`
* `arcpy.Select_analysis()`
* `arcpy.AddMessage()`
* `arcpy.AddWarning()`

---

## 📦 Input Parameters

The Script Tool requires **three parameters**:

| Parameter               | Description                                          |
| ----------------------- | ---------------------------------------------------- |
| **Input Feature Layer** | Feature layer containing the field you want to check |
| **Field**               | Attribute field whose values will be checked         |
| **Output Folder**       | Folder where the output shapefiles will be created   |

The script retrieves these parameters using ArcMap's `GetParameterAsText()` function.

---

## 📤 Output

The tool creates two Shapefiles in the selected output folder:

### 🟢 Unique Features

```text
unique_UID.shp
```

Contains features where the selected field value occurs **exactly once**.

### 🔴 Duplicate Features

```text
duplicate_UID.shp
```

Contains features where the selected field value occurs **more than once**.

The output names and selection logic are defined directly in the script.

---

## 🚀 Installation

### 1. Download the Repository

Clone or download this repository:

```bash
git clone https://github.com/abhinandshah/arcmap-split-unique-duplicates.git
```

Or download the repository as a ZIP file from GitHub.

### 2. Add the Script to ArcMap

Open **ArcMap** and:

```text
ArcToolbox
   ↓
Right Click
   ↓
Add Toolbox
```

Add the toolbox containing the script tool.

### 3. Run the Tool

Open:

```text
ArcToolbox
   ↓
Split Unique & Duplicates
```

Select:

1. Input Feature Layer
2. Field to check
3. Output Folder

Then click **OK**.

---

## 🧪 Example

Suppose your feature layer contains a field called:

```text
House_UID
```

with the following values:

| Feature | House_UID |
| ------: | --------- |
|       1 | H001      |
|       2 | H002      |
|       3 | H003      |
|       4 | H002      |
|       5 | H004      |
|       6 | H005      |
|       7 | H003      |

The tool identifies:

### Unique

```text
H001
H004
H005
```

These features are exported to:

```text
unique_UID.shp
```

### Duplicate

```text
H002
H002
H003
H003
```

All features containing these repeated values are exported to:

```text
duplicate_UID.shp
```

---

## 💡 GIS Use Cases

This tool can be useful for:

### 🏠 House Numbering

Check whether house IDs or house numbers have been assigned more than once.

### 🗺️ Cadastral Mapping

Identify duplicate parcel/kitta identifiers.

### 🌐 GIS Database Cleaning

Find repeated IDs before importing or merging datasets.

### 🏙️ Urban Planning

Validate unique identifiers for buildings, roads, parcels, wards, or other spatial features.

### 📊 Attribute Quality Control

Quickly separate records that require further investigation from records with unique identifiers.

---

## 🔧 Technical Details

The script uses a dictionary to count occurrences of each field value:

```python
uid_count = {}

with arcpy.da.SearchCursor(input_fc, [field_name]) as cursor:
    for row in cursor:
        uid = row[0]

        if uid in uid_count:
            uid_count[uid] += 1
        else:
            uid_count[uid] = 1
```

It then separates the values into two groups:

```python
unique_uids = [
    uid for uid, count in uid_count.items()
    if count == 1
]

duplicate_uids = [
    uid for uid, count in uid_count.items()
    if count > 1
]
```

This logic is implemented in the uploaded script.

---

## 🛡️ SQL Handling

The tool builds an SQL `IN` clause for selecting the matching features.

For text values, single quotes are escaped before constructing the SQL statement:

```python
v.replace("'", "''")
```

This helps the selection query handle text values containing apostrophes.

---

## 📁 Recommended Repository Structure

```text
arcmap-split-unique-duplicates/
│
├── README.md
│
├── toolbox/
│   └── SplitUniqueDuplicates.tbx
│
├── scripts/
│   └── arcmapuniqueanddup.py
│
├── sample/
│   └── sample_data/
│
├── screenshots/
│   └── tool-interface.png
│
└── LICENSE
```

---

## ⚠️ Notes

* The tool produces **Shapefile** outputs.
* Existing outputs may be overwritten because the script enables ArcPy's `overwriteOutput` environment.
* If no unique values are found, the tool reports a warning instead of creating an empty unique output.
* Likewise, if no duplicate values are found, the tool reports a warning.
* The script is intended for the ArcMap/ArcGIS Desktop scripting environment.

---

## 👨‍💻 Author

**Abhinand Shah**

GIS Analyst • GIS & Remote Sensing • WebGIS

### Areas of Interest

* GIS & Spatial Analysis
* Remote Sensing
* WebGIS
* Urban Planning & Land Management
* Drone/UAV Mapping
* GeoAI

---



## 📸 Tool Preview

<div align="center">

<!-- Replace this image with your actual ArcMap toolbox screenshot -->

![Tool Preview](screenshots)

*ArcMap Script Tool — Split Unique & Duplicates*

</div>

> **Screenshot placeholder:**
> Add your ArcMap tool dialog screenshot as:
>
> `screenshots/tool-preview.png`

---

## ⭐ Support

If this tool is useful for your GIS workflow, consider giving the repository a ⭐ on GitHub.

Contributions, suggestions, and improvements are welcome.

---

## 📄 License


[MIT License](LICENSE)

