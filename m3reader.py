from gltf_utils import *
import numpy as np
import struct
import array
import math


class Header:
    SIZE = 1584
    def __init__(self):
        self.name = None
        self.signature = None
        self.version = None
        self.nrUnk08 = None
        self.ofsUnk08 = None
        self.nrModelAnimations = None
        self.ofsModelAnimations = None
        self.nrAnimationRelated020 = None           # animation related
        self.ofsAnimationRelated020A = None           # animation related
        self.ofsAnimationRelated020B = None           # animation related
        self.nrUnk038 = None           # animation related
        self.ofsUnk038A = 0            # animation related
        self.ofsUnk038B = 0           # animation related
        self.nrUnk050 = 0            # animation related
        self.ofsUnk050A = 0           # animation related
        self.ofsUnk050B = 0            # animation related
        self.nrUnk068 = 0           # animation related
        self.ofsUnk068A = 0            # animation related
        self.ofsUnk068B = 0           # animation related
        self.nrUnk080 = 0 
        self.ofsUnk080 = 0
        self.nrUnk090 = 0 
        self.ofsUnk090A = 0
        self.ofsUnk090B = 0 
        self.nrUnk0A8 = 0
        self.ofsUnk0A8A = 0 
        self.ofsUnk0A8B = 0
        self.nrUnk0C0 = 0 
        self.ofsUnk0C0A = 0
        self.ofsUnk0C0B = 0 
        self.nrUnk0D8 = 0
        self.ofsUnk0D8A = 0 
        self.ofsUnk0D8B = 0
        self.nrUnk0F0 = 0           # always present looks important
        self.ofsUnk0F0 = 0          # always present looks important
        self.nrUnk100 = 0 
        self.ofsUnk100A = 0
        self.ofsUnk100B = 0 
        self.nrUnk118 = 0
        self.ofsUnk118A = 0 
        self.ofsUnk118B = 0
        self.nrUnk130 = 0 
        self.ofsUnk130A = 0
        self.ofsUnk130B = 0 
        self.nrUnk148 = 0
        self.ofsUnk148A = 0 
        self.ofsUnk148B = 0
        self.nrUnk160 = 0                # "holo" objects related
        self.ofsUnk160A = 0              # "holo" objects related
        self.ofsUnk160B = 0              # "holo" objects related
        self.ofsUnk170 = 0               # "holo" objects related
        self.nrBones = None
        self.ofsBones = None
        self.nrUnk190 = 0
        self.ofsUnk190 = 0
        self.nrUnk1A0 = 0
        self.ofsUnk1A0 = 0
        self.nrBonesTable = None
        self.ofsBonesTable = None
        self.nrTextures = None
        self.ofsTextures = None
        self.nrUnk1D0 = None
        self.ofsUnk1D0 = None
        self.nrUnk1E0 = 0 
        self.ofsUnk1E0 = 0
        self.nrMaterials = None
        self.ofsMaterials = None
        self.nrSubmeshGroupsTable = None
        self.ofsSubmeshGroupsTable = None
        self.nrUnk210 = 0
        self.ofsUnk210 = 0
        self.padding220 = 0       # 0 for all m3, padding
        self.padding228 = 0       # 0 for all m3, padding
        self.padding230 = 0       # 0 for all m3, padding
        self.padding238 = 0       # 0 for all m3, padding
        self.padding240 = 0       # 0 for all m3, padding
        self.padding248 = 0       # 0 for all m3, padding
        self.nrGeometry = None
        self.ofsGeometry = None
        self.nrUnk260 = 0 
        self.ofsUnk260 = 0
        self.nrUnk270 = 0 
        self.ofsUnk270 = 0
        self.nrUnk280 = 0 
        self.ofsUnk280 = 0
        self.nrUnk290 = 0 
        self.ofsUnk290A = 0
        self.ofsUnk290B = 0 
        self.padding2A8 = 0       # 0 for all m3, padding
        self.padding2B0 = 0       # 0 for all m3, padding
        self.nrUnk2B8 = 0
        self.ofsUnk2C0 = 0 
        self.nrUnk2C8 = 0
        self.ofsUnk2D0 = 0 
        self.padding2D0 = 0       # 0 for all m3, padding
        self.padding2E0 = 0       # 0 for all m3, padding
        self.padding2E8 = 0       # 0 for all m3, padding
        self.padding2F0 = 0       # 0 for all m3, padding
        self.nrUnk2F8 = 0
        self.ofsUnk300 = 0 
        self.nrUnk308 = 0
        self.ofsUnk310 = 0 
        self.nrUnk318 = 0
        self.ofsUnk320 = 0 
        self.nrUnk328 = 0
        self.ofsUnk330 = 0 
        self.nrUnk338 = 0
        self.nrUnk340 = 0 
        self.idUnk340 = 0       # some kind of id related to structure nrUnk350
        self.nrUnk350 = 0 
        self.ofsUnk350A = 0
        self.ofsUnk350B = 0 
        self.idUnk368 = 0       # some kind of id related to structure nrUnk370
        self.nrUnk370 = 0 
        self.ofsUnk370A = 0
        self.ofsUnk370B = 0 
        self.ofsUnk380 = 0
        self.nrUnk390 = 0 
        self.ofsUnk390 = 0
        self.nrUnk3A0 = 0 
        self.ofsUnk3A0 = 0
        self.nrUnk3B0 = 0 
        self.ofsUnk3B0 = 0
        self.nrUnk3C0 = 0 
        self.ofsUnk3C0 = 0      # 0 for all m3, padding
        self.nrUnk3D0 = 0 
        self.ofsUnk3D0 = 0
        self.nrUnk3E0 = 0 
        self.ofsUnk3E0 = 0
        self.nrUnk3F0 = 0 
        self.ofsUnk3F0 = 0
        self.nrUnk400 = 0
        self.ofsUnk400 = 0      # 0 for all m3, padding
        self.nrUnk410 = 0
        self.ofsUnk410 = 0
        self.nrUnk420 = 0
        self.ofsUnk420 = 0
        self.nrUnk430 = 0
        self.ofsUnk430 = 0
        self.nrUnk440 = 0
        self.ofsUnk440 = 0      # 0 for all m3, padding
        self.nrUnk450 = 0
        self.ofsUnk450 = 0
        self.nrUnk460 = 0
        self.ofsUnk460 = 0
        self.nrUnk470 = 0
        self.ofsUnk470 = 0
        self.nrUnk480 = 0
        self.ofsUnk480 = 0      # 0 for all m3, padding
        self.nrUnk490 = 0
        self.ofsUnk490 = 0
        self.nrUnk4A0 = 0
        self.ofsUnk4A0 = 0
        self.nrUnk4B0 = 0
        self.ofsUnk4B0 = 0
        self.nrUnk4C0 = 0
        self.ofsUnk4C0 = 0
        self.nrUnk4D0 = 0
        self.ofsUnk4D0 = 0
        self.nrUnk4E0 = 0
        self.ofsUnk4E0 = 0      # 0 for all m3, padding
        self.nrUnk4F0 = 0
        self.ofsUnk4F0 = 0
        self.nrUnk500 = 0
        self.ofsUnk500 = 0
        self.nrUnk510 = 0
        self.ofsUnk510 = 0
        self.nrUnk520 = 0
        self.ofsUnk520 = 0
        self.nrUnk530 = 0
        self.ofsUnk530 = 0
        self.nrUnk540 = 0       # mount related
        self.ofsUnk540 = 0
        self.nrUnk550 = 0       # mount related
        self.ofsUnk550 = 0
        self.nrUnk560 = 0
        self.ofsUnk560 = 0
        self.nrUnk570 = 0
        self.ofsUnk570 = 0
        self.idUnk580 = 0       # some kind of id related to structure nrUnk588 and 
        self.nrUnk588 = 0
        self.ofsUnk590 = 0
        self.nrUnk598 = 0
        self.ofsUnk5A0 = 0
        self.nrUnk5A8 = 0
        self.ofsUnk5B0 = 0
        self.ofsUnk5B0 = 0      # 0 for all m3, padding
        self.nrUnk5C0 = 0
        self.ofsUnk5C0A = 0
        self.ofsUnk5C0B = 0
        self.ofsUnk5D0 = 0
        self.nrUnk5E0 = 0
        self.ofsUnk5E0 = 0
        self.nrUnk5F0 = 0
        self.ofsUnk5F0 = 0
        self.nrUnk600 = 0
        self.ofsUnk600 = 0
        self.nrUnk610 = 0
        self.ofsUnk610 = 0
        self.nrUnk620 = 0
        self.ofsUnk620 = 0      # 0 for all m3, padding
        
    @staticmethod
    def read_header(br, only_header=False, name=None):
        header = Header()
        header.name = name
        # Read signature
        header.signature = br.read(4).decode('utf-8')
        # Read version
        header.version = struct.unpack('<I', br.read(4))[0]
        # print(f"VERSION: {header.version}")

        if header.version != 100:
            raise "unknown version {header.version}"

        # Read header data
        header.nrUnk08, header.ofsUnk08 = struct.unpack('<II', br.read(8))
        header.nrModelAnimations, header.ofsModelAnimations = struct.unpack('<qq', br.read(16))
        header.nrAnimationRelated020, header.ofsAnimationRelated020A, header.ofsAnimationRelated020B = struct.unpack('<qqq', br.read(24))
        header.nrUnk038, header.ofsUnk038A, header.ofsUnk038B = struct.unpack('<qqq', br.read(24))
        header.nrUnk050, header.ofsUnk050A, header.ofsUnk050B = struct.unpack('<qqq', br.read(24))
        header.nrUnk068, header.ofsUnk068A, header.ofsUnk068B = struct.unpack('<qqq', br.read(24))
        
        header.nrUnk080, header.ofsUnk080 = struct.unpack('<qq', br.read(16))

        header.nrUnk090, header.ofsUnk090A, header.ofsUnk090B = struct.unpack('<qqq', br.read(24))
        header.nrUnk0A8, header.ofsUnk0A8A, header.ofsUnk0A8B = struct.unpack('<qqq', br.read(24))
        header.nrUnk0C0, header.ofsUnk0C0A, header.ofsUnk0C0B = struct.unpack('<qqq', br.read(24))
        header.nrUnk0D8, header.ofsUnk0D8A, header.ofsUnk0D8B = struct.unpack('<qqq', br.read(24))
        header.nrUnk0F0, header.ofsUnk0F0 = struct.unpack('<qq', br.read(16))
        header.nrUnk100, header.ofsUnk100A, header.ofsUnk100B = struct.unpack('<qqq', br.read(24))
        header.nrUnk118, header.ofsUnk118A, header.ofsUnk118B = struct.unpack('<qqq', br.read(24))
        header.nrUnk130, header.ofsUnk130A, header.ofsUnk130B = struct.unpack('<qqq', br.read(24))
        header.nrUnk148, header.ofsUnk148A, header.ofsUnk148B = struct.unpack('<qqq', br.read(24))
        header.nrUnk160, header.ofsUnk160A, header.ofsUnk160B = struct.unpack('<qqq', br.read(24))
        header.ofsUnk170 = struct.unpack('<q', br.read(8))
        br.seek(0x180, 0)
        header.nrBones, header.ofsBones = struct.unpack("<qq", br.read(16))
        header.nrUnk190, header.ofsUnk190 = struct.unpack('<qq', br.read(16))
        header.nrUnk1A0, header.ofsUnk1A0 = struct.unpack('<qq', br.read(16))

        br.seek(0x1B0, 0)
        header.nrBonesTable, header.ofsBonesTable = struct.unpack("<qq", br.read(16))

        br.seek(0x1C0, 0)
        header.nrTextures, header.ofsTextures = struct.unpack("<qq", br.read(16))

        header.nrUnk1D0, header.ofsUnk1D0 = struct.unpack("<qq", br.read(16))
        header.nrUnk1E0, header.ofsUnk1E0 = struct.unpack('<qq', br.read(16))

        br.seek(0x1F0, 0)
        header.nrMaterials, header.ofsMaterials = struct.unpack("<qq", br.read(16))

        br.seek(0x200, 0)
        header.nrSubmeshGroupsTable, header.ofsSubmeshGroupsTable = struct.unpack("<qq", br.read(16))
        header.nrUnk210, header.ofsUnk210 = struct.unpack('<qq', br.read(16))
        header.padding220, header.padding228 = struct.unpack('<qq', br.read(16))
        header.padding230, header.padding238 = struct.unpack('<qq', br.read(16))
        header.padding240, header.padding248 = struct.unpack('<qq', br.read(16))

        br.seek(0x250, 0)
        header.nrGeometry, header.ofsGeometry = struct.unpack("<qq", br.read(16))

        header.nrUnk260, header.ofsUnk260 = struct.unpack('<qq', br.read(16))
        header.nrUnk270, header.ofsUnk270 = struct.unpack('<qq', br.read(16))
        header.nrUnk280, header.ofsUnk280 = struct.unpack('<qq', br.read(16))
        header.nrUnk290, header.ofsUnk290A, header.ofsUnk290B = struct.unpack('<qqq', br.read(24))
        header.padding2A8, header.padding2B0 = struct.unpack('<qq', br.read(16))
        header.nrUnk2B8, header.ofsUnk2C0 = struct.unpack('<qq', br.read(16))
        header.nrUnk2C8, header.ofsUnk2D0 = struct.unpack('<qq', br.read(16))
        header.padding2D0, header.padding2E0 = struct.unpack('<qq', br.read(16))
        header.padding2E0, header.padding2F0 = struct.unpack('<qq', br.read(16))
        header.nrUnk2F8, header.ofsUnk300 = struct.unpack("<qq", br.read(16))

        header.nrUnk308, header.ofsUnk310 = struct.unpack("<qq", br.read(16))
        header.nrUnk318, header.ofsUnk320 = struct.unpack("<qq", br.read(16))
        header.nrUnk328, header.ofsUnk330 = struct.unpack("<qq", br.read(16))
        header.nrUnk338, header.nrUnk340 = struct.unpack("<qq", br.read(16))
        header.idUnk340 = struct.unpack("<q", br.read(8))
        header.nrUnk350, header.ofsUnk350A = struct.unpack("<qq", br.read(16))
        header.ofsUnk350B, header.idUnk368 = struct.unpack("<qq", br.read(16))
        header.nrUnk370, header.ofsUnk370A = struct.unpack("<qq", br.read(16))
        header.ofsUnk370B, header.ofsUnk380 = struct.unpack("<qq", br.read(16))
        header.nrUnk390, header.ofsUnk390 = struct.unpack("<qq", br.read(16))
        header.nrUnk3A0, header.ofsUnk3A0 = struct.unpack("<qq", br.read(16))
        header.nrUnk3B0, header.ofsUnk3B0 = struct.unpack("<qq", br.read(16))
        header.nrUnk3C0, header.ofsUnk3C0 = struct.unpack("<qq", br.read(16))
        header.nrUnk3D0, header.ofsUnk3D0 = struct.unpack("<qq", br.read(16))
        header.nrUnk3E0, header.ofsUnk3E0 = struct.unpack("<qq", br.read(16))
        header.nrUnk3F0, header.ofsUnk3F0 = struct.unpack("<qq", br.read(16))

        header.nrUnk400, header.ofsUnk400 = struct.unpack("<qq", br.read(16))
        header.nrUnk410, header.ofsUnk410 = struct.unpack("<qq", br.read(16))
        header.nrUnk420, header.ofsUnk420 = struct.unpack("<qq", br.read(16))
        header.nrUnk430, header.ofsUnk430 = struct.unpack("<qq", br.read(16))
        header.nrUnk440, header.ofsUnk440 = struct.unpack("<qq", br.read(16))
        header.nrUnk450, header.ofsUnk450 = struct.unpack("<qq", br.read(16))
        header.nrUnk460, header.ofsUnk460 = struct.unpack("<qq", br.read(16))
        header.nrUnk470, header.ofsUnk470 = struct.unpack("<qq", br.read(16))
        header.nrUnk480, header.ofsUnk480 = struct.unpack("<qq", br.read(16))
        header.nrUnk490, header.ofsUnk490 = struct.unpack("<qq", br.read(16))
        header.nrUnk4A0, header.ofsUnk4A0 = struct.unpack("<qq", br.read(16))
        header.nrUnk4B0, header.ofsUnk4B0 = struct.unpack("<qq", br.read(16))
        header.nrUnk4C0, header.ofsUnk4C0 = struct.unpack("<qq", br.read(16))
        header.nrUnk4D0, header.ofsUnk4D0 = struct.unpack("<qq", br.read(16))
        header.nrUnk4E0, header.ofsUnk4E0 = struct.unpack("<qq", br.read(16))
        header.nrUnk4F0, header.ofsUnk4F0 = struct.unpack("<qq", br.read(16))
        
        header.nrUnk500, header.ofsUnk500 = struct.unpack("<qq", br.read(16))
        header.nrUnk510, header.ofsUnk510 = struct.unpack("<qq", br.read(16))
        header.nrUnk520, header.ofsUnk520 = struct.unpack("<qq", br.read(16))
        header.nrUnk530, header.ofsUnk530 = struct.unpack("<qq", br.read(16))
        header.nrUnk540, header.ofsUnk540 = struct.unpack("<qq", br.read(16))
        header.nrUnk550, header.ofsUnk550 = struct.unpack("<qq", br.read(16))
        header.nrUnk560, header.ofsUnk560 = struct.unpack("<qq", br.read(16))
        header.nrUnk570, header.ofsUnk570 = struct.unpack("<qq", br.read(16))
        header.idUnk580, header.nrUnk588 = struct.unpack("<qq", br.read(16))
        header.ofsUnk590, header.nrUnk598 = struct.unpack("<qq", br.read(16))
        header.ofsUnk5A0, header.nrUnk5A8 = struct.unpack("<qq", br.read(16))
        header.ofsUnk5B0, header.ofsUnk5B0 = struct.unpack("<qq", br.read(16))
        header.nrUnk5C0, header.ofsUnk5C0A = struct.unpack("<qq", br.read(16))
        header.ofsUnk5C0B, header.ofsUnk5D0 = struct.unpack("<qq", br.read(16))
        header.nrUnk5E0, header.ofsUnk5E0 = struct.unpack("<qq", br.read(16))
        header.nrUnk5F0, header.ofsUnk5F0 = struct.unpack("<qq", br.read(16))
        
        header.nrUnk600, header.ofsUnk600 = struct.unpack("<qq", br.read(16))
        header.nrUnk610, header.ofsUnk610 = struct.unpack("<qq", br.read(16))
        header.nrUnk620, header.ofsUnk620 = struct.unpack("<qq", br.read(16))
        
        if only_header:
            return header
        # BONE MAPPING
        if header.nrBonesTable > 0:
            header.boneMapping = []
            bone_table_start = header.SIZE + header.ofsBonesTable;
            br.seek(bone_table_start)
            header.boneMapping = struct.unpack("<"+"".join(["H" for _ in range(header.nrBonesTable)]), br.read(2*header.nrBonesTable))
        #  READ OBJECTS
        header.model_animations = ModelAnimation.read_all(br, header)
        header.bones = Bone.read_all_bones(br, header)
        header.textures = Texture.read_all(br, header)
        header.materials = M3Material.read_all(br, header)
        header.submesh_groups = SubmeshGroupTable.read_all(br, header)
        header.geometry = Geometry.ReadGeometry(br, header)
        return header

    def print(self):
        # Print all fields
        print("Header Fields and Values:")
        for field, value in vars(self).items():
            print(f"{field}: {value}")
        self.geometry.print("--")

