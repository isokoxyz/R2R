import bpy
import math

def customize_world_shader_nodes(hdri, type):
    context = bpy.context
    scene = context.scene

    #Get the environment node tree of the current scene
    node_tree = scene.world.node_tree
    tree_nodes = node_tree.nodes
    links = node_tree.links

    #Clear all nodes
    tree_nodes.clear()

    #Add background node
    node_background = tree_nodes.new(type='ShaderNodeBackground')
    
    #Add output node
    node_output = tree_nodes.new(type='ShaderNodeOutputWorld')
    node_output.location = 200,0

    if type == 'mountain':
        mapping_node = tree_nodes.new('ShaderNodeMapping')
        tex_coord_node = tree_nodes.new('ShaderNodeTexCoord')

        node_background.inputs['Strength'].default_value = 3.5

        #Add environment texture node
        node_environment = tree_nodes.new('ShaderNodeTexEnvironment')

        #Load and assign the image to then node property
        node_environment.image = bpy.data.images.load(hdri)
        # node_environment.location = -300, 0
    
        mapping_node.vector_type = "POINT"
        mapping_node.inputs["Location"].default_value = (1.1, 0.0, 0.0)
        mapping_node.inputs["Rotation"].default_value = (math.radians(0.0), math.radians(0.0), math.radians(0.5))

        #Link all nodes
        # links = node_tree.links
        links.new(tex_coord_node.outputs["Generated"], mapping_node.inputs["Vector"])
        links.new(mapping_node.outputs["Vector"], node_environment.inputs["Vector"])
        links.new(node_environment.outputs["Color"], node_background.inputs["Color"]) #connect sky texture to background node
        links.new(node_background.outputs["Background"], node_output.inputs["Surface"]) #connect background node to world node
    
    elif type == 'storage':
        mapping_node = tree_nodes.new('ShaderNodeMapping')
        tex_coord_node = tree_nodes.new('ShaderNodeTexCoord')

        node_background.inputs['Strength'].default_value = 3.0

        #Add environment texture node
        node_environment = tree_nodes.new('ShaderNodeTexEnvironment')

        #Load and assign the image to then node property
        node_environment.image = bpy.data.images.load(hdri)
        # node_environment.location = -300, 0
    
        mapping_node.vector_type = "POINT"
        mapping_node.inputs["Rotation"].default_value = (math.radians(-8.2), math.radians(5.7), math.radians(131.0))

        #Link all nodes
        # links = node_tree.links
        links.new(tex_coord_node.outputs["Generated"], mapping_node.inputs["Vector"])
        links.new(mapping_node.outputs["Vector"], node_environment.inputs["Vector"])
        links.new(node_environment.outputs["Color"], node_background.inputs["Color"]) #connect sky texture to background node
        links.new(node_background.outputs["Background"], node_output.inputs["Surface"]) #connect background node to world node

    elif type == 'snow':
        node_background.inputs['Strength'].default_value = 1.5

        sky_texture = tree_nodes.new('ShaderNodeTexSky')
        mapping_node = tree_nodes.new('ShaderNodeMapping')
        tex_coord_node = tree_nodes.new('ShaderNodeTexCoord')

        #Customize sky texture
        sky_texture.sky_type = 'NISHITA'
        sky_texture.sun_disc = False
        sky_texture.sun_elevation = math.radians(27.2)
        sky_texture.sun_rotation = math.radians(-212.0)
        sky_texture.air_density = 3.0
        sky_texture.dust_density = 10.0
        sky_texture.ozone_density = 6.0

        #Customize mapping node
        mapping_node.vector_type = "POINT"
        mapping_node.inputs["Rotation"].default_value = (math.radians(-10.5), math.radians(6.1), math.radians(272.0))

        #Link nodes
        links.new(tex_coord_node.outputs["Generated"], mapping_node.inputs["Vector"])
        links.new(mapping_node.outputs["Vector"], sky_texture.inputs["Vector"])
        links.new(sky_texture.outputs["Color"], node_background.inputs["Color"]) #connect sky texture to background node
        links.new(node_background.outputs["Background"], node_output.inputs["Surface"]) #connect background node to world node
    
    elif type == 'beach':
        mapping_node = tree_nodes.new('ShaderNodeMapping')
        tex_coord_node = tree_nodes.new('ShaderNodeTexCoord')

        node_background.inputs['Strength'].default_value = 0.6

        #Add environment texture node
        node_environment = tree_nodes.new('ShaderNodeTexEnvironment')

        #Load and assign the image to then node property
        node_environment.image = bpy.data.images.load(hdri)

        mapping_node.vector_type = "POINT"
        mapping_node.inputs["Rotation"].default_value = (math.radians(0.0), math.radians(9.8), math.radians(-20.2))

        #Link nodes
        links.new(tex_coord_node.outputs["Generated"], mapping_node.inputs["Vector"])
        links.new(mapping_node.outputs["Vector"], node_environment.inputs["Vector"])
        links.new(node_environment.outputs["Color"], node_background.inputs["Color"]) #connect sky texture to background node
        links.new(node_background.outputs["Background"], node_output.inputs["Surface"]) #connect background node to world node
    
    elif type == 'cyber':
        node_background.inputs['Strength'].default_value = 3.0

        sky_texture = tree_nodes.new('ShaderNodeTexSky')

        #Customize sky texture
        sky_texture.sky_type = 'NISHITA'
        sky_texture.sun_disc = True
        sky_texture.sun_size = math.radians(1.1)
        sky_texture.sun_intensity = 68.7
        sky_texture.sun_elevation = math.radians(-3.3)
        sky_texture.sun_rotation = math.radians(-94.7)
        sky_texture.altitude = 29
        sky_texture.air_density = 1.309
        sky_texture.dust_density = 4.0
        sky_texture.ozone_density = 6.0

        links.new(sky_texture.outputs["Color"], node_background.inputs["Color"]) #connect sky texture to background node
        links.new(node_background.outputs["Background"], node_output.inputs["Surface"]) #connect background node to world node

