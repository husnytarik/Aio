from bpy_extras import image_utils
from bpy.props import EnumProperty
from bpy.types import Panel
from PIL import Image
import bmesh
import bpy
import os
import sys
import subprocess
bl_info = {
    "name": "AIO",
    "author": "HusnyTarik",
    "version": (1, 0),
    "blender": (3, 5, 1),
    "location": "View3D > N-Panel",
    "description": "Optimization is easy!",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
}

#


# path to python.exe
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')

# upgrade pip
subprocess.call([python_exe, "-m", "ensurepip"])
subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

# install required packages
subprocess.call([python_exe, "-m", "pip", "install", "Pillow"])

print("DONE")

##

# Panel


class AIOPanel(bpy.types.Panel):
    bl_label = "AIO"
    bl_idname = "TEXTURE_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AIO"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Apply Transform
        box = layout.box()
        box.label(text="Apply Transform")
        row = box.row(align=True)
        # Location Check
        row.operator("object.apply_location_operator", text="Location")
        # Rotation Check
        row.operator("object.apply_rotation_operator", text="Rotation")
        # Scale Check
        row.operator("object.apply_scale_operator", text="Scale")
        # All Check
        row.operator("object.apply_all_operator", text="All")

        # Set Origin
        # Options Dropdown
        box = layout.box()
        box.label(text="Set Origin")
        row = box.row()
        row.label(text="Options:")
        row = box.row()
        row.prop(context.scene, "vertex_position_option", expand=True)
        # Button
        row = box.row()
        row.operator("object.set_origin", text="Origin Noktasını Ayarla")

        # Mesh Optimization
        layout.separator()
        box = layout.box()
        box.label(text="Mesh Optimization")
        row = box.row(align=True)
        # Remove Unconnected Vertices
        row.operator("object.remove_unconnected_vertices",
                     text="Remove Unconnected Vertices")
        # Merge By Distance
        box.operator("object.merge_by_distance")
        # Recalculate Normals
        box.operator("object.recalculate_normals", text="Recalculate Normals")
        # Triangulate Faces
        box.operator("object.triangulate_faces")
        # Smart Uv Project
        box.operator("object.smart_uv_project")

        # Object Naming
        layout.separator()
        box = layout.box()
        box.label(text="Naming Object & Mesh")

        # Rename
        col = box.column()
        col.label(text="Rename:")
        col.prop(context.scene, "new_name", text="")
        col.operator("object.rename_objects", text="Apply Rename")

        # Prefix
        col = box.column()
        col.label(text="Enter the prefix:")
        row = col.row(align=False)
        row.prop(context.scene, "custom_prefix", text="")
        # Button
        row.operator("object.add_prefix_operator")
        # Suffix
        col = box.column()
        col.label(text="Enter the suffix:")
        row = col.row(align=False)
        row.prop(context.scene, "custom_suffix", text="")
        # Button
        row.operator("object.add_suffix_operator")

        # UV Rename
        layout.separator()
        box = layout.box()
        box.label(text="Naming Uv")
        obj = context.object
        if obj:
            # UV Maps Dropdown List
            box.prop(obj, "selected_uv_map", text="UV Map")
            # UV Map Name Change
            row = box.row()
            row.prop(obj, "new_uv_map_name", text="New Name")
            row.operator("object.rename_uv_map", text="Rename UV Map")

        # Texture Size Reduce
        layout.separator()
        box = layout.box()
        box.label(text="Texture Optimization")
        # All Textures
        textures = bpy.data.images
        # Texture Select Dropdown
        box.label(text="Select Texture:")
        box.prop(scene, "selected_texture", text="")
        # Size and Quality
        box.label(text="Image Settings:")
        row = box.row(align=True)
        row.prop(scene, "new_width", text="Width")
        row.prop(scene, "new_height", text="Height")
        box.prop(scene, "quality", text="Quality")
        # Output name
        box.prop(context.scene, "newName", text="Output Name")
        # Extension name
        box.prop(scene, "selected_extension", text="Extension")

        # Resize File Size Button
        box.separator()
        box.operator("texture.reduce_size_operator", text="Reduce Image Size")
        # Selected Texture Infos
        if scene.selected_texture:
            texture = textures.get(scene.selected_texture)
            if texture:
                box.label(text="Texture Details:")
                box.label(text="Name: " + texture.name)
                box.label(text="Type: " + texture.type)
                box.label(text="Resolution: " +
                          str(texture.size[0]) + " x " + str(texture.size[1]))
                box.label(text="Path: " + texture.filepath)
            else:
                box.label(text="Texture not found.")

        # Texture Prefix & Suffix
        layout.separator()
        box = layout.box()
        box.label(text="Set Prefix & Suffix for Linked Textures")
        # Material Select Dropdown
        box.prop(scene, "selected_material", text="Material")
        # Checkbox List
        row = box.row(align=True)
        box.label(text="Linked to:")
        row.prop(scene, "selected_base_color", text="Base Color")
        row.prop(scene, "selected_metallic", text="Metallic")
        row.prop(scene, "selected_roughness", text="Roughness")
        row.prop(scene, "selected_emission", text="Emission")
        row.prop(scene, "selected_normal", text="Normal")
        row = box.row(align=False)
        row.prop(scene, "prefix", text="Prefix")
        row.prop(scene, "suffix", text="Suffix")
        # Button
        box.operator("object.add_prefix_suffix_operator",
                     text="Apply Prefix&Suffix")