class Geometry:
    SIZE = 208
    def __init__(self):
        self.unk004 = 0
        self.unk008 = 0
        self.unk00B = 0
        self.unk010 = 0
        self.unk014 = 0
        self.unk018 = 0
        self.nrVertices = 0
        self.vertexSize = 0
        self.vertexFlags = 0
        self.vertexFieldTypes = [0] * 11
        self.unk02B = 0
        self.unk030 = 0
        self.unk034 = 0
        self.unk038 = 0
        self.unk03B = 0
        self.unk040 = 0
        self.unk044 = 0
        self.unk048 = 0
        self.unk04B = 0
        self.unk050 = 0
        self.unk054 = 0
        self.unk058 = 0
        self.unk05B = 0
        self.unk060 = 0
        self.unk064 = 0
        self.unk068 = 0
        self.nrIndices = 0
        self.indexFlags = 0     # 256 - 2 bit indices, 512 - 4 bit indices
        self.ofsIndices = 0
        self.nrSubmeshes = 0
        self.ofsSubmeshes = 0
        self.unk0 = 0
        self.nrUnk1 = 0
        self.ofsUnk1 = 0
        self.nrUnk2 = 0
        self.ofsUnk2 = 0
        self.nrUnk3 = 0
        self.ofsUnk3 = 0
        self.vertex_positions = []
        self.tangents = []
        self.normals = []
        self.bitangents = []
        self.uv1 = []
        self.uv2 = []
        self.vertexColor0 = []
        self.vertexBlend = []
        self.bone_index = []
        self.bone_weights = []
        self.indices = []
        self.submesh = []

    @staticmethod
    def ReadGeometry(br, header):
        geometry = Geometry()
        geometryOfs = header.SIZE + header.ofsGeometry;
        br.seek(geometryOfs)
        geometry.unk004, geometry.unk008 = struct.unpack("<II", br.read(8))
        geometry.unk00B, geometry.unk010 = struct.unpack("<II", br.read(8))
        geometry.unk014, geometry.unk018 = struct.unpack("<II", br.read(8))
        # Move to the vertex data section
        br.seek(geometryOfs + 0x18)
        geometry.nrVertices, = struct.unpack("<I", br.read(4))
        geometry.vertexSize, geometry.vertexFlags = struct.unpack("<Hh", br.read(4))    #0x020
        
        # Read vertex field types
        geometry.vertexFieldTypes = list(struct.unpack("<11B", br.read(11)))
        geometry.unk02B, = struct.unpack("<B", br.read(1))
        geometry.unk030, = struct.unpack("<I", br.read(4))  #030
        geometry.unk034, geometry.unk038 = struct.unpack("<II", br.read(8))
        geometry.unk03B, geometry.unk040 = struct.unpack("<II", br.read(8)) #0x40
        geometry.unk044, geometry.unk048 = struct.unpack("<II", br.read(8))
        geometry.unk04B, geometry.unk050 = struct.unpack("<II", br.read(8)) #0x50
        geometry.unk054, geometry.unk058 = struct.unpack("<II", br.read(8))
        geometry.unk05B, geometry.unk060 = struct.unpack("<II", br.read(8)) #0x60
        geometry.unk064, geometry.unk068 = struct.unpack("<II", br.read(8))
        # Move to index count and offset
        br.seek(geometryOfs + 0x68)
        geometry.nrIndices, = struct.unpack("<I", br.read(4))
        geometry.indexFlags = struct.unpack("<h", br.read(2))[0]
        br.seek(geometryOfs + 0x78)
        geometry.ofsIndices, = struct.unpack("<I", br.read(4))
        
        # Move to submesh count and offset
        br.seek(geometryOfs + 0x80)
        geometry.nrSubmeshes, = struct.unpack("<I", br.read(4))
        br.seek(geometryOfs + 0x88)
        geometry.ofsSubmeshes, = struct.unpack("<I", br.read(4))
        
        # Read unknown fields
        br.seek(geometryOfs + 0x90)
        geometry.unk0, = struct.unpack("<I", br.read(4))
        br.seek(geometryOfs + 0x98)
        geometry.nrUnk1, = struct.unpack("<I", br.read(4))
        br.seek(geometryOfs + 0xA0)
        geometry.ofsUnk1, = struct.unpack("<I", br.read(4))
        br.seek(geometryOfs + 0xA8)
        geometry.nrUnk2, = struct.unpack("<I", br.read(4))
        br.seek(geometryOfs + 0xB0)
        geometry.ofsUnk2, = struct.unpack("<I", br.read(4))
        br.seek(geometryOfs + 0xB8)
        geometry.nrUnk3, = struct.unpack("<I", br.read(4))
        br.seek(geometryOfs + 0xC0)
        geometry.ofsUnk3, = struct.unpack("<I", br.read(4))
        
        # Read indices
        indexOfs = geometryOfs + Geometry.SIZE + geometry.ofsIndices
        br.seek(indexOfs)
        if geometry.indexFlags & 0x0100 == 256:
            geometry.indices = [struct.unpack("<H", br.read(2))[0] for _ in range(geometry.nrIndices)]
        if geometry.indexFlags & 0x0200 == 512:
            geometry.indices = [struct.unpack("<I", br.read(4))[0] for _ in range(geometry.nrIndices)]

        # Read vertices (simplified example)
        vertexStart = geometryOfs + Geometry.SIZE
        for i in range(geometry.nrVertices):
            vertexOfs = vertexStart + i * geometry.vertexSize
            br.seek(vertexOfs)
            if (geometry.vertexFlags & 0x0001) == 1:  # Position
                geometry.vertex_positions.append(VertexReadV3(br, geometry.vertexFieldTypes[0]))
            if (geometry.vertexFlags & 0x0002) == 2:  # Tangents
                geometry.tangents.append(VertexReadV3(br, geometry.vertexFieldTypes[1]))
            # Read normals (3 floats)
            if (geometry.vertexFlags & 0x0004) == 4:
                geometry.normals.append(VertexReadV3(br, geometry.vertexFieldTypes[2]))
            # Read bitangents (3 floats)
            if (geometry.vertexFlags & 0x0008) == 8:
                geometry.bitangents.append(VertexReadV3(br, geometry.vertexFieldTypes[3]))
            # Read bone indices (4 bytes)
            if (geometry.vertexFlags & 0x0010) == 16:
                x = list(VertexReadV4(br, geometry.vertexFieldTypes[4]))
                geometry.bone_index.append(x)
            else:
                geometry.bone_index.append([0,0,0,0])
            # Read bone weights (4 bytes)
            if (geometry.vertexFlags & 0x0020) != 0:
                geometry.bone_weights.append([x/255.0 for x in VertexReadV4(br, geometry.vertexFieldTypes[5])])
            else:
                geometry.bone_weights.append((1.0, 0.0, 0.0, 0.0))
            # Read vertex color (4 bytes as RGBA)
            if (geometry.vertexFlags & 0x0040) != 0:
                geometry.vertexColor0.append([x/255.0 for x in VertexReadV4(br, geometry.vertexFieldTypes[6])])
            else:
                geometry.vertexColor0.append((1.0, 1.0, 1.0, 1.0))
            # Read blend weights for vertex blending (4 floats)
            if (geometry.vertexFlags & 0x0080) != 0:
                geometry.vertexBlend.append(VertexReadV4(br, geometry.vertexFieldTypes[7]))
            # Read UV1 (2 floats)
            if (geometry.vertexFlags & 0x0100) != 0:
                geometry.uv1.append(VertexReadV2(br, geometry.vertexFieldTypes[8]))
            # Read UV2 (2 floats)
            if (geometry.vertexFlags & 0x0200) != 0:
                geometry.uv2.append(VertexReadV2(br, geometry.vertexFieldTypes[9]))

        # Read submeshes
        submeshOfs = geometryOfs + Geometry.SIZE + geometry.ofsSubmeshes
        geometry.submesh = []
        for _ in range(geometry.nrSubmeshes):
            br.seek(submeshOfs)
            submesh = Submesh()
            submesh.startIndex, submesh.startVertex, submesh.nrIndex, submesh.nrVertex = struct.unpack("<IIII", br.read(16))
            submesh.startBoneMapping, submesh.nrBoneMapping, unk1 = struct.unpack("<HHH", br.read(6))
            submesh.material_id, submesh.unk2, submesh.unk3, submesh.unk4, submesh.group_id, submesh.unk_Group_related = struct.unpack("<HHHHBB", br.read(10))

            submesh.color0 = struct.unpack("<BBBB", br.read(4))
            submesh.color1 = struct.unpack("<BBBB", br.read(4))
            submesh.boundMin = struct.unpack("<ffff", br.read(16))
            submesh.boundMax = struct.unpack("<ffff", br.read(16))
            submesh.unkVec4 = struct.unpack("<ffff", br.read(16))
            geometry.submesh.append(submesh)

            #  HANDLE BONE MAPPING
            boneSubmap = []
            for i in range(submesh.startBoneMapping, submesh.startBoneMapping + submesh.nrBoneMapping):
                boneSubmap.append(header.boneMapping[i])
            for j in range(submesh.startVertex, submesh.startVertex + submesh.nrVertex):
                if geometry.bone_weights[j][0] > 0:
                    geometry.bone_index[j][0] = boneSubmap[geometry.bone_index[j][0]]
                if geometry.bone_weights[j][1] > 0:
                    geometry.bone_index[j][1] = boneSubmap[geometry.bone_index[j][1]]
                if geometry.bone_weights[j][2] > 0:
                    geometry.bone_index[j][2] = boneSubmap[geometry.bone_index[j][2]]
                if geometry.bone_weights[j][3] > 0:
                    geometry.bone_index[j][3] = boneSubmap[geometry.bone_index[j][3]]
            submeshOfs += 0x70  # Increment offset to next submesh
        return geometry

    def print(self, pre=None):
        prepend = ""
        if pre is not None:
            prepend = pre
        # Print all fields
        print("Geometry Fields and Values:")
        for field, value in vars(self).items():
            try:
                if len(value) > 1000:
                    print(f"{prepend}{field}: len()={len(value)}")
                else:
                    print(f"{prepend}{field}: {value}")
            except:
                print(f"{prepend}{field}: {value}")
        for a_submesh in self.submesh:
            a_submesh.print("----")

