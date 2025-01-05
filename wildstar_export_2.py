import dearpygui.dearpygui as dpg
from DataManager import *
from m3_to_gltf import *
from tex_to_png import *
from m3reader import *
import numpy as np
import io

class DataStore:
    EXPORT_LOCATION = ""
    LDOM_HEADER = None
    DATA_MANAGER = None
    TEX_HEADER = None
    PNG_FILE = None
    SELECTED_FILE_PATH = None
    SELECTED_FILE_DATA = None
    SELECTED_FILE_NAME = None
    MODEL_ROTATION_Y = 0
    MESHES_TO_DRAW = [True]*1000
    CHOSEN_VARIANT = "Other"
    EXPORT_FILTERS = {
        "textures": False,
        "skeleton": True,
        "embed_textures": False,
        "submeshes": [],
    }
    ARCHIVE_FILE_TYPES = [".map", ".form", ".xml", ".lua", ".txd", ".bk2", ".sky", ".wem", ".jpg", ".tbl", ".dgn", ".m3", ".psd", ".area", ".bnk", ".tex", ".ttf", ".tga", ".i3", ".sho"]
    LIST_TO_DOWNLOAD = []

dpg.create_context()

def file_selected_callback(sender, app_data, data_store):
    dpg.add_loading_indicator(style=1,radius=12.5, tag="archive_loading", parent="main_window", pos=[500,300])
    dpg.set_value("wildstar_exe_location", app_data["file_path_name"])
    data_store.DATA_MANAGER.initialize_data(app_data["file_path_name"])
    dpg.delete_item("dir_tree", children_only=True)
    dpg.delete_item("dir_tree", children_only=True, slot=1)
    dpg.push_container_stack("dir_tree")
    recursive_folders("AIDX", data_store)
    dpg.pop_container_stack()
    dpg.delete_item("archive_loading")

def add_m3_file_details(data_store):
    if data_store.LDOM_HEADER is None:
        return
    dpg.delete_item("file_details", children_only=True, slot=1)
    dpg.push_container_stack("file_details")
    nr_verts = 0
    nr_tris = 0
    for i, a_submesh in enumerate(data_store.LDOM_HEADER.geometry.submesh):
        if not data_store.MESHES_TO_DRAW[i]:
            continue
        nr_verts += a_submesh.nrVertex
        nr_tris += int(a_submesh.nrIndex/3)
    with dpg.group(horizontal=True):
        dpg.add_text("No. Vertices:", wrap=150)
        dpg.add_text(nr_verts)
    with dpg.group(horizontal=True):
        dpg.add_text("No. Triangles:", wrap=150)
        dpg.add_text(nr_tris)
    with dpg.group(horizontal=True):
        dpg.add_text("No. Textures:", wrap=150)
        dpg.add_text(data_store.LDOM_HEADER.nrTextures)
    with dpg.group(horizontal=True):
        dpg.add_text("No. Submeshes:", wrap=150)
        dpg.add_text(data_store.LDOM_HEADER.geometry.nrSubmeshes)
    with dpg.group(horizontal=True):
        dpg.add_text("No. Bones:", wrap=150)
        dpg.add_text(data_store.LDOM_HEADER.nrBones)
    with dpg.group(horizontal=True):
        dpg.add_text("No. Materials:", wrap=150)
        dpg.add_text(data_store.LDOM_HEADER.nrMaterials)
    with dpg.group(horizontal=True):
        dpg.add_text("No. Animations(?):", wrap=150)
        with dpg.tooltip(dpg.last_item()):
            dpg.add_text("All animations are stored in 1 track.")
        dpg.add_text(data_store.LDOM_HEADER.nrModelAnimations)
    with dpg.group(horizontal=True):
        dpg.add_text("No. Variants(?): ", wrap=150)
        with dpg.tooltip(dpg.last_item()):
            dpg.add_text("A value of 0 means there is only the default variant")
        dpg.add_text(data_store.LDOM_HEADER.nrSubmeshGroupsTable)
    dpg.add_separator()
    with dpg.group(horizontal=True):
        dpg.add_text("submeshes(?)")
        with dpg.tooltip(dpg.last_item()):
            dpg.add_text("A list of submeshes. Choose which submesh you want to view.")
            dpg.add_text("NOTE: Submeshes selected here are also the submeshes that will be exported.")
        dpg.add_text("variants(?)", indent=160)
        with dpg.tooltip(dpg.last_item()):
            dpg.add_text("Some .m3 models have multiple variants. EX: strain vs normal of a creature. These variants are all stored in the same .m3 file. Therefore, if you export a single .m3 file, you could end up exporting multiple versions of the same model. The devs at W* most likely grouped the different variants using this structure.", wrap=500)
            dpg.add_text("Note: sometimes, a variant is empty, and other times, it only contains an accessory of the model instead a version of the model. Most likely we do not understand how this structure works completely.", wrap=500)
            dpg.add_text("Note2: currently, variants are conencted to the submeshes through the group_id property.", wrap=500)
            dpg.add_text("Note3: the variant_id appears in creature2DisplayInfo.tbl. This could contain the missing variant info on how to combine meshes.", wrap=500)
    with dpg.child_window(width=300, autosize_y=True, autosize_x=False, border=False):
        with dpg.group(horizontal=True):
            with dpg.group(tag="visible_meshes"):
                for i, a_submesh in enumerate(data_store.LDOM_HEADER.geometry.submesh):
                    dpg.add_checkbox(label="submesh_" + str(i)+"(group:"+str(a_submesh.group_id)+")", default_value=data_store.MESHES_TO_DRAW[i], user_data=data_store, callback=redraw_model_mesh)
            groups = []
            for i, a_submesh_group in enumerate(data_store.LDOM_HEADER.submesh_groups):
                groups.append("variant_"+str(a_submesh_group.submesh_id))
            groups.append("Other")
            with dpg.group(tag="visible_variants"):
                dpg.add_radio_button(groups, callback=redraw_model_mesh_variant, user_data=data_store, default_value=data_store.CHOSEN_VARIANT)
    dpg.pop_container_stack()