##

# Apply Transform
# Apply Location


class ApplyLocationOperator(bpy.types.Operator):
    bl_idname = "object.apply_location_operator"
    bl_label = "Apply Location"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            bpy.ops.object.transform_apply(
                location=True, rotation=False, scale=False)

        return {'FINISHED'}

# Apply Rotation


class ApplyRotationOperator(bpy.types.Operator):
    bl_idname = "object.apply_rotation_operator"
    bl_label = "Apply Rotation"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            bpy.ops.object.transform_apply(
                location=False, rotation=True, scale=False)

        return {'FINISHED'}

# Apply Scale


class ApplyScaleOperator(bpy.types.Operator):
    bl_idname = "object.apply_scale_operator"
    bl_label = "Apply Scale"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)

        return {'FINISHED'}

# Apply All


class ApplyAllOperator(bpy.types.Operator):
    bl_idname = "object.apply_all_operator"
    bl_label = "Apply All"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            bpy.ops.object.transform_apply(
                location=True, rotation=True, scale=True)

        return {'FINISHED'}

##

# Set Origin
# Origin Operation


class OBJECT_OT_SetOrigin(bpy.types.Operator):
    bl_idname = "object.set_origin"
    bl_label = "Set Origin"

    def execute(self, context):
        # Selected Obj
        obj = bpy.context.active_object
        if obj is None:
            self.report({'ERROR'}, "No object is selected.")
            return {'CANCELLED'}
        if obj.type != 'MESH':
            self.report({'ERROR'}, "The selected object is not a Mesh object.")
            return {'CANCELLED'}

        # Setting origin options
        option = context.scene.vertex_position_option
        if option == 'BOUNDING_BOX':
            bpy.ops.object.origin_set(
                type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
        elif option == '3D_CURSOR':
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        elif option == 'BOTTOM':
            bpy.ops.object.origin_set(
                type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
            # Lowest vertex z location
            lowest_z = float('inf')
            for vertex in obj.data.vertices:
                if vertex.co.z < lowest_z:
                    lowest_z = vertex.co.z
            # Edit Mode
            bpy.ops.object.mode_set(mode='EDIT')
            # Select All
            bpy.ops.mesh.select_all(action='SELECT')
            # Translate Z
            bpy.ops.transform.translate(
                value=(0, 0, -lowest_z), orient_type='GLOBAL')
            # Exit edit mode
            bpy.ops.object.mode_set(mode='OBJECT')
            print("LOWEST Z:", lowest_z)
        return {'FINISHED'}


# Options Hodler
bpy.types.Scene.vertex_position_option = bpy.props.EnumProperty(
    name="Vertex Position",
    description="Select vertex position option",
    items=[
        ("BOUNDING_BOX", "Bounding Box", ""),
        ("3D_CURSOR", "3D Cursor", ""),
        ("BOTTOM", "Bottom", "")
    ]
)

##

# Remove Unused Vertices


class RemoveUnconnectedVerticesOperator(bpy.types.Operator):
    bl_idname = "object.remove_unconnected_vertices"
    bl_label = "Remove Unconnected Vertices"
    bl_description = "Removes vertices with no connections using limit dissolve"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        # Clear selected
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get active object
        obj = context.active_object

        # Select All
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        # Remove unconnected vertices
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_non_manifold()
        bpy.ops.mesh.dissolve_limited()

        # Deselect all & Object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}

##

# Merge By Distance


class MergeByDistanceOperator(bpy.types.Operator):
    bl_idname = "object.merge_by_distance"
    bl_label = "Merge by Distance"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) == 0 or selected_objects[0].type != 'MESH':
            self.report({'WARNING'}, "Please select a mesh object.")
            return {'CANCELLED'}

        active_object = bpy.context.active_object
        if active_object is None or active_object.type != 'MESH':
            self.report({'WARNING'}, "Please set an active mesh object.")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, "Mege by Distance Done.")
        return {'FINISHED'}

