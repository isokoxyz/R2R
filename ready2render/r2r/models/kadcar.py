from r2r.models.nft import NFT
from r2r.models.image import Image
from r2r.ipfs_utils.ipfs_utils import download_glb_asset
from r2r.bpy_handlers.BpyContext import BpyContext


class Kadcar(NFT):
    def __init__(
        self,
        bpy_context: BpyContext,
        token_id: str,
        nft_id: str,
        collection_id: str,
        collection_name: str,
        chain_id: str
    ):
        super().__init__(bpy_context, token_id, nft_id,
                         collection_id, collection_name, chain_id)
        self.metadata = self.fetch_nft_metadata()
        self.kadcar_w_uvs = 'C:/Users/Mohannad Ahmad\Desktop\AppDev\Crypto\Kadena\Kadcars\R2R/ready2render/r2r\kadcars/kadcar_w_uvs.glb'

    def fetch_nft_metadata(self):
        kadcar_nft_data = super().fetch_nft_data_from_blockchain()

        kadcar_nft_metadata = super().fetch_nft_metadata(
            kadcar_nft_data["uri"])

        return kadcar_nft_metadata

    def attach_image_texture(self, image_nft: Image):
        bpy = self.bpy_context

        kadcar_glb = download_glb_asset(self.get_kadcar_model_uri())

        # import nft glbs into scene
        bpy.scene_handler.import_scene_into_collection(
            kadcar_glb, "kadcar")
        bpy.scene_handler.import_scene_into_collection(
            self.kadcar_w_uvs, "kadcar_w_uvs")

        # deselect everything
        bpy.scene_handler.deselect_all_scene_objects()

        # select target kadcar
        kadcar_object = bpy.object_handler.select_object_by_name_and_make_active(
            "Car_Body")
        bpy.object_handler.set_object_origin(
            type='ORIGIN_GEOMETRY', center='MEDIAN')

        # select kadcars with object
        kadcar_w_uvs_object = bpy.object_handler.select_object_by_name_and_make_active(
            "Car_Body.001")
        bpy.object_handler.set_object_origin(
            type='ORIGIN_GEOMETRY', center='MEDIAN')

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
        print("SETTING UP SHADER NODES")
        bsdf = bpy.shader_handler.get_principled_bsdf_for_active_material(
            kadcar_object)
        base_color = bpy.shader_handler.get_input_value_from_bsdf(
            bsdf, 'Base Color')
        metallic_value = bpy.shader_handler.get_input_value_from_bsdf(
            bsdf, 'Metallic')
        node_tree = bpy.shader_handler.get_node_tree_for_selected_object(
            kadcar_object)

        image_nft.add_shader_nodes_for_image_texture(
            base_color, bsdf, node_tree)

        self.bpy_context.shader_handler.set_input_value_in_bsdf(
            bsdf, 'Metallic', metallic_value)

    def get_kadcar_image_uri(self):
        return self.metadata["uri"]["data"]

    def get_kadcar_model_uri(self):
        return self.metadata["data"][2]["datum"]["art-asset"]["data"]