def load_file_on_right_panel(data_store):
    file_name = os.path.basename(data_store.SELECTED_FILE_PATH)
    data_store.SELECTED_FILE_NAME = file_name
    dpg.set_value("right_title", data_store.SELECTED_FILE_NAME)
    dpg.set_value("right_path", data_store.SELECTED_FILE_PATH)
    data_store.SELECTED_FILE_DATA = data_store.DATA_MANAGER.get_file_bytes(data_store.SELECTED_FILE_PATH)
    file_signature = data_store.SELECTED_FILE_DATA[:4].decode("utf-8")
    if file_signature == "LDOM":
        data_store.MESHES_TO_DRAW = [True]*1000
        data_store.CHOSEN_VARIANT = "Other"
        data_store.LDOM_HEADER = Header.read_header(io.BytesIO(data_store.SELECTED_FILE_DATA))
        m3_template(data_store)
        dpg.set_value("file_signature", file_signature)
        add_m3_file_details(data_store)
        add_m3_export_details(data_store)
        draw_3d_model(data_store)
    elif data_store.SELECTED_FILE_DATA[:4] == b'XFG\x00':
        data_store.TEX_HEADER = Tex.read_header(io.BytesIO(data_store.SELECTED_FILE_DATA))
        tex_template(data_store)
        dpg.add_loading_indicator(style=1,radius=12.5, tag="image_loading", parent="main_file_view", pos=[500,300])
        add_tex_file_details(data_store)
        data_store.PNG_FILE = Tex.decode(io.BytesIO(data_store.SELECTED_FILE_DATA))
        dpg.delete_item("image_loading")
        dpg.set_value("file_signature", file_signature)
        draw_tex_image(None, None, data_store)
        add_tex_export_details(data_store)
    else:
        add_file_not_supported_template(data_store)
        dpg.set_value("file_signature", file_signature)

def add_file_not_supported_template(data_store):
    dpg.delete_item("main_file_view", children_only=True, slot=1)
    dpg.push_container_stack("main_file_view")
    with dpg.child_window(width=200, autosize_y=True, border=True):
        with dpg.group(horizontal=True):
            dpg.add_text("Signature:", wrap=150)
            dpg.add_text("", tag="file_signature")
        dpg.add_text("FILE NOT SUPPORTED")
        dpg.add_button(label="Export Raw File", callback=export_raw_file, user_data=data_store)
    dpg.pop_container_stack()

