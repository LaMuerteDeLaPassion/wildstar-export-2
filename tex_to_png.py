from io import BytesIO
from PIL import Image
import numpy as np
import struct
import math


class Huffmann:
    MAX_DC_LUMINANCE_LEN = 16
    MAX_AC_LUMINANCE_LEN = 16
    MAX_DC_CHROMINANCE_LEN = 16
    MAX_AC_CHROMINANCE_LEN = 16
    # Define Huffman table lengths and values
    dc_luminance_lengths = [0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    ac_luminance_lengths = [0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 125]
    dc_chrominance_lengths = [0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    ac_chrominance_lengths = [0, 2, 1, 2, 4, 4, 3, 4, 7, 5, 4, 4, 0, 1, 2, 119]
    
    dc_luminance_vals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    ac_luminance_vals = [
        0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12, 0x21, 0x31, 0x41, 0x06, 0x13, 0x51,
        0x61, 0x07, 0x22, 0x71, 0x14, 0x32, 0x81, 0x91, 0xA1, 0x08, 0x23, 0x42, 0xB1, 0xC1,
        0x15, 0x52, 0xD1, 0xf0, 0x24, 0x33, 0x62, 0x72, 0x82, 0x09, 0x0A, 0x16, 0x17, 0x18,
        0x19, 0x1A, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39,
        0x3A, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x53, 0x54, 0x55, 0x56, 0x57,
        0x58, 0x59, 0x5A, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x73, 0x74, 0x75,
        0x76, 0x77, 0x78, 0x79, 0x7A, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x92,
        0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0xA2, 0xA3, 0xA4, 0xa5, 0xA6, 0xA7,
        0xA8, 0xA9, 0xAA, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xC2, 0xC3,
        0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9, 0xCA, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8,
        0xD9, 0xDA, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEa, 0xF1, 0xF2,
        0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFa
    ]
    dc_chrominance_vals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    ac_chrominance_vals = [
        0x00, 0x01, 0x02, 0x03, 0x11, 0x04, 0x05, 0x21, 0x31, 0x06, 0x12, 0x41, 0x51, 0x07,
        0x61, 0x71, 0x13, 0x22, 0x32, 0x81, 0x08, 0x14, 0x42, 0x91, 0xA1, 0xB1, 0xC1, 0x09,
        0x23, 0x33, 0x52, 0xF0, 0x15, 0x62, 0x72, 0xD1, 0x0A, 0x16, 0x24, 0x34, 0xE1, 0x25,
        0xF1, 0x17, 0x18, 0x19, 0x1A, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x35, 0x36, 0x37, 0x38,
        0x39, 0x3A, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x53, 0x54, 0x55, 0x56,
        0x57, 0x58, 0x59, 0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x73, 0x74,
        0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
        0x8A, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0xa2, 0xA3, 0xA4, 0xA5,
        0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA,
        0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9, 0xCA, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6,
        0xD7, 0xD8, 0xD9, 0xDA, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xF2,
        0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA
    ]
    lum_quant_template = [
        16, 11, 10, 16, 24, 40, 51, 61,
        12, 12, 14, 19, 26, 58, 60, 55,
        14, 13, 16, 24, 40, 57, 69, 56,
        14, 17, 22, 29, 51, 87, 80, 62,
        18, 22, 37, 56, 68, 109, 103, 77,
        24, 35, 55, 64, 81, 104, 113, 92,
        49, 64, 78, 87, 103, 121, 120, 101,
        72, 92, 95, 98, 112, 100, 103, 99
    ]
    chroma_quant_template = [
        17, 18, 24, 47, 99, 99, 99, 99,
        18, 21, 26, 66, 99, 99, 99, 99,
        24, 26, 56, 99, 99, 99, 99, 99,
        47, 66, 99, 99, 99, 99, 99, 99,
        99, 99, 99, 99, 99, 99, 99, 99,
        99, 99, 99, 99, 99, 99, 99, 99,
        99, 99, 99, 99, 99, 99, 99, 99,
        99, 99, 99, 99, 99, 99, 99, 99
    ]

    def __init__(self):
        self.dcLumTable = self.load_huff_table(Huffmann.dc_luminance_lengths, Huffmann.MAX_DC_LUMINANCE_LEN, Huffmann.dc_luminance_vals)
        self.acLumTable = self.load_huff_table(Huffmann.ac_luminance_lengths, Huffmann.MAX_AC_LUMINANCE_LEN, Huffmann.ac_luminance_vals)
        self.dcChromaTable = self.load_huff_table(Huffmann.dc_chrominance_lengths, Huffmann.MAX_DC_CHROMINANCE_LEN, Huffmann.dc_chrominance_vals)
        self.acChromaTable = self.load_huff_table(Huffmann.ac_chrominance_lengths, Huffmann.MAX_AC_CHROMINANCE_LEN, Huffmann.ac_chrominance_vals)

        self.luminanceQuantTables = [Huffmann.load_quant_table(i, Huffmann.lum_quant_template) for i in range(100)]
        self.chrominanceQuantTables = [Huffmann.load_quant_table(i, Huffmann.chroma_quant_template) for i in range(100)]

        
    @staticmethod
    def load_huff_table(lengths, num_lengths, values):
        out_table = {}
        cur_index = 0
        code = 0
        for length in range(num_lengths):
            num_values = lengths[length]
            for _ in range(num_values):
                out_table[f"{length + 1}_{code}"] = values[cur_index]
                cur_index += 1
                code += 1
            code <<= 1
        return out_table

    @staticmethod
    def load_quant_table(quality_factor, quant_template):
        multiplier = (200.0 - quality_factor * 2.0) * 0.01
        return [quant_template[i] * multiplier for i in range(64)]

        """
        Return a dictionary, e.g. quality -> [64 floating-point values].
        """
        return {}

class DCT:
    SIDE = 8
    SIDE_SQUARED = SIDE * SIDE

    _DCT = None
    _DCT_T = None

    @classmethod
    def _initialize(cls):
        """
        Initialize class-level DCT and DCT_T if not already done.
        """
        if cls._DCT is None:
            cls._DCT = cls._generate_dct()
            # Make a copy so we can transpose in-place
            dct_copy = cls._DCT[:]
            cls._DCT_T = cls._transpose(dct_copy)

    @staticmethod
    def _generate_dct():
        """
        Equivalent to C# GenerateDct().
        Creates the 8x8 DCT matrix in a single 64-element list.
        """
        result = [0.0] * DCT.SIDE_SQUARED
        o = 0
        for y in range(DCT.SIDE):
            for x in range(DCT.SIDE):
                # sqrt(1/8) if y == 0, else sqrt(1/4)
                scale = math.sqrt(0.125 if y == 0 else 0.25)
                # Cos(((2*x + 1)*y*pi)/16) => (2*x+1)*y*pi*0.0625
                result[o] = scale * math.cos(((2*x + 1) * y * math.pi) * 0.0625)
                o += 1
        return result

    @staticmethod
    def _transpose(m):
        """
        In-place transpose of an 8x8 matrix stored in a 64-element list.
        Equivalent to C# Transpose(double[] m).
        Returns the same list (after transposing).
        """
        assert len(m) == DCT.SIDE_SQUARED
        for y in range(DCT.SIDE):
            for x in range(y + 1, DCT.SIDE):
                m[y * DCT.SIDE + x], m[x * DCT.SIDE + y] = m[x * DCT.SIDE + y], m[y * DCT.SIDE + x]
        return m

    @staticmethod
    def _matrix_multiply(m1, m2):
        """
        Multiply two 8x8 matrices (each stored in 1D) => result is also 1D length 64.
        This matches the logic in C# MatrixMultiply(double[] m1, double[] m2).
        """
        assert len(m1) == DCT.SIDE_SQUARED
        assert len(m2) == DCT.SIDE_SQUARED

        result = [0.0] * DCT.SIDE_SQUARED
        for y in range(DCT.SIDE):
            for x in range(DCT.SIDE):
                s = 0.0
                for k in range(DCT.SIDE):
                    s += m1[y * DCT.SIDE + k] * m2[k * DCT.SIDE + x]
                result[y * DCT.SIDE + x] = s
        return result

    @staticmethod
    def swap(lst, i1, i2):
        """
        Equivalent to C# extension:
            public static void Swap<T>(this IList<T> arr, int i1, int i2)
        """
        assert 0 <= i1 < len(lst), "i1 out of range"
        assert 0 <= i2 < len(lst), "i2 out of range"
        lst[i1], lst[i2] = lst[i2], lst[i1]

    @staticmethod
    def _to_double(m):
        """
        Convert int[] to double[] equivalent in Python.
        """
        return [float(val) for val in m]

    @staticmethod
    def _to_int(m):
        """
        Convert double[] to int[], using Math.Round -> round() in Python.
        """
        return [int(round(val)) for val in m]

    @classmethod
    def do_dct(cls, m):
        """
        Equivalent to C# DoDct(int[] m).
        1) Convert to double
        2) Multiply by DCT
        3) Multiply by DCT_T
        4) Convert back to int
        """
        cls._initialize()  # Ensure DCT matrices exist
        source = cls._to_double(m)  # step 1
        # shape is effectively 8x8
        # step 2
        source = cls._matrix_multiply(cls._DCT, source)
        # step 3
        source = cls._matrix_multiply(source, cls._DCT_T)
        # step 4
        return cls._to_int(source)

    @classmethod
    def do_idct(cls, m):
        """
        Equivalent to C# DoIdct(int[] m).
        1) Convert to double
        2) Multiply by DCT_T
        3) Multiply by DCT
        4) Convert back to int
        """
        cls._initialize()  # Ensure DCT matrices exist
        source = cls._to_double(m)
        source = cls._matrix_multiply(cls._DCT_T, source)
        source = cls._matrix_multiply(source, cls._DCT)
        return cls._to_int(source)

class TexJPEG:
    zigzag_mapping = [0, 1, 5, 6, 14, 15, 27, 28, 2, 4, 7, 13, 16, 26, 29, 42, 3, 8, 12, 17, 25, 30, 41, 43, 9, 11, 18, 24, 31, 40, 44, 53, 10, 19, 23, 32, 39, 45, 52, 54, 20, 22, 33, 38, 46, 51, 55, 60, 21, 34, 37, 47, 50, 56, 59, 61, 35, 36, 48, 49, 57, 58, 62, 63]
    def __init__(self, header, br):
        self.header = header
        self.huffman = Huffmann()
        self.reader = BinaryReader2(BytesIO(br))
        
        self.luminanceQuantTable = []
        self.chrominanceQuantTable = []
        for i in range(4):
            if self.header.layer_infos[i]["quality"] > 100:
                raise "Quality level must be <= 100"
            self.luminanceQuantTable.append(self.huffman.luminanceQuantTables[self.header.layer_infos[i]["quality"]])
            self.chrominanceQuantTable.append(self.huffman.chrominanceQuantTables[self.header.layer_infos[i]["quality"]])

    @staticmethod
    def decode(header_in, image_bytes) -> bytes:
        tex_jpg = TexJPEG(header_in, image_bytes)

        # "round up to multiple of 8" approach from C#
        actual_height = (tex_jpg.header.height + 7) & 0xFFFFFFF8
        actual_width  = (tex_jpg.header.width  + 7) & 0xFFFFFFF8
        out_image = None

        if tex_jpg.header.compression_format == 0:
            out_image = tex_jpg._decode_image_type0(actual_width, actual_height, tex_jpg.reader)
        elif tex_jpg.header.compression_format == 1:
            out_image = tex_jpg._decode_image_type1(actual_width, actual_height, tex_jpg.reader)
        elif tex_jpg.header.compression_format == 2:
            out_image = tex_jpg._decode_image_type2(actual_width, actual_height, tex_jpg.reader)
        else:
            print("image format not supported")
            out_image = bytes()

        return out_image

    def _decode_image_type0(self, width: int, height: int, br: 'BinaryReader2') -> bytes:
        actual_height = ((height + 15) // 16) * 16
        actual_width  = ((width  + 15) // 16) * 16

        lum0  = [[0]*64 for _ in range(4)]
        lum1  = [[0]*64 for _ in range(4)]
        crom0 = [0]*64
        crom1 = [0]*64
        prevDc = [0, 0, 0, 0]
        image_data = bytearray(actual_width * actual_height * 4)

        for y in range(actual_height // 16):
            for x in range(actual_width // 16):
                # Decode blocks
                # lum0 blocks
                for i in range(4):
                    prevDc[0], lum0[i] = self._process_block(prevDc[0], br, self.huffman.dcLumTable, self.huffman.acLumTable, self.luminanceQuantTable[0], is_luminance=True)

                # print(lum0[3])
                # chroma blocks
                prevDc[1], crom0 = self._process_block(prevDc[1], br, self.huffman.dcChromaTable, self.huffman.acChromaTable, self.chrominanceQuantTable[1], is_luminance=False)
                prevDc[2], crom1 = self._process_block(prevDc[2], br, self.huffman.dcChromaTable, self.huffman.acChromaTable, self.chrominanceQuantTable[2], is_luminance=False)

                # lum1 blocks
                for i in range(4):
                    prevDc[3], lum1[i] = self._process_block(prevDc[3], br, self.huffman.dcLumTable, self.huffman.acLumTable, self.luminanceQuantTable[3], is_luminance=True)

                # Reconstruct color block
                color_block = self._decode_color_block_type0(lum0, crom0, crom1, lum1)
                # Write block to final image
                for row in range(16):
                    out_row = y * 16 + row
                    if out_row >= height:
                        continue
                    out_col = x * 16
                    if out_col >= width:
                        continue

                    num_pixels = min(16, width - out_col)
                    # color_block is 16*16 int's, each 4 bytes when turned into RGBA
                    start_src = row * 16 * 4
                    start_dst = (out_row * width + out_col) * 4

                    image_data[start_dst : start_dst + num_pixels*4] = color_block[start_src : start_src + num_pixels*4]
        return bytes(image_data)

    def _decode_image_type1(self, width: int, height: int, br: 'BinaryReader2') -> bytes:
        """
        Equivalent to C# private static byte[] decodeImageType1(...)
        """
        actual_width  = ((width  + 7) // 8) * 8
        actual_height = ((height + 7) // 8) * 8
        image_data = bytearray(actual_width * actual_height * 4)
        lum = [[0]*64 for _ in range(4)]
        prevDc = [0, 0, 0, 0]

        for y in range(actual_height // 8):
            for x in range(actual_width // 8):
                # For each of the 4 layers
                for layer in range(4):
                    if self.header.layer_infos[layer]["has_replacement"] == 0:
                        prevDc[layer], lum[layer] = self._process_block(prevDc[layer], br, self.huffman.dcLumTable, self.huffman.acLumTable, self.luminanceQuantTable[layer], is_luminance=True)
                    else:
                        # Replacement
                        temp_block = [self.header.layer_infos[layer]["replacement"]]*64
                        lum[layer] = temp_block

                # Write pixel data
                for iy in range(8):
                    out_row = y * 8 + iy
                    if out_row >= height:
                        continue

                    for ix in range(8):
                        out_col = x * 8 + ix
                        if out_col >= width:
                            continue

                        r = lum[0][iy * 8 + ix]
                        g = lum[1][iy * 8 + ix]
                        b = lum[2][iy * 8 + ix]
                        a = lum[3][iy * 8 + ix]

                        # Assign RGBA
                        idx = (out_row * width + out_col) * 4
                        image_data[idx]   = r & 0xFF
                        image_data[idx+1] = g & 0xFF
                        image_data[idx+2] = b & 0xFF
                        image_data[idx+3] = a & 0xFF

        return bytes(image_data)

    def _decode_image_type2(self, width: int, height: int, br: 'BinaryReader2') -> bytes:
        actual_width  = ((width  + 7) // 8) * 8
        actual_height = ((height + 7) // 8) * 8
        image_data = bytearray(actual_width * actual_height * 4)
        lum = [[0]*64 for _ in range(4)]
        prevDc = [0, 0, 0, 0]
        color_stats = [0, 0, 0, 0]
        for y in range(actual_height // 8):
            for x in range(actual_width // 8):
                # if self.header.layer_infos[0]["has_replacement"] == 0:
                prevDc[0], lum[0] = self._process_block(prevDc[0], br, self.huffman.dcLumTable, self.huffman.acLumTable, self.luminanceQuantTable[0], is_luminance=True)
                # else:
                #     lum[0] = [self.header.layer_infos[0]["replacement"]]*64

                # Layer 1
                # if self.header.layer_infos[1]["has_replacement"] == 0:
                prevDc[1], lum[1] = self._process_block(prevDc[1], br, self.huffman.dcChromaTable, self.huffman.acChromaTable, self.chrominanceQuantTable[1], is_luminance=False)
                # else:
                #     lum[1] = [self.header.layer_infos[1]["replacement"]]*64

                # Layer 2
                # if self.header.layer_infos[2]["has_replacement"] == 0:
                prevDc[2], lum[2] = self._process_block(prevDc[2], br, self.huffman.dcChromaTable, self.huffman.acChromaTable, self.chrominanceQuantTable[2], is_luminance=False)
                # else:
                #     lum[2] = [self.header.layer_infos[2]["replacement"]]*64

                # Layer 3
                # if self.header.layer_infos[3]["has_replacement"] == 0:
                prevDc[3], lum[3] = self._process_block(prevDc[3], br, self.huffman.dcLumTable, self.huffman.acLumTable, self.luminanceQuantTable[3], is_luminance=True)
                # else:
                #     lum[3] = [self.header.layer_infos[3]["replacement"]]*64

                # Write pixel data
                for iy in range(8):
                    out_row = y * 8 + iy
                    if out_row >= height:
                        continue

                    for ix in range(8):
                        out_col = x * 8 + ix
                        if out_col >= width:
                            continue

                        r = lum[0][iy * 8 + ix]
                        g = lum[1][iy * 8 + ix]
                        b = lum[2][iy * 8 + ix]
                        a = lum[3][iy * 8 + ix]

                        idx = (out_row * width + out_col) * 4
                        image_data[idx]   = r & 0xFF
                        image_data[idx+1] = g & 0xFF
                        image_data[idx+2] = b & 0xFF
                        image_data[idx+3] = a & 0xFF
        return bytes(image_data)

    def _decode_color_block_type0(self, lum0, crom0, crom1, lum1):
        """
        Equivalent to C# private static int[] decodeColorBlockType0(...)
        Returns a bytearray (or similar) of length 16*16*4 (RGBA).
        In C#, the method returned int[], where each int contained 4 bytes (ABGR).
        Here, we'll directly build a bytearray in RGBA order (matching how the image data
        is stored).
        """
        # color_block is 16*16 pixels, each pixel = 4 bytes
        color_block = bytearray(16 * 16 * 4)

        for y in range(16):
            for x in range(16):
                cy = 1 if y >= 8 else 0
                cx = 1 if x >= 8 else 0
                by = y % 8
                bx = x % 8

                block_index = cy*2 + cx
                lum_idx = by * 8 + bx
                crm_idx = (y // 2)*8 + (x // 2)

                # The function 'toColor' in C# returned an int ARGB or ABGR.
                # We'll replicate that logic but generate RGBA bytes instead.
                pixel_int = TexJPEG._to_color(
                    lum0[block_index][lum_idx],
                    crom0[crm_idx],
                    crom1[crm_idx],
                    lum1[block_index][lum_idx]
                )

                # pixel_int is A in high byte, R in low, etc. However the original code
                # appears to store in the order (B, G, R, A). We'll follow the snippet's logic:
                #    (gamma & 0xFF) | ((beta & 0xFF) << 8) | ((delta & 0xFF) << 16) | ((yy & 0xFF) << 24);
                # That means:
                #   byte0 = gamma   (blue)
                #   byte1 = beta    (green)
                #   byte2 = delta   (red)
                #   byte3 = yy      (alpha)
                # We'll reorder them to standard RGBA to store them in image_data or just keep that layout
                # consistent with the original indexing. For simplicity, let's keep the same order
                # (B, G, R, A) if you want to remain consistent with how the code copies blocks.
                # If you prefer RGBA, you'd reorder the bytes.

                # Extract B, G, R, A from integer
                B = pixel_int & 0xFF
                G = (pixel_int >> 8) & 0xFF
                R = (pixel_int >> 16) & 0xFF
                A = (pixel_int >> 24) & 0xFF

                idx = (y * 16 + x) * 4
                color_block[idx]   = R
                color_block[idx+1] = G
                color_block[idx+2] = B
                color_block[idx+3] = A

        return color_block

    @staticmethod
    def _to_color(y, cb, cr, yy):
        """
        Equivalent to C# private static int toColor(int y, int cb, int cr, int yy)
        Returns a single 32-bit int with channel packing in BGRA order, if you follow the original code:

            alpha = y - (cr >> 1)
            beta  = Clamp(alpha + cr, 0, 255)
            gamma = Clamp(alpha - (cb >> 1), 0, 255)
            delta = Clamp(gamma + cb, 0, 255)

            return (gamma & 0xFF)
                 | ((beta & 0xFF)  << 8)
                 | ((delta & 0xFF) << 16)
                 | ((yy & 0xFF)    << 24);
        """
        alpha = y - (cr >> 1)
        beta  = TexJPEG._clamp(alpha + cr, 0, 255)
        gamma = TexJPEG._clamp(alpha - (cb >> 1), 0, 255)
        delta = TexJPEG._clamp(gamma + cb, 0, 255)

        return ((gamma & 0xFF)
                | ((beta & 0xFF)  << 8)
                | ((delta & 0xFF) << 16)
                | ((yy & 0xFF)    << 24))

    def _process_block(self, prev_dc: int,
                       br: 'BinaryReader2',
                       dc_table: dict,
                       ac_table: dict,
                       quant_table: list,
                       is_luminance: bool):
        """
        Equivalent to C# private static int processBlock(...)
        Returns (cur_dc, out_block)
        """
        work_block = [0]*64
        out_block  = [0]*64

        cur_dc, decoded_block = TexJPEG._decode_block(br, dc_table, ac_table, prev_dc)
        zz_block = TexJPEG._unzigzag(decoded_block)
        dq_block = TexJPEG._dequantize(zz_block, quant_table)
        dct_result = DCT.do_idct(dq_block)

        # final clamp
        for i in range(64):
            val = dct_result[i]
            if is_luminance:
                val = TexJPEG._clamp(int(val + 128), 0, 255)
            else:
                val = TexJPEG._clamp(int(val), -256, 255)

            out_block[i] = val

        return (cur_dc, out_block)

    @staticmethod
    def _decode_block(br: 'BinaryReader2',
                      dc_table: dict,
                      ac_table: dict,
                      prev_dc: int = 0):
        """
        Equivalent to C# private static int decodeBlock(...)
        Returns (cur_dc, block)
        """
        block = [0]*64

        # DC
        dc_len = TexJPEG._decode_value(br, dc_table)
        epsilon = br.read_bits(dc_len)
        delta_dc = TexJPEG._extend(epsilon, dc_len)
        cur_dc = delta_dc + prev_dc
        block[0] = cur_dc

        # AC
        idx = 1
        while idx < 64:
            ac_coded_value = TexJPEG._decode_value(br, ac_table)
            if ac_coded_value == 0:
                break
            if ac_coded_value == 0xF0:  # EOB
                idx += 16
                continue

            run = (ac_coded_value >> 4) & 0xF
            ac_len = ac_coded_value & 0xF
            idx += run
            if idx >= 64:
                break

            epsilon = br.read_bits(ac_len)
            ac_value = TexJPEG._extend(epsilon, ac_len)
            block[idx] = ac_value
            idx += 1

        return (cur_dc, block)

    @staticmethod
    def _decode_value(br: 'BinaryReader2', table: dict):
        word = 0
        word_length = 0

        while word_length < 16:
            word <<= 1
            bit = br.read_bit()
            word |= bit
            word_length += 1

            # Construct the key as "word_length_word", e.g. "3_5"
            lookup = f"{word_length}_{word}"
            if lookup in table:
                return table[lookup]

        raise Exception("Did not find value in Huffman tree")

    @staticmethod
    def _extend(value: int, length: int) -> int:
        # (1 << (length-1)) is 2^(length-1)
        if length <= 0:
            return value
        boundary = 1 << (length - 1)
        if value < boundary:
            return value + ((-1 << length) + 1)
        else:
            return value

    @staticmethod
    def _clamp(val: int, minimum: int, maximum: int) -> int:
        """
        Equivalent to the C# extension method Clamp<T>(this T val, T min, T max).
        """
        return max(minimum, min(val, maximum))

    # Zig-zag map as in your C# code
    _zigzag_mapping = [
         0,  1,  5,  6, 14, 15, 27, 28,
         2,  4,  7, 13, 16, 26, 29, 42,
         3,  8, 12, 17, 25, 30, 41, 43,
         9, 11, 18, 24, 31, 40, 44, 53,
        10, 19, 23, 32, 39, 45, 52, 54,
        20, 22, 33, 38, 46, 51, 55, 60,
        21, 34, 37, 47, 50, 56, 59, 61,
        35, 36, 48, 49, 57, 58, 62, 63
    ]

    @staticmethod
    def _unzigzag(block: list) -> list:     # checked
        """
        Equivalent to C# private static int[] unzigzag(int[] block)
        """
        tmp = [0]*64
        for i in range(64):
            tmp[i] = block[TexJPEG._zigzag_mapping[i]]
        return tmp

    @staticmethod
    def _dequantize(block: list, quantization_table: list) -> list:     # checked
        for i in range(64):
            block[i] = int(round(block[i] * quantization_table[i] + 0.001))
        return block

class TexDXT:
    # https://github.com/leamsii/Python-DXT-Decompress/blob/master/DXTDecompress.py
    def __init__(self, header, br):
        self.header = header
        self.reader = BytesIO(br)
        self.img_raw = np.zeros((self.header.height, self.header.width, 4), dtype=np.uint8)

    @staticmethod
    def decodeDXT1(header_in, image_bytes) -> bytes:
        tex_dxt = TexDXT(header_in, image_bytes)

        texture = tex_dxt.DXT1Decompress(BytesIO(image_bytes))
        return texture
    @staticmethod
    def decodeDXT5(header_in, image_bytes) -> bytes:
        tex_dxt = TexDXT(header_in, image_bytes)

        texture = tex_dxt.DXT5Decompress(BytesIO(image_bytes))
        return texture

    def DXT1Decompress(self, file):
        blocks_count_width = (self.header.width + 3) // 4
        blocks_count_height = (self.header.height + 3) // 4
        for row in range(blocks_count_height):
            for col in range(blocks_count_width):
                c0 = struct.unpack('<H', file.read(2))[0]
                c1 = struct.unpack('<H', file.read(2))[0]
                ctable = struct.unpack('<I', file.read(4))[0]
                
                for j in range(4):
                    for i in range(4):
                        self.getColors(row * 4, col * 4, i, j, ctable, self.unpackRGB(c0) ,self.unpackRGB(c1), 255)
        return Image.fromarray(self.img_raw, "RGBA")

    def DXT5Decompress(self, file):
        blocks_count_width = (self.header.width + 3) // 4
        blocks_count_height = (self.header.height + 3) // 4
        # Loop through each block and decompress it
        for row in range(blocks_count_height):
            for col in range(blocks_count_width):

                # Get the alpha values
                a0 = struct.unpack('<B', file.read(1))[0]
                a1 = struct.unpack('<B', file.read(1))[0]
                atable = file.read(6)

                acode0 = atable[2] | (atable[3] << 8) | (atable[4] << 16) | (atable[5] << 24)
                acode1 = atable[0] | (atable[1] << 8)

                # Color 1 color 2, color look up table
                c0 = struct.unpack('<H', file.read(2))[0]
                c1 = struct.unpack('<H', file.read(2))[0]
                ctable = struct.unpack('<I', file.read(4))[0]

                # The 4x4 Lookup table loop
                for j in range(4):
                    for i in range(4):
                        alpha = self.getAlpha(j, i, a0, a1, atable, acode0, acode1)
                        self.getColors(row * 4, col * 4, i, j, ctable, self.unpackRGB(c0) ,self.unpackRGB(c1), alpha) # Set the color for the current pixel
        return Image.fromarray(self.img_raw, "RGBA")

    @staticmethod
    def unpackRGB(packed):
        R = (packed >> 11) & 0x1F
        G = (packed >> 5) & 0x3F
        B = (packed) & 0x1F
        R = (R << 3) | (R >> 2)
        G = (G << 2) | (G >> 4)
        B = (B << 3) | (B >> 2)
        return (R, G, B, 255)

    def getColors(self, x, y, i, j, ctable, c0, c1, alpha):
        code = (ctable >> ( 2 * (4 * i + j))) & 0x03 # Get the color of the current pixel
        pixel_color = None

        r0 = c0[0]
        g0 = c0[1]
        b0 = c0[2]

        r1 = c1[0]
        g1 = c1[1]
        b1 = c1[2]
        # Main two colors
        if code == 0:
            pixel_color = (r0, g0, b0, alpha)
        if code == 1:
            pixel_color = (r1, g1, b1, alpha)

        # Use the lookup table to determine the other two colors
        if c0 > c1:
            if code == 2:
                pixel_color = ((2*r0+r1)//3, (2*g0+g1)//3, (2*b0+b1)//3, alpha)
            if code == 3:
                pixel_color = ((r0+2*r1)//3, (g0+2*g1)//3, (b0+2*b1)//3, alpha)
        else:
            if code == 2:
                pixel_color = ((r0+r1)//2, (g0+g1)//2, (b0+b1)//2, alpha)
            if code == 3:
                pixel_color = (0, 0, 0, alpha)
        self.img_raw[(x + i), (y + j), 0] = pixel_color[0]
        self.img_raw[(x + i), (y + j), 1] = pixel_color[1]
        self.img_raw[(x + i), (y + j), 2] = pixel_color[2]
        self.img_raw[(x + i), (y + j), 3] = pixel_color[3]

    def getAlpha(self, i, j, a0, a1, atable, acode0, acode1):
        # Using the same method as the colors calculate the alpha values
        alpha = 255
        alpha_index = 3 * (4 * j+i)
        alpha_code = None

        if alpha_index <= 12:
            alpha_code = (acode1 >> alpha_index) & 0x07
        elif alpha_index == 15:
            alpha_code = (acode1 >> 15) | ((acode0 << 1) & 0x06)
        else:
            alpha_code = (acode0 >> (alpha_index - 16)) & 0x07

        if alpha_code == 0:
            alpha = a0
        elif alpha_code == 1:
            alpha = a1
        else:
            if a0 > a1:
                alpha = ((8-alpha_code) * a0 + (alpha_code-1) * a1) // 7
            else:
                if alpha_code == 6:
                    alpha = 0
                elif alpha_code == 7:
                    alpha = 255
                elif alpha_code == 5:
                    alpha = (1 * a0 + 4 * a1) // 5
                elif alpha_code == 4:
                    alpha = (2 * a0 + 3 * a1) // 5
                elif alpha_code == 3:
                    alpha = (3 * a0 + 2 * a1) // 5
                elif alpha_code == 2:
                    alpha = (4 * a0 + 1 * a1) // 5
                else:
                    alpha = 0 # For safety
        return alpha

class BinaryReader2:
    """
    Equivalent to C# public class BinaryReader2 : BinaryReader
    We implement read_bit() and read_bits() logic using a BytesIO.
    """
    def __init__(self, base_stream: BytesIO):
        self._stream = base_stream
        self._current_byte = 0
        self._index = 8  # so that we trigger a read on first call

    def read_bit(self) -> int:
        """
        Equivalent to C# public byte ReadBit()
        """
        if self._index >= 8:
            # read next byte
            data = self._stream.read(1)
            if not data:
                # We are out of data. In a real decoder, handle end-of-stream carefully.
                return 0
            self._current_byte = data[0]
            self._index = 0

        bit = (self._current_byte >> (7 - self._index)) & 0x1
        self._index += 1
        return bit

    def read_bits(self, num_bits: int) -> int:
        """
        Equivalent to C# public UInt16 ReadBits(byte numBits)
        We limit to 16 bits per original code.
        """
        if num_bits >= 16:
            raise Exception("Invalid bit count")

        result = 0
        for _ in range(num_bits):
            result = (result << 1) | self.read_bit()

        return result

class Tex:
    def __init__(self):
        self.header = None
    class Header:
        SIZE = 112
        def __init__(self):
            self.signature = None,
            self.version = 0
            self.width = 0
            self.height = 0
            self.depth = 0
            self.sides = 0
            self.nr_mip_maps = 0
            self.tex_format = 0
            self.is_compressed = 0
            self.compression_format = 0
            self.layer_infos = []
            self.image_sizes_count = 0
            self.image_sizes = []
            self.unk_06C = 0

        @staticmethod
        def read_header(br):
            header = Tex.Header()
            header.signature = br.read(4).decode('utf-8')
            header.version = struct.unpack('<I', br.read(4))[0]
            header.width = struct.unpack('<I', br.read(4))[0]
            header.height = struct.unpack('<I', br.read(4))[0]
            header.depth = struct.unpack('<I', br.read(4))[0]
            header.sides = struct.unpack('<I', br.read(4))[0]
            header.nr_mip_maps = struct.unpack('<I', br.read(4))[0]
            header.tex_format = struct.unpack('<I', br.read(4))[0]
            header.is_compressed = struct.unpack('<I', br.read(4))[0]
            header.compression_format = struct.unpack('<I', br.read(4))[0]
            header.layer_infos = []
            for _ in range(4):
                quality, has_replacement, replacement = struct.unpack("<BBB", br.read(3))
                header.layer_infos.append({"quality": quality, "has_replacement": has_replacement, "replacement": replacement})
            header.image_sizes_count = struct.unpack('<I', br.read(4))[0]
            header.image_sizes = []
            for _ in range(13):
                header.image_sizes.append(struct.unpack("<I", br.read(4))[0])
            header.unk_06C = struct.unpack('<I', br.read(4))[0]
            return header

        def print(self):
            pr = (
                f"TEX HEADER: {self.signature}\t{self.version}\t{self.width}\t{self.height}\t{self.depth}\t"
                f"{self.sides}\t{self.nr_mip_maps}\t{self.tex_format}\t{self.is_compressed}\t{self.compression_format}\t"
                f"{self.image_sizes_count}\t{self.unk_06C}"
            )
            print(pr)
            print(self.layer_infos)
            print(self.image_sizes)

    @staticmethod
    def read_header(br):
        return Tex.Header.read_header(br)

    @staticmethod
    def decode(br):
        tex = Tex()
        tex.header = tex.read_header(br)

        ofs = tex.header.SIZE
        byte_size = 0
        # Calculate offset and size of the image data
        if tex.header.image_sizes_count > 0:
            br.seek(56)
            for i in range(tex.header.nr_mip_maps - 1):
                ofs += tex.header.image_sizes[i]
            byte_size = tex.header.image_sizes[tex.header.nr_mip_maps - 1]
        else:
            byte_size = len(br.getvalue()) - tex.header.SIZE

        br.seek(ofs)
        image_bytes = br.read(byte_size)
        raw_image_data = None
        texture = None
        # Decode based on format
        if tex.header.tex_format == 0:  # JPEG
            pass
            raw_image_data = TexJPEG.decode(tex.header, image_bytes)
            texture = Image.frombytes("RGBA", (tex.header.width, tex.header.height), raw_image_data)
        elif tex.header.tex_format == 6:  # R8
            print("FORMAT 6!!!!!")
            # texture = Image.frombytes("L", (self.header["width"], self.header["height"]), image_bytes)
        elif tex.header.tex_format == 13:   # DXT1
            br.seek(ofs)
            image_bytes = tex.get_dxt_bytes(tex.header.nr_mip_maps, br, tex.header.width, tex.header.height, 8)
            texture = TexDXT.decodeDXT1(tex.header, image_bytes)
        elif tex.header.tex_format == 15:  # DXT5
            br.seek(ofs)
            image_bytes = tex.get_dxt_bytes(tex.header.nr_mip_maps, br, tex.header.width, tex.header.height, 16)
            texture = TexDXT.decodeDXT5(tex.header, image_bytes)
        else:
            print(f"Unsupported format: {tex.header['format']} for file: {path_to_file}")
        return texture

    @staticmethod
    def decode_and_save(br):
        texture = Tex.decode(br)
        texture.save("output.png")
        return texture

    @staticmethod
    def get_dxt_bytes(mip_level, br, w, h, block_size):
        x = (w + 3) // 4 * (h + 3) // 4 * block_size
        for m in range(mip_level - 1, -1, -1):
            exp = 2 ** m
            width = w // exp
            height = h // exp
            byte_nr = ((width + 3) // 4) * ((height + 3) // 4) * block_size
            output = br.read(byte_nr)
        return output


# file_name = "./AgressorBot_Color.tex"
# with open(file_name, "rb") as br:
#     tex = Tex.decode(br, False)
# tex.header.print()
