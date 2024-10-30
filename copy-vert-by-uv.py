bl_info = {
    "name": "Copy Vertices Location by UV Map",
    "author": "Alireza Farzaneh",
    "version": (3, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool",
    "description": "Copies vertices location of one object to another according to their UVs.",
    "warning": "Blender's UI might not respond but it's working. Do not exit, until it's done.",
    "category": "3D View",
    }
    
import bpy
import bmesh
import math
import time
from bpy.types import Panel, Operator
from bpy.props import StringProperty, FloatProperty, PointerProperty
from mathutils import Vector, kdtree

########################## main functions
def main(self, context):
    source = context.scene.cpy_uv_loc_src
    target = context.scene.cpy_uv_loc_trg
    source_uv_name = context.scene.cpy_uv_loc_src_uv_name
    target_uv_name = context.scene.cpy_uv_loc_trg_uv_name
    
    # if both 'Source' and 'Target' objects exists
    if source.name == target.name :
        self.report( {'ERROR_INVALID_INPUT'}, "Can't apply a mesh on itself.")
    else:
        if not objectExists(source.name) or not objectExists(target.name):
            self.report( {'ERROR_INVALID_INPUT'}, "\"" + source.name + "\" or \"" + target.name + "\" doesn't exist!")
        else:
            start_time = time.time()
            compare_uvs(context, source, source_uv_name, target, target_uv_name)
            end_time = time.time()
            self.report({'INFO'}, "Applied locations from \"" + source.name + "\"" + " to " + "\"" + target.name + "\" successfully : "
             + str(end_time - start_time) + " ms.")
    
# Returns boolean if object exists
def objectExists(objectName):
    return bpy.data.objects.find(objectName) != -1

def make_kd_from_uvs(uvs):
    #Create a kd tree
    size = len(uvs)
    kd = kdtree.KDTree(size)
    #Populate it
    for i, uv in enumerate(uvs):
        kd.insert(uv.uv.to_3d(), i) #With 3d coordinates
    #Prepare for querying
    kd.balance()
    return kd
    
def loop_to_vertex_map(obj):
    #Create an array of loop indices to vertex indices
    polygons = obj.data.polygons
    return [v for p in polygons for v in p.vertices]

def compare_uvs(context, src, uv_name1, trg, uv_name2):
    uv_distance_threshold = context.scene.cpy_uv_loc_uv_distance_threshold
    
    #Get uvs for each
    uvs1 = src.data.uv_layers[uv_name1].data
    uvs2 = trg.data.uv_layers[uv_name2].data
    
    #Get maps to look up from loop indices to vertex indices
    map1 = loop_to_vertex_map(src)
    map2 = loop_to_vertex_map(trg)

    #Make a kd tree from the first
    kd = make_kd_from_uvs(uvs1)

    #Loop over the second
    for index2, uv2 in enumerate(uvs2):
        co2 = uv2.uv.to_3d() #With 3d coordinates
        #Query the kd tree
        co1, index1, distance = kd.find(co2)
        uv1 = uvs1[index1]
        
        if distance < uv_distance_threshold:
            v1 = src.data.vertices[map1[index1]]
            #v2 = trg.data.vertices[map2[index2]]
            trg.data.vertices[map2[index2]].co = v1.co
            
            #print(v1.co, v2.co)
            #print(uv1.uv, uv2.uv)

################### End of main functions


## Operator
class Copy_Vert_Loc_By_UV(Operator):
    """Copies Vertices location judging by two objects' UVs"""
    bpy.types.Scene.cpy_uv_loc_src_uv_name = StringProperty(name="Source UV Name", description="The source's UV Name to copy locations from", default="UVMap")
    bpy.types.Scene.cpy_uv_loc_trg_uv_name = StringProperty(name="Target UV Name", description="The target's UV Name to copy locations to", default="UVMap")
    bpy.types.Scene.cpy_uv_loc_src = PointerProperty(name="Source Mesh", type=bpy.types.Object, description="The mesh to copy locations from")
    bpy.types.Scene.cpy_uv_loc_trg = PointerProperty(name="Target Mesh", type=bpy.types.Object, description="The mesh to copy locations to")
    # bpy.types.Scene.source_dup_uv_threshold = FloatProperty(name="Source Duplicate UV Threshold", description="Maximum value used to determine if two uv vertex locations in source uv are referring to the same thing or not (Do not change it most of the time)", min=0.0, default=0.000001)
    bpy.types.Scene.cpy_uv_loc_uv_distance_threshold = FloatProperty(name="UV Distance Threshold", description="Maximum value used to determine if two uv locations of source and target are referring to the same vertex or not (Change it in realy small amount if it can not find two similar uv locations)", min=0.0, default=0.000001)
    bl_idname = "object.copy_vert_loc_by_uv"
    bl_label = "Copies Vertices location by comparing UVs"
    
    def execute(self, context):
        main(self, context)
        return {'FINISHED'}

## UI Panel
class Copy_Vert_Loc_By_UV_Panel(Panel):
    bl_label = "Copy vertices location by UV"
    bl_idname = "PT_CopyVertLocByUV"
    bl_space_type = 'VIEW_3D'
    bl_region_type   = 'UI'
    bl_category = '3D View'

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        
        row = layout.row()
        row.prop(scn, "cpy_uv_loc_src", icon="OBJECT_DATA")
        row = layout.row()
        row.prop(scn, "cpy_uv_loc_src_uv_name", icon="OUTLINER_OB_MESH")
        row = layout.row()
        row.prop(scn, "cpy_uv_loc_trg", icon="MATSPHERE")
        row = layout.row()
        row.prop(scn, "cpy_uv_loc_trg_uv_name", icon="MESH_DATA")
        # row = layout.row()
        # row.prop(scn, "source_dup_uv_threshold")
        row = layout.row()
        row.prop(scn, "cpy_uv_loc_uv_distance_threshold")
        row = layout.row()
        row.operator("object.copy_vert_loc_by_uv", "Do the Magic!", icon="IMPORT")
        row = layout.row()
        row.label("Made by: Alireza Farzaneh", icon="INFO")
        row = layout.row()
        row.operator("wm.url_open",text="AlirezaF's Contact",icon="URL").url='mailto:alirezafarzaneh138@gmail.com'
        

def register():
    bpy.utils.register_class(Copy_Vert_Loc_By_UV)
    bpy.utils.register_class(Copy_Vert_Loc_By_UV_Panel)
    
def unregister():
    bpy.utils.unregister_class(Copy_Vert_Loc_By_UV)
    bpy.utils.unregister_class(Copy_Vert_Loc_By_UV_Panel)
    
if __name__ == "__main__":
    register()