def add_m3_export_details(data_store):
    dpg.delete_item("export_window", children_only=True, slot=1)
    dpg.push_container_stack("export_window")
    with dpg.group(horizontal=True):
        with dpg.group():
            dpg.add_checkbox(label="Include Skeleton", default_value=data_store.EXPORT_FILTERS['skeleton'], user_data=data_store, callback=change_export_settings, tag="export_settings_skeleton")
            dpg.add_checkbox(label="Include Textures (slow)", default_value=data_store.EXPORT_FILTERS['textures'], user_data=data_store, callback=change_export_settings, tag="export_settings_textures")
            dpg.add_checkbox(label="Embed Textures(?)", default_value=data_store.EXPORT_FILTERS['textures'], user_data=data_store, callback=change_export_settings, tag="export_settings_embed_textures")
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text("Store the textures inside the .gltf file instead of exporting them as separate files.")
        with dpg.group(width=150, indent=370):
            dpg.add_button(label="Export M3", callback=export_raw_file, user_data=data_store)
            dpg.add_button(label="Export GLTF", callback=export_gltf_model, user_data=data_store)
    dpg.add_progress_bar(label="Export progress", default_value=0, overlay="",height=25, tag="export_progress")
    dpg.pop_container_stack()

def add_tex_file_details(data_store):
    dpg.delete_item("file_details", children_only=True, slot=1)
    dpg.push_container_stack("file_details")
    tex_format = ""
    if data_store.TEX_HEADER.tex_format == 0:
        tex_format = "jpg based"
    elif data_store.TEX_HEADER.tex_format == 6:
        tex_format = "R8"
    elif data_store.TEX_HEADER.tex_format == 13:
        tex_format = "DXT1"
    elif data_store.TEX_HEADER.tex_format == 14:
        tex_format = "DXT3"
    elif data_store.TEX_HEADER.tex_format == 15:
        tex_format = "DXT5"
    if data_store.TEX_HEADER.compression_format == 0:
        compression_format = "color"
    elif data_store.TEX_HEADER.compression_format == 1:
        compression_format = "normal"
    else:
        compression_format = "unk"
    with dpg.group(horizontal=True):
        dpg.add_text("Width:", wrap=150)
        dpg.add_text(data_store.TEX_HEADER.width)
    with dpg.group(horizontal=True):
        dpg.add_text("Height:", wrap=150)
        dpg.add_text(data_store.TEX_HEADER.height)
    with dpg.group(horizontal=True):
        dpg.add_text("No. Mip Maps:", wrap=150)
        dpg.add_text(data_store.TEX_HEADER.nr_mip_maps)
    with dpg.group(horizontal=True):
        dpg.add_text("Format:", wrap=150)
        dpg.add_text(str(data_store.TEX_HEADER.tex_format) + " (" + tex_format + ")")
    if data_store.TEX_HEADER.tex_format == 0:
        with dpg.group(horizontal=True):
            dpg.add_text("Compression:", wrap=150)
            dpg.add_text(str(data_store.TEX_HEADER.compression_format) + " ("+ compression_format +")")
    with dpg.group(horizontal=True):
        dpg.add_text("Compressed size:", wrap=150)
        dpg.add_text(str(len(data_store.SELECTED_FILE_DATA)) + " b")
    dpg.add_separator()
    dpg.add_text("Channels(?)", wrap=150)
    with dpg.tooltip(dpg.last_item()):
        dpg.add_text("You can use these properties to inspect the different channels of the textures. Some color textures contain information in the alpha (A) channel and will look beter if you disable that channel.", wrap=400)
        dpg.add_text("Note: the alpha channel to store transparency. depending how you want to use the texture, you might need to export the alpha channel in order for the models to look correct.", wrap=400)
    with dpg.group(horizontal=True):
        dpg.add_checkbox(label="R", default_value=True, user_data=data_store, callback=draw_tex_image, tag="tex_channel_r")
        dpg.add_checkbox(label="G", default_value=True, user_data=data_store, callback=draw_tex_image, tag="tex_channel_g")
        dpg.add_checkbox(label="B", default_value=True, user_data=data_store, callback=draw_tex_image, tag="tex_channel_b")
        dpg.add_checkbox(label="A", default_value=True, user_data=data_store, callback=draw_tex_image, tag="tex_channel_a")
    dpg.pop_container_stack()

