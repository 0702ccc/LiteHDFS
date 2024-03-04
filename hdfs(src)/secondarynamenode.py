import grpc
from concurrent import futures
import file_system_pb2_grpc
import file_system_pb2
import time
import threading
import base64


class SecondaryNameNode(file_system_pb2_grpc.FileSystemServiceServicer):
    def __init__(self, name_node_stub):
        self.name_node_stub = name_node_stub
        self.metadata_file_path = "metadata.txt"  # 文件元数据保存的文件路径

    def perform_checkpoint(self):
        # 获取主节点的文件元数据
        response = self.name_node_stub.GetMetadata(file_system_pb2.FileRequest())
        file_metadata_map = {metadata.file_path: metadata for metadata in response.metadata}

        # # 执行检查点，更新文件元数据
        # for file_path, metadata in file_metadata_map.items():
        #     metadata.version += 1

        # 模拟写入持久存储
        self.save_metadata_to_file(file_metadata_map)

    def save_metadata_to_file(self, metadata_map):
        with open(self.metadata_file_path, "w") as file:
            # 将文件元数据以文本形式写入文件
            for file_path, metadata in metadata_map.items():
                file.write(f"{file_path} {metadata.SerializeToString().hex()}\n")

    def load_metadata_from_file(self):
        metadata_map = {}
        try:
            with open(self.metadata_file_path, "r") as file:
                # 从文件中加载文件元数据
                for line in file:
                    parts = line.split()
                    file_path = parts[0]
                    metadata_hex = parts[1]
                    metadata = file_system_pb2.FileMetadata().FromString(bytes.fromhex(metadata_hex))
                    metadata_map[file_path] = metadata
        except FileNotFoundError:
            pass
        return metadata_map

    def GetMetadata(self, request, context):
        metadata_map = self.load_metadata_from_file()
        # 返回 SecondaryNameNode 中保存的元数据信息
        metadata_list = list(metadata_map.values())
        return file_system_pb2.MetadataResponse(metadata=metadata_list)

    def PeriodicCheckpoint(self):
        while True:
            # 每隔一段时间执行一次检查点
            time.sleep(60)  # 假设每隔1分钟执行一次
            self.perform_checkpoint()


if __name__ == '__main__':
    # 主节点地址
    name_node_address = 'localhost:50051'
    # 创建到主节点的 gRPC stub
    name_node_channel = grpc.insecure_channel(name_node_address)
    name_node_stub = file_system_pb2_grpc.FileSystemServiceStub(name_node_channel)

    secondary_name_node = SecondaryNameNode(name_node_stub)

    # 在程序启动时加载文件元数据
    initial_metadata_map = secondary_name_node.load_metadata_from_file()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_system_pb2_grpc.add_FileSystemServiceServicer_to_server(secondary_name_node, server)
    server.add_insecure_port('[::]:50060')  # 备份节点监听的端口
    print("SecondaryNameNode listening on port 50060")
    server.start()

    # 启动定期执行检查点的线程
    checkpoint_thread = threading.Thread(target=secondary_name_node.PeriodicCheckpoint, daemon=True)
    checkpoint_thread.start()

    server.wait_for_termination()
