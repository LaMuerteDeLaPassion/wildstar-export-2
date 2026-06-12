from gltf_utils import *
import numpy as np
import struct
import array
import math


class Header:
    SIZE = 1584
    def __init__(self):
        self.name = None
        # START OF M3 HEADER
        self.signature = None                       # int32
        self.version = None                         # int32
        self.nrUnk008 = None                        # int32                                                 -  values of 0,1
        #                                           # padding 4
        self.AnimationsMeta_def = {}                # 0x010 - number:uint64, ofset:uint64
        self.trackdef_anim_0 = []                   # 0x020 - number:uint64, ofset_A:uint64, ofset_B:uint64  -  animation meta related
        self.trackdef_anim_1 = []                   # 0x038 - number:uint64, ofset_A:uint64, ofset_B:uint64  -  animation meta related
        self.trackdef_anim_2 = []                   # 0x050 - number:uint64, ofset_A:uint64, ofset_B:uint64  -  animation meta related
        self.trackdef_anim_3 = []                   # 0x068 - number:uint64, ofset_A:uint64, ofset_B:uint64  -  animation meta related
        self.BindPose_def = {}                      # 0x080 - number:uint64, ofset:uint64,                   -  200ms bind pose of model. 
        self.trackdef_unk090 = []                   # 0x090 - number:uint64, ofset_A:uint64, ofset_B:uint64
        self.trackdef_unk0A8 = []                   # 0x0A8 - number:uint64, ofset_A:uint64, ofset_B:uint64
        self.trackdef_unk0C0 = []                   # 0x0C0 - number:uint64, ofset_A:uint64, ofset_B:uint64
        self.trackdef_unk0D8 = []                   # 0x0D9 - number:uint64, ofset_A:uint64, ofset_B:uint64
        self.struct0F0_def = {}                     # 0x0F0 - number:uint64, ofset:uint64,                   -  always present looks important
        self.trackdef_unk100 = []                   # 0x100 - number:uint64, ofset_A:uint64, ofset_B:uint64
        self.trackdef_unk118 = []                   # 0x118 - number:uint64, ofset_A:uint64, ofset_B:uint64
        self.trackdef_unk130 = []                   # 0x130 - number:uint64, ofset_A:uint64, ofset_B:uint64
        self.trackdef_unk148 = []                   # 0x148 - number:uint64, ofset_A:uint64, ofset_B:uint64
        self.trackdef_unk160 = []                   # 0x160 - number:uint64, ofset_A:uint64, ofset_B:uint64  -  holo related related to UnkFloat178
        self.UnkFloat178 = 0                        # 0x178                                                  -  holo related related to nrUnk160
        #                                           # padding 4
        self.bones_def = {}                         # 0x180 - number:uint64, ofset:uint64,                   -  bones meta data
        self.lutdef_unk190 = []                     # 0x190 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids
        self.lutdef_unk1A0 = []                     # 0x1A0 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids
        self.lutdef_bone_ids = []                   # 0x1B0 - number:uint64, ofset:uint64,                   -  bone id lookup table
        self.textures_def = {}                      # 0x1C0 - number:uint64, ofset:uint64,                   -  textures meta data
        self.lutdef_unk1D0 = []                     # 0x1D0 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids
        self.struct1E0_def = {}                     # 0x0F0 - number:uint64, ofset:uint64,                   -  
        self.materials_def = {}                     # 0x1F0 - number:uint64, ofset:uint64,                   -  materials meta data
        self.submesh_ids_def = {}                   # 0x200 - number:uint64, ofset:uint64,                   -  submesh id meta data
        self.lutdef_unk210 = []                     # 0x210 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids
        #                                           # padding 48
        self.geometry_def = {}                      # 0x250 - number:uint64, ofset:uint64,                   -  bones meta data
        self.lutdef_unk260 = []                     # 0x260 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids
        self.lutdef_unk270 = []                     # 0x270 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids
        self.lutdef_unk280 = []                     # 0x280 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids
        self.trackdef_unk290 = []                   # 0x290 - number:uint64, ofset_A:uint64, ofset_B:uint64
        #                                           # padding 16
        self.struct2B8_def = {}                     # 0x2B8 - number:uint64, ofset:uint64,                   -  
        self.lutdef_unk2C8 = []                     # 0x2C8 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids
        #                                           # padding 32
        self.ParticleEmitter_def = {}               # 0x2F8 - number:uint64, ofset:uint64,                   -  
        self.struct308_def = {}                     # 0x308 - number:uint64, ofset:uint64,                   -  
        self.light_def = {}                         # 0x318 - number:uint64, ofset:uint64,                   -  Light meta
        self.SpriteAttachment_def = {}              # 0x328 - number:uint64, ofset:uint64,                   -  
        self.lutdef_unk338 = []                     # 0x338 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids
        self.idUnk348 = 0                           # 0x338 - uint64                                         -  some kind of id related to structure trackdef_unk350. if idUnk348 == -1, there is not Track350
        self.trackdef_unk350 = []                   # 0x350 - number:uint64, ofset_A:uint64, ofset_B:uint64
        self.idUnk368 = 0                           # 0x368 - uint64                                         -  some kind of id related to structure trackdef_unk370. if idUnk368 == -1, there is not Track370
        self.trackdef_unk370 = []                   # 0x370 - number:uint64, ofset_A:uint64, ofset_B:uint64
        self.FloatUnk380 = 0                        # 0x380 - float, float                                   -  
        self.has_BB_1 = 0                           # 0x390 - struct(3f,f,3f,f,3f,f,f,f)                     -  structure of bounds. TODO: refactor this code
        #                                           # padding 8
        self.has_BB_2 = 0                           # 0x3D0 - struct(3f,f,3f,f,3f,f,f,f)                     -  structure of bounds. TODO: refactor this code
        #                                           # padding 8
        self.has_BB_3 = 0                           # 0x410 - struct(3f,f,3f,f,3f,f,f,f)                     -  structure of bounds. TODO: refactor this code
        #                                           # padding 8
        self.has_BB_4 = 0                           # 0x450 - struct(3f,f,3f,f,3f,f,f,f)                     -  structure of bounds. TODO: refactor this code
        #                                           # padding 8
        self.struct490_def = {}                     # 0x328 - number:uint64, ofset:uint64,                   -  contains geometry data. Either LODs or Collision meshes. most likely LODs
        self.lutdef_unk4A0 = []                     # 0x4A0 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids
        self.has_BB_5 = 0                           # 0x4B0 - struct(3f,f,3f,f,3f,f,f,f)                     -  structure of bounds. TODO: refactor this code
        #                                           # padding 8
        self.FloatUnk4F0 = 0                        # 0x4F0 - float,                                         -  
        #                                           # padding 4
        self.FloatUnk4F8 = 0                        # 0x4F8 - float,                                         -  
        #                                           # padding 4
        self.PosUnk500  = 0                         # 0x500 - float, float, float,                           -  some kind of vector3 position in 3d space
        #                                           # padding 4
        self.lutdef_unk510 = []                     # 0x510 - number:uint64, ofset:uint64,                   -  some kind of structured array of (x,y,z,w). (x,y,z) are points in 3d space. and w is unknown for now. 0<w<1
        self.lutdef_unk520 = []                     # 0x520 - number:uint64, ofset:uint64,                   -  indices for data stored in nrUnk510
        self.lutdef_unk530 = []                     # 0x530 - number:uint64, ofset:uint64,                   -  indices for data stored in nrUnk510
        self.struct540_def = {}                     # 0x540 - number:uint64, ofset:uint64,                   -  
        self.lutdef_unk550 = []                     # 0x550 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids, mount related
        self.EffectTimeline_def = {}                # 0x560 - number:uint64, ofset:uint64,                   -  possibly emotes
        self.struct570_def = {}                     # 0x570 - number:uint64, ofset:uint64,                   -  
        self.idUnk580 = 0                           # 0x580 - int64,                                         -  some kind of id related to structure struct588_def and 
        self.struct588_def = {}                     # 0x588 - number:uint64, ofset:uint64,                   -  
        self.CustomBoneMinMaxValues_def = {}        # 0x598 - number:uint64, ofset:uint64,                   -  structure related to character face bones. probably contains min-max ranges for bone motions
        self.lutdef_BoneToCustomBoneMinMax = []     # 0x5A8 - number:uint64, ofset:uint64,                   -  some kind of lookup table with ids, related to character faces, lutdef_BoneToCustomBoneMinMax[bone_id] = CustomBoneMinMaxValues_def.id
        #                                           # padding 8
        self.trackdef_unk5C0 = []                   # 0x5C0 - number:uint64, ofset_A:uint64, ofset_B:uint64
        self.FloatUnk5D8 = 0
        self.FloatUnk5E0 = 0
        self.FloatUnk5E8 = 0
        self.FloatUnk5F0 = 0
        self.FloatUnk5F8 = 0
        self.FloatUnk600 = 0
        self.FloatUnk608 = 0
        self.FloatUnk610 = 0
        self.FloatUnk618 = 0
        self.FloatUnk620 = 0
        #                                     # padding 8
        
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
        header.nrUnk008, = struct.unpack('<I', br.read(4))
        struct.unpack('<I', br.read(4))
        header.AnimationsMeta_def["nr"], header.AnimationsMeta_def["ofs"] = struct.unpack('<qq', br.read(16))
        header.trackdef_anim_0 = struct.unpack('<qqq', br.read(24))
        header.trackdef_anim_1 = struct.unpack('<qqq', br.read(24))
        header.trackdef_anim_2 = struct.unpack('<qqq', br.read(24))
        header.trackdef_anim_3 = struct.unpack('<qqq', br.read(24))
        header.BindPose_def["nr"], header.BindPose_def["ofs"] = struct.unpack('<qq', br.read(16))
        header.trackdef_unk090 = struct.unpack('<qqq', br.read(24))
        header.trackdef_unk0A8 = struct.unpack('<qqq', br.read(24))
        header.trackdef_unk0C0 = struct.unpack('<qqq', br.read(24))
        header.trackdef_unk0D8 = struct.unpack('<qqq', br.read(24))
        header.struct0F0_def["nr"], header.struct0F0_def["ofs"] = struct.unpack('<qq', br.read(16))
        header.trackdef_unk100 = struct.unpack('<qqq', br.read(24))
        header.trackdef_unk118 = struct.unpack('<qqq', br.read(24))
        header.trackdef_unk130 = struct.unpack('<qqq', br.read(24))
        header.trackdef_unk148 = struct.unpack('<qqq', br.read(24))
        header.trackdef_unk160 = struct.unpack('<qqq', br.read(24))
        header.UnkFloat178, = struct.unpack('<f', br.read(4))
        br.read(4)      # padding
        header.bones_def["nr"], header.bones_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.lutdef_unk190 = struct.unpack('<qq', br.read(16))
        header.lutdef_unk1A0 = struct.unpack('<qq', br.read(16))
        header.lutdef_bone_ids = struct.unpack("<qq", br.read(16))
        header.textures_def["nr"], header.textures_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.lutdef_unk1D0 = struct.unpack("<qq", br.read(16))
        header.struct1E0_def["nr"], header.struct1E0_def["ofs"] = struct.unpack('<qq', br.read(16))
        header.materials_def["nr"], header.materials_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.submesh_ids_def["nr"], header.submesh_ids_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.lutdef_unk210 = struct.unpack('<qq', br.read(16))
        br.read(48)     # padding
        header.geometry_def["nr"], header.geometry_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.lutdef_unk260 = struct.unpack('<qq', br.read(16))
        header.lutdef_unk270 = struct.unpack('<qq', br.read(16))
        header.lutdef_unk280 = struct.unpack('<qq', br.read(16))
        header.trackdef_unk290 = struct.unpack('<qqq', br.read(24))
        br.read(16)     # padding
        header.struct2B8_def["nr"], header.struct2B8_def["ofs"] = struct.unpack('<qq', br.read(16))
        header.lutdef_unk2C8 = struct.unpack('<qq', br.read(16))
        br.read(32)     # padding
        header.ParticleEmitter_def["nr"], header.ParticleEmitter_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.struct308_def["nr"], header.struct308_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.light_def["nr"], header.light_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.SpriteAttachment_def["nr"], header.SpriteAttachment_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.lutdef_unk338 = struct.unpack("<qq", br.read(16))
        header.idUnk348, = struct.unpack("<q", br.read(8))
        header.trackdef_unk350 = struct.unpack("<qqq", br.read(24))
        header.idUnk368, = struct.unpack("<q", br.read(8))
        header.trackdef_unk370 = struct.unpack("<qqq", br.read(24))
        header.FloatUnk380    = struct.unpack("<2f", br.read(8))
        BB1 = Bounds.read_all(br)       
        header.has_BB_1 = BB1.is_set()
        br.read(8)      # padding
        BB2 = Bounds.read_all(br)
        header.has_BB_2 = BB2.is_set()
        br.read(8)      # padding
        BB3 = Bounds.read_all(br)
        header.has_BB_3 = BB3.is_set()
        br.read(8)      # padding
        BB4 = Bounds.read_all(br)
        header.has_BB_4 = BB4.is_set()
        br.read(8)      # padding
        header.struct490_def["nr"], header.struct490_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.lutdef_unk4A0 = struct.unpack("<qq", br.read(16))
        BB5 = Bounds.read_all(br)
        header.has_BB_5 = BB5.is_set()
        br.read(8)      # padding
        header.FloatUnk4F0,  = struct.unpack("<f", br.read(4))
        br.read(4)      # padding
        header.FloatUnk4F8, = struct.unpack("<f", br.read(4))
        br.read(4)      # padding
        header.PosUnk500  = struct.unpack("<3f", br.read(12))
        br.read(4)      # padding
        header.lutdef_unk510 = struct.unpack("<qq", br.read(16))
        header.lutdef_unk520 = struct.unpack("<qq", br.read(16))
        header.lutdef_unk530 = struct.unpack("<qq", br.read(16))
        header.struct540_def["nr"], header.struct540_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.lutdef_unk550 = struct.unpack("<qq", br.read(16))
        header.EffectTimeline_def["nr"], header.EffectTimeline_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.struct570_def["nr"], header.struct570_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.idUnk580, = struct.unpack("<q", br.read(8))
        header.struct588_def["nr"], header.struct588_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.CustomBoneMinMaxValues_def["nr"], header.CustomBoneMinMaxValues_def["ofs"] = struct.unpack("<qq", br.read(16))
        header.lutdef_BoneToCustomBoneMinMax = struct.unpack("<qq", br.read(16))
        br.read(8)      # padding
        header.trackdef_unk5C0 = struct.unpack("<qqq", br.read(24))
        header.FloatUnk5D8 = struct.unpack("<ff", br.read(8))[0]
        header.FloatUnk5E0 = struct.unpack("<ff", br.read(8))[0]
        header.FloatUnk5E8 = struct.unpack("<ff", br.read(8))[0]
        header.FloatUnk5F0 = struct.unpack("<ff", br.read(8))[0]
        header.FloatUnk5F8 = struct.unpack("<ff", br.read(8))[0]
        header.FloatUnk600 = struct.unpack("<ff", br.read(8))[0]
        header.FloatUnk608 = struct.unpack("<ff", br.read(8))[0]
        header.FloatUnk610 = struct.unpack("<ff", br.read(8))[0]
        header.FloatUnk618 = struct.unpack("<ff", br.read(8))[0]
        header.FloatUnk620 = struct.unpack("<ff", br.read(8))[0]
        br.read(8)      # padding
        if br.tell() != Header.SIZE:        # sanity check
            raise "incorrect header read..."
        if only_header:
            return header
        # read tracks
        header.track_anim_0 = Track.read_track(br, Header.SIZE, *header.trackdef_anim_0, "2i") # confirmed to be int16
        header.track_anim_1 = Track.read_track(br, Header.SIZE, *header.trackdef_anim_1, "1i") # values are stored in 1 byte either int8 or uint8
        header.track_anim_2 = Track.read_track(br, Header.SIZE, *header.trackdef_anim_2, "1?") # values are stored in 1 byte
        header.track_anim_3 = Track.read_track(br, Header.SIZE, *header.trackdef_anim_3, "1?") # values are stored in 1 byte
        header.track090     = Track.read_track(br, Header.SIZE, *header.trackdef_unk090, "1?") # values are stored in 1 bytes
        header.track0A8     = Track.read_track(br, Header.SIZE, *header.trackdef_unk0A8, "1?") # values are stored in 1 bytes
        header.track0C0     = Track.read_track(br, Header.SIZE, *header.trackdef_unk0C0, "1?") # values are stored in 1 bytes
        header.track0D8     = Track.read_track(br, Header.SIZE, *header.trackdef_unk0D8, "1?") # values are stored in 1 bytes
        header.track100     = Track.read_track(br, Header.SIZE, *header.trackdef_unk100, "1?") # values are stored in 1 bytes
        header.track118     = Track.read_track(br, Header.SIZE, *header.trackdef_unk118, "1?") # values are stored in 1 bytes
        header.track130     = Track.read_track(br, Header.SIZE, *header.trackdef_unk130, "1?") # values are stored in 1 bytes
        header.track148     = Track.read_track(br, Header.SIZE, *header.trackdef_unk148, "1?") # values are stored in 1 bytes
        header.track160     = Track.read_track(br, Header.SIZE, *header.trackdef_unk160, "1?") # values are stored in 1 bytes
        header.track290     = Track.read_track(br, Header.SIZE, *header.trackdef_unk290, "2?") # values are stored in 2 bytes
        header.track350     = Track.read_track(br, Header.SIZE, *header.trackdef_unk350, "2?") # values are stored in 4 bytes
        header.track370     = Track.read_track(br, Header.SIZE, *header.trackdef_unk370, "4?") # values are stored in 4 bytes
        header.track5C0     = Track.read_track(br, Header.SIZE, *header.trackdef_unk5C0, "2?") # confirmed to be stored as int16
        # LOOKUP TABELES
        header.LUT_unk190      = LUT.read_lut(br, header, *header.lutdef_unk190, 'h')   # confirmed datatype to be int16
        header.LUT_unk1A0      = LUT.read_lut(br, header, *header.lutdef_unk1A0, 'h')   # confirmed datatype to be int16
        header.LUT_boneMapping = LUT.read_lut(br, header, *header.lutdef_bone_ids, 'h') # confirmed datatype to be int16
        header.LUT_unk1D0      = LUT.read_lut(br, header, *header.lutdef_unk1D0, 'h')   # confirmed datatype to be int16
        header.LUT_unk210      = LUT.read_lut(br, header, *header.lutdef_unk210, 'h')   # confirmed datatype to be int16
        header.LUT_unk260      = LUT.read_lut(br, header, *header.lutdef_unk260, 'h')   # confirmed datatype to be int16
        header.LUT_unk270      = LUT.read_lut(br, header, *header.lutdef_unk270, 'h')   # confirmed datatype to be int16
        header.LUT_unk280      = LUT.read_lut(br, header, *header.lutdef_unk280, 'h')   # confirmed datatype to be int16
        header.LUT_unk2C8      = LUT.read_lut(br, header, *header.lutdef_unk2C8, '2i')  # TODO: probably 2I or something of the sort
        header.LUT_unk338      = LUT.read_lut(br, header, *header.lutdef_unk338, 'h')
        header.LUT_unk4A0      = LUT.read_lut(br, header, *header.lutdef_unk4A0, 'h')
        header.LUT_unk510      = LUT.read_lut(br, header, *header.lutdef_unk510, '4f')  # confirmed to be 4 floats.
        header.LUT_unk520      = LUT.read_lut(br, header, *header.lutdef_unk520, 'i')   # confirmed to be integers
        header.LUT_unk530      = LUT.read_lut(br, header, *header.lutdef_unk530, 'i')   # confirmed to be integers
        header.LUT_unk550      = LUT.read_lut(br, header, *header.lutdef_unk550, 'i')
        header.LUT_BoneToCustomBoneMinMax      = LUT.read_lut(br, header, *header.lutdef_BoneToCustomBoneMinMax, 'h')
        # print(header.LUT_unk190)
        # print(header.LUT_unk1A0)
        # print(header.LUT_boneMapping)
        # print(header.LUT_unk1D0)
        # print(header.LUT_unk210)
        # print(header.LUT_unk260)
        # print(header.LUT_unk270)
        # print(header.LUT_unk280)
        # print(header.LUT_unk2C8)
        # print(header.LUT_unk338)
        # print(header.LUT_unk4A0)
        # print(header.LUT_unk510)
        # print(header.LUT_unk520)
        # print(header.LUT_unk530)
        # print(header.LUT_unk550)
        # print(header.LUT_BoneToCustomBoneMinMax)
        # BOUNDS
        header.bounds_1 = BB1
        header.bounds_2 = BB2
        header.bounds_3 = BB3
        header.bounds_4 = BB4
        header.bounds_5 = BB5
        #  READ OBJECTS
        header.model_animations = ModelAnimation.read_all(br, header)
        header.bind_poses = BindPose.read_all(br, header)
        header.unk0F0 = Unk0F0.read_all(br, header)
        header.unk1E0s = UNK1E0.read_all(br, header)
        header.unk2B8s = UNK2B8.read_all(br, header)
        header.particle_emitters = ParticleEmitter.read_all(br, header)
        header.bones = Bone.read_all_bones(br, header)
        header.textures = Texture.read_all(br, header)
        header.materials = M3Material.read_all(br, header)
        header.submesh_groups = SubmeshGroupTable.read_all(br, header)
        header.geometry = Geometry.ReadGeometry(br, header)
        header.unk308 = UNK308.read_all(br, header)
        header.lights = LIGHT.read_all(br, header)
        header.sprite_attachments = SpriteAttachment.read_all(br, header)
        header.unk490s = UNK490.read_all(br, header)
        header.unk540s = UNK540.read_all(br, header)
        header.effect_timelines = EffectTimeline.read_all(br, header)
        header.unk570s = UNK570.read_all(br, header)
        header.unk588s = UNK588.read_all(br, header)
        header.CustomBoneMinMaxValuess = CustomBoneMinMaxValues.read_all(br, header)
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
        geometryOfs = header.SIZE + header.geometry_def["ofs"]
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
        # print("NR submesh: " + str(geometry.nrSubmeshes))
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
                boneSubmap.append(header.LUT_boneMapping[i])
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
        # Print all fields
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
        start_pos = m3.SIZE + m3.textures_def["ofs"]
        textures = []
        for i in range(m3.textures_def["nr"]):
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
            br.seek(start_pos + m3.textures_def["nr"] * Texture.SIZE + texture.offset)
            path_data = br.read(texture.nr_letters * 2)  # Assuming 2 bytes per letter (Unicode)
            texture.path = path_data.decode("utf-16").rstrip("\x00")  # nr_letters includes the NUL terminator
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
        self.cb1_28_x = 0  # Specular multiplier x (int)
        self.cb1_28_y = 0  # Specular multiplier y (int)
        self.nr_material_descriptions = 0  # UInt64
        self.ofs_material_descriptions = 0  # UInt64

        self.material_descriptions = []  # List of MaterialDescription objects

    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.materials_def["ofs"]

        materials = []
        for i in range(m3.materials_def["nr"]):
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
            mat_des_start_pos = start_pos + m3.materials_def["nr"] * M3Material.SIZE + material.ofs_material_descriptions
            material.material_descriptions = MaterialDescription.read_all(br, mat_des_start_pos, material.nr_material_descriptions, m3)

            materials.append(material)

        return materials

    def print(self):
        """
        Prints the M3Material object's fields.
        """
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
            # Seek to the start of the current material description
            br.seek(start_pos + i * MaterialDescription.SIZE)

            # Create a MaterialDescription instance
            material_description = MaterialDescription()

            # Read texture selectors
            material_description.texture_selector_a, material_description.texture_selector_b = struct.unpack(
                "<hh", br.read(4)
            )

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
    SIZE = 176*2  # Assuming this matches Bone.GetSize() in the C# code
    def __init__(self):
        self.name = ""
        self.id = 0
        self.bone_global_id = 0       # if this is not -1, it is the id that the bone will have when it will be part of a different model. face bones => body bones
        self.flags = 0                      # somehow connected to LUT_5A8 
        self.parent_id = -1
        self.unk01 = 0
        self.unk02 = 0
        self.unk03 = 0
        self.unk04 = 0
        self.unk05 = 0
        self.unk06 = 0
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

        start_pos = header.SIZE + header.bones_def["ofs"]
        for i in range(header.bones_def["nr"]):
            br.seek(start_pos + i * Bone.SIZE)
            bone = Bone()
            bone.name = "Bone_" + str(i)
            bone.id = i
            bone.bone_global_id,bone.flags = struct.unpack("<hH", br.read(4))  # flags
            bone.parent_id, bone.unk01 = struct.unpack("<hh", br.read(4))  # parent_id, submesh_id?
            bone.unk02, bone.unk03, bone.unk04, bone.unk05 = struct.unpack("<BBBB", br.read(4))
            bone.unk06, = struct.unpack("<I", br.read(4))  # padding?

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
        animation_start = start_pos + header.bones_def["nr"] * Bone.SIZE
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
        for a_mirrored_anim in mirrored_anim_list:
            if a_mirrored_anim not in mirrored_bone_list:
                for i in range(len(bones[a_mirrored_anim].timestamps1.keyframes)):
                    bones[a_mirrored_anim].timestamps1.keyframes[i].scale = list(bones[a_mirrored_anim].timestamps1.keyframes[i].scale)
                    bones[a_mirrored_anim].timestamps1.keyframes[i].scale[0] *= -1
                    bones[a_mirrored_anim].timestamps1.keyframes[i].scale[1] *= -1
                    bones[a_mirrored_anim].timestamps1.keyframes[i].scale[2] *= -1
        return bones

    def print_flags(self):
        f1 = self.flags & 0x0001
        f2 = self.flags & 0x0002
        f4 = self.flags & 0x0004
        f8 = self.flags & 0x0008
        f10 = self.flags & 0x0010
        f20 = self.flags & 0x0020
        f40 = self.flags & 0x0040
        f80 = self.flags & 0x0080
        f100 = self.flags & 0x0100
        f200 = self.flags & 0x0200
        f400 = self.flags & 0x0400      # is modifiable from character creation (face bones)
        pr = (f"Flags: {self.id}\t{f1}\t{f2}\t{f4}\t{f8}\t{f10}\t{f20}\t{f40}\t{f80}\t{f100}\t{f200}\t{f400}")
        print(pr)

    def print(self):
        print(f"{self.id}\t{self.bone_global_id}\t{self.flags}\t{self.parent_id}\t{self.unk01}\t{self.unk02}\t{self.unk03}\t{self.unk04}\t{self.unk05}\t{self.unk06}".expandtabs(10))
        # self.print_flags()

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
        start_pos = m3.SIZE + m3.AnimationsMeta_def["ofs"]
        animations = []
        for i in range(m3.AnimationsMeta_def["nr"]):
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
            # animation.print()
            # unk16, unk20, unk24, unk26 seem so be some kind of bounding box?
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
        start_pos = m3.SIZE + m3.submesh_ids_def["ofs"]
        submesh_group_table_entries = []
        for i in range(m3.submesh_ids_def["nr"]):
            br.seek(start_pos + i * SubmeshGroupTable.SIZE)
            submesh_id, unk1 = struct.unpack('<HH', br.read(4))
            submesh_group_table_entries.append(SubmeshGroupTable(submesh_id, unk1))
        return submesh_group_table_entries

    def print(self, index):
        print(f"{index}\t {self.submesh_id}\t {self.unk1}")