def draw_tex_image(sender, keyword, data_store):
    dpg.delete_item("image_id")
    dpg.delete_item("texture_canvas", children_only=True)
    dpg.push_container_stack("texture_canvas")
    pil_image = data_store.PNG_FILE
    width = pil_image.width
    height = pil_image.height
    R,G,B,A = pil_image.split()
    if not dpg.get_value("tex_channel_r"):
        R = R.point(lambda i:i*0)
    if not dpg.get_value("tex_channel_g"):
        G = G.point(lambda i:i*0)
    if not dpg.get_value("tex_channel_b"):
        B = B.point(lambda i:i*0)
    pil_image = Image.merge('RGBA',(R,G,B,A))
    if not dpg.get_value("tex_channel_a"):
        pil_image.putalpha(255)
    data = np.frombuffer(pil_image.tobytes(), dtype=np.uint8) / 255.0
    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="image_id")
    with dpg.drawlist(width=700, height=700):
        dpg.draw_image("image_id", (0, 0), (700, 700), uv_min=(0, 0), uv_max=(1, 1))
    dpg.pop_container_stack()

def tex_template(data_store):
    dpg.delete_item("main_file_view", children_only=True, slot=1)
    dpg.push_container_stack("main_file_view")
    with dpg.child_window(width=200, autosize_y=True, border=True):
        with dpg.group(horizontal=True):
            dpg.add_text("Signature:", wrap=150)
            dpg.add_text("", tag="file_signature")
        with dpg.group(tag="file_details"):
            pass
        
        with dpg.child_window(width=200, autosize_x=True, border=True, tag="export_window"):
            pass
    with dpg.group(tag="texture_canvas"):
        pass

    dpg.pop_container_stack()

def m3_template(data_store):
    dpg.delete_item("main_file_view", children_only=True, slot=1)
    dpg.push_container_stack("main_file_view")
    with dpg.child_window(width=300, autosize_y=True, border=False):
        with dpg.group(horizontal=True):
            dpg.add_text("Signature:", wrap=150)
            dpg.add_text("", tag="file_signature")
        with dpg.group(tag="file_details"):
            pass
    with dpg.group():
        with dpg.child_window(width=520, height=540, border=True):
            with dpg.drawlist(width=500, height=500):
                with dpg.draw_layer(tag="main_3d_window", depth_clipping=False, perspective_divide=True, cull_mode=dpg.mvCullMode_Back):
                    pass

            with dpg.group(horizontal=True):
                dpg.add_button(label="Rotate Left", callback=rotate_model_left, user_data=data_store)
                dpg.add_button(label="Rotate Left", callback=rotate_model_right, user_data=data_store)
        with dpg.child_window(width=520, height=135, border=False, tag="export_window"):
            pass
    dpg.pop_container_stack()

def add_tex_export_details(data_store):
    dpg.delete_item("export_window", children_only=True, slot=1)
    dpg.push_container_stack("export_window")
    dpg.add_button(label="Export TEX", callback=export_raw_file, user_data=data_store)
    dpg.add_button(label="Export PNG", callback=export_png_image, user_data=data_store)
    dpg.pop_container_stack()

def redraw_model_mesh_variant(sender, keyword, data_store):
    children = dpg.get_item_children("visible_variants", 1)
    submesh_groups = ["variant_"+str(a_submesh_group.submesh_id) for a_submesh_group in data_store.LDOM_HEADER.submesh_groups]
    chosen_variant = 0
    for i, a_child in enumerate(children):
        chosen_variant = dpg.get_value(a_child)
    if chosen_variant == "Other":
        return
    group_id = submesh_groups.index(chosen_variant)
    data_store.CHOSEN_VARIANT = chosen_variant
    for i, a_submesh in enumerate(data_store.LDOM_HEADER.geometry.submesh):
        if a_submesh.group_id == group_id:
            data_store.MESHES_TO_DRAW[i] = True
        else:
            data_store.MESHES_TO_DRAW[i] = False
    add_m3_file_details(data_store)
    draw_3d_model(data_store)

