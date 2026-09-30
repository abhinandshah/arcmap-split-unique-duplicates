import arcpy
import os

def build_sql_clause(field, values):
    """Builds an SQL WHERE clause for the Select tool."""
    clauses = []
    for v in values:
        if isinstance(v, basestring):
            clauses.append("'{}'".format(v.replace("'", "''")))  # escape single quotes
        else:
            clauses.append(str(v))
    return "{} IN ({})".format(arcpy.AddFieldDelimiters(None, field), ",".join(clauses))

def main():
    arcpy.env.overwriteOutput = True

    # Script tool parameters
    input_fc = arcpy.GetParameterAsText(0)       # Feature layer
    field_name = arcpy.GetParameterAsText(1)     # UID field
    output_folder = arcpy.GetParameterAsText(2)  # Folder for outputs

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        arcpy.AddMessage("Output folder created: {}".format(output_folder))

    # Count UID values
    uid_count = {}
    with arcpy.da.SearchCursor(input_fc, [field_name]) as cursor:
        for row in cursor:
            uid = row[0]
            if uid in uid_count:
                uid_count[uid] += 1
            else:
                uid_count[uid] = 1

    # Separate UIDs
    unique_uids = [uid for uid, count in uid_count.items() if count == 1]
    duplicate_uids = [uid for uid, count in uid_count.items() if count > 1]

    # Output shapefile paths
    unique_out = os.path.join(output_folder, "unique_UID.shp")
    duplicate_out = os.path.join(output_folder, "duplicate_UID.shp")

    # Export unique features
    if unique_uids:
        where_unique = build_sql_clause(field_name, unique_uids)
        arcpy.AddMessage("Selecting unique features...")
        arcpy.Select_analysis(input_fc, unique_out, where_unique)
        arcpy.AddMessage("Unique features saved to: {}".format(unique_out))
    else:
        arcpy.AddWarning("No unique UID values found.")

    # Export duplicate features
    if duplicate_uids:
        where_duplicate = build_sql_clause(field_name, duplicate_uids)
        arcpy.AddMessage("Selecting duplicate features...")
        arcpy.Select_analysis(input_fc, duplicate_out, where_duplicate)
        arcpy.AddMessage("Duplicate features saved to: {}".format(duplicate_out))
    else:
        arcpy.AddWarning("No duplicate UID values found.")

# ArcMap requires this for script tools
if __name__ == '__main__':
    main()
