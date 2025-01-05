import os
import zlib
import struct
from collections import defaultdict
from io import BytesIO
from pathlib import Path
import lzma
# based on https://github.com/CucFlavius/ws-tool/blob/main/Engine/GameData/Archive.cs

def to_hex(byte_data):
    return ''.join(f'{b:02x}' for b in byte_data)

class IndexFile:
    class Header:
        def __init__(self):
            self.signature = 0
            self.version = 0
            self.index_file_size = 0
            self.ofs_block_table = 0
            self.num_blocks = 0
    class PackBlockHeader:
        def __init__(self, block_offset=0, block_size=0):
            self.block_offset = block_offset
            self.block_size = block_size
    class AIDX:
        def __init__(self, magic=0, version=0, unk1=0, root_block=0):
            self.magic = magic
            self.version = version
            self.unk1 = unk1
            self.root_block = root_block
    class FolderBlock:
        def __init__(self):
            self.num_subdirectories = 0
            self.num_files = 0
            self.sub_directories = []
            self.files = []
            self.names = ""
    class DirectoryEntry:
        def __init__(self, name_offset=0, next_block=0):
            self.name_offset = name_offset
            self.next_block = next_block
    class FileEntry:
        def __init__(self, name_offset=0, flags=0, write_time=0, uncompressed_size=0, compressed_size=0, hash_val=b"", unk2=0):
            self.name_offset = name_offset
            self.flags = flags
            self.write_time = write_time
            self.uncompressed_size = uncompressed_size
            self.compressed_size = compressed_size
            self.hash = hash_val
            self.unk2 = unk2
            self.name = ""

    def __init__(self):
        self.header = None
        self.pack_block_headers = []
        self.aidx_block_number = -1
        self.aidx = None

    def read_index_file(self, data_location, file_name):
        file_path = os.path.join(data_location, file_name)
        if os.path.exists(file_path):
            with open(file_path, "rb") as br:
                self._read_header(br)
                self._read_global_block_info(br)
                self._read_aidx_block(br)
                folder_block = self._read_block(self.aidx.root_block, "AIDX", br)
                DataManager.directory_tree["AIDX"] = folder_block  # Add root directory
        else:
            print(f"Missing file: {file_name}")

    def _read_header(self, br):
        self.header = self.Header()
        self.header.signature = br.read(4).decode('utf-8')      # KCAP
        if self.header.signature != "KCAP":
            print("File signature does not match: KCAP !=" + self.header.signature)
        self.header.version = struct.unpack('<I', br.read(4))[0]
        # print(f"INDEX VERSION: {self.header.version}")
        br.read(512)  # Skip empty bytes
        self.header.index_file_size = struct.unpack("<Q", br.read(8))[0]
        br.read(8)  # Skip empty bytes
        self.header.ofs_block_table, self.header.num_blocks = struct.unpack("<QI", br.read(12))
        br.read(28)  # Skip unknown bytes

    def _read_global_block_info(self, br):
        self.pack_block_headers = []
        br.seek(self.header.ofs_block_table)
        for _ in range(self.header.num_blocks):
            block_offset, block_size = struct.unpack("<QQ", br.read(16))
            pbh = self.PackBlockHeader(block_offset, block_size)
            if block_size == 16:
                self.aidx_block_number = len(self.pack_block_headers)
            self.pack_block_headers.append(pbh)

    def _read_aidx_block(self, br):
        if self.aidx_block_number != -1:
            br.seek(self.pack_block_headers[self.aidx_block_number].block_offset)
            self.aidx = self.AIDX(*struct.unpack("<IIII", br.read(16)))
        else:
            print("Missing AIDX Block.")

    def _read_block(self, block_number, current_dir, br):
        br.seek(self.pack_block_headers[block_number].block_offset)
        folder_block = self.FolderBlock()
        folder_block.num_subdirectories, folder_block.num_files = struct.unpack("<II", br.read(8))
        if folder_block.num_subdirectories > 0:
            folder_block.sub_directories = [self._read_directory_entry(br) for _ in range(folder_block.num_subdirectories)]
        if folder_block.num_files > 0:
            folder_block.files = [self._read_file_entry(br) for _ in range(folder_block.num_files)]
        remaining_size = self.pack_block_headers[block_number].block_size - (br.tell() - self.pack_block_headers[block_number].block_offset)
        folder_block.names = br.read(remaining_size).decode("utf-8", errors="ignore")

        if folder_block.sub_directories:
            for directory_entry in folder_block.sub_directories:
                word = ""
                increment = 0
                for _ in range(200):
                    c = folder_block.names[directory_entry.name_offset + increment]
                    increment += 1
                    if c != "\0":
                        word += c
                    else:
                        break
                sub_folder_block = self._read_block(directory_entry.next_block, os.path.join(current_dir, word), br)
                DataManager.directory_tree[os.path.join(current_dir, word)] = sub_folder_block

        if folder_block.files:
            for file_entry in folder_block.files:
                word = ""
                increment = 0
                for _ in range(250):
                    c = folder_block.names[file_entry.name_offset + increment]
                    increment += 1
                    if c == "\0":
                        break
                    else:
                        word += c
                hash_value = to_hex(file_entry.hash)
                file_entry.name = word
                if hash_value not in DataManager.file_names:
                    DataManager.file_names[hash_value] = word
                DataManager.file_list[os.path.join(current_dir, word)] = file_entry

        return folder_block

    def _read_directory_entry(self, br):
        return self.DirectoryEntry(*struct.unpack("<II", br.read(8)))

    def _read_file_entry(self, br):
        return self.FileEntry(*struct.unpack("<IIQQQ20sI", br.read(56)))