##

# Recalculate Normals


class OBJECT_OT_RecalculateNormals(bpy.types.Operator):
    bl_idname = "object.recalculate_normals"
    bl_label = "Recalculate Normals"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        if not selected_objects:
            self.report({'INFO'}, "No object selected.")
            return {'CANCELLED'}

        for obj in selected_objects:
            if obj.type != 'MESH':
                self.report({'WARNING'}, "Selected object is not a mesh.")
                return {'CANCELLED'}

            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')
            self.report({'INFO'}, "Normals Recalculated")
        return {'FINISHED'}

##

# Triangulate Faces


class TriangulateFacesOperator(bpy.types.Operator):
    bl_idname = "object.triangulate_faces"
    bl_label = "Triangulate Faces"

    def execute(self, context):
        obj = context.object

        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Selected object is not a mesh.")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Triangulate Faces Done")
        return {'FINISHED'}

##

# Smart Uv Projection


class SmartUVProjectOperator(bpy.types.Operator):
    bl_idname = "object.smart_uv_project"
    bl_label = "Smart UV Project"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def invoke(self, context, event):
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) == 0 or selected_objects[0].type != 'MESH':
            self.report({'WARNING'}, "Please select a mesh object.")
            return {'CANCELLED'}

        active_object = bpy.context.active_object
        if active_object is None or active_object.type != 'MESH':
            self.report({'WARNING'}, "Please set an active mesh object.")
            return {'CANCELLED'}

        obj = context.object

        if obj.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.uv.smart_project(margin_method='SCALED', angle_limit=1.15192,
                                 island_margin=0.000, area_weight=0.000, correct_aspect=True)

        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, "Smart Uv Project Done.")

        return {'FINISHED'}

##

# Rename


class RenameObjectsOperator(bpy.types.Operator):
    bl_idname = "object.rename_objects"
    bl_label = "Rename"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        new_name = bpy.context.scene.new_name

        for obj in selected_objects:
            obj.name = new_name
            if obj.type == 'MESH':
                obj.data.name = new_name

        return {'FINISHED'}


# Set Prefix


class AddPrefixOperator(bpy.types.Operator):
    bl_idname = "object.add_prefix_operator"
    bl_label = "Add Prefix"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            if obj.type == 'MESH':
                obj.name = context.scene.custom_prefix + obj.name
                mesh = obj.data
                mesh.name = context.scene.custom_prefix + mesh.name

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

##

# Set Suffix


class AddSuffixOperator(bpy.types.Operator):
    bl_idname = "object.add_suffix_operator"
    bl_label = "Add Suffix"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            if obj.type == 'MESH':
                obj.name = obj.name + "_" + context.scene.custom_suffix
                mesh = obj.data
                mesh.name = mesh.name + "_" + context.scene.custom_suffix

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

##

# UV-Rename
# UV maps list


def get_uv_maps(self, context):
    obj = context.object
    uv_maps = []

    if obj and obj.type == 'MESH':
        mesh = obj.data
        for uv_map in mesh.uv_layers:
            uv_maps.append((uv_map.name, uv_map.name, ""))

    return uv_maps

# UV Rename


class OBJECT_OT_RenameUVMap(bpy.types.Operator):
    bl_idname = "object.rename_uv_map"
    bl_label = "Rename UV Map"

    def execute(self, context):
        obj = context.object
        uv_map_name = obj.selected_uv_map
        new_uv_map_name = obj.new_uv_map_name

        if uv_map_name and new_uv_map_name:
            mesh = obj.data
            uv_map = mesh.uv_layers.get(uv_map_name)

            if uv_map:
                uv_map.name = new_uv_map_name

        return {'FINISHED'}