class Submesh:
    def __init__(self):
        self.startIndex = 0
        self.startVertex = 0
        self.nrIndex = 0
        self.nrVertex = 0
        self.startBoneMapping = 0
        self.nrBoneMapping = 0
        self.unk1 = 0
        self.material_id = 0
        self.unk2 = 0
        self.unk3 = 0
        self.unk4 = 0
        self.group_id = 0
        self.unk_Group_related = 0
        self.unk5 = 0
        self.unk6 = 0
        self.unk7 = 0
        self.unk8 = 0
        self.unk9 = 0
        self.unk10 = 0
        self.unk11 = 0
        self.unk12 = 0
        self.color0 = (0, 0, 0, 0)
        self.color1 = (0, 0, 0, 0)
        self.unk13 = 0
        self.unk14 = 0
        self.unk15 = 0
        self.unk16 = 0
        self.unk17 = 0
        self.unk18 = 0
        self.unk19 = 0
        self.unk20 = 0
        self.boundMin = (0.0, 0.0, 0.0, 0.0)
        self.boundMax = (0.0, 0.0, 0.0, 0.0)
        self.unkVec4 = (0.0, 0.0, 0.0, 0.0)

    def print(self, pre=None):
        prepend = ""
        if pre is not None:
            prepend = pre
        print("Submesh Fields and Values:")
        for field, value in vars(self).items():
            print(f"{prepend}{field}: {value}")

