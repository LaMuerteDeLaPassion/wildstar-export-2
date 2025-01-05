from m3reader import *
from gltf_utils import *
from pygltflib import GLTF2, Node, Skin, Scene, Animation, AnimationChannel, AnimationSampler, Accessor, Buffer, BufferView, FLOAT, VEC2, VEC3, VEC4, Primitive, Mesh, UNSIGNED_BYTE, MAT4, UNSIGNED_INT, UNSIGNED_SHORT, Image, Sampler, Texture, Material, PbrMetallicRoughness, NormalMaterialTexture
import pyrender
import trimesh
import base64
import os


def normalize(list_to_normalize):
    for a_item in list_to_normalize:
        mag = math.sqrt(a_item[0]**2+a_item[1]**2+a_item[2]**2)
        a_item[0] /= mag
        a_item[1] /= mag
        a_item[2] /= mag
    return list_to_normalize

def v3_to_v4(list_to_modify):
    list_to_modify = normalize(list_to_modify)
    for a_item in list_to_modify:
        a_item.append(-1)
    return list_to_modify


def create_material(m3, material_lists, material_id, export_filters):
    material = m3.materials[material_id]
    texture_ids = []
    for a_matdesc in material.material_descriptions:
        if not a_matdesc.texture_color:
            continue
        if not a_matdesc.texture_normal:
            continue
        color_tex_path = a_matdesc.texture_color
        normal_tex_path = a_matdesc.texture_normal

        tex_name = os.path.basename(color_tex_path)+'.png'
        norm_name = os.path.basename(normal_tex_path)+'.png'
        if export_filters["embed_textures"]:
            tex_name = bytearray(m3.textures[a_matdesc.texture_selector_a].byte_data)
            norm_name = bytearray(m3.textures[a_matdesc.texture_selector_b].byte_data)
            tex_name = base64.b64encode(tex_name).decode("utf-8")
            norm_name = base64.b64encode(norm_name).decode("utf-8")
            tex_name = f"data:image/png;base64,{tex_name}"
            norm_name = f"data:image/png;base64,{norm_name}"
        sampler_id = len(material_lists["samplers"])
        image_id = len(material_lists["images"])
        textures_id = len(material_lists["textures"])
        texture_ids.append(textures_id)

        material_lists["images"].append(Image(uri=tex_name))   # color
        material_lists["images"].append(Image(uri=norm_name))   # normal
        material_lists["samplers"].append(Sampler())
        material_lists["textures"].append(Texture(sampler=sampler_id, source=image_id))     # color
        material_lists["textures"].append(Texture(sampler=sampler_id, source=image_id+1))   # normal
    layers = []
    for a_texture_layer_id in texture_ids:
        layers.append({
            "texture": {"index": a_texture_layer_id},
        })
    if len(texture_ids):
        material = Material(
            pbrMetallicRoughness=PbrMetallicRoughness(baseColorTexture={"index": texture_ids[0]}),  # consider layer 0 to be the main layer
            normalTexture=NormalMaterialTexture(index=textures_id+1),
            extensions={
                "CUSTOM_materials_multilayer":{
                    "layers": layers,
                }
            }
        )
        material_lists["materials"].append(material)
    return material_lists

def create_accessor(binary_data, buffer_list, buffer_id, ofs, raw_data, data_type):
    if data_type == "float32":
        dtype = np.float32
        component_type = FLOAT
        accessor_type = "SCALAR"
    elif data_type == "float32v3":
        dtype = np.float32
        component_type = FLOAT
        accessor_type = VEC3
    elif data_type == "float32v4":
        dtype = np.float32
        component_type = FLOAT
        accessor_type = VEC4
    elif data_type == "float32m4":
        dtype = np.float32
        component_type = FLOAT
        accessor_type = MAT4
    elif data_type == "uint32":
        dtype = np.uint32
        component_type = UNSIGNED_INT
        accessor_type = "SCALAR"
    elif data_type == "uint16v4":
        dtype = np.uint16
        component_type = UNSIGNED_SHORT
        accessor_type = VEC4
    elif data_type == "float32v2":
        dtype = np.float32
        component_type = FLOAT
        accessor_type = VEC2

    raw_data = np.array(raw_data, dtype=dtype)
    raw_data_binary = raw_data.tobytes()

    binary_data += raw_data_binary
    buffer_view = BufferView(buffer=buffer_id, byteOffset=ofs, byteLength=len(raw_data_binary))
    ofs += len(raw_data_binary)

    accessor = Accessor(
        bufferView=len(buffer_list),
        byteOffset=0,
        componentType=component_type,
        count=len(raw_data),
        type=accessor_type
    )
    if accessor_type == "SCALAR":
        accessor.max.extend([float(max(raw_data))])
        accessor.min.extend([float(min(raw_data))])
    elif accessor_type in [VEC2, VEC3, VEC4]:
        accessor.max.extend(list(map(float, np.max(raw_data, axis=0))))
        accessor.min.extend(list(map(float, np.min(raw_data, axis=0))))
    buffer_list.append(buffer_view)
    return binary_data, accessor, buffer_list, ofs


