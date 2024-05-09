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