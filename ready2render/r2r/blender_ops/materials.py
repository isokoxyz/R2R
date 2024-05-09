import bpy

def transfer_materials(clean, src, tgt):
    if clean:
        tgt.data.materials.clear() # ensure the target material slots are clean
    
    for mat in src.data.materials:
        tgt.data.materials.append(mat)

def transfer_materials_bulk(clean, src, target_object_names):
    print(target_object_names)
    for tgt in target_object_names:
        print(tgt)
        target_object = bpy.data.objects.get(tgt)
        transfer_materials(clean, src, target_object)