class BindPose:
    """0x080 header block -- STATIC/BIND POSE TIME RANGE (1 entry observed). (was UNK080)

    Decodes to (252, n, 100, t_start_ms, t_end_ms) where t_end = t_start + 200
    and the window lies on the global animation timeline:
      Rowsdower:   (252, 0,  100, 106667, 106867)
      Boulderback: (252, 14, 100, 193333, 193533)
    Interpretation: a 200 ms sequence used as the model's rest/static pose
    (e.g. for portraits/preview). unk_id = 252 in both models (a standard
    sequence id?); unk_0 varies per model.
    """
    SIZE = 48
    def __init__(self):
        self.unk_id = 0   # sequence/db id? (252 / 917756 observed)
        self.unk_0 = 0    # maybe combined with unk_id in an integer32
        self.unk_1 = 0    # together with unk_2 forms uint32 = 100 in both models
        self.unk_2 = 0
        self.start_frame = 0   # timestamp in ms on the global animation timeline
        self.end_frame = 0     # = start + 200 ms in both observed models
        self.values = None
    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.BindPose_def["ofs"]
        br.seek(start_pos)
        bindPoses = []
        for i in range(m3.BindPose_def["nr"]):
            br.seek(start_pos + i*BindPose.SIZE)
            a_bindPose = BindPose()
            a_bindPose.unk_id, a_bindPose.unk_0, a_bindPose.unk_1, a_bindPose.unk_2 = struct.unpack("<4h", br.read(8))
            a_bindPose.start_frame, a_bindPose.end_frame = struct.unpack("<2I", br.read(8))
            a_bindPose.values = struct.unpack("<16h", br.read(32))
            # a_bindPose.print()
            bindPoses.append(a_bindPose)
        return bindPoses
    def print(self):
        print(f"{self.unk_id},{self.unk_0},{self.unk_1},{self.unk_2},{self.start_frame},{self.end_frame},{self.values}")