class Texture:
    SIZE = 32

    def __init__(self):
        self.unk0 = 0
        self.type = 0
        self.unk1 = 0
        self.unk2 = 0
        self.unk3 = 0.0
        self.unk4 = 0
        self.unk5 = 0
        self.unk6 = 0
        self.unk7 = 0
        self.nr_letters = 0
        self.offset = 0

        self.path = ""
        self.texture_type = "unset"

    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.ofsTextures
        nr = m3.nrTextures

        textures = []
        for i in range(nr):
            # Seek to the texture data start
            br.seek(start_pos + i * Texture.SIZE)

            # Read the fixed-size fields
            texture = Texture()
            texture.unk0, = struct.unpack("<h", br.read(2))     # could this tie in to player customizations??
            texture.type, = struct.unpack("<B", br.read(1))
            texture.unk1, = struct.unpack("<B", br.read(1))
            texture.unk2, = struct.unpack("<i", br.read(4))     # flags?
            texture.unk3, = struct.unpack("<f", br.read(4))     # reflectivity, transparency, or intensity???
            texture.unk4, texture.unk5, texture.unk6, texture.unk7 = struct.unpack("<4B", br.read(4))
            texture.nr_letters, texture.offset = struct.unpack("<QQ", br.read(16))

            # Read the texture path
            br.seek(start_pos + nr * Texture.SIZE + texture.offset)
            path_data = br.read(texture.nr_letters * 2)  # Assuming 2 bytes per letter (Unicode)
            texture.path = path_data.decode("utf-16").encode("utf-8").decode("utf-8")  # Convert UTF-16 to UTF-8
            if texture.type == 0:
                texture.texture_type = "color"
            elif texture.type == 1:
                texture.texture_type = "normal"
            else:   #specular, emissive??
                texture.texture_type = "unk: " + str(texture.type)
            # texture.print()
            textures.append(texture)

        return textures

    def print(self):
        pr = (
            f"TEXTURE: {self.unk0}\t{self.texture_type}\t{self.unk1}\t{self.unk2}\t{self.unk3}\t"
            f"{self.unk4}\t{self.unk5}\t{self.unk6}\t{self.unk7}\t{self.nr_letters}\t"
            f"{self.offset}\t{self.path}"
        )
        print(pr)