class ArchiveFile:
    class Header:
        def __init__(self):
            self.signature = 0
            self.version = 0
            self.index_file_size = 0
            self.ofs_block_table = 0
            self.num_blocks = 0

    class PackBlockHeader:
        def __init__(self):
            self.block_offset = 0
            self.block_size = 0

    class AARC:
        def __init__(self):
            self.magic = 0
            self.version = 0
            self.num_aarc_entries = 0
            self.ofs_aarc_entries = 0

    class AARCEntry:
        def __init__(self):
            self.block_index = 0
            self.sha_hash = b""
            self.uncompressed_size = 0

    def __init__(self):
        self.header = ArchiveFile.Header()
        self.aarc_block_number = -1
        self.aarc = ArchiveFile.AARC()
        self.aarc_entries = {}
        self.pack_block_headers = []

    def read_archive_file(self, data_location, file_name):
        file_path = os.path.join(data_location, file_name)
        if os.path.exists(file_path):
            with open(file_path, "rb") as br:
                self._read_header(br)
                self._read_global_block_info(br)
                self._read_aarc_block(br)
                self._read_aarc_entries(br)
        else:
            print(f"Missing file: {file_name}")

    def _read_header(self, br):
        self.header.signature = br.read(4).decode('utf-8')      # KCAP
        if self.header.signature != "KCAP":
            print("File signature does not match: KCAP !=" + self.header.signature)
        self.header.version = struct.unpack('<I', br.read(4))[0]
        # print(f"ARCHIVE VERSION: {self.header.version}")
        br.read(512)  # Skip empty
        self.header.index_file_size = struct.unpack("<Q", br.read(8))[0]
        br.read(8)  # Skip empty
        self.header.ofs_block_table, self.header.num_blocks = struct.unpack("<QI", br.read(12))
        br.read(28)  # Skip unknown

    def _read_global_block_info(self, br):
        self.pack_block_headers = []
        br.seek(self.header.ofs_block_table)
        for _ in range(self.header.num_blocks):
            pbh = ArchiveFile.PackBlockHeader()
            pbh.block_offset, pbh.block_size = struct.unpack("<QQ", br.read(16))
            if pbh.block_size == 16:
                self.aarc_block_number = len(self.pack_block_headers)
            self.pack_block_headers.append(pbh)

    def _read_aarc_block(self, br):
        if self.aarc_block_number != -1:
            br.seek(self.pack_block_headers[self.aarc_block_number].block_offset)
            self.aarc.magic, self.aarc.version, self.aarc.num_aarc_entries, self.aarc.ofs_aarc_entries = struct.unpack("<IIII", br.read(16))
        else:
            print("Missing AARC Block.")

    def _read_aarc_entries(self, br):
        br.seek(self.pack_block_headers[self.aarc.ofs_aarc_entries].block_offset)
        self.aarc_entries = {}
        for _ in range(self.aarc.num_aarc_entries):
            aarc_entry = ArchiveFile.AARCEntry()
            aarc_entry.block_index = struct.unpack("<I", br.read(4))[0]
            aarc_entry.sha_hash = br.read(20)
            aarc_entry.uncompressed_size = struct.unpack("<Q", br.read(8))[0]
            hash_value = to_hex(aarc_entry.sha_hash)
            if hash_value not in self.aarc_entries:
                self.aarc_entries[hash_value] = aarc_entry
                