##


# Reduce Image Size
# Extensions
extension_items = [
    (".jpg", "JPEG", ""),
    (".png", "PNG", ""),
    (".tiff", "TIFF", "")
]

# Operator


class ReduceSizeOperator(bpy.types.Operator):
    bl_idname = "texture.reduce_size_operator"
    bl_label = "Reduce Image Size"

    def execute(self, context):
        scene = context.scene
        selected_texture = scene.selected_texture

        if selected_texture:
            texture = bpy.data.images.get(selected_texture)
            if texture:
                # Get new sizes
                new_width = scene.new_width
                new_height = scene.new_height
                # Get quality
                quality = scene.quality

                # New file path file name
                old_filepath = texture.filepath
                directory = os.path.dirname(old_filepath)
                filename = os.path.splitext(old_filepath)
                ext = scene.selected_extension
                newName = scene.newName
                new_filepath = os.path.join(directory, newName + ext)

                # Resize file size
                reduce_image_size(old_filepath, new_filepath,
                                  new_width, new_height, quality)

                self.report({'INFO'}, "Image size reduced successfully.")
            else:
                self.report({'WARNING'}, "Selected texture not found.")
        else:
            self.report({'WARNING'}, "No texture selected.")

        return {'FINISHED'}


def reduce_image_size(input_path, output_path, width, height, quality):
    # Open image
    image = Image.open(input_path)

    # Recalculate sizes
    new_size = (width, height)
    resized_image = image.resize(new_size, Image.ANTIALIAS)

    # Save file
    resized_image.save(output_path, quality=quality)


def get_texture_items(self, context):
    textures = bpy.data.images
    items = []
    for texture in textures:
        items.append((texture.name, texture.name, ""))
    return items

##

# Texture Suffix&Prefix


def get_texture_nodes(material):
    texture_nodes = []
    if material.use_nodes:
        node_tree = material.node_tree
        texture_nodes = [
            node for node in node_tree.nodes if node.type == 'TEX_IMAGE' and node.image]
    return texture_nodes


def get_textures(self, context):
    obj = context.object
    if obj is not None:
        materials = obj.data.materials
        items = []
        for mat in materials:
            texture_nodes = get_texture_nodes(mat)
            for node in texture_nodes:
                items.append((node.image.name, node.image.name, ""))
        return items
    else:
        return []


def get_materials(self, context):
    obj = context.object
    if obj is not None:
        materials = obj.data.materials
        items = []
        for mat in materials:
            items.append((mat.name, mat.name, ""))
        return items
    else:
        return []


bpy.types.Scene.prefix = bpy.props.StringProperty(
    name="Prefix",
    default="prefix_"
)
bpy.types.Scene.suffix = bpy.props.StringProperty(
    name="Suffix",
    default="_suffix"
)
bpy.types.Scene.selected_material = bpy.props.EnumProperty(
    items=get_materials,
    description="Select Material"
)
bpy.types.Scene.selected_texture = bpy.props.EnumProperty(
    items=get_textures,
    description="Select Texture"
)
bpy.types.Scene.selected_base_color = bpy.props.BoolProperty(
    name="Base Color",
    default=False
)
bpy.types.Scene.selected_metallic = bpy.props.BoolProperty(
    name="Metallic",
    default=False
)
bpy.types.Scene.selected_roughness = bpy.props.BoolProperty(
    name="Roughness",
    default=False
)
bpy.types.Scene.selected_emission = bpy.props.BoolProperty(
    name="Emission",
    default=False
)
bpy.types.Scene.selected_normal = bpy.props.BoolProperty(
    name="Normal",
    default=False
)


