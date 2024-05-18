

class MaterialHandler:
    def __init__(self, bpy):
        self.bpy = bpy

    def transfer_materials(self, clean, src, tgt):
        if clean:
            tgt.data.materials.clear()  # ensure the target material slots are clean

        for mat in src.data.materials:
            tgt.data.materials.append(mat)

    def transfer_materials_bulk(self, clean, src, target_object_names):
        print(target_object_names)
        for tgt in target_object_names:
            print(tgt)
            target_object = self.bpy.data.objects.get(tgt)
            self.transfer_materials(clean, src, target_object)