def get_principled_bsdf_for_material_by_name(material_name):
    material = bpy.data.materials[material_name]
    material.use_nodes = True
    tree = material.node_tree
    nodes = tree.nodes
    bsdf = nodes["Principled BSDF"]

    return bsdf

def get_principled_bsdf_for_active_material(tgt_object):
    material = tgt_object.material_slots[0].material
    print(tgt_object.material_slots)
    bsdf = material.node_tree.nodes["Principled BSDF"]
    return bsdf

def get_node_tree_for_selected_object(tgt_object):
    material = tgt_object.material_slots[0].material
    node_tree = material.node_tree
    return node_tree

def change_object_base_color(color, mtl_name, tgt_object):
    tgt_object.data.materials.clear()
    material = bpy.data.materials.new(name=mtl_name)
    
    bsdf = get_principled_bsdf_for_material_by_name(mtl_name)

    bsdf.inputs['Base Color'].default_value = color
    material.diffuse_color = color

    tgt_object.data.materials.append(material)

def get_input_value_from_bsdf(principled_bsdf, value_name):
    value = principled_bsdf.inputs[value_name].default_value
    return value

def set_input_value_in_bsdf(principled_bsdf, value_name, value):
    principled_bsdf.inputs[value_name].default_value = value

def change_object_emission_level(tgt_object, emission_value, emission_color):
    bsdf = get_principled_bsdf_for_active_material(tgt_object)
    bsdf.inputs["Emission Strength"].default_value = emission_value
    bsdf.inputs["Emission"].default_value = emission_color
    print(bsdf.inputs["Emission Strength"].default_value)

def apply_texture_image_to_object(clean, tex_image_path, tgt_object):
    # if clean:
    #     tgt_object.data.materials.clear()

    bsdf = get_principled_bsdf_for_active_material(tgt_object)
    material = tgt_object.material_slots[0].material
    texImage = material.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load(tex_image_path)

    material.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

    if tgt_object.data.materials:
        tgt_object.data.materials[0] = material
    else:
        tgt_object.data.materials.append(material)

def transfer_materials_bulk(clean, src, target_object_names):
    print(target_object_names)
    for tgt in target_object_names:
        print(tgt)
        target_object = bpy.data.objects.get(tgt)
        transfer_materials(clean, src, target_object)

def transfer_materials(clean, src, tgt):
    if clean:
        tgt.data.materials.clear() # ensure the target material slots are clean
    
    for mat in src.data.materials:
        tgt.data.materials.append(mat)

def add_background_shader_node(tree_nodes, strength):
    node_background = tree_nodes.new(type='ShaderNodeBackground')
    node_background.inputs['Strength'].default_value = strength

def add_sky_texture_shader_node(tree_nodes, sky_type, sun_disc, sun_elevation, sun_rotation, air_density, dust_density, ozone_density):
    sky_texture = tree_nodes.new('ShaderNodeTexSky')

    sky_texture.sky_type = sky_type
    sky_texture.sun_disc = sun_disc
    sky_texture.sun_elevation = sun_elevation
    sky_texture.sun_rotation = sun_rotation
    sky_texture.air_density = air_density
    sky_texture.dust_density = dust_density
    sky_texture.ozone_density = ozone_density

def add_mapping_shader_node(tree_nodes, vector_type, rotation):
    mapping_node = tree_nodes.new('ShaderNodeMapping')

    mapping_node.vector_type = vector_type
    mapping_node.inputs["Rotation"].default_value = rotation

def add_texture_coordinates_shader_node(tree_nodes, from_instancer):
    tex_coord_node = tree_nodes.new('ShaderNodeTexCoord')

    tex_coord_node.from_instancer = from_instancer