class Unk0F0:
    SIZE = 184
    def __init__(self):
        self.unk00 = None
        self.unk01 = None
        self.unk02 = None
        self.unk03 = None
        self.unk04 = None
        self.unk05 = None
        self.unk06 = None
        self.unk07 = None
        self.unk08 = None
        self.unk09 = None
        self.unk10 = None
        self.unk11 = None
        self.unk12 = None
        self.unk13 = None
        self.unk14 = None
        self.unk15 = None
        self.unk16 = None
        self.unk17 = None
        self.unk18 = None
        self.unk19 = None
        self.values = []

    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.struct0F0_def["ofs"]
        br.seek(start_pos)
        unk0F0s = []
        for i in range(m3.struct0F0_def["nr"]):
            br.seek(start_pos + i * Unk0F0.SIZE)
            unk0F0 = Unk0F0()
            unk0F0.unk00, unk0F0.unk01, unk0F0.unk02, unk0F0.unk03, unk0F0.unk035 = struct.unpack("<HhHHH", br.read(10))
            unk0F0.unk04, = struct.unpack("<H", br.read(2))
            x = sum(struct.unpack("<H", br.read(2)))
            unk0F0.unk05, = struct.unpack("<I", br.read(4))
            unk0F0.unk06, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<HH", br.read(4)))
            unk0F0.unk07, = struct.unpack("<H", br.read(2))
            unk0F0.unk08, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<HH", br.read(4)))
            unk0F0.unk09, = struct.unpack("<H", br.read(2))
            unk0F0.unk10, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<HH", br.read(4)))
            unk0F0.unk11, = struct.unpack("<H", br.read(2))
            unk0F0.unk12, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<HH", br.read(4)))
            unk0F0.unk13, = struct.unpack("<H", br.read(2))
            unk0F0.unk14, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<HH", br.read(4)))
            unk0F0.unk15, = struct.unpack("<H", br.read(2))
            unk0F0.unk16, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<HH", br.read(4)))
            unk0F0.unk17, = struct.unpack("<H", br.read(2))
            unk0F0.unk18, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<HH", br.read(4)))
            unk0F0.unk19, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<15H", br.read(30)))
            unk0F0.unk20, = struct.unpack("<H", br.read(2))
            unk0F0.unk21, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<HH", br.read(4)))
            unk0F0.unk22, = struct.unpack("<H", br.read(2))
            unk0F0.unk23, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<HH", br.read(4)))
            unk0F0.unk24, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<HHH", br.read(6)))
            unk0F0.unk25, = struct.unpack("<H", br.read(2))
            x += sum(struct.unpack("<HHH", br.read(6)))
            unk0F0.unk26, = struct.unpack("<H", br.read(2))
            if x > 0:
                raise "must not be greater than 0"

            # unk0F0.print()
            raw_data = br.read(Unk0F0.SIZE-122)
            unk0F0.values = struct.unpack("<31H", raw_data)  # Little-endian, 92 unsigned shorts
            # print(br.tell()-start_pos - i * Unk0F0.SIZE)
            # Debug output
            # print(f"0F0: {unk0F0.unk00}, {unk0F0.unk01}, {unk0F0.unk02}, {unk0F0.unk03}")
            # print(f"0F0: {unk0F0.values}")
            unk0F0s.append(unk0F0)
        return unk0F0s

    def print(self):
        print(f"UNK0F0: {self.unk00},{self.unk01},{self.unk02},{self.unk03},{self.unk04},{self.unk05},{self.unk06},{self.unk07},{self.unk08},{self.unk09},{self.unk10},{self.unk11},{self.unk12},{self.unk13},{self.unk14},{self.unk15},{self.unk16},{self.unk17},{self.unk18},{self.unk19}")