class M3Material:
    SIZE = 0x30

    def __init__(self):
        self.unk0 = 0
        self.unk1 = 0
        self.unk2 = 0
        self.unk3 = 0
        self.unk4 = 0
        self.unk5 = 0
        self.unk6 = 0
        self.unk7 = 0
        self.unk8 = 0
        self.unk9 = 0
        self.unk10 = 0
        self.unk11 = 0
        self.unk12 = 0  # UInt16
        self.unk14 = 0  # UInt16 (padding)
        self.unk16 = 0  # UInt32
        self.unk20 = 0  # UInt32
        self.cb1_28_x = 0  # Specular multiplier x (int) value is sent directly to shader
        self.cb1_28_y = 0  # Specular multiplier y (int) value is sent directly to shader
        self.nr_material_descriptions = 0  # UInt64
        self.ofs_material_descriptions = 0  # UInt64

        self.material_descriptions = []  # List of MaterialDescription objects

    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.ofsMaterials
        nr = m3.nrMaterials

        materials = []
        for i in range(nr):
            # Seek to the start of the current material
            br.seek(start_pos + i * M3Material.SIZE)

            # Create an M3Material instance and populate its fields
            material = M3Material()
            material.unk0, material.unk1, material.unk2, material.unk3 = struct.unpack("<BBBB", br.read(4))
            material.unk4, material.unk5, material.unk6, material.unk7 = struct.unpack("<BBBB", br.read(4))
            material.unk8, material.unk9, material.unk10, material.unk11 = struct.unpack("<BBBB", br.read(4))
            material.unk12, material.unk14 = struct.unpack("<HH", br.read(4))
            material.unk16, material.unk20 = struct.unpack("<II", br.read(8))
            material.cb1_28_x, material.cb1_28_y = struct.unpack("<ii", br.read(8))
            material.nr_material_descriptions, material.ofs_material_descriptions = struct.unpack("<QQ", br.read(16))

            # material.print()
            # Read material descriptions
            mat_des_start_pos = start_pos + nr * M3Material.SIZE + material.ofs_material_descriptions
            material.material_descriptions = MaterialDescription.read_all(br, mat_des_start_pos, material.nr_material_descriptions, m3)

            materials.append(material)

        return materials

    def print(self):
        fields = vars(self)
        pr = "\t".join(f"{field}: {value}" for field, value in fields.items())
        print(f"MATERIAL: {pr}")