class DataManager:
    data_source = "ClientData"
    directory_tree = {}
    file_names = {}
    file_list = {}

    def __init__(self):
        self.index = None
        self.archive = None
        self.install_location = None

    def initialize_data(self, path):
        self.install_location = path
        if self.install_location:
            data_location = os.path.join(os.path.dirname(self.install_location), "Patch")
            self.index = IndexFile()
            self.index.read_index_file(data_location, f"{self.data_source}.index")
            self.archive = ArchiveFile()
            self.archive.read_archive_file(data_location, f"{self.data_source}.archive")

    @staticmethod
    def extract_file(path):
        data = DataManager.get_file_bytes(path)
        output_path = Path("C:/") / Path(path).parent
        output_path.mkdir(parents=True, exist_ok=True)
        with open(f"C:/{path}", "wb") as f:
            f.write(data)
        return data

    def get_file_bytes(self, path):
        if path in self.file_list:
            file_entry = self.file_list[path]
            compression = file_entry.flags
            byte_hash = file_entry.hash
            hash_value = to_hex(byte_hash)

            if hash_value in self.archive.aarc_entries:
                aarc_entry = self.archive.aarc_entries[hash_value]
                pack_block_header = self.archive.pack_block_headers[aarc_entry.block_index]
                file_path = os.path.join(os.path.dirname(self.install_location), "Patch", f"{self.data_source}.archive")
                with open(file_path, "rb") as f:
                    f.seek(pack_block_header.block_offset)
                    data = f.read(pack_block_header.block_size)

                if compression == 3:
                    return DataManager.decompress_zlib(data, file_entry.uncompressed_size)
                elif compression == 5:
                    return DataManager.decompress_lzma(data, file_entry.uncompressed_size)
                else:
                    return data
            else:
                print(f"Missing AARC Entry: {hash_value}")
                return None
        else:
            print(f"Missing File: {path}")
            return None

    @staticmethod
    def decompress_zlib(data, decompressed_size):
        try:
            decompressed_data = zlib.decompress(data[2:], bufsize=decompressed_size)
            return decompressed_data
        except Exception as e:
            print(f"ZLIB Decompression Error: {e}")
            return None

    @staticmethod
    def decompress_lzma(data, decompressed_size):
        # maybe this also works: https://github.com/Narthorn/Halon/blob/master/halon.py
        try:
            filter_props = lzma._decode_filter_properties(lzma.FILTER_LZMA1, data[:5])
            dec = lzma.LZMADecompressor(lzma.FORMAT_RAW, None, [filter_props])
            decompressed_data = dec.decompress(data[5:])
            return decompressed_data
        except Exception as e:
            print(f"LZMA Decompression Error: {e}")
            return None

    def get_folder_list(self, path):
        folder_list = []
        if path in self.directory_tree and self.directory_tree[path].sub_directories:
            for directory_entry in self.directory_tree[path].sub_directories:
                word = ""
                increment = 0
                for _ in range(200):
                    c = self.directory_tree[path].names[directory_entry.name_offset + increment]
                    increment += 1
                    if c != "\0":
                        word += c
                    else:
                        break
                folder_list.append(word)
        return folder_list

    def get_file_list(self, path):
        file_list = {}
        if path in self.directory_tree and self.directory_tree[path].files:
            for file_entry in self.directory_tree[path].files:
                hash_value = to_hex(file_entry.hash)
                if hash_value in DataManager.file_names and DataManager.file_names[hash_value] not in file_list:
                    file_list[file_entry.name] = file_entry
        return file_list