def redraw_model_mesh(sender, keyword, data_store):
    children = dpg.get_item_children("visible_meshes", 1)
    meshes_to_draw = []
    for a_child in children:
        meshes_to_draw.append(dpg.get_value(a_child))
    data_store.MESHES_TO_DRAW = meshes_to_draw
    data_store.CHOSEN_VARIANT = "Other"
    add_m3_file_details(data_store)
    draw_3d_model(data_store)

def draw_3d_model(data_store):
    if data_store.LDOM_HEADER is None:
        return
    COLORS = [
        [255,255,255],
        [255,0,0],
        [0,255,0],
        [0,0,255],
        [255,255,0],
        [255,0,255],
        [0,255,255],
        [0,255,255],
        [255,255,0],
        [255,0,255],
        [255,0,255],
        [0,255,255],
        [255,255,0],
        [255,255,255],
        [255,255,255],
        [255,255,255],
    ]
    dpg.delete_item("main_3d_window", children_only=True, slot=2)
    dpg.push_container_stack("main_3d_window")
    bounds = [[9999,9999,9999], [-9999,-9999,-9999]]
    with dpg.draw_node(tag="cube"):
        for i, a_submesh in enumerate(data_store.LDOM_HEADER.geometry.submesh):
            if not data_store.MESHES_TO_DRAW[i]:
                continue
            indices = data_store.LDOM_HEADER.geometry.indices[a_submesh.startIndex:a_submesh.startIndex+a_submesh.nrIndex]
            points = data_store.LDOM_HEADER.geometry.vertex_positions[a_submesh.startVertex:a_submesh.startVertex+a_submesh.nrVertex]
            for a_point in points:
                if a_point[0] < bounds[0][0]:
                    bounds[0][0] = a_point[0]
                if a_point[0] > bounds[1][0]:
                    bounds[1][0] = a_point[0]

                if a_point[1] < bounds[0][1]:
                    bounds[0][1] = a_point[1]
                if a_point[1] > bounds[1][1]:
                    bounds[1][1] = a_point[1]

                if a_point[2] < bounds[0][2]:
                    bounds[0][2] = a_point[2]
                if a_point[2] > bounds[1][2]:
                    bounds[1][2] = a_point[2]
            triange_nr = int(len(indices)/3)
            color_id = i % len(COLORS)
            for a_triangle in range(triange_nr):
                p1 = points[indices[a_triangle*3]]
                p2 = points[indices[a_triangle*3+1]]
                p3 = points[indices[a_triangle*3+2]]
                dpg.draw_triangle(p1,p2,p3,color=[0,0,0],fill=COLORS[color_id])
    pos_x = abs(bounds[1][0] - bounds[0][0])
    pos_y = abs(bounds[1][1] - bounds[0][1])
    pos_z = abs(bounds[1][2] - bounds[0][2])
    scale = 450/max(pos_x, pos_y, pos_z)

    move_x = (500 - pos_x * scale)/2
    # print(move_x)
    view_matrix = dpg.create_fps_matrix([0, 0, 50], 0.0, 0.0)
    dpg.apply_transform("cube", view_matrix*dpg.create_rotation_matrix(math.pi*data_store.MODEL_ROTATION_Y/180.0 , [0, 1, 0]))
    dpg.set_clip_space("main_3d_window", 190, 365, scale, scale, -1.0, 1.0)
    dpg.pop_container_stack()

def select_file_callback(sender, app_data, data):
    data["data_store"].SELECTED_FILE_PATH = data["path"]
    load_file_on_right_panel(data_store)

def recursive_folders(path, data_store):
    for a_folder in data_store.DATA_MANAGER.get_folder_list(path):
        with dpg.tree_node(label=a_folder):
            recursive_folders(path+"\\"+a_folder, data_store)
            for a_file in data_store.DATA_MANAGER.get_file_list(path+"\\"+a_folder):
                data = {
                    "data_store": data_store,
                    "path": path+"\\"+a_folder+"\\"+a_file
                }
                dpg.add_button(label=a_file, callback=select_file_callback, user_data=data)

def rotate_model_right(sender, app_data, data_store):
    data_store.MODEL_ROTATION_Y -= 15
    view_matrix = dpg.create_fps_matrix([0, 0, 50], 0.0, 0.0)
    dpg.apply_transform("cube", view_matrix*dpg.create_rotation_matrix(math.pi*data_store.MODEL_ROTATION_Y/180.0 , [0, 1, 0]))
