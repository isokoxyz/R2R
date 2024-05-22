from r2r.models.nft import NFT
from r2r.bpy_handlers.BpyContext import BpyContext


class Image(NFT):
    def __init__(
        self,
        bpy_context: BpyContext,
        token_id: str,
        nft_id: str,
        collection_id: str,
        collection_name: str,
        chain_id: str,
        uri: str,
        uv_map: str
    ):
        super().__init__(bpy_context, token_id, nft_id,
            collection_id, collection_name, chain_id, uri)
        self.metadata = self.fetch_nft_metadata()
        self.uv_map = uv_map

    def fetch_nft_metadata(self):
        pass

    def add_shader_nodes_for_image_texture(self, tgt_base_color, tgt_node_tree, tgt_node, tgt_node_input):
        nodes = tgt_node_tree.nodes

        # Create UV map node to specify destination
        uv_node = nodes.new("ShaderNodeUVMap")
        # TODO: this will be the name of the actual uv which will be in the image metadata
        uv_node.uv_map = self.uv_map
        uv_node.name = "UV_MAP_NODE_{}".format(self.nft_id)

        # Create texture shader node for sticker
        texture_node = nodes.new("ShaderNodeTexImage")
        texture_node.image = self.bpy_context.bpy.data.images.load(
            self.get_image_uri())  # TODO: load image
        texture_node.name = "STICKER_NODE_{}".format(self.nft_id)

        # Create Mix RGB node to set kadcar color
        mix_node = nodes.new("ShaderNodeMixRGB")
        mix_node.inputs['Color1'].default_value = tgt_base_color
        mix_node.name = "MIX_NODE_{}".format(self.nft_id)

        # Link all created nodes to the principled bsdf
        print("CONNECTING ALL SHADER NODES")
        tgt_node_tree.links.new(
            uv_node.outputs['UV'], texture_node.inputs['Vector'])
        tgt_node_tree.links.new(
            texture_node.outputs['Color'], mix_node.inputs['Color2'])
        tgt_node_tree.links.new(
            texture_node.outputs['Alpha'], mix_node.inputs['Fac'])
        tgt_node_tree.links.new(
            mix_node.outputs['Color'], tgt_node.inputs[tgt_node_input])
            # mix_node.outputs['Color'], tgt_node.inputs['Base Color'])
        
        return mix_node, 'Color1'

    def get_image_uri(self):
        pass