class MaterialDescription:
    SIZE = 296

    def __init__(self):
        self.texture_selector_a = 0
        self.texture_selector_b = 0
        self.unk_values = [0] * 146  # 146 UInt16 fields
        self.texture_color = ""
        self.texture_normal = ""

    @staticmethod
    def read_all(br, start_pos, nr, m3):
        material_descriptions = []

        for i in range(nr):
            br.seek(start_pos + i * MaterialDescription.SIZE)

            material_description = MaterialDescription()

            material_description.texture_selector_a, material_description.texture_selector_b = struct.unpack("<hh", br.read(4))

            # Read 146 UInt16 fields
            material_description.unk_values = list(struct.unpack("<146H", br.read(292)))

            # Resolve texture paths if selectors are valid
            if material_description.texture_selector_a > -1:
                texture_a = m3.textures[material_description.texture_selector_a]
                material_description.texture_color = texture_a.path.split(".")[0] + ".tex"

            if material_description.texture_selector_b > -1:
                texture_b = m3.textures[material_description.texture_selector_b]
                material_description.texture_normal = texture_b.path.split(".")[0] + ".tex"

            # material_description.print(0)
            material_descriptions.append(material_description)

        return material_descriptions

    def print(self, id):
        fields = vars(self)
        pr = "\t".join(f"{field}: {value}" for field, value in fields.items())
        print(f"MATERIAL DESCRIPTION {id}: {pr}")

