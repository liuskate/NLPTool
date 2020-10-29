#coding=utf-8
# 常用的预处理

# ####### 将大量特征文件以二进制的方式合并成大文件 #######################################################
import struct
# 写二进制文件
def pack_write_list(f, fmt_, paras):
    packed_bytes = struct.pack(fmt_, *paras)
    f.write(packed_bytes)

def write_block_to_file(data_block, output, feat_dim=512):
    example_count = len(data_block)
    if example_count == 0:
        print("example count is 0, return")

    offset = 0
    print("start to write data nto file {}".format(output))

    data_handler = open(output, "wb")
    desc_handler = open("{}_desc".format(output), "w")

    desc_handler.write("0 %d 2\n" % example_count)
    for key, feat in data_block:
        cur_size = len(feat)
        cur_len = cur_size // feat_dim
        pack_write_list(data_handler, 'f'*cur_size, feat)
        desc_handler.write("{} 0 {} {} {} {}\n".format(key, offset, cur_size * 4, cur_len, feat_dim))
        offset += cur_size * 4


# 使用描述文件，解析读取数据文件
def read_file(data_file, desc_file):
    data = open(data_file, "rb").read()
    with open(desc_file) as ifd:
        lines = [line.strip() for line in ifd.readlines()]
        num_example = int(lines[0].split(" ")[1])
        assert num_example == len(lines) - 1
        for line in lines[1:]:
            parts = line.split(" ")
            assert len(parts) == 6
            key, offset, byte_size, feat_len, dim = parts
            offset, byte_size, feat_len, dim = int(offset), int(byte_size), int(feat_len), int(dim)
            byte_feat = data[offset: offset + byte_size]
            int_feat = struct.unpack("f"*(feat_len * dim), byte_feat)
            print("{}\t{}".format(key, " ".join(map(str, int_feat))))

# ####### END 将大量特征文件以二进制的方式合并成大文件 #######################################################