class UNK1E0:
    SIZE = 152
    def __init__(self):
        self.unk_id = 0 # maybe??
        self.unk_0 = 0
        self.unk_1 = 0
        self.unk_2 = 0
        self.trackdef_0 = []
        self.values1 = []
        self.trackdef_1 = []
        self.trackdef_2 = []
        # end of header
        self.track_0 = None
        self.track_1 = None
        self.track_2 = None

    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.struct1E0_def["ofs"]
        data_start_pos = start_pos + m3.struct1E0_def["nr"]*UNK1E0.SIZE
        br.seek(start_pos)
        temps = []
        for i in range(m3.struct1E0_def["nr"]):
            br.seek(start_pos + i*UNK1E0.SIZE)
            a_temp = UNK1E0()
            a_temp.unk_id, a_temp.unk_0, a_temp.unk_1, a_temp.unk_2 = struct.unpack("<4h", br.read(8))
            a_temp.trackdef_0 = struct.unpack("<3q", br.read(24))
            a_temp.values1 = struct.unpack("<36H", br.read(48+24))
            a_temp.trackdef_1 = struct.unpack("<3q", br.read(24))
            a_temp.trackdef_2 = struct.unpack("<3q", br.read(24))
            
            a_temp.track_0 = Track.read_track(br, data_start_pos, *a_temp.trackdef_0, "4B") # TODO: make sure values are actually 2 bytes
            a_temp.track_1 = Track.read_track(br, data_start_pos, *a_temp.trackdef_1, "12f") # confirmed to be 12 bytes as 3float
            a_temp.track_2 = Track.read_track(br, data_start_pos, *a_temp.trackdef_2, "12f") # confirmed to be 12 bytes as 3float
            # a_temp.print()
            temps.append(a_temp)
        return temps
    def print(self):
        print(f"{self.unk_id},{self.unk_0},{self.unk_1},{self.unk_2},{self.trackdef_0},{self.trackdef_1},{self.trackdef_2}")
        # print(self.values1)

class UNK2B8:
    SIZE = 48
    def __init__(self):
        self.unk_id = 0 # maybe??
        self.values1 = []
        self.nrSubstruct = 0
        self.ofsSubstruct = 0
        # end header
        self.subclass = None
    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.struct2B8_def["ofs"]
        subclass_start_pos = start_pos + m3.struct2B8_def["nr"]*UNK2B8.SIZE
        br.seek(start_pos)
        temps = []
        for i in range(m3.struct2B8_def["nr"]):
            br.seek(start_pos + i*UNK2B8.SIZE)
            a_temp = UNK2B8()
            a_temp.unk_id, = struct.unpack("<h", br.read(2))
            a_temp.values1 = struct.unpack("<11H", br.read(22))
            a_temp.nrSubstruct, a_temp.ofsSubstruct = struct.unpack("<2Q", br.read(16))

            # a_temp.print()
            # a_temp.subclass = UNK2B8_SUBCLASS.read_all(br, subclass_start_pos, a_temp.nrSubstruct, a_temp.ofsSubstruct)   # TODO: skip for now because it is an odd class and its broken for many models. so something is not read right :/
            temps.append(a_temp)
        return temps
    def print(self):
        print(f"{self.unk_id},{self.values1},{self.nrSubstruct},{self.ofsSubstruct}")

class UNK2B8_SUBCLASS:
    SIZE = 32
    def __init__(self):
        self.unk_0 = 0
        self.unk_1 = 0
        self.vals2 = 0
        self.trackdef_0 = 0

        self.track_0 = None
    @staticmethod
    def read_all(br, start_pos, nr, ofs):
        start_pos += ofs
        br.seek(start_pos + ofs)
        data_start_pos = start_pos + nr*UNK2B8_SUBCLASS.SIZE
        temps = []
        for i in range(nr):
            br.seek(start_pos + i*UNK2B8_SUBCLASS.SIZE)
            a_temp = UNK2B8_SUBCLASS()
            a_temp.unk_0, a_temp.unk_1 = struct.unpack("<2H", br.read(4))
            a_temp.vals2 = struct.unpack("<2H", br.read(4))
            a_temp.trackdef_0 = struct.unpack("<3Q", br.read(24))
            a_temp.print()
            
            a_temp.track_0 = Track.read_track(br, data_start_pos, *a_temp.trackdef_0, "2?") # TODO: make sure values are actually 4 bytes
            # print(a_temp.track_0.values)
            temps.append(a_temp)
        return temps
    def print(self):
        print(f"{self.unk_0},{self.unk_1},{self.vals2},{self.trackdef_0}")
        