def rotate_model_left(sender, app_data, data_store):
    data_store.MODEL_ROTATION_Y += 15
    view_matrix = dpg.create_fps_matrix([0, 0, 50], 0.0, 0.0)
    dpg.apply_transform("cube", view_matrix*dpg.create_rotation_matrix(math.pi*data_store.MODEL_ROTATION_Y/180.0 , [0, 1, 0]))

def set_export_location(sender, app_data, data_store):
    data_store.EXPORT_LOCATION = app_data["file_path_name"]
    dpg.set_value("export_location", data_store.EXPORT_LOCATION)

def export_png_image(sender, app_data, data_store):
    
    R,G,B,A = data_store.PNG_FILE.split()
    if not dpg.get_value("tex_channel_r"):
        R = R.point(lambda i:i*0)
    if not dpg.get_value("tex_channel_g"):
        G = G.point(lambda i:i*0)
    if not dpg.get_value("tex_channel_b"):
        B = B.point(lambda i:i*0)
    pil_image = Image.merge('RGBA',(R,G,B,A))
    if not dpg.get_value("tex_channel_a"):
        pil_image.putalpha(255)
    export_location = os.path.join(data_store.EXPORT_LOCATION, data_store.SELECTED_FILE_NAME)
    export_location += ".png"
    pil_image.save(export_location)

def export_raw_file(sender, app_data, data_store):
    export_location = os.path.join(data_store.EXPORT_LOCATION, data_store.SELECTED_FILE_NAME)
    with open(export_location, "wb") as file:
        file.write(data_store.SELECTED_FILE_DATA)

def export_gltf_model(sender, app_data, data_store):
    data_store.EXPORT_FILTERS["submeshes"] = []
    for i, a_submesh_value in enumerate(data_store.LDOM_HEADER.geometry.submesh):
        if data_store.MESHES_TO_DRAW[i]:
            data_store.EXPORT_FILTERS["submeshes"].append(i)
    export_number = 1   # at least 1 3d model
    progress = 0
    dpg.set_value("export_progress", progress)
    textures = []
    # tex
    if data_store.EXPORT_FILTERS["textures"]:
        for i, a_submesh in enumerate(data_store.LDOM_HEADER.geometry.submesh):
            if i not in data_store.EXPORT_FILTERS["submeshes"]:
                continue
            material = data_store.LDOM_HEADER.materials[a_submesh.material_id]
            for a_matdesc in material.material_descriptions:
                color_tex_path = a_matdesc.texture_color
                normal_tex_path = a_matdesc.texture_normal
                if len(color_tex_path):
                    textures.append("AIDX\\"+color_tex_path)
                if len(color_tex_path):
                    textures.append("AIDX\\"+normal_tex_path)
        textures = set(textures)
    export_number += len(textures)
    # export textures
    for a_texture in textures:
        image_bytes = data_store.DATA_MANAGER.get_file_bytes(a_texture)
        tex = Tex.decode(io.BytesIO(image_bytes))
        file_name = os.path.basename(a_texture)
        if data_store.EXPORT_FILTERS["embed_textures"]:
            for a_m3_texture in data_store.LDOM_HEADER.textures:
                if a_m3_texture.path[:-1] in a_texture:
                    membuf = io.BytesIO()
                    tex.save(membuf, format="png")
                    png_data = membuf.getvalue()
                    a_m3_texture.byte_data = png_data
        else:
            export_location = os.path.join(data_store.EXPORT_LOCATION, file_name)
            export_location += ".png"
            tex.save(export_location)
        progress += 1
        dpg.set_value("export_progress", progress/export_number)
        dpg.configure_item("export_progress", overlay='{0:.2f}%'.format(progress/export_number*100))
    # export mesh
    file_name, extension = os.path.splitext(data_store.SELECTED_FILE_NAME)
    if data_store.CHOSEN_VARIANT != "Other":
        file_name += "_" + data_store.CHOSEN_VARIANT
    file_name += extension
    export_location = os.path.join(data_store.EXPORT_LOCATION, file_name)
    create_m3_skeleton(data_store.LDOM_HEADER, export_location, data_store.EXPORT_FILTERS)
    progress += 1
    dpg.set_value("export_progress", progress/export_number)
    dpg.configure_item("export_progress", overlay='{0:.2f}%'.format(progress/export_number*100))

