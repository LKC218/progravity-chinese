import os
import struct
import json
import shutil

class AsarArchive:
    """
    纯 Python 原生 Electron ASAR 归档文件解析与打包引擎。
    零依赖 (无需 Node.js, npm, @electron/asar)。
    """

    @staticmethod
    def extract(asar_path: str, dest_dir: str) -> bool:
        """从 asar 归档中解压全部文件到 dest_dir"""
        if not os.path.exists(asar_path):
            raise FileNotFoundError(f"ASAR 文件未找到: {asar_path}")

        os.makedirs(dest_dir, exist_ok=True)
        with open(asar_path, 'rb') as f:
            f.seek(12)
            header_size = struct.unpack('<I', f.read(4))[0]
            header_json = f.read(header_size).decode('utf-8')
            header = json.loads(header_json)
            base_offset = 16 + header_size

            def _extract_node(node, cur_dir):
                if 'files' in node:
                    for name, subnode in node['files'].items():
                        target_path = os.path.join(cur_dir, name)
                        if 'files' in subnode:
                            os.makedirs(target_path, exist_ok=True)
                            _extract_node(subnode, target_path)
                        else:
                            if subnode.get('unpacked'):
                                # unpacked 类型文件位于外部 app.asar.unpacked 目录
                                continue
                            offset = int(subnode['offset'])
                            size = int(subnode['size'])
                            f.seek(base_offset + offset)
                            content = f.read(size)
                            os.makedirs(os.path.dirname(target_path), exist_ok=True)
                            with open(target_path, 'wb') as out_f:
                                out_f.write(content)

            _extract_node(header, dest_dir)
        return True

    @staticmethod
    def pack(src_dir: str, asar_dest: str) -> bool:
        """将 src_dir 目录完整重新打包为标准 Electron ASAR 归档文件"""
        if not os.path.isdir(src_dir):
            raise NotADirectoryError(f"源目录不存在: {src_dir}")

        files_to_pack = []
        header = {'files': {}}
        current_offset = 0

        def _build_header(cur_path, cur_node):
            nonlocal current_offset
            entries = sorted(os.listdir(cur_path))
            for name in entries:
                full_path = os.path.join(cur_path, name)
                if os.path.isdir(full_path):
                    sub_node = {'files': {}}
                    cur_node[name] = sub_node
                    _build_header(full_path, sub_node['files'])
                else:
                    size = os.path.getsize(full_path)
                    cur_node[name] = {
                        'size': size,
                        'offset': str(current_offset)
                    }
                    files_to_pack.append((full_path, size))
                    current_offset += size

        _build_header(src_dir, header['files'])

        # JSON 紧凑序列化
        header_json = json.dumps(header, separators=(',', ':')).encode('utf-8')
        # 4 字节对其填充
        pad_len = (4 - (len(header_json) % 4)) % 4
        if pad_len > 0:
            header_json += b' ' * pad_len
        header_size = len(header_json)

        # 写入临时文件再原子替换，保证文件操作安全
        temp_dest = asar_dest + '.tmp_pack'
        with open(temp_dest, 'wb') as out_f:
            # 16 字节 ASAR 标准头: magic(4), total_header_len(4), header_padding(4), json_len(4)
            out_f.write(struct.pack('<IIII', 4, header_size + 8, header_size + 4, header_size))
            out_f.write(header_json)
            for file_path, _ in files_to_pack:
                with open(file_path, 'rb') as in_f:
                    shutil.copyfileobj(in_f, out_f, length=64 * 1024)

        if os.path.exists(asar_dest):
            os.remove(asar_dest)
        os.rename(temp_dest, asar_dest)
        return True
