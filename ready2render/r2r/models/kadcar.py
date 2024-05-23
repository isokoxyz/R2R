from r2r.models.nft import NFT
from r2r.models.image import Image
from r2r.ipfs_utils.ipfs_utils import download_glb_asset
from r2r.bpy_handlers.BpyContext import BpyContext
from r2r.ipfs_utils.ipfs_utils import upload_nft_files_to_ipfs

class Kadcar(NFT):
    def __init__(
        self,
        bpy_context: BpyContext,
        token_id: str,
        nft_id: str,
        collection_id: str,
        collection_name: str,
        chain_id: str,
        uri: str
    ):
        super().__init__(bpy_context, token_id, nft_id, collection_id, collection_name, chain_id, uri)
        self.metadata = self.fetch_nft_metadata()
        self.kadcar_w_uvs = 'C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars/kadcar_w_uvs.glb'

    def fetch_nft_metadata(self):
        kadcar_nft_data = super().fetch_nft_data_from_blockchain()
        kadcar_nft_metadata = super().fetch_nft_metadata(kadcar_nft_data["uri"])

        return kadcar_nft_metadata

    def attach_image_texture(self, image_nft: Image):
        bpy = self.bpy_context

        # import nft glbs into scene
        kadcar_glb = download_glb_asset(self.get_kadcar_model_uri())
        bpy.scene_handler.import_scene_into_collection(kadcar_glb, "kadcar")
        bpy.scene_handler.import_scene_into_collection(self.kadcar_w_uvs, "kadcar_w_uvs")

        # deselect everything
        bpy.scene_handler.deselect_all_scene_objects()

        # select target kadcar
        kadcar_object = bpy.object_handler.select_object_by_name_and_make_active("Car_Body")
        bpy.object_handler.set_object_origin(type='ORIGIN_GEOMETRY', center='MEDIAN')

        # select kadcars with object
        kadcar_w_uvs_object = bpy.object_handler.select_object_by_name_and_make_active("Car_Body.001")
        bpy.object_handler.set_object_origin(type='ORIGIN_GEOMETRY', center='MEDIAN')

        # link objects
        bpy.object_handler.link_selected_objects_in_scene(type='OBDATA')

        # fix the rotation
        bpy.object_handler.make_object_active(kadcar_w_uvs_object)
        # uvs_object.rotation_quaternion.x = 1.0
        # bpy.object_handler.apply_transform_to_selected_object(uvs_object, location=True, rotation=True)

        # remove kadcar with uvs
        bpy.scene_handler.deselect_all_scene_objects()
        bpy.scene_handler.delete_objects_from_collection_name("kadcar_w_uvs")

        # Retrieve bsdf values and node tree
        bsdf = bpy.shader_handler.get_principled_bsdf_for_active_material(kadcar_object)
        base_color = bpy.shader_handler.get_input_value_from_bsdf(bsdf, 'Base Color')
        metallic_value = bpy.shader_handler.get_input_value_from_bsdf(bsdf, 'Metallic')
        node_tree = bpy.shader_handler.get_node_tree_for_selected_object(kadcar_object)

        tgt_node, tgt_node_input = self.add_kadcar_image_texture_shader_nodes(bpy=bpy, kadcar_object=kadcar_object)
        tgt_node, tgt_node_input = image_nft.add_shader_nodes_for_image_texture(
            tgt_base_color=base_color,
            tgt_node_tree=node_tree,
            tgt_node=tgt_node,
            tgt_node_input=tgt_node_input
        )
        self.metadata["attachments"].append(image_nft.get_image_data())

        self.bpy_context.shader_handler.set_input_value_in_bsdf(bsdf, 'Metallic', metallic_value)

        return self.metadata

    def remove_image_texture(self, image_texture_id: str):
        bpy = self.bpy_context

        # import nft glbs into scene
        kadcar_glb = download_glb_asset(self.get_kadcar_model_uri())
        bpy.scene_handler.import_scene_into_collection(kadcar_glb, "kadcar")

        # deselect everything
        bpy.scene_handler.deselect_all_scene_objects()

        # select target kadcar
        kadcar_object = bpy.object_handler.select_object_by_name_and_make_active("Car_Body")
        self.add_kadcar_image_texture_shader_nodes(bpy=bpy, kadcar_object=kadcar_object, to_exclude=image_texture_id)

    def add_kadcar_image_texture_shader_nodes(self, bpy: BpyContext, kadcar_object, to_exclude: str=None):
        # Retrieve bsdf values and node tree
        bsdf = bpy.shader_handler.get_principled_bsdf_for_active_material(kadcar_object)
        base_color = bpy.shader_handler.get_input_value_from_bsdf(bsdf, 'Base Color')
        metallic_value = bpy.shader_handler.get_input_value_from_bsdf(bsdf, 'Metallic')
        node_tree = bpy.shader_handler.get_node_tree_for_selected_object(kadcar_object)

        # loop over all stickers, create image nft, add shader nodes
        tgt_node = bsdf
        tgt_node_input = "Base Color"

        if self.metadata["attachments"] is not None:
            for attachment in self.metadata["attachments"]:
                if attachment["token_id"] == to_exclude:
                    continue

                attachment_nft = Image(
                    bpy_context=bpy,
                    token_id=attachment["token_id"],
                    nft_id=attachment["nft_id"],
                    collection_id=attachment["collection_id"],
                    collection_name=attachment["collection_name"],
                    chain_id=attachment["chain_id"],
                    uri=attachment["uri"],
                    uv_map=attachment["uv_map"]
                )

                tgt_node, tgt_node_input = attachment_nft.add_shader_nodes_for_image_texture(
                    tgt_base_color=base_color,
                    tgt_node_tree=node_tree,
                    tgt_node=tgt_node,
                    tgt_node_input=tgt_node_input
                )
        else:
            self.metadata["attachments"] = []

        return tgt_node, tgt_node_input

    def upload_nft_to_ipfs(self):
        kadcar_glb_path = self.get_kadcar_glb_path()
        kadcar_render_path = self.get_kadcar_render_path()

        glb_url, webp_url = upload_nft_files_to_ipfs(kadcar_glb_path, kadcar_render_path)

        self.set_kadcar_model_uri(glb_url)
        self.set_kadcar_image_uri(webp_url)

        return self.metadata

    def get_kadcar_glb_path(self):
        return ""
    
    def get_kadcar_render_path(self):
        return ""

    def set_kadcar_image_uri(self, uri):
        self.metadata["uri"]["data"] = uri

    def set_kadcar_model_uri(self, uri):
        self.metadata["data"][2]["datum"]["art-asset"]["data"] = uri

    def get_kadcar_image_uri(self):
        return self.metadata["uri"]["data"]

    def get_kadcar_model_uri(self):
        return self.metadata["data"][2]["datum"]["art-asset"]["data"]