def change_export_settings(sender, app_data, data_store):
    data_store.EXPORT_FILTERS['skeleton'] = dpg.get_value("export_settings_skeleton")
    data_store.EXPORT_FILTERS['textures'] = dpg.get_value("export_settings_textures")
    if not data_store.EXPORT_FILTERS['textures']:
        dpg.set_value("export_settings_embed_textures", False)
        dpg.configure_item("export_settings_embed_textures", enabled=False)
    else:
        dpg.configure_item("export_settings_embed_textures", enabled=True)
    data_store.EXPORT_FILTERS['embed_textures'] = dpg.get_value("export_settings_embed_textures")

def export_list_of_files(sender, app_data, data_store):
    dpg.add_loading_indicator(style=1,radius=12.5, tag="image_loading", parent="tab_mass_export", pos=[500,300])
    file_list = get_filtered_files()
    with open('file_list.txt', 'w') as f:
        for a_file_line in file_list:
            f.write(f"{a_file_line}\n")
    dpg.delete_item("image_loading")

def export_filtered_files(sender, app_data, data_store):
    dpg.add_loading_indicator(style=1,radius=12.5, tag="image_loading", parent="tab_mass_export", pos=[500,300])
    file_list = get_filtered_files(data_store)
    for a_file in file_list:
        file_name = os.path.basename(a_file)
        export_location = os.path.join(data_store.EXPORT_LOCATION, file_name)
        try:
            file_data = data_store.DATA_MANAGER.get_file_bytes(a_file)
            with open(export_location, "wb") as file:
                file.write(file_data)
        except:
            print("Could not find file: " + a_file)
    dpg.delete_item("image_loading")

def get_filtered_files(data_store):
    accepted_extensions = []
    filetype_selectors = dpg.get_item_children("filetype_selector", slot=1)
    for a_tag in filetype_selectors:
        if dpg.get_value(a_tag):
            accepted_extensions.append(dpg.get_item_label(a_tag))
    return get_all_files_recursively("AIDX", data_store, accepted_extensions)

def get_all_files_recursively(path, data_store, accepted_extensions):
    file_list = []
    for a_folder in data_store.DATA_MANAGER.get_folder_list(path):
        file_list.extend(get_all_files_recursively(path + "\\" + a_folder, data_store, accepted_extensions))
    for a_file in data_store.DATA_MANAGER.get_file_list(path):
        if os.path.splitext(a_file)[1] in accepted_extensions:
            file_list.append(path + "\\" + a_file)
    return file_list

def export_list_file_selected_callback(sender, app_data, data_store):
    selected_file = None
    for a_file in app_data["selections"]:
        selected_file = app_data["selections"][a_file]
    with open(selected_file) as file:
        lines = [line.rstrip() for line in file]
    data_store.LIST_TO_DOWNLOAD = lines
    dpg.delete_item("download_list", children_only=True)
    for a_line in lines:
        dpg.add_text(a_line, parent="download_list")

def mass_export(sender, app_data, data_store):
    export_filters = {
        "textures": True,
        "skeleton": True,
        "embed_textures": True,
        "submeshes": [-1],
    }
    export_number = len(data_store.LIST_TO_DOWNLOAD)
    progress = 0
    dpg.set_value("mass_export_progress", progress/export_number)
    dpg.configure_item("mass_export_progress", overlay='{0:.2f}%'.format(progress/export_number*100))
    for a_model_path in data_store.LIST_TO_DOWNLOAD:
        file_data = data_store.DATA_MANAGER.get_file_bytes(a_model_path)
        header = Header.read_header(io.BytesIO(file_data))
        for a_m3_texture in header.textures:
            image_bytes = data_store.DATA_MANAGER.get_file_bytes("AIDX\\"+a_m3_texture.path[:-1])
            tex = Tex.decode(io.BytesIO(image_bytes))
            membuf = io.BytesIO()
            tex.save(membuf, format="png")
            png_data = membuf.getvalue()
            a_m3_texture.byte_data = png_data
        file_name = os.path.basename(a_model_path)
        export_location = os.path.join(data_store.EXPORT_LOCATION, file_name)
        create_m3_skeleton(header, export_location, export_filters)
        progress += 1
        dpg.set_value("mass_export_progress", progress/export_number)
        dpg.configure_item("mass_export_progress", overlay='{0:.2f}%'.format(progress/export_number*100))