def create_m3_skeleton(m3, file_name, export_filters):
    gltf = GLTF2()
    BUFFER_COUNT = 0
    buffer_list = []
    accessor_list = []
    if export_filters["skeleton"]:
        bones = []
        for a_bone in m3.bones:
            # using local matrices.         https://www.gamedev.net/forums/topic/271748-global-to-local-transformation---matrices-bones/
            a_bone.InverseTM[3,3] = 1    # fix to avoid validation errors
            bone_local_matrix = a_bone.TM
            if a_bone.parent_id > -1:
                bone_global_matrix = a_bone.TM
                parent_global_matrix_inverse = m3.bones[a_bone.parent_id].InverseTM
                bone_local_matrix = np.matmul(bone_global_matrix, parent_global_matrix_inverse)
            x = bone_local_matrix
            bone_local_matrix = [x[0,0], x[0,1], x[0,2], x[0,3], x[1,0], x[1,1], x[1,2], x[1,3],x[2,0], x[2,1], x[2,2], x[2,3],x[3,0], x[3,1], x[3,2], x[3,3]]
            t,r,s = decompose(bone_local_matrix)
            avg = math.sqrt(r[0]*r[0]+r[1]*r[1]+r[2]*r[2]+r[3]*r[3])
            r[0] /= avg
            r[1] /= avg
            r[2] /= avg
            r[3] /= avg
            bones.append(Node(name=a_bone.name, translation=t, rotation=r, scale=s))
            if a_bone.parent_id > -1:
                bones[a_bone.parent_id].children.append(a_bone.id)
        for a_bone in bones:
            gltf.nodes.append(a_bone)

        # Animation data
        bynary_stream = bytearray()
        ofs = 0
        sampler_list = []
        channel_list = []
        for a_bone in m3.bones:
            times_s = []
            scales = []
            for a_keyframe in a_bone.timestamps1.keyframes:
                times_s.append(a_keyframe.get_timestamp_in_seconds())
                scales.append(a_keyframe.scale)
            if len(times_s) > 0:
                bynary_stream, times_s_accessor, buffer_list, ofs = create_accessor(bynary_stream, buffer_list, BUFFER_COUNT, ofs, times_s, "float32")
                bynary_stream, scales_accessor, buffer_list, ofs = create_accessor(bynary_stream, buffer_list, BUFFER_COUNT, ofs, scales, "float32v3")
                # Create animation sampler
                s_sampler = AnimationSampler(
                    input=len(accessor_list),  # Index of the times accessor
                    output=len(accessor_list)+1,  # Index of the translations accessor
                    interpolation="LINEAR"
                )
                accessor_list.append(times_s_accessor)
                accessor_list.append(scales_accessor)
            
                s_channel = AnimationChannel(
                    sampler=len(sampler_list),
                    target={
                        "node": a_bone.id,  # Index of the child joint
                        "path": "scale"
                    }
                ),
                sampler_list.append(s_sampler)
                channel_list.extend(s_channel)

            times_r = []
            rotations = []
            for a_keyframe in a_bone.timestamps5.keyframes:
                times_r.append(a_keyframe.get_timestamp_in_seconds())
                rotations.append(a_keyframe.quaternion)
            if len(times_r) > 0:
                bynary_stream, times_r_accessor, buffer_list, ofs = create_accessor(bynary_stream, buffer_list, BUFFER_COUNT, ofs, times_r, "float32")
                bynary_stream, rotations_accessor, buffer_list, ofs = create_accessor(bynary_stream, buffer_list, BUFFER_COUNT, ofs, rotations, "float32v4")
                # Create animation sampler
                r_sampler = AnimationSampler(
                    input=len(accessor_list),  # Index of the times accessor
                    output=len(accessor_list)+1,  # Index of the translations accessor
                    interpolation="LINEAR"
                )
                accessor_list.append(times_r_accessor)
                accessor_list.append(rotations_accessor)
            
                r_channel = AnimationChannel(
                    sampler=len(sampler_list),
                    target={
                        "node": a_bone.id,  # Index of the child joint
                        "path": "rotation"
                    }
                ),
                sampler_list.append(r_sampler)
                channel_list.extend(r_channel)    # weird issue. must use extend, because AnimationChannel seems to return a list sometimes :/
            
            times_t = []
            translations = []
            for a_keyframe in a_bone.timestamps7.keyframes:
                times_t.append(a_keyframe.get_timestamp_in_seconds())
                translations.append(a_keyframe.translation)
            if len(times_t) > 0:           # 
                bynary_stream, times_t_accessor, buffer_list, ofs = create_accessor(bynary_stream, buffer_list, BUFFER_COUNT, ofs, times_t, "float32")
                bynary_stream, translations_accessor, buffer_list, ofs = create_accessor(bynary_stream, buffer_list, BUFFER_COUNT, ofs, translations, "float32v3")

                t_sampler = AnimationSampler(
                    input=len(accessor_list),  # Index of the times accessor
                    output=len(accessor_list)+1,  # Index of the translations accessor
                    interpolation="LINEAR"
                )
                accessor_list.append(times_t_accessor)
                accessor_list.append(translations_accessor)
                
                t_channel = AnimationChannel(
                    sampler=len(sampler_list),
                    target={
                        "node": a_bone.id,  # Index of the child joint
                        "path": "translation"
                    }
                ),
                sampler_list.append(t_sampler)
                channel_list.extend(t_channel)
        
        bynary_stream, inverse_bind_poses_accessor, buffer_list, ofs = create_accessor(bynary_stream, buffer_list, BUFFER_COUNT, ofs, [a_bone.InverseTM for a_bone in m3.bones], "float32m4")

        ibp_accessor_id = len(accessor_list)
        accessor_list.append(inverse_bind_poses_accessor)
        # Create the buffer and embed binary data
        encoded_binary = base64.b64encode(bynary_stream).decode('utf-8')
        animation_buffer = Buffer(
            uri="data:application/octet-stream;base64," + encoded_binary,
            byteLength=len(bynary_stream)
        )
        gltf.buffers.append(animation_buffer)
        BUFFER_COUNT = len(gltf.buffers)
        gltf.animations = [
            Animation(samplers=sampler_list, channels=channel_list)
        ]
    # Mesh data
    binary_stream_mesh = bytearray()
    ofs = 0
    primitive_list = []
    if export_filters["textures"]:
        material_lists = {
            "images": [],
            "samplers": [],
            "textures": [],
            "materials": []
        }
    for i, a_submesh in enumerate(m3.geometry.submesh):
        if i not in export_filters["submeshes"] and export_filters["submeshes"][0] != -1:
            continue
        indices = m3.geometry.indices[a_submesh.startIndex:a_submesh.startIndex+a_submesh.nrIndex]
        points = m3.geometry.vertex_positions[a_submesh.startVertex:a_submesh.startVertex+a_submesh.nrVertex]
        normals = m3.geometry.normals[a_submesh.startVertex:a_submesh.startVertex+a_submesh.nrVertex]
        tangents = m3.geometry.tangents[a_submesh.startVertex:a_submesh.startVertex+a_submesh.nrVertex]
        bitangents = m3.geometry.bitangents[a_submesh.startVertex:a_submesh.startVertex+a_submesh.nrVertex]   # not stored in gltf format. they are internally calculated from normals and tangents
        bone_indices = m3.geometry.bone_index[a_submesh.startVertex:a_submesh.startVertex+a_submesh.nrVertex]
        bone_weights = m3.geometry.bone_weights[a_submesh.startVertex:a_submesh.startVertex+a_submesh.nrVertex]
        uv1 = m3.geometry.uv1[a_submesh.startVertex:a_submesh.startVertex+a_submesh.nrVertex]
        uv2 = m3.geometry.uv2[a_submesh.startVertex:a_submesh.startVertex+a_submesh.nrVertex]
        vertex_colors = m3.geometry.vertexColor0[a_submesh.startVertex:a_submesh.startVertex+a_submesh.nrVertex]
        vertex_blends = m3.geometry.vertexBlend[a_submesh.startVertex:a_submesh.startVertex+a_submesh.nrVertex]

        # print("Tangents and Normals most likely still incorrect. see implementations and check with W* values")
        normals = normalize(normals)      # to avoid gltf complaints since w* encodes them using byte format.
        tangents = v3_to_v4(tangents)      # to avoid gltf complaints since w* encodes them using byte format.

        binary_stream_mesh, indices_accessor, buffer_list, ofs = create_accessor(binary_stream_mesh, buffer_list, BUFFER_COUNT, ofs, indices, "uint32")
        binary_stream_mesh, points_accessor, buffer_list, ofs = create_accessor(binary_stream_mesh, buffer_list, BUFFER_COUNT, ofs, points, "float32v3")
        binary_stream_mesh, normals_accessor, buffer_list, ofs = create_accessor(binary_stream_mesh, buffer_list, BUFFER_COUNT, ofs, normals, "float32v3")
        binary_stream_mesh, tangents_accessor, buffer_list, ofs = create_accessor(binary_stream_mesh, buffer_list, BUFFER_COUNT, ofs, tangents, "float32v4")
        if export_filters["skeleton"]:
            binary_stream_mesh, bone_indices_accessor, buffer_list, ofs = create_accessor(binary_stream_mesh, buffer_list, BUFFER_COUNT, ofs, bone_indices, "uint16v4")
            binary_stream_mesh, bone_weights_accessor, buffer_list, ofs = create_accessor(binary_stream_mesh, buffer_list, BUFFER_COUNT, ofs, bone_weights, "float32v4")
        binary_stream_mesh, uv1_accessor, buffer_list, ofs = create_accessor(binary_stream_mesh, buffer_list, BUFFER_COUNT, ofs, uv1, "float32v2")
        if len(uv2):
            binary_stream_mesh, uv2_accessor, buffer_list, ofs = create_accessor(binary_stream_mesh, buffer_list, BUFFER_COUNT, ofs, uv2, "float32v2")
        binary_stream_mesh, vertex_colors_accessor, buffer_list, ofs = create_accessor(binary_stream_mesh, buffer_list, BUFFER_COUNT, ofs, vertex_colors, "float32v4")
        if len(vertex_blends):
            binary_stream_mesh, vertex_blends_accessor, buffer_list, ofs = create_accessor(binary_stream_mesh, buffer_list, BUFFER_COUNT, ofs, vertex_blends, "uint16v4")

        # Material
        if export_filters["textures"]:
            material_lists = create_material(m3, material_lists, a_submesh.material_id, export_filters)

        prim = Primitive(
            indices=len(accessor_list),
            attributes={
                "POSITION": len(accessor_list)+1,
                "NORMAL": len(accessor_list)+2,
                "TANGENT": len(accessor_list)+3,
            }
        )
        accessor_list.append(indices_accessor)
        accessor_list.append(points_accessor)
        accessor_list.append(normals_accessor)
        accessor_list.append(tangents_accessor)
        if export_filters["skeleton"]:
            prim.attributes["JOINTS_0"] = len(accessor_list)
            accessor_list.append(bone_indices_accessor)
            prim.attributes["WEIGHTS_0"] = len(accessor_list)
            accessor_list.append(bone_weights_accessor)
        prim.attributes["TEXCOORD_0"] = len(accessor_list)   #UV Channel 0
        accessor_list.append(uv1_accessor)
        if len(uv2):
            prim.attributes["TEXCOORD_1"] = len(accessor_list)   #UV Channel 1
            accessor_list.append(uv2_accessor)
        prim.attributes["COLOR_0"] = len(accessor_list)   # Vertex Color
        accessor_list.append(vertex_colors_accessor)
        if len(vertex_blends):
            prim.attributes["COLOR_1"] = len(accessor_list)   # Texture blending factor
            accessor_list.append(vertex_blends_accessor)

        if export_filters["textures"]:
            prim.material = len(material_lists["materials"]) - 1
        primitive_list.append(prim)
        # break
    mesh = Mesh(primitives=primitive_list)
    # Create the buffer and embed binary data
    encoded_binary = base64.b64encode(binary_stream_mesh).decode('utf-8')
    geometry_buffer = Buffer(
        uri="data:application/octet-stream;base64," + encoded_binary,
        byteLength=len(binary_stream_mesh)
    )
    gltf.buffers.append(geometry_buffer)
    BUFFER_COUNT = len(gltf.buffers)
    gltf.meshes.append(mesh)
    if export_filters["textures"]:
        gltf.materials.extend(material_lists["materials"])
        gltf.textures.extend(material_lists["textures"])
        gltf.images.extend(material_lists["images"])
        gltf.samplers.extend(material_lists["samplers"])
    gltf.extensionsUsed.append("CUSTOM_materials_multilayer")

    gltf.bufferViews.extend(buffer_list)
    gltf.accessors.extend(accessor_list)
    # Create a skin that references these joints
    if export_filters["skeleton"]:
        skin = Skin(
            joints=[x.id for x in m3.bones],  # Indices of the joints
            skeleton=0,      # Index of the root joint
            inverseBindMatrices=ibp_accessor_id,
        )
        gltf.skins.append(skin)
    mesh_node = Node(mesh=0, name="Mesh")
    if export_filters["skeleton"]:
        mesh_node.skin = 0
    gltf.nodes.append(mesh_node)
    # Define the scene
    scene = Scene(nodes=[0, len(gltf.nodes)-1], name="SceneName")  # Add the root joint to the scene, and the mesh??
    gltf.scenes.append(scene)
    gltf.scene = 0  # Set the active scene
    # Save the GLTF
    gltf.save(file_name + ".gltf")