class UNK308:
    SIZE = 80
    def __init__(self):
        self.unk1 = 0
        self.trackdef_1 = []
        self.trackdef_2 = []
        self.trackdef_3 = []

        self.track_1 = []
        self.track_2 = []
        self.track_3 = []
    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.struct308_def["ofs"]
        track_start_pos = start_pos + m3.struct308_def["nr"]*UNK308.SIZE
        br.seek(start_pos)
        unk308s = []
        for i in range(m3.struct308_def["nr"]):
            br.seek(start_pos + i*UNK308.SIZE)
            a_unk308 = UNK308()
            a_unk308.unk1 = struct.unpack("<Q", br.read(8))
            a_unk308.trackdef_1 = struct.unpack("<3q", br.read(24))
            a_unk308.trackdef_2 = struct.unpack("<3q", br.read(24))
            a_unk308.trackdef_3 = struct.unpack("<3q", br.read(24))

            a_unk308.track_1 = Track.read_track(br, track_start_pos, *a_unk308.trackdef_1, "2?") # TODO: make sure values are actually 2 bytes
            a_unk308.track_2 = Track.read_track(br, track_start_pos, *a_unk308.trackdef_2, "2?") # TODO: make sure values are actually 2 bytes
            a_unk308.track_3 = Track.read_track(br, track_start_pos, *a_unk308.trackdef_3, "2?") # TODO: make sure values are actually 2 bytes
            unk308s.append(a_unk308)
        return unk308s

class LIGHT:
    SIZE = 400
    def __init__(self):
        self.boneid = 0 # maybe??
        self.unk00 = 0
        self.unk01 = 0
        self.unk02 = 0
        self.unk03 = 0
        self.values1 = []
        self.trackdef_0 = []
        self.trackdef_1 = []    # LIGHT COLOR (maybe uses default of 255 255 255)
        self.trackdef_2 = []    # LIGHT INTENSITY as float 16
        self.trackdef_3 = []
        self.trackdef_4 = []
        self.trackdef_5 = []
        self.values2 = []
        self.values3 = []

        self.track0 = None
        self.track1 = None
        self.track2 = None
        self.track3 = None
        self.track4 = None
        self.track5 = None


    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.light_def["ofs"]
        lights = []
        track_start_pos = start_pos + m3.light_def["nr"] * LIGHT.SIZE
        for i in range(m3.light_def["nr"]):
            br.seek(start_pos + i*LIGHT.SIZE)
            a_light = LIGHT()
            a_light.boneid, a_light.unk00, a_light.unk01, a_light.unk02, a_light.unk03 = struct.unpack("<HHhhh", br.read(10))
            a_light.values1 = struct.unpack("<39h", br.read(78))
            a_light.trackdef_0 = struct.unpack("<3q", br.read(24))
            a_light.trackdef_1 = struct.unpack("<3q", br.read(24))
            a_light.trackdef_2 = struct.unpack("<3q", br.read(24))
            a_light.values2 = struct.unpack("<60h", br.read(120))
            a_light.trackdef_3 = struct.unpack("<3q", br.read(24))
            a_light.trackdef_4 = struct.unpack("<3q", br.read(24))
            a_light.trackdef_5 = struct.unpack("<3q", br.read(24))
            a_light.values3 = struct.unpack("<24h", br.read(LIGHT.SIZE-10-51*2-24-24-120-24*3))

            a_light.track0 = Track.read_track(br, track_start_pos, *a_light.trackdef_0, "2?") # TODO: make sure values are actually 2 bytes
            a_light.track1 = Track.read_track(br, track_start_pos, *a_light.trackdef_1, "4B") # confirmed to be 4 bytes of data
            a_light.track2 = Track.read_track(br, track_start_pos, *a_light.trackdef_2, "2f") # confirmed to be 2 bytes of data
            a_light.track3 = Track.read_track(br, track_start_pos, *a_light.trackdef_3, "2f") # TODO: make sure values are actually 2 bytes
            a_light.track4 = Track.read_track(br, track_start_pos, *a_light.trackdef_4, "2f") # confirmed to be 2 bytes of data
            a_light.track5 = Track.read_track(br, track_start_pos, *a_light.trackdef_5, "2f") # confirmed to be 2 bytes of data
            # a_light.print()
            lights.append(a_light)
        return lights

    def print(self):
        print(f"LIGHT: {self.boneid},{self.unk00},{self.unk01},{self.unk02},{self.unk03}")
        print(f"{self.trackdef_0},{self.trackdef_1},{self.trackdef_2},{self.trackdef_3}; {self.trackdef_4},{self.trackdef_5}")
        print(self.values1)
        print(self.values2)
        print(self.values3)

class ParticleEmitter:
    """0x2F8 header block  --  PARTICLE EMITTER  (was: Unk2F8)

    Validated on two models:
      - Party_Rowsdower.m3: 6 emitters on the firework prop bones
        (29,30,31 / 34,35,36 - two mirrored chains), firework colors,
        sparks/streamer/flash parameter sets.
      - Boulderback.m3:     15 emitters on spine/leg/feet bones
        (1,2,4,5,7,8,10,11,13,14,18), smoke/dust textures, with spawn-count
        tracks animated so dust only fires during step/impact moments.

    Memory layout of one entry's data region (offsets relative to
    track_start_pos = end of the entry array). The per-entry stride VARIES
    (9.5-22 KB observed in Boulderback) because the keyframe area grows with
    animation; it is recovered here from consecutive entries' params_ofs:

        +0x0000    64 B                  keyframe data for the entry's own
                                         td1/td2 (track_base-relative offsets)
        +0x0040    PARAMS_SIZE (3792) B  ParticleEmitterParams struct
        +0x0F10    rest of stride        keyframe data for the params tracks.
                                         THE PARAMS STRUCT'S TRACK OFFSETS ARE
                                         RELATIVE TO THIS POINT (end of the
                                         3792-byte struct).
    """
    SIZE = 160

    def __init__(self):
        self.bone_id = 0        # attachment bone the emitter follows (confirmed on both models)
        self.unk01 = 0          # int16 reference id: 0 in Rowsdower, -1 in Boulderback
        self.unk02 = 0
        self.unk03 = 0
        self.unk04 = 0          # 2 for most emitters, 0 for a few - emitter subtype?
        self.unk05 = 0
        self.unk06_10 = []      # 5 x uint32; (0,3,1,*,*) observed - type/blend enums
        self.unk11_18 = []      # 8 x int16; flags - [4] and [6] vary per emitter
        self.unk19 = 0          # float, 0.0 in both models
        self.unk20 = 0
        self.unk21 = 0
        self.trackdef_1 = []    # nr, posA, posB   (track_base-relative)
        self.trackdef_2 = []    # nr, posA, posB   (track_base-relative)
        self.values1 = 0
        self.params_ofs = 0     # offset of ParticleEmitterParams, track_base-relative
        self.values2 = 0        # 4 x uint16, 0xFFFF = unset references

        self.track1 = None
        self.track2 = None
        self.params = None      # ParticleEmitterParams

    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.ParticleEmitter_def["ofs"]
        emitters = []
        nr = m3.ParticleEmitter_def["nr"]
        track_start_pos = start_pos + nr * ParticleEmitter.SIZE
        # upper bound for keyframe timestamps = end of the global animation
        # timeline (used to reject false-positive trackdefs while scanning)
        anims = getattr(m3, "model_animations", None) or []
        time_bound = max((a.timestamp_end for a in anims), default=10_000_000) + 1
        raw_entries = []
        for i in range(nr):
            br.seek(start_pos + i * ParticleEmitter.SIZE)
            e = ParticleEmitter()
            e.bone_id, e.unk01, e.unk02, e.unk03, e.unk04, e.unk05 = struct.unpack("<HhHHHH", br.read(12))
            e.unk06_10 = struct.unpack("<5I", br.read(20))
            e.unk11_18 = struct.unpack("<8h", br.read(16))
            e.unk19, e.unk20, e.unk21 = struct.unpack("<fhh", br.read(8))
            e.trackdef_1 = struct.unpack("<QQQ", br.read(24))
            e.trackdef_2 = struct.unpack("<QQQ", br.read(24))
            e.values1 = struct.unpack("<40B", br.read(40))
            e.params_ofs, = struct.unpack("<Q", br.read(8))
            e.values2 = struct.unpack("<4H", br.read(8))
            raw_entries.append(e)
        for i, e in enumerate(raw_entries):
            e.track1 = Track.read_track(br, track_start_pos, *e.trackdef_1, "2?")
            e.track2 = Track.read_track(br, track_start_pos, *e.trackdef_2, "2?")
            if i + 1 < nr:
                region_size = raw_entries[i + 1].params_ofs - e.params_ofs + 64
            else:
                region_size = None  # derived inside the params reader
            e.params = ParticleEmitterParams.read(
                br, track_start_pos + e.params_ofs, region_size, time_bound)
            emitters.append(e)
        return emitters

    def print(self):
        print(f"PARTICLE EMITTER: bone={self.bone_id} subtype?={self.unk04} "
              f"params_ofs={self.params_ofs} tracks={len(self.params.tracks) if self.params else 0}")
        if self.params:
            self.params.print()