with dpg.window(label="Main", width=800, height=800, tag="main_window"):
    data_store = DataStore()
    data_store.DATA_MANAGER = DataManager()
    data_store.EXPORT_LOCATION = os.path.abspath(os.getcwd())
    # DIALOGS
    dpg.add_file_dialog(directory_selector=True, show=False, callback=set_export_location, tag="file_export_dialog_id", width=700 ,height=400, user_data=data_store)
    with dpg.file_dialog(directory_selector=False, show=False, callback=file_selected_callback, id="file_dialog_id", width=700 ,height=400, user_data=data_store):
        dpg.add_file_extension(".exe")
    with dpg.file_dialog(directory_selector=False, show=False, callback=export_list_file_selected_callback, id="export_list_file_dialog_id", width=700 ,height=400, user_data=data_store):
        dpg.add_file_extension(".*")
    
    # MAIN WINDOW
    with dpg.group(horizontal=True):
        dpg.add_button(label="Open Wildstar.exe", callback=lambda: dpg.show_item("file_dialog_id"))
        dpg.add_input_text(label="Wildstar.exe path", tag="wildstar_exe_location")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Export Location", callback=lambda: dpg.show_item("file_export_dialog_id"), user_data=data_store)
        dpg.add_input_text(default_value=data_store.EXPORT_LOCATION, label="Export path", tag="export_location")
    
    with dpg.tab_bar(tag="test_tab_bar") as tb:
        with dpg.tab(label="Explore Archive", tag="tab_explore_archive"):
            with dpg.group(horizontal=True):
                with dpg.child_window(tag="dir_tree", width=500, autosize_y=True, horizontal_scrollbar=True):
                    # recursive_folders("AIDX", data_store)
                    pass
                with dpg.child_window(tag="file_view", autosize_x=True, autosize_y=True, horizontal_scrollbar=True):
                    with dpg.group(horizontal=True):
                        dpg.add_text("File Name:", wrap=150)
                        dpg.add_text("", tag="right_title")
                    with dpg.group(horizontal=True):
                        dpg.add_text("File Path:", wrap=150)
                        dpg.add_text("", tag="right_path")
                    dpg.add_separator() 
                    with dpg.group(horizontal=True, tag="main_file_view"):
                        pass
        with dpg.tab(label="Mass Export (WIP)", tag="tab_mass_export"):
            with dpg.group(horizontal=True):
                with dpg.child_window(tag="download_list_of_files_window", width=200, autosize_y=True, horizontal_scrollbar=True):
                    with dpg.group(tag="filetype_selector"):
                        for a_file_type in data_store.ARCHIVE_FILE_TYPES:
                            dpg.add_checkbox(label=a_file_type, default_value=False)
                    dpg.add_button(label="Export list of files", user_data=data_store, callback=export_list_of_files)
                    dpg.add_button(label="Export raw files", user_data=data_store, callback=export_filtered_files)
                with dpg.child_window(tag="upload_list_window", width=500, autosize_y=True, horizontal_scrollbar=True, border=False):
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Upload list", callback=lambda: dpg.show_item("export_list_file_dialog_id"))
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text("Upload a list of .m3 file paths to convert. The list can be obtained from the left panel. Make sure to only include the paths to the objects that you want to download", wrap=500)
                            dpg.add_text("Example:")
                            dpg.add_text("AIDX\\Art\\Creature\\AshHen\\AshHen.m3")
                            dpg.add_text("AIDX\\Art\\Creature\\Ship\\Attack_Ship\\Attackship_defiance_000.m3")
                        dpg.add_text("(this can be very slow)")
                    with dpg.child_window(tag="download_list", height=500, autosize_x=True, horizontal_scrollbar=True):
                        pass
                    dpg.add_button(label="Start mass convert", user_data=data_store, callback=mass_export)
                    dpg.add_progress_bar(label="Export progress", default_value=0, overlay="",height=25, tag="mass_export_progress")

dpg.create_viewport(title='Wildstar Export 2', width=1400, height=850)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()
