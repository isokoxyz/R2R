from r2r.models.nft import NFT
from r2r.bpy_handlers.BpyContext import BpyContext
from config import IMAGE_OUTPUT_PATH
import requests

class Image(NFT):
    """
    This class defines an Image type NFT and all the functionality to alter, or combine it
    with other assets in Blender
    """
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
        super().__init__(bpy_context, token_id, nft_id, collection_id, collection_name, chain_id, uri)
        self.metadata = self.fetch_nft_metadata()
        self.uv_map = uv_map

    def fetch_nft_metadata(self):
        """
        This function fetches the Kadcar NFT's metadata

        Returns:
            dict: json object containing the Kadcar's metadata
        """
        pass

    def add_shader_nodes_for_image_texture(self, tgt_base_color, tgt_node_tree, tgt_node, tgt_node_input):
        """
        This function creates image texture shader nodes to attach the NFT image to the given target

        Returns:
            tuple(ShaderNodeMixRGB, string): BPY Node object and string representing the target shader node and its input field
        """
        nodes = tgt_node_tree.nodes

        # Create UV map node to specify destination
        uv_node = nodes.new("ShaderNodeUVMap")
        # TODO: this will be the name of the actual uv which will be in the image metadata
        uv_node.uv_map = self.uv_map
        uv_node.name = "UV_MAP_NODE_{}".format(self.nft_id)

        # Create texture shader node for sticker
        texture_node = nodes.new("ShaderNodeTexImage")
        img_path = self.download_image()
        texture_node.image = self.bpy_context.bpy.data.images.load(img_path)  # TODO: load image
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

    def download_image(self):
        """
        This function downloads the image NFT

        Returns:
            string: file path of downloaded image
        """
        img_uri = self.get_image_uri()
        img_uri_tokens = img_uri.split("/")
        img_name = img_uri_tokens[len(img_uri_tokens) - 1]
        img_data = requests.get(img_uri).content
        img_path = IMAGE_OUTPUT_PATH + "/" + img_name
        with open(img_path, 'wb') as f:
            f.write(img_data)
        f.close()

        return img_path

    def get_asset_s3_uri(self):
        """
        This function gets the digital ocean URL for the NFT render
        """
        pass

    def get_image_uri(self):
        """
        This function returns the URI to the NFT's image asset

        Returns:
            string: image NFT URI
        """

        return self.uri

    def get_image_data(self):
        """
        This function retrieves the NFT image's data 

        Returns:
            dict: contains image data
        """
        return {
            "token_id": self.token_id,
            "nft_id": self.nft_id,
            "collection_id": self.collection_id,
            "collection_name": self.collection_name,
            "chain_id": self.chain_id,
            "uri": self.uri,
            "uv_map": self.uv_map
        }