class ParticleEmitterParams:
    """The 3792-byte parameter struct of a ParticleEmitter (was Unk2F8_SUBCLASS).

    Layout: a short fixed header (counts at +0x08, int64 reference ids -
    mostly -1 - up to +0x68), then a dense table of 24-byte track definitions
    (int64 nr, int64 time_ofs, int64 value_ofs) in groups, with small scalar
    parameter runs between groups (~139 trackdefs total; exact group sizes
    vary slightly per model, so this reader scans rather than assuming a
    fixed table).

    TRACK ENCODING (validated on Rowsdower + Boulderback, 2000+ tracks):
      - offsets are relative to the END of this struct (struct_pos + 3792)
      - timestamps: nr x uint32 (milliseconds, global animation timeline),
        packed at time_ofs
      - the unified rule  value_ofs == align16(time_ofs + 4*nr)  holds for
        every track; nr == 1 degenerates to the old value_ofs == time_ofs+16
      - values follow at value_ofs; element size varies per parameter
        (2 B float16 scalar / 4 B / 6 B float16 vec3 / 16 B for single-key
        slots) and is inferred from the gap to the next track's data.

    Use `describe()` for a decoded {name: value} view of the tracks listed
    in PARAM_TRACK_HINTS.
    """
    SIZE = 3792           # confirmed on both models
    TRACKS_START = 0x68

    # struct_ofs -> (name, value_view, description)
    # confidence: [C] = consistent across both validated models,
    #             [H] = hypothesis from one model / indirect evidence
    PARAM_TRACK_HINTS = {
        0x068: ("spawn_count_min", "u16", "[C] particles per emission, lower bound; animated per-step in Boulderback"),
        0x080: ("spawn_count_max", "u16", "[C] particles per emission, upper bound"),
        0x098: ("burst_count_min", "u16", "[H] secondary emission count, lower bound (25-200 observed)"),
        0x0B0: ("burst_count_max", "u16", "[H] secondary emission count, upper bound"),
        0x0E0: ("multiplier_0E0", "f16", "[C] scalar multiplier, 1.0 in all observed emitters"),
        0x0F8: ("lifetime_ms_min", "u16", "[C] particle lifetime in ms, lower bound (533/833/1333 observed)"),
        0x110: ("lifetime_ms_max", "u16", "[C] particle lifetime in ms, upper bound (800/1166/1666 observed)"),
        0x128: ("emission_vector", "f16v3", "[C] float16 vec3, 6 B/key; emission direction/velocity, e.g. (0,1,-4); 30 fps-sampled when animated"),
        0x158: ("speed_min", "f16", "[C] particle speed, lower bound (0.18-1.0 observed)"),
        0x170: ("speed_max", "f16", "[C] particle speed, upper bound (0.5-1.72 observed)"),
        0x188: ("acceleration", "f16v3", "[H] float16 vec3; (0,+-1,0) Rowsdower, (0,+-4..15,0) Boulderback - gravity/accel or aim vector"),
        0x1D0: ("scale_ramp_0", "f16", "[H] scalar f16; animated 0.5->0.85 ramp observed in Boulderback"),
        0x218: ("param_218", "f16", "[H] scalar f16 (0.1-1.0 observed)"),
        0x230: ("param_230", "f16", "[H] scalar f16 (0.025-1.0 observed)"),
        0x248: ("param_248", "f16", "[H] scalar f16 (0.2-2.0 observed)"),
        0x260: ("delay_ms", "u16", "[H] uint16; 60/100/300 observed - emission delay or period in ms"),
        0x298: ("color_a_key0", "rgb", "[C] RGB byte triple - color ramp A over particle life"),
        0x2B0: ("color_a_key1", "rgb", "[C] RGB byte triple"),
        0x2C8: ("color_a_key2", "rgb", "[C] RGB byte triple"),
        0x2E0: ("color_a_key3", "rgb", "[C] RGB byte triple"),
        0x2F8: ("color_a_key4", "rgb", "[C] RGB byte triple"),
        0x310: ("color_b_key0", "rgb", "[C] RGB byte triple - color ramp B (second layer/end state)"),
        0x328: ("color_b_key1", "rgb", "[C] RGB byte triple"),
        0x340: ("color_b_key2", "rgb", "[C] RGB byte triple"),
        0x358: ("color_b_key3", "rgb", "[C] RGB byte triple"),
        0x370: ("color_b_key4", "rgb", "[C] RGB byte triple"),
        0x3A0: ("alpha_a_key0", "u8", "[H] opacity ramp keys, 0-255"),
        0x3B8: ("alpha_a_key1", "u8", "[H]"),
        0x3D0: ("alpha_a_key2", "u8", "[H]"),
        0x3E8: ("alpha_a_key3", "u8", "[H]"),
        0x500: ("size_key0", "f16", "[H] particle size keys over life (0.25-2.25 observed)"),
        0x518: ("size_key1", "f16", "[H]"),
        0x530: ("size_key2", "f16", "[H]"),
        0x548: ("size_key3", "f16", "[H]"),
        0x560: ("size_key4", "f16", "[H]"),
    }

    _ELEM_SIZES = (16, 12, 8, 6, 4, 2, 1)

    def __init__(self):
        self.header_counts = ()   # 3 x uint16 at +0x08
        self.ref_ids = ()         # int64 ids at +0x20..+0x68, -1 = unset
        self.tracks = []          # list of dicts, in struct order (see read())
        self.scalars = []         # (struct_offset, raw bytes) runs between track groups
        self.data_size = 0

    @staticmethod
    def _align16(x):
        return (x + 15) & ~15

    @staticmethod
    def read(br, struct_pos, region_size=None, time_bound=10_000_000):
        p = ParticleEmitterParams()
        br.seek(struct_pos)
        raw = br.read(ParticleEmitterParams.SIZE)
        if len(raw) < ParticleEmitterParams.SIZE:
            return p
        p.header_counts = struct.unpack_from("<3H", raw, 0x08)
        p.ref_ids = struct.unpack_from("<9q", raw, 0x20)
        data_pos = struct_pos + ParticleEmitterParams.SIZE
        if region_size is not None:
            p.data_size = region_size - 64 - ParticleEmitterParams.SIZE
        else:
            p.data_size = 1 << 20   # provisional upper bound

        # --- scan for trackdefs (unified rule, timestamp-validated) ---
        defs = []
        scalars = []
        o = ParticleEmitterParams.TRACKS_START
        gap_start = None
        a16 = ParticleEmitterParams._align16
        while o + 24 <= ParticleEmitterParams.SIZE:
            ok = False
            nr, a, b = struct.unpack_from("<3q", raw, o)
            if 0 < nr < 0x10000 and 0 <= a < p.data_size and b == a16(a + 4 * nr) and b <= p.data_size:
                br.seek(data_pos + a)
                ts = struct.unpack(f"<{nr}I", br.read(4 * nr))
                if all(ts[j] <= ts[j + 1] for j in range(nr - 1)) and ts[-1] < time_bound:
                    ok = True
            if ok:
                if gap_start is not None:
                    scalars.append((gap_start, raw[gap_start:o]))
                    gap_start = None
                defs.append((o, nr, a, b, ts))
                o += 24
            else:
                if gap_start is None:
                    gap_start = o
                o += 4
        if gap_start is not None:
            scalars.append((gap_start, raw[gap_start:ParticleEmitterParams.SIZE]))
        p.scalars = scalars
        if region_size is None and defs:
            p.data_size = max(d[3] for d in defs) + 32

        # --- read values; infer per-track element size from slot extents ---
        starts = sorted(d[2] for d in defs)
        for (o, nr, a, b, ts) in defs:
            import bisect
            j = bisect.bisect_right(starts, a)
            region_end = starts[j] if j < len(starts) else p.data_size
            vsize = max(0, region_end - b)
            elem = next((s for s in ParticleEmitterParams._ELEM_SIZES if s * nr <= vsize), 0)
            br.seek(data_pos + b)
            vraw = br.read(min(vsize, max(elem * nr, 16)))
            t = {"struct_ofs": o, "nr": nr, "time_ofs": a, "value_ofs": b,
                 "timestamps": ts, "elem_size": elem, "values_raw": vraw,
                 # first-key views (back-compat with earlier revisions):
                 "raw": vraw[:16], "u8": (), "u16": (), "f16": (), "f32": ()}
            head = vraw[:16].ljust(16, b"\x00")
            t["u8"] = struct.unpack("<16B", head)
            t["u16"] = struct.unpack("<8H", head)
            t["f16"] = tuple(float(x) for x in struct.unpack("<8e", head))
            t["f32"] = struct.unpack("<4f", head)
            # per-key decoded values (float16 lanes; use values_raw for other views)
            t["values"] = []
            if elem:
                for k in range(nr):
                    kraw = vraw[k * elem:(k + 1) * elem]
                    if len(kraw) < elem:
                        break
                    if elem % 2 == 0:
                        t["values"].append(tuple(float(x) for x in struct.unpack(f"<{elem // 2}e", kraw)))
                    else:
                        t["values"].append(tuple(kraw))
            p.tracks.append(t)
        return p

    # ------------------------------------------------------------------
    def nonzero_tracks(self):
        return [t for t in self.tracks if any(t["timestamps"]) or any(t["values_raw"])]

    def describe(self):
        """Decoded {name: value} for the tracks in PARAM_TRACK_HINTS.
        Single-key tracks give the value; animated tracks give
        [(t_ms, value), ...]."""
        by_ofs = {t["struct_ofs"]: t for t in self.tracks}
        out = {}
        for ofs, (name, view, _desc) in ParticleEmitterParams.PARAM_TRACK_HINTS.items():
            t = by_ofs.get(ofs)
            if t is None:
                continue
            def one(raw16, f16):
                if view == "u16":
                    return struct.unpack_from("<H", raw16)[0] if raw16 else None
                if view == "f16":
                    return round(f16[0], 4) if f16 else None
                if view == "f16v3":
                    return [round(x, 4) for x in f16[:3]]
                if view == "rgb":
                    return list(raw16[:3])
                if view == "u8":
                    return raw16[0] if raw16 else None
            if t["nr"] <= 1:
                out[name] = one(t["raw"], t["f16"])
            else:
                elem = t["elem_size"] or 2
                keys = []
                for k, ts in enumerate(t["timestamps"]):
                    kraw = t["values_raw"][k * elem:(k + 1) * elem]
                    kf16 = tuple(float(x) for x in struct.unpack(f"<{len(kraw) // 2}e", kraw)) if len(kraw) >= 2 else ()
                    keys.append((ts, one(kraw, kf16)))
                out[name] = keys
        return out

    def print(self):
        print(f"  params: header_counts={self.header_counts} tracks={len(self.tracks)} "
              f"({len(self.nonzero_tracks())} non-zero) data_size={self.data_size}")
        d = self.describe()
        for k in ("spawn_count_min", "spawn_count_max", "lifetime_ms_min", "lifetime_ms_max",
                  "speed_min", "speed_max", "emission_vector", "acceleration"):
            if k in d:
                v = d[k]
                if isinstance(v, list) and v and isinstance(v[0], tuple):
                    v = f"<animated, {len(v)} keys, first={v[0]} last={v[-1]}>"
                print(f"    {k} = {v}")
        cols = [d[k] for k in d if k.startswith("color_") and d[k] and not isinstance(d[k][0], tuple)]
        if cols:
            print(f"    color ramp: {cols}")


