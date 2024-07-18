from config import MODELS_WITH_UV_MAPS_PATH, BLENDER_EXPORT_PATH, RENDER_OUTPUT_PATH, HDR_FILES_PATH
from r2r.utils.io_utils import load_gltf, extract_json_attribute_data
from r2r.models.nft import NFT
from r2r.models.image import Image
from r2r.bpy_handlers.BpyContext import BpyContext
from r2r.ipfs_utils.ipfs_utils import download_asset_from_ipfs, upload_nft_files_to_ipfs, get_file_name_from_ipfs_dir

class Kadcar(NFT):
    """
    This class represents a Kadcar NFT and provides the functionality needed to 
    fetch and alter the NFT's data
    """
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
        self.kadcar_w_uvs = MODELS_WITH_UV_MAPS_PATH
        self.s3_metadata_acl = "public"
        self.glb_extras = None

    def fetch_nft_metadata(self):
        """
        This function fetches the Kadcar NFT's metadata

        Returns:
            dict: json object containing the Kadcar's metadata
        """
        kadcar_nft_data = super().fetch_nft_data_from_blockchain()
        kadcar_nft_metadata = super().fetch_nft_metadata(kadcar_nft_data["result"]["data"]["uri"])

        return kadcar_nft_metadata

    def attach_image_texture(self, image_nft: Image):
        """
        This function adds an image texture to the Kadcar's shader nodes

        Returns:
            dict: json object containing the Kadcar's metadata
        """
        bpy = self.bpy_context

        # import nft glbs into scene
        # kadcar_glb = download_asset_from_ipfs(self)
        kadcar_glb = "K:/UpgradeTest/ipfs_downloads/kadcars/nft_3356.glb"
        # kadcar_glb = "/Users/mohannadahmad/Desktop/AppDev/Kadena/R2R/ready2render/r2r/kadcars/nft_3356.glb"
        glb = load_gltf(kadcar_glb)
        self.glb_extras = glb.extras
        print("IMPORTING KADCAR INTO SCENE")
        bpy.scene_handler.import_scene_into_collection(kadcar_glb, "kadcar")
        print("IMPORTING KADCAR WITH UVS INTO SCENE")
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
        bpy.object_handler.make_object_active(kadcar_object)
        kadcar_object.rotation_quaternion.x = 1.0
        bpy.object_handler.apply_transform_to_selected_object(kadcar_object, location=True, rotation=True)

        # remove kadcar with uvs
        print("REMOVING UV KADCAR")
        bpy.scene_handler.deselect_all_scene_objects()
        bpy.scene_handler.delete_objects_from_collection_name("kadcar_w_uvs")

        # Retrieve bsdf values and node tree
        bsdf = bpy.shader_handler.get_principled_bsdf_for_active_material(kadcar_object)
        base_color = bpy.shader_handler.get_input_value_from_bsdf(bsdf, 'Base Color')
        metallic_value = bpy.shader_handler.get_input_value_from_bsdf(bsdf, 'Metallic')
        node_tree = bpy.shader_handler.get_node_tree_for_selected_object(kadcar_object)

        print("SETTING UP SHADER NODES")
        tgt_node, tgt_node_input = self.add_kadcar_image_texture_shader_nodes(bpy=bpy, kadcar_object=kadcar_object)
        tgt_node, tgt_node_input = image_nft.add_shader_nodes_for_image_texture(
            tgt_base_color=base_color,
            tgt_node_tree=node_tree,
            tgt_node=tgt_node,
            tgt_node_input=tgt_node_input
        )
        self.metadata["attachments"].append(image_nft.get_image_data())
        print(self.metadata)

        self.bpy_context.shader_handler.set_input_value_in_bsdf(bsdf, 'Metallic', metallic_value)
        self.add_hdr_background_to_scene()

        return self.metadata

    def remove_image_texture(self, image_texture_id: str):
        """
        This function removes the specified image texture from the Kadcar's shader nodes
        """
        bpy = self.bpy_context

        # import nft glbs into scene
        kadcar_glb = download_asset_from_ipfs(self)
        bpy.scene_handler.import_scene_into_collection(kadcar_glb, "kadcar")

        # deselect everything
        bpy.scene_handler.deselect_all_scene_objects()

        # select target kadcar
        kadcar_object = bpy.object_handler.select_object_by_name_and_make_active("Car_Body")
        self.add_kadcar_image_texture_shader_nodes(bpy=bpy, kadcar_object=kadcar_object, to_exclude=image_texture_id)

    def add_kadcar_image_texture_shader_nodes(self, bpy: BpyContext, kadcar_object, to_exclude: str=None):
        """
        This function the shader nodes for the image textures the Kadcar model has

        Returns:
            tuple(ShaderNodeMixRGB, string): BPY Node object and string representing the target shader node and its input field
        """
        # Retrieve bsdf values and node tree
        bsdf = bpy.shader_handler.get_principled_bsdf_for_active_material(kadcar_object)
        base_color = bpy.shader_handler.get_input_value_from_bsdf(bsdf, 'Base Color')
        metallic_value = bpy.shader_handler.get_input_value_from_bsdf(bsdf, 'Metallic')
        node_tree = bpy.shader_handler.get_node_tree_for_selected_object(kadcar_object)

        # loop over all stickers, create image nft, add shader nodes
        tgt_node = bsdf
        tgt_node_input = "Base Color"

        if "attachments" in self.metadata:
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
        """
        This function uploads the Kadcar NFT to IPFS

        Returns:
            dict: json object containing the Kadcar's metadata
        """
        kadcar_glb_path = self.get_asset_glb_path()
        kadcar_render_path = self.get_asset_render_path()

        glb_url, webp_url = upload_nft_files_to_ipfs(kadcar_glb_path, kadcar_render_path)

        self.set_kadcar_model_uri(glb_url)
        self.set_kadcar_image_uri(webp_url)

        return self.metadata

    def get_nft_name(self):
        """
        This function returns the Kadcar NFT's name
        """
        return self.get_kadcar_vin()

    def set_kadcar_image_uri(self, uri):
        """
        This function sets the Kadcar's render URI value in the metadata
        """
        self.metadata["uri"]["data"] = uri

    def set_kadcar_model_uri(self, uri):
        """
        This function sets the Kadcar's GLB URI value in the metadata
        """
        self.metadata["data"][2]["datum"]["art-asset"]["data"] = uri

    def get_asset_render_format(self):
        """
        This function gets the Kadcar's render format

        Returns:
            string: name of render output format
        """
        return "WEBP"

    def get_kadcar_image_uri(self):
        """
        This function gets the Kadcar's render URI from the metadata

        Returns:
            string: Kadcar's image URI
        """
        return self.metadata["uri"]["data"]

    def get_kadcar_model_uri(self):
        """
        This function gets the Kadcar's GLB URI from the metadata
        """
        return self.metadata["data"][2]["datum"]["art-asset"]["data"]

    def get_kadcar_type(self):
        """
        This function gets the Kadcar's type from the metadata

        Returns:
            string: name of Kadcar type
        """
        return self.metadata["data"][0]["datum"]["components"][0]["stats"][0]["val"]

    def get_kadcar_vin(self):
        """
        This function gets the Kadcar's VIN from the metadata

        Returns:
            string: Kadcar's VIN string
        """
        return self.metadata["data"][1]["datum"]["vehicle-information"]["vin"]
    
    def get_kadcar_model_cid(self):
        """
        This function gets the Kadcar's IPFS CID

        Returns:
            string: Kadcar IPFS CID from URI
        """
        return str(self.get_kadcar_model_uri().split("://")[1])
    
    def get_asset_ipfs_cid(self):
        """
        This function gets the Kadcar's IPFS CID

        Returns:
            string: Kadcar IPFS CID from URI
        """
        return str(self.get_kadcar_model_uri().split("://")[1])

    def get_asset_render_aspect_ratio(self):
        """
        This function gets the render's aspect ratio from the GLB file

        Returns:
            object: contains x and y values for the Kadcar render's aspect ratio
        """
        return self.glb_extras["config"]["render_settings"]["aspect-ratio"]

    def get_asset_render_aspect_ratio_x(self):
        """
        This function gets the x value of the render's aspect ratio
        
        Returns:
            int: contains x value for the Kadcar render's aspect ratio
        """
        return self.get_asset_render_aspect_ratio()["res_x"]

    def get_asset_render_aspect_ratio_y(self):
        """
        This function gets the y value of the render's aspect ratio
        
        Returns:
            int: contains y value for the Kadcar render's aspect ratio
        """
        return self.get_asset_render_aspect_ratio()["res_y"]

    def export_nft(self, file_path, format="GLB"):
        """
        This function exports the Kadcar blender file in the specified format
        """
        self.bpy_context.camera_handler.set_scene_camera("Camera_Orientation")
        super().export_nft(file_path, format)

        glb = load_gltf(self.get_asset_glb_path())
        glb.extras = self.glb_extras
        glb.save(self.get_asset_glb_path())

    # HDRI settings
    def get_kadcar_background(self):
        """
        This function gets the Kadcar background from its metadata

        Returns:
            string: name of the background
        """
        return self.metadata["data"][3]["datum"]["datum"]["attributes"][0]["value"]
    
    def get_background_hdr_file_name(self, background):
        """
        This function gets the name of the HDR file bsaed on the background
        
        Returns:
            string: name of the HDR file for the given background
        """
        if background == "Digital Den":
            return "storage_background"
        elif background == "Kadena Beach":
            return "beach_background"
        elif background == "K:2 Summit":
            return "snow_background"
        elif background == "Crystal Caves":
            return "mountain_background"

    def get_background_hdr(self):
        """
        This function gets the HDR file for the background specified

        Returns:
            string: HDR background file path
        """
        background = self.get_kadcar_background()
        hdr_name = self.get_background_hdr_file_name(background)
        hdr_file_path = f"{HDR_FILES_PATH}/{hdr_name}"

        if background == 'Digital Den':
            hdr_file_path = hdr_file_path + ".exr"
        else:
            hdr_file_path = hdr_file_path + ".hdr"
        
        return hdr_file_path
    
    def add_hdr_background_to_scene(self):
        """
        This function adds HDR background to the scene
        """
        background = self.get_kadcar_background()
        hdr_file = self.get_background_hdr()

        self.bpy_context.shader_handler.customize_world_shader_nodes(hdr_file, background)

    # Path getters
    def get_s3_md_bucket_name(self):
        """
        This function gets the name of the Kadcar NFT's metadata bucket name

        Returns:
            string: name of the S3 bucket
        """

        # return "kadcars-nft-metadata"
        return "kadcars-manifests"
    
    def get_s3_render_bucket_name(self):
        """
        This function gets the name of the Kadcar NFT's render bucket name

        Returns:
            string: name of the S3 bucket
        """

        return "kadcars-renders"
    
    def get_kadcar_w_uvs_path(self):
        """
        This function gets the Kadcar GLB file containing the sticker location UV Maps

        Returns:
            string: Kadcar model with UV map's file path
        """
        kadcar_type = self.get_kadcar_type()

        if kadcar_type == "K:2":
            return MODELS_WITH_UV_MAPS_PATH
        else:
            pass

    def get_asset_glb_path(self):
        """
        This function gets the NFT asset's GLB path

        Returns:
            string: file path for Kadcar GLB
        """
        dir_name = self.get_asset_export_dir_name()
        vin = self.get_kadcar_vin()

        return f"{BLENDER_EXPORT_PATH}/{dir_name}/kadcar_{vin}.glb"
    
    def get_asset_render_path(self):
        """
        This function gets the path where the NFT render file will be saved

        Returns:
            string: file path for the Kadcar's render
        """
        dir_name = self.get_asset_render_dir_name()
        vin = self.get_kadcar_vin()

        return f"{RENDER_OUTPUT_PATH}/{dir_name}/kadcar_{vin}.webp"

    def get_base_asset_s3_uri(self):
        """
        This function gets the digital ocean Base URL for the NFT render
        """
        vin = self.get_kadcar_vin()

        return f"https://{self.collection_name}.nyc3.digitaloceanspaces.com/{vin}"

    def get_md_s3_uri(self):
        """
        This function gets the digital ocean URL for the NFT metadata
        """

        return f"{self.get_base_asset_s3_uri()}.json"
    
    def get_asset_s3_uri(self):
        """
        This function gets the digital ocean URL for the NFT render
        """

        return f"{self.get_base_asset_s3_uri()}.webp"

    def get_asset_ipfs_file_name(self):
        """
        This function gets the NFTs file name on IPFS

        Returns:
            string: name of NFT file on IPFS
        """
        return get_file_name_from_ipfs_dir(self.get_kadcar_model_cid())
    
    def get_asset_ipfs_download_dir_name(self):
        """
        This function gets the file path where the IPFS asset gets downloaded

        Returns:
            string: name of directory for Kadcar IPFS downloads
        """
        dir_name = super().get_asset_ipfs_download_dir_name("kadcars")
        return dir_name
    
    def get_asset_export_dir_name(self):
        """
        This function gets the directory where assets get exported

        Returns:
            string: name of directory where Kadcar exports are stored
        """
        dir_name = super().get_asset_export_dir_name("kadcars")
        return dir_name

    def get_asset_render_dir_name(self):
        """
        This function gets the directory where the NFT asset render is saved

        Returns:
            string: name of directory where render files are stored
        """
        dir_name = super().get_asset_render_dir_name("kadcars")
        return dir_name
    
    def get_nft_render_file_name(self):
        """
        This function returns the name of the render file

        Returns:
            string: name of the NFT render's file
        """
        return self.get_nft_name() + "." + self.get_asset_render_format().lower()