class AddPrefixSuffixOperator(bpy.types.Operator):
    bl_idname = "object.add_prefix_suffix_operator"
    bl_label = "Add Prefix&Suffix"

    def execute(self, context):
        selected_material = context.scene.selected_material
        material = bpy.data.materials.get(selected_material)

        if material is None:
            self.report({'ERROR'}, "Invalid material selected.")
            return {'CANCELLED'}

        prefix = context.scene.prefix
        suffix = context.scene.suffix

        node_tree = material.node_tree
        principled_node = None

        # Finding Principled BSDF node
        for node in node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                principled_node = node
                break

        if principled_node is None:
            self.report(
                {'ERROR'}, "No Principled BSDF node found in material node tree.")
            return {'CANCELLED'}

        updated_textures = []

        # Base Color
        if context.scene.selected_base_color:
            for input in principled_node.inputs:
                if input.name == 'Base Color' and input.is_linked and input.links[0].from_node.type == 'TEX_IMAGE':
                    texture_node = input.links[0].from_node
                    old_texture_name = texture_node.image.name

                    # File extension
                    file_extension = os.path.splitext(old_texture_name)[1]

                    # Prefix&Suffix
                    new_texture_name = prefix + \
                        old_texture_name[:-len(file_extension)] + \
                        suffix + file_extension

                    # Rename Texture
                    texture_node.image.name = new_texture_name

                    updated_textures.append(
                        (old_texture_name, new_texture_name))

        # Metallic
        if context.scene.selected_metallic:
            for input in principled_node.inputs:
                if input.name == 'Metallic' and input.is_linked and input.links[0].from_node.type == 'TEX_IMAGE':
                    texture_node = input.links[0].from_node
                    old_texture_name = texture_node.image.name

                    # File extension
                    file_extension = os.path.splitext(old_texture_name)[1]

                    # Prefix&Suffix
                    new_texture_name = prefix + \
                        old_texture_name[:-len(file_extension)] + \
                        suffix + file_extension

                    # Rename Texture
                    texture_node.image.name = new_texture_name

                    updated_textures.append(
                        (old_texture_name, new_texture_name))

        # Roughness
        if context.scene.selected_roughness:
            for input in principled_node.inputs:
                if input.name == 'Roughness' and input.is_linked and input.links[0].from_node.type == 'TEX_IMAGE':
                    texture_node = input.links[0].from_node
                    old_texture_name = texture_node.image.name

                    # File extension
                    file_extension = os.path.splitext(old_texture_name)[1]

                    # Prefix&Suffix
                    new_texture_name = prefix + \
                        old_texture_name[:-len(file_extension)] + \
                        suffix + file_extension

                    # Rename Texture
                    texture_node.image.name = new_texture_name

                    updated_textures.append(
                        (old_texture_name, new_texture_name))

        # Emission
        if context.scene.selected_emission:
            for input in principled_node.inputs:
                if input.name == 'Emission' and input.is_linked and input.links[0].from_node.type == 'TEX_IMAGE':
                    texture_node = input.links[0].from_node
                    old_texture_name = texture_node.image.name

                    # File extension
                    file_extension = os.path.splitext(old_texture_name)[1]

                    # Prefix&Suffix
                    new_texture_name = prefix + \
                        old_texture_name[:-len(file_extension)] + \
                        suffix + file_extension

                    # Rename Texture
                    texture_node.image.name = new_texture_name

                    updated_textures.append(
                        (old_texture_name, new_texture_name))

        # Normal
        if context.scene.selected_normal:
            for input in principled_node.inputs:
                if input.name == 'Normal' and input.is_linked and input.links[0].from_node.type == 'TEX_IMAGE':
                    texture_node = input.links[0].from_node
                    old_texture_name = texture_node.image.name

                    # File extension
                    file_extension = os.path.splitext(old_texture_name)[1]

                    # Prefix&Suffix
                    new_texture_name = prefix + \
                        old_texture_name[:-len(file_extension)] + \
                        suffix + file_extension

                    # Rename Texture
                    texture_node.image.name = new_texture_name

                    updated_textures.append(
                        (old_texture_name, new_texture_name))

        # Warning msg
        if updated_textures:
            message = "Textures are renamed:\n\n"
            for texture_names in updated_textures:
                message += texture_names[0] + " -> " + texture_names[1] + "\n"
            self.report({'INFO'}, message)
        else:
            self.report(
                {'WARNING'}, "Could not find 'Selected' texture' linked to Principled BSDF node.")

        return {'FINISHED'}

##

# Register