class SpriteAttachment:
    """0x328 header block  --  BONE-ANCHORED SPRITE/GLOW  (was: UNK328)

    In Party_Rowsdower.m3 there are exactly four entries matching the four FX
    sprite textures in the model (Glow_Circ_01, Smoke_Puff_01, Glow_Cross_01,
    Light_01). Each entry anchors to a bone (spine/head chain: 1, 2, 4, 5) and
    carries one animated float16 scalar (sizes/intensities 0.349/0.582 in two
    symmetric pairs) plus constants that look like attenuation/range
    parameters (0.1, 0.01, 3276.8).

    Boulderback.m3 confirms the pattern: 2 entries on bones 1 and 2 (root/
    spine) with the SAME constants (multiplier 1.3333, value 0.5815,
    attenuation (0.1, 0.01, 3276.8)) and `unk_id_b` = 76/77 - again high
    indices near the end of the skeleton (86 bones). So `unk_id_b` references
    a utility/attachment bone appended at the end of the bone list, and these
    entries look like a standard rig glow/billboard anchor present on
    creatures generally (not party-specific).
    """
    SIZE = 56

    def __init__(self):
        self.bone_id = 0        # (was unkid_1) anchor bone
        self.unk_id_b = 0       # (was unkid_2) 67,68,69,74 in reference file; also in bone-id range
        self.unk0 = 0
        self.unk1 = 0
        self.multiplier = 0.0   # f32; 1.0 or 1.333 in reference file
        self.unk_flag = 0       # uint64-ish; 1 in reference file
        self.trackdef_0 = []
        self.attenuation = []   # 3 x f32: (0.1, 0.01, 3276.8) in reference file
        self.unk6 = 0

        self.track_0 = None     # single animated float16 (sprite size/intensity)

    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.SpriteAttachment_def["ofs"]
        temps = []
        track_start_pos = start_pos + m3.SpriteAttachment_def["nr"] * SpriteAttachment.SIZE
        for i in range(m3.SpriteAttachment_def["nr"]):
            br.seek(start_pos + i * SpriteAttachment.SIZE)
            a_temp = SpriteAttachment()
            a_temp.bone_id, a_temp.unk_id_b = struct.unpack("<HH", br.read(4))
            a_temp.unk0, = struct.unpack("<I", br.read(4))
            a_temp.multiplier, = struct.unpack("<f", br.read(4))
            a_temp.unk1, = struct.unpack("<I", br.read(4))
            a_temp.trackdef_0 = struct.unpack("<QQQ", br.read(24))
            a_temp.attenuation = struct.unpack("<3f", br.read(12))
            a_temp.unk6 = struct.unpack("<I", br.read(4))

            a_temp.track_0 = Track.read_track(br, track_start_pos, *a_temp.trackdef_0, "2f")  # confirmed float16
            temps.append(a_temp)
        return temps

    def print(self):
        print(f"SPRITE ATTACHMENT: bone={self.bone_id} id_b={self.unk_id_b} mult={self.multiplier} "
              f"atten={self.attenuation} track={list(zip(self.track_0.keyframes, self.track_0.values))}")


class UNK490:
    SIZE = 64
    def __init__(self):
        self.nrUnk1 = 0
        self.ofsUnk1 = 0
        self.nrVertices = 0
        self.ofsVertices = 0
        self.nrIndices = 0
        self.ofsIndices = 0

        self.unk_struct = []
        self.vertices = []
        self.indices = []
        self.extra_data = []
    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.struct490_def["ofs"]
        temps = []
        data_start_pos = start_pos + m3.struct490_def["nr"] * UNK490.SIZE
        for i in range(m3.struct490_def["nr"]):
            br.seek(start_pos + i*UNK490.SIZE)
            a_temp = UNK490()
            a_temp.nrUnk1, a_temp.ofsUnk1, a_temp.nrVertices, a_temp.ofsVertices, a_temp.nrIndices, a_temp.ofsIndices, a_temp.nrUnkStruct, a_temp.ofsUnkStruct = struct.unpack("<8Q", br.read(64))
            if a_temp.nrUnk1 > 0:
                br.seek(data_start_pos + a_temp.ofsUnk1)
                a_struct = {}
                a_struct["unk1"] = struct.unpack(f"<2I", br.read(8))
                a_struct["index_nr?"], = struct.unpack(f"<I", br.read(4))
                a_struct["unk2"], = struct.unpack(f"<I", br.read(4))
                a_temp.unk_struct = a_struct
            br.seek(data_start_pos + a_temp.ofsVertices)
            a_temp.vertices = [struct.unpack("<3f", br.read(12)) for _ in range(a_temp.nrVertices)]
            br.seek(data_start_pos + a_temp.ofsIndices)
            a_temp.indices = struct.unpack(f"<{a_temp.nrIndices}I", br.read(a_temp.nrIndices*4))
            br.seek(data_start_pos + a_temp.ofsUnkStruct)
            for a in range(a_temp.nrUnkStruct):
                a_struct = {}
                a_struct["unk_float"], = struct.unpack("<f", br.read(4))
                a_struct["index"], = struct.unpack("<I", br.read(4))
                a_struct["unk_0"], = struct.unpack("<I", br.read(4))
                a_struct["unk_1"], = struct.unpack("<I", br.read(4))
                a_struct["unk_2"], = struct.unpack("<I", br.read(4))
                a_temp.extra_data.append(a_struct)
            # a_temp.print()
            temps.append(a_temp)
        return temps
    def print(self):
        print(f"UNK490: {self.nrUnk1},{self.ofsUnk1},{self.nrVertices},{self.ofsVertices},{self.nrIndices},{self.ofsIndices},{self.nrUnkStruct},{self.ofsUnkStruct},")

class UNK540:
    SIZE = 112      # TODO: not enough data to be sure about this
    def __init__(self):
        self.unk0 = 0
        self.unk1 = 0
        self.unk2 = 0
        self.unk3 = 0
        self.trackdef_0 = 0
        self.values = []

        self.track_0 = []
    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.struct540_def["ofs"]
        temps = []
        data_start_pos = start_pos + m3.struct540_def["nr"] * UNK540.SIZE
        for i in range(m3.struct540_def["nr"]):
            br.seek(start_pos + i*UNK540.SIZE)
            a_temp = UNK540()
            a_temp.unk0,a_temp.unk1,a_temp.unk2,a_temp.unk3, = struct.unpack(f"<4H", br.read(8))
            a_temp.trackdef_0 = struct.unpack("<QQQ",  br.read(24))
            a_temp.values = struct.unpack(f"<40H", br.read(80))

            a_temp.track_0 = Track.read_track(br, data_start_pos, *a_temp.trackdef_0, "2f") # TODO: confirm the type of data that is in here.
            # a_temp.print()
            temps.append(a_temp)
        return temps
    def print(self):
        print(f"UNK540: {self.unk0},{self.unk1},{self.unk2},{self.unk3},{self.trackdef_0},{self.values},")