class Bone:
    SIZE = 176*2
    def __init__(self):
        self.name = ""
        self.id = 0
        self.unk00 = 0
        self.parent_id = -1
        self.unk01 = 0
        self.unk02 = 0
        self.unk03 = 0
        self.unk04 = 0
        self.unk05 = 0
        self.unk06 = 0
        self.rotationMatrix = None      # maybe? most likely not though...
        self.timestamps1 = None
        self.timestamps2 = None
        self.timestamps3 = None
        self.timestamps4 = None
        self.timestamps5 = None
        self.timestamps6 = None
        self.timestamps7 = None
        self.timestamps8 = None
        self.TM = None
        self.InverseTM = None
        self.position = None
        self.parent_path = ""
        self.TM_raw = None

    @staticmethod
    def read_all_bones(br, header):
        bones = []

        start_pos = header.SIZE + header.ofsBones
        for i in range(header.nrBones):
            br.seek(start_pos + i * Bone.SIZE)
            bone = Bone()
            bone.name = "Bone_" + str(i)
            bone.id = i
            bone.unk00, = struct.unpack("<I", br.read(4))  # flags
            bone.parent_id, bone.unk01 = struct.unpack("<hh", br.read(4))  # parent_id, submesh_id?
            bone.unk02, bone.unk03, bone.unk04, bone.unk05 = struct.unpack("<BBBB", br.read(4))
            bone.unk06, = struct.unpack("<I", br.read(4))  # padding?
            # Rotation Matrix
            bone.rotationMatrix = np.array([[bone.unk02, 0, bone.unk03, 0],[0, 1, 0, 0],[bone.unk04, 0, bone.unk05, 0],[ 0, 0, 0, 1]])

            # Key Frame Locations
            bone.timestamps1 = AnimationTrack(*struct.unpack("<Qqq", br.read(24)), 1)
            bone.timestamps2 = AnimationTrack(*struct.unpack("<Qqq", br.read(24)), 2)
            bone.timestamps3 = AnimationTrack(*struct.unpack("<Qqq", br.read(24)), 3)
            bone.timestamps4 = AnimationTrack(*struct.unpack("<Qqq", br.read(24)), 4)
            bone.timestamps5 = AnimationTrack(*struct.unpack("<Qqq", br.read(24)), 5)
            bone.timestamps6 = AnimationTrack(*struct.unpack("<Qqq", br.read(24)), 6)
            bone.timestamps7 = AnimationTrack(*struct.unpack("<Qqq", br.read(24)), 7)
            bone.timestamps8 = AnimationTrack(*struct.unpack("<Qqq", br.read(24)), 8)

            # Transformation Matrices
            br.seek(start_pos + i * Bone.SIZE + 0xD0)
            bone.TM_raw = struct.unpack("<ffffffffffffffff", br.read(16*4))
            bone.TM = np.array([bone.TM_raw[0:4],bone.TM_raw[4:8],bone.TM_raw[8:12],bone.TM_raw[12:16]])       # global matrix

            br.seek(start_pos + i * Bone.SIZE + 0x110)
            bone.InverseTM_raw = struct.unpack("<ffffffffffffffff", br.read(16*4))
            bone.InverseTM = np.array([bone.InverseTM_raw[0:4],bone.InverseTM_raw[4:8],bone.InverseTM_raw[8:12],bone.InverseTM_raw[12:16]])     # inverse global matrix
            # bone.TM.GetInverse() == bone.InverseTM (proven. the values are too close to be coincidence)

            br.seek(start_pos + i * Bone.SIZE + 0x150)
            bone.position = struct.unpack("<fff", br.read(12))      # global position

            # Adjust rotation matrix if needed (logic inferred from C# code)
            unk02 = (bone.unk02 - 127.0) / 127.0
            unk03 = (bone.unk03 - 127.0) / 127.0
            unk04 = (bone.unk04 - 127.0) / 127.0
            unk05 = (bone.unk05 - 127.0) / 127.0

            # Adjust rotation matrix if the sum doesn't match expected
            if unk02 + unk03 + unk04 + unk05 != -4:
                # Logic for quaternion adjustment, if needed
                pass
            # bone.print()
            bones.append(bone)

        for a_bone in bones:     # needs to have the form [bone_0, bone_0/bone_1, bone_0/bone_1/bone_2]
            if a_bone.parent_id == -1:
                a_bone.parent_path = a_bone.name
            else:
                a_bone.parent_path = bones[a_bone.parent_id].parent_path + "/" + a_bone.name

        # Handle animation tracks
        animation_start = start_pos + header.nrBones * Bone.SIZE
        for bone in bones:
            bone.timestamps1.read_keyframes(br, animation_start)
            bone.timestamps2.read_keyframes(br, animation_start)
            bone.timestamps3.read_keyframes(br, animation_start)
            bone.timestamps4.read_keyframes(br, animation_start)
            bone.timestamps5.read_keyframes(br, animation_start)
            bone.timestamps6.read_keyframes(br, animation_start)
            bone.timestamps7.read_keyframes(br, animation_start)
            bone.timestamps8.read_keyframes(br, animation_start)

        # Fix mirrored bones
        mirrored_bone_list = []
        mirrored_anim_list = []
        for a_bone in bones:
            bone_local_matrix = a_bone.TM
            if a_bone.parent_id > -1:
                bone_global_matrix = a_bone.TM
                parent_global_matrix_inverse = bones[a_bone.parent_id].InverseTM
                bone_local_matrix = np.matmul(bone_global_matrix, parent_global_matrix_inverse)
            x = bone_local_matrix
            bone_local_matrix = [x[0,0], x[0,1], x[0,2], x[0,3], x[1,0], x[1,1], x[1,2], x[1,3],x[2,0], x[2,1], x[2,2], x[2,3],x[3,0], x[3,1], x[3,2], x[3,3]]
            t,r,s = decompose(bone_local_matrix)
            if s[0] < 0 or s[1]<0 or s[2]<0:
                mirrored_bone_list.append(a_bone.id)

            if len(a_bone.timestamps1.keyframes) > 0 and a_bone.timestamps1.keyframes[0].scale[0] < 0:
                mirrored_anim_list.append(a_bone.id)
            if len(a_bone.timestamps2.keyframes) > 0 and a_bone.timestamps2.keyframes[0].scale[0] < 0:
                mirrored_anim_list.append(a_bone.id)
        mirrored_anim_list = list(set(mirrored_anim_list))
        # if a bone is mirrored and animation is mirrored => ok
        # if a bone is mirrored and has no animation => ok
        # if a bone is NOT mirrored but animation is mirrored => mirror animation again
        # TODO: check drusera model right foot
        for a_mirrored_anim in mirrored_anim_list:
            if a_mirrored_anim not in mirrored_bone_list:
                for i in range(len(bones[a_mirrored_anim].timestamps1.keyframes)):
                    bones[a_mirrored_anim].timestamps1.keyframes[i].scale = list(bones[a_mirrored_anim].timestamps1.keyframes[i].scale)
                    bones[a_mirrored_anim].timestamps1.keyframes[i].scale[0] *= -1
                    bones[a_mirrored_anim].timestamps1.keyframes[i].scale[1] *= -1
                    bones[a_mirrored_anim].timestamps1.keyframes[i].scale[2] *= -1
        return bones

    def print_flags(self):
        f1 = self.unk00 & 0x0001
        f2 = self.unk00 & 0x0002
        f4 = self.unk00 & 0x0004
        f8 = self.unk00 & 0x0008
        f10 = self.unk00 & 0x0010
        f20 = self.unk00 & 0x0020
        f40 = self.unk00 & 0x0040
        f80 = self.unk00 & 0x0080
        f100 = self.unk00 & 0x0100
        f200 = self.unk00 & 0x0200
        pr = (f"Flags: {self.id}\t{f1}\t{f2}\t{f4}\t{f8}\t{f10}\t{f20}\t{f40}\t{f80}\t{f100}\t{f200}\t")
        print(pr)

    def print(self):
        # print(self.name)
        # print(self.TM)
        # print(self.InverseTM)
        # print(self.InverseTM.GetInverse())
        # print(self.position)
        pass

class KeyFrame:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.scale = None
        self.quaternion = None
        self.translation = None
        self.f_unk = None

    @staticmethod
    def int16_to_float(value):
        return value/16383.5
    
    def get_timestamp_in_seconds(self):
        return self.timestamp/1000.0

    def set_scale(self, v1, v2, v3):
        self.scale = (v1, v2, v3)

    def set_translation(self, v1, v2, v3):
        self.translation = (v1, v2, v3)

    def set_quaternion(self, v1, v2, v3, v4):
        self.quaternion = (self.int16_to_float(v1), self.int16_to_float(v2), self.int16_to_float(v3), self.int16_to_float(v4))

    def set_values(self, v1, v2, v3, v4):
        self.f_unk = (v1, v2, v3, v4)

