import os
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor
from fontTools.varLib import build

def create_varfont():
    doc = DesignSpaceDocument()

    # Define the weight axis
    weight_axis = AxisDescriptor()
    weight_axis.maximum = 700
    weight_axis.minimum = 400
    weight_axis.default = 400
    weight_axis.name = "weight"
    weight_axis.tag = "wght"
    doc.addAxis(weight_axis)

    # Add Regular Source
    src_reg = SourceDescriptor()
    src_reg.filename = "Elvan_Sans_Output/ElvanSans-Regular.ttf"
    src_reg.name = "Regular"
    src_reg.location = {"weight": 400}
    doc.addSource(src_reg)

    # Add Bold Source
    src_bold = SourceDescriptor()
    src_bold.filename = "Elvan_Sans_Output/ElvanSans-Bold.ttf"
    src_bold.name = "Bold"
    src_bold.location = {"weight": 700}
    doc.addSource(src_bold)

    # Write the designspace file
    doc.write("temp_var.designspace")

    try:
        # Build the variable font
        print("Attempting to build Variable Font...")
        vf, _, _ = build("temp_var.designspace", master_finder=lambda x: x)
        vf.save("Elvan_Sans_Output/ElvanSans-Variable.ttf")
        print("Variable font created successfully!")
    except Exception as e:
        print(f"Failed to create Variable Font. Error: {e}")

if __name__ == "__main__":
    create_varfont()