def register():
    bpy.utils.register_class(AIOPanel)
    #
    bpy.utils.register_class(ApplyLocationOperator)
    bpy.utils.register_class(ApplyRotationOperator)
    bpy.utils.register_class(ApplyScaleOperator)
    bpy.utils.register_class(ApplyAllOperator)
    #
    bpy.utils.register_class(OBJECT_OT_SetOrigin)
    #
    bpy.utils.register_class(RemoveUnconnectedVerticesOperator)
    bpy.utils.register_class(MergeByDistanceOperator)
    bpy.utils.register_class(OBJECT_OT_RecalculateNormals)
    bpy.utils.register_class(TriangulateFacesOperator)
    bpy.utils.register_class(SmartUVProjectOperator)
    #
    bpy.utils.register_class(RenameObjectsOperator)
    bpy.types.Scene.new_name = bpy.props.StringProperty(
        default="Name")
    bpy.utils.register_class(AddPrefixOperator)
    bpy.types.Scene.custom_prefix = bpy.props.StringProperty(
        name="Prefix", default="SM_")
    bpy.utils.register_class(AddSuffixOperator)
    bpy.types.Scene.custom_suffix = bpy.props.StringProperty(
        name="Suffix", default="_SM")
    #
    bpy.types.Object.selected_uv_map = bpy.props.EnumProperty(
        items=get_uv_maps,
        name="Selected UV Map",
        description="Selected UV Map"
    )
    bpy.types.Object.new_uv_map_name = bpy.props.StringProperty(
        name="New UV Map Name",
        description="New UV Map Name"
    )
    bpy.types.Scene.new_uv_name = bpy.props.StringProperty(
        name="", default="UV_Map")
    bpy.utils.register_class(OBJECT_OT_RenameUVMap)
    #
    bpy.types.Scene.selected_extension = EnumProperty(
        items=extension_items,
        name="Selected Extension",
        description="Selected image extension",
        default=".jpg"
    )
    bpy.types.Scene.selected_texture = bpy.props.EnumProperty(
        items=get_texture_items)
    bpy.types.Scene.new_width = bpy.props.IntProperty(name="New Width")
    bpy.types.Scene.new_height = bpy.props.IntProperty(name="New Height")
    bpy.types.Scene.quality = bpy.props.IntProperty(
        name="Quality", min=0, max=100, default=85)
    bpy.types.Scene.newName = bpy.props.StringProperty(name="", default="")
    bpy.utils.register_class(ReduceSizeOperator)
    #
    bpy.utils.register_class(AddPrefixSuffixOperator)
    bpy.types.Scene.prefix_text = bpy.props.StringProperty(
        name="Prefix", default="")
    bpy.types.Scene.suffix_text = bpy.props.StringProperty(
        name="Suffix", default="")

    # Update Panel
    bpy.app.handlers.depsgraph_update_post.append(update_panel)

# Unregister


def unregister():
    bpy.utils.unregister_class(AIOPanel)
    #
    bpy.utils.unregister_class(ApplyLocationOperator)
    bpy.utils.unregister_class(ApplyRotationOperator)
    bpy.utils.unregister_class(ApplyScaleOperator)
    bpy.utils.unregister_class(ApplyAllOperator)
    #
    bpy.utils.unregister_class(OBJECT_OT_SetOrigin)
    #
    bpy.utils.unregister_class(RemoveUnconnectedVerticesOperator)
    bpy.utils.unregister_class(MergeByDistanceOperator)
    bpy.utils.unregister_class(OBJECT_OT_RecalculateNormals)
    bpy.utils.unregister_class(TriangulateFacesOperator)
    bpy.utils.unregister_class(SmartUVProjectOperator)
    #
    bpy.utils.unregister_class(RenameObjectsOperator)
    del bpy.types.Scene.new_name
    bpy.utils.unregister_class(AddPrefixOperator)
    del bpy.types.Scene.custom_prefix
    bpy.utils.unregister_class(AddSuffixOperator)
    del bpy.types.Scene.custom_suffix
    #
    del bpy.types.Object.selected_uv_map
    del bpy.types.Object.new_uv_map_name
    del bpy.types.Scene.new_uv_name
    bpy.utils.unregister_class(OBJECT_OT_RenameUVMap)
    #
    del bpy.types.Scene.selected_extension
    del bpy.types.Scene.selected_texture
    del bpy.types.Scene.new_width
    del bpy.types.Scene.new_height
    del bpy.types.Scene.quality
    bpy.utils.unregister_class(ReduceSizeOperator)
    #
    bpy.utils.unregister_class(AddPrefixSuffixOperator)
    del bpy.types.Scene.prefix_text
    del bpy.types.Scene.suffix_text

# Remove update panel
    bpy.app.handlers.depsgraph_update_post.remove(update_panel)

# Update Panel


def update_panel(scene, depsgraph):
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


# Run
if __name__ == "__main__":
    register()