class AnimationTrack:
    def __init__(self, duration, time_start_ofs, value_start_ofs, track_type):
        # maybe input order is: duration, time_start_ofs, value_start_ofs
        self.time_start_ofs = time_start_ofs
        self.duration = duration
        self.value_start_ofs = value_start_ofs
        self.track_type = track_type
        self.keyframes = [None] * duration

    def read_keyframes(self, br, animation_start):
        # TODO: review this logic...
        if self.duration == 0:
            return
        br.seek(animation_start + self.time_start_ofs)
        for i in range(self.duration):
            timestamp = struct.unpack("<I", br.read(4))[0]
            self.keyframes[i] = KeyFrame(timestamp)
        # Read values based on track_type
        br.seek(animation_start + self.value_start_ofs)
        if self.track_type in [1, 2, 3]:
            for i in range(self.duration):
                v1 = np.float16(struct.unpack("<e", br.read(2))[0])
                v2 = np.float16(struct.unpack("<e", br.read(2))[0])
                v3 = np.float16(struct.unpack("<e", br.read(2))[0])
                self.keyframes[i].set_scale(v1, v2, v3)
        elif self.track_type in [5, 6]:
            for i in range(self.duration):
                v1, v2, v3, v4 = struct.unpack("<hhhh", br.read(8))
                self.keyframes[i].set_quaternion(v1, v2, v3, v4)
        elif self.track_type == 7:
            for i in range(self.duration):
                v1, v2, v3 = struct.unpack("<fff", br.read(12))
                self.keyframes[i].set_translation(v1, v2, v3)
        elif self.track_type == 8:
            for i in range(self.duration):
                v1 = struct.unpack("<h", br.read(2))[0]/16383.5
                v2 = struct.unpack("<h", br.read(2))[0]/16383.5
                v3 = struct.unpack("<h", br.read(2))[0]/16383.5
                v4 = struct.unpack("<h", br.read(2))[0]/16383.5
                self.keyframes[i].set_values(v1, v2, v3, v4)
        else:
            for i in range(self.duration):
                v1 = np.float16(struct.unpack("<e", br.read(2))[0])
                v2 = np.float16(struct.unpack("<e", br.read(2))[0])
                v3 = np.float16(struct.unpack("<e", br.read(2))[0])
                v4 = np.float16(struct.unpack("<e", br.read(2))[0])
                self.keyframes[i].set_values(v1, v2, v3, v4)

class ModelAnimation:
    SIZE = 112

    def __init__(self):
        self.model_sequence_db_id = 0
        self.unk1 = 0
        self.unk2 = 0
        self.unk3 = 0
        self.unk4 = 0
        self.fallback_sequence = 0
        self.timestamp_start = 0
        self.timestamp_end = 0
        self.unk10 = 0
        self.unk11 = 0
        self.unk12 = 0
        self.unk13 = 0
        self.unk14 = 0
        self.unk15 = 0
        self.unk16 = []
        self.unk19 = 0
        self.unk20 = []
        self.unk23 = 0
        self.unk24 = []
        self.unk25 = 0
        self.unk26 = []
        self.unk27 = 0
        self.unk28 = 0
        self.unk29 = 0

    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.ofsModelAnimations
        nr = m3.nrModelAnimations
        animations = []
        for i in range(nr):
            br.seek(start_pos + i * ModelAnimation.SIZE)

            animation = ModelAnimation()
            animation.model_sequence_db_id = struct.unpack("<H", br.read(2))[0]
            animation.unk1, animation.unk2, animation.unk3, animation.unk4 = struct.unpack("<4H", br.read(2*4))
            animation.fallback_sequence = struct.unpack("<H", br.read(2))[0]
            animation.timestamp_start = struct.unpack("<I", br.read(4))[0]
            animation.timestamp_end = struct.unpack("<I", br.read(4))[0]
            animation.unk10, animation.unk11, animation.unk12, animation.unk13, animation.unk14, animation.unk15 = struct.unpack("<6H", br.read(2*6))

            animation.unk16 = struct.unpack("<fff", br.read(12))
            animation.unk19 = struct.unpack("<I", br.read(4))[0]
            animation.unk20 = struct.unpack("<fff", br.read(12))
            animation.unk23 = struct.unpack("<I", br.read(4))[0]
            animation.unk24 = struct.unpack("<fff", br.read(12))
            animation.unk25 = struct.unpack("<I", br.read(4))[0]
            animation.unk26 = struct.unpack("<fff", br.read(12))
            animation.unk27 = struct.unpack("<I", br.read(4))[0]
            animation.unk28, animation.unk29 = struct.unpack("<QQ", br.read(16))
            # unk16, unk20, unk24, unk26 seem so be some kind of bounding box?
            # animation.print()
            animations.append(animation)

        return animations

    def print(self):
        fields = vars(self)
        pr = "\t".join(f"{field}: {value}" for field, value in fields.items())
        print(f"MODEL ANIMATION: {pr}")

class SubmeshGroupTable:
    SIZE = 4
    def __init__(self, submesh_id, unk1):
        self.submesh_id = submesh_id
        self.unk1 = unk1

    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.ofsSubmeshGroupsTable
        submesh_group_table_entries = []
        for i in range(m3.nrSubmeshGroupsTable):
            entry_pos = start_pos + i * SubmeshGroupTable.SIZE
            br.seek(entry_pos)

            submesh_id, unk1 = struct.unpack('<HH', br.read(4))
            submesh_group_table_entries.append(SubmeshGroupTable(submesh_id, unk1))
        return submesh_group_table_entries

    def print(self, index):
        print(f"{index}\t {self.submesh_id}\t {self.unk1}")


def VertexReadV3(br, field_type):
    if field_type == 1:
        return struct.unpack("<fff", br.read(12))
    elif field_type == 2:
        xyz = struct.unpack("<hhh", br.read(6))
        return [xyz[0]/1024.0, xyz[1]/1024.0, xyz[2]/1024.0]
    elif field_type == 3:
        # 1 = x2 + y2 + z2
        # z = sqrt(1-x2-y2)
        x = float(struct.unpack("<B", br.read(1))[0])
        y = float(struct.unpack("<B", br.read(1))[0])
        x = (x - 127.0) / 127.0
        y = (y - 127.0) / 127.0
        z = math.sqrt(max(1-x*x-y*y, 0))
        # z = 1.0 - math.sqrt(x*x + y*y);   # why, Carbine? why? is 1 extra byte too much?? is it cheaper to do sqrt?
        return [x, y, z]  
    return [0,0,0]

def VertexReadV4(br, field_type):
    if field_type == 4:
        return struct.unpack("<4B", br.read(4))
    return [1,1,1,1]
    
def VertexReadV2(br, field_type):
    if field_type == 5:
        x = np.float16(struct.unpack("<e", br.read(2))[0])
        y = np.float16(struct.unpack("<e", br.read(2))[0])
        return [x, y]

