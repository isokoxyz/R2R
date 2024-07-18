

class MaterialHandler:
    """
    This class contains helper functions to control the materials on an object
    in a Blender scene
    """
    def __init__(self, bpy):
        self.bpy = bpy

    def transfer_materials(self, clean, src, tgt):
        """
        This function transfers the materials from an object to a specified target
        """
        if clean:
            tgt.data.materials.clear()  # ensure the target material slots are clean

        for mat in src.data.materials:
            tgt.data.materials.append(mat)

    def transfer_materials_bulk(self, clean, src, target_object_names):
        """
        This function transfers the materials from an object to a list of specified targets
        """
        for tgt in target_object_names:
            target_object = self.bpy.data.objects.get(tgt)
            self.transfer_materials(clean, src, target_object)
