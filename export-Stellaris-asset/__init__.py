import bpy
from bpy.types import Panel, Operator

bl_info = {
    "name": "Stellaris .asset Exporter",
    "category": "Import-Export",
    "author": "Oninoni (oninoni@oninoni.de), Dayshine",
    "version": (0, 0, 2),
    "blender": (2, 73, 0),
    "support": "COMMUNITY"
}

def createLocator(object):
    data = "locator = {name=\"" + object.name + "\" "
    data += "position={"
    data += '%.10f' % object.location[0]
    data += " "
    data += '%.10f' % object.location[1]
    data += " "
    data += '%.10f' % object.location[2]
    data += "} rotation={"
    data += '%.10f' % object.rotation_euler[0]
    data += " "
    data += '%.10f' % object.rotation_euler[1]
    data += " "
    data += '%.10f' % object.rotation_euler[2]
    data += "}}"
    
    return data

def createAttach(object):
    return "attach = {" + object.name + "=\"YouNeedToAddTheMeshHere\"}"

def main(context):
    selected = context.object
    others = context.visible_objects
    
    print("Main: \"" + selected.name + "\"")
    
    print(bpy.path.abspath("//") + "\STH_" + selected.name + ".asset")
    assetFile = open(bpy.path.abspath("//") + "STH_" + selected.name + ".asset","w")
    assetFile.write("# Created by the .asset-Creator v0.0.2 written by Oninoni (oninoni@oninoni.de) and edited by Dayshine for Star Trek New Horizon\n\n")
    
    for object in others:
        print(object.type)
        if(object.type == 'MESH' or object.type == "EMPTY"):
            if(selected == object):
                continue
            print("Sub: \"" + object.name + "\"")
            print(createLocator(object))
            assetFile.write(createLocator(object) + "\n")
            print(createAttach(object))
            assetFile.write(createAttach(object) + "\n\n")
        
    assetFile.close()

class AssetExporterOperator(Operator):
    """Tooltip"""
    bl_idname = "object.asset_export"
    bl_label = ".asset Exporter Operator"
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        main(context)
        return {'FINISHED'}

class ClausewitzAssetExporterPanel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Clausewitz Model Exporter'
    bl_context = 'objectmode'
    bl_category = 'Exporter'
    
    #Add UI elements here
    def draw(self, context):
        layout = self.layout
        layout.row().label('To export select the MAIN Object!')
        layout.row().label('Currently Selected: ' + context.object.name)
        
        layout.operator('object.asset_export', text='Export!')
        

#Register
def register():
    bpy.utils.register_class(AssetExporterOperator)
    bpy.utils.register_class(ClausewitzAssetExporterPanel)

#Unregister
def unregister():
    bpy.utils.unregister_class(AssetExporterOperator)
    bpy.utils.unregister_class(ClausewitzAssetExporterPanel)

# Needed to run script in Text Editor
if __name__ == '__main__':
    register()