class EffectTimeline: # (maybe emotes)
    """0x560 header block  --  FX ENABLE / VISIBILITY ENVELOPE  (was: UNK560)

    In Party_Rowsdower.m3 the single entry references utility bone 75 and
    track_0 holds a 4-key float16 envelope:

        timestamps: (0, 83333, 93300, 113400) ms
        values:     (0.0, 0.0, 1.0, 1.0)

    83333-93333 ms is exactly the model's 10-second celebration animation
    (seq_db_id 7504) - this block gates an effect (the fireworks/party FX) to
    that sequence on the global animation timeline.

    The byte layout matches the old UNK560 reading; the field names and the
    semantic interpretation are new. track_1 carried a single integer 1 at
    t=0 in the reference file (likely an enable flag).

    Boulderback.m3 has 0 entries - the block only appears when an effect is
    gated to a specific window of the animation timeline.
    """
    SIZE = 160

    def __init__(self):
        self.bone_id = 0        # (was values1[0]) bone the effect is anchored to / driven by
        self.unk_a = 0          # (was values1[1])
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
        self.values2 = []
        self.trackdef_0 = []
        self.trackdef_1 = []
        self.values3 = []

        self.track_0 = None     # float16 weight envelope over the global animation timeline
        self.track_1 = None     # integer flag track

    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.EffectTimeline_def["ofs"]
        temps = []
        data_start_pos = start_pos + m3.EffectTimeline_def["nr"] * EffectTimeline.SIZE
        for i in range(m3.EffectTimeline_def["nr"]):
            br.seek(start_pos + i * EffectTimeline.SIZE)
            a_temp = EffectTimeline()
            a_temp.bone_id, a_temp.unk_a = struct.unpack("<2H", br.read(4))
            (a_temp.unk0, a_temp.unk1, a_temp.unk2, a_temp.unk3, a_temp.unk4,
             a_temp.unk5, a_temp.unk6, a_temp.unk7, a_temp.unk8, a_temp.unk9) = struct.unpack("<10H", br.read(20))
            a_temp.values2 = struct.unpack("<8H", br.read(16))
            a_temp.trackdef_0 = struct.unpack("<QQQ", br.read(24))
            a_temp.trackdef_1 = struct.unpack("<QQQ", br.read(24))
            a_temp.values3 = struct.unpack("<36H", br.read(72))

            a_temp.track_0 = Track.read_track(br, data_start_pos, *a_temp.trackdef_0, "2f")  # confirmed float16
            a_temp.track_1 = Track.read_track(br, data_start_pos, *a_temp.trackdef_1, "2?")
            temps.append(a_temp)
        return temps

    def print(self):
        print(f"EFFECT TIMELINE: bone={self.bone_id} "
              f"envelope={list(zip(self.track_0.keyframes, self.track_0.values))} "
              f"flags={list(zip(self.track_1.keyframes, self.track_1.values))}")


class UNK570:
    SIZE = 32
    def __init__(self):
        self.unk0 = 0
        self.unk1 = 0
        self.unk2 = 0
        self.unk3 = 0
    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.struct570_def["ofs"]
        temps = []
        br.seek(start_pos)
        data_start_pos = start_pos + m3.struct570_def["nr"] * UNK570.SIZE
        for i in range(m3.struct570_def["nr"]):
            br.seek(start_pos + i*UNK570.SIZE)
            a_temp = UNK570()
            a_temp.unk0,a_temp.unk1,a_temp.unk2,a_temp.unk3 = struct.unpack(f"<4H", br.read(8))
            a_temp.trackdef_0 = struct.unpack("<QQQ",  br.read(24))
            # a_temp.print()
            a_temp.track_0 = Track.read_track(br, data_start_pos, *a_temp.trackdef_0, "4B") # TODO: determine the data type here.
            temps.append(a_temp)
        return temps
    def print(self):
        print(f"UNK570: {self.unk0},{self.unk1},{self.unk2},{self.unk3},{self.trackdef_0},")

class UNK588:
    SIZE = 32
    def __init__(self):
        self.unk_id = 0
        self.unk1 = 0
        self.unk2 = 0
        self.unk3 = 0
        self.trackdef_0 = []

        self.track_0 = None
    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.struct588_def["ofs"]
        temps = []
        br.seek(start_pos)
        data_start_pos = start_pos + m3.struct588_def["nr"] * UNK588.SIZE
        for i in range(m3.struct588_def["nr"]):
            br.seek(start_pos + i*UNK588.SIZE)
            a_temp = UNK588()
            a_temp.unk_id,a_temp.unk1,a_temp.unk2,a_temp.unk3 = struct.unpack(f"<4H", br.read(8))
            a_temp.trackdef_0 = struct.unpack("<QQQ",  br.read(24))

            a_temp.track_0 = Track.read_track(br, data_start_pos, *a_temp.trackdef_0, "2f") # confirmed to be float16
            # a_temp.print()
            temps.append(a_temp)
        return temps
    def print(self):
        print(f"UNK588: {self.unk_id},{self.unk1},{self.unk2},{self.unk3},{self.trackdef_0},")

class CustomBoneMinMaxValues:
    SIZE = 76
    def __init__(self):
        self.bone_id = 0        # value comes from the bone id
        self.unk1 = 0
        self.unknown_6_floats = []          # TODO: transition or rotation
        self.unknown_6_floats2 = []         # TODO: transition or rotation
        self.scale_minmax_range = []        # scale min max deformation values
    @staticmethod
    def read_all(br, m3):
        start_pos = m3.SIZE + m3.CustomBoneMinMaxValues_def["ofs"]
        temps = []
        br.seek(start_pos)
        data_start_pos = start_pos + m3.CustomBoneMinMaxValues_def["nr"] * CustomBoneMinMaxValues.SIZE
        for i in range(m3.CustomBoneMinMaxValues_def["nr"]):
            br.seek(start_pos + i*CustomBoneMinMaxValues.SIZE)
            a_temp = CustomBoneMinMaxValues()
            a_temp.bone_id,a_temp.unk1, = struct.unpack(f"<2H", br.read(4))  # these 2 together could form an int32 intead of 2xint16
            a_temp.unknown_6_floats = struct.unpack(f"<6f", br.read(24))
            a_temp.unknown_6_floats2 = struct.unpack(f"<6f", br.read(24))
            a_temp.scale_minmax_range.append(struct.unpack(f"<3f", br.read(12)))
            a_temp.scale_minmax_range.append(struct.unpack(f"<3f", br.read(12)))
            a_temp.print()
            temps.append(a_temp)
        return temps
    def print(self):
        # print(f"UNK328: {self.bone_id},{self.unk1}\t{self.unknown_6_floats}\t")
        print(f"{self.unknown_6_floats2}")
        # print(f"{self.scale_minmax_range}")


class Bounds:
    def __init__(self):
        self.bb_A = []
        self.bb_B = []
        self.circle_center = []
        self.circle_radius = 0
        # usually: BoundingBox1_390A == BoundingBox2_3D0A == BoundingBox3_410A == BoundingBox4_450A
        # usually: BoundingBox1_3A0B == BoundingBox2_3E0B == BoundingBox3_420B == BoundingBox4_460B == nrUnk500
        # usually: nrUnk3B0 == Unk3F0 == nrUnk430 == nrUnk470
        # usually: nrUnk3C0 == Unk400 == nrUnk440 == nrUnk480
    @staticmethod
    def read_all(br):
        bounds = Bounds()
        bounds.bb_A = struct.unpack("<3f", br.read(12))
        struct.unpack("<I", br.read(4)) #padding
        bounds.bb_B  = struct.unpack("<3f", br.read(12))
        struct.unpack("<I", br.read(4)) #padding
        bounds.circle_center  = struct.unpack("<3f", br.read(12))
        struct.unpack("<I", br.read(4)) #padding
        bounds.circle_radius,  = struct.unpack("<f", br.read(4))
        struct.unpack("<f", br.read(4)) #padding
        return bounds
    def is_set(self):
        total = sum(self.bb_A) + sum(self.bb_B) + sum(self.circle_center) + self.circle_radius
        return 1 if total == 0 else 0

class Track:
    def __init__(self, keyframe_type):
        self.type = keyframe_type
        self.keyframes = []
        self.values = []

    @staticmethod
    def read_track(br, start_pos, nr, pos1, pos2, keyframe_type):
        track = Track(keyframe_type)
        br.seek(start_pos + pos1)
        timestamps = struct.unpack(f"<{nr}I", br.read(nr*4))
        br.seek(start_pos + pos2)
        if keyframe_type == "1?":
            values = struct.unpack(f"<{nr}B", br.read(nr))
        elif keyframe_type == "1i":   # int8
            values = struct.unpack(f"<{nr}b", br.read(nr))
        elif keyframe_type == "2?": # uint16
            values = struct.unpack(f"<{nr}H", br.read(nr*2))
        elif keyframe_type == "2i": # int16
            values = struct.unpack(f"<{nr}h", br.read(nr*2))
        elif keyframe_type == "2f":
            values = [float(np.float16(struct.unpack(f"<e", br.read(2))[0])) for i in range(nr)]
        elif keyframe_type == "4B":
            values = [struct.unpack(f"<4B", br.read(4)) for i in range(nr)]
        elif keyframe_type == "4?":
            values = struct.unpack(f"<{nr}I", br.read(nr*4))
        elif keyframe_type == "12f":
            values = [struct.unpack(f"<3f", br.read(12)) for i in range(nr)]
        else:
            raise "Unknown value type to read"
        track.keyframes = timestamps
        track.values = values
        return track

class LUT:
    @staticmethod
    def read_lut(br, m3, nr, ofs, data_format):
        br.seek(m3.SIZE + ofs)
        if data_format == "h":
            values = struct.unpack(f"<{nr}h", br.read(nr*2))
        elif data_format == "H":
            values = struct.unpack(f"<{nr}H", br.read(nr*2))
        elif data_format == "2i":
            values = [struct.unpack(f"<2i", br.read(8)) for _ in range(nr)]
        elif data_format == "4f":
            values = [struct.unpack("<4f", br.read(16)) for _ in range(nr)]
        elif data_format == "i":
            values = struct.unpack(f"<{nr}I", br.read(nr*4))
        else:
            raise "unknown format for reading LUTs"
        return values
    

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

