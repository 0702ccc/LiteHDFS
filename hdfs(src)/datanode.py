# data_node_server.py
import threading
from concurrent import futures
import grpc
import file_system_pb2_grpc
import file_system_pb2
import time
from queue import Queue


class DataNode(file_system_pb2_grpc.FileSystemServiceServicer):
    def __init__(self, data_node_address, name_node_address):
        self.data_storage = {}
        self.name_node_address = name_node_address
        self.data_node_address = data_node_address

    def WriteData(self, request, context):
        file_path = request.file_path
        data = request.data
        offset = request.offset
        if file_path not in self.data_storage:
            self.data_storage[file_path] = b""
        # 获取主节点和次节点列表
        main_node = request.nodes[0]
        secondary_nodes = request.nodes[1:]
        # 阶段一：向所有次节点发送Prepare请求
        prepare_responses = []
        for secondary_node in secondary_nodes:
            print(f"Preparing {secondary_node}")
            vote_request = file_system_pb2.FileRequest(file_path=file_path)
            with grpc.insecure_channel(secondary_node) as channel:
                stub = file_system_pb2_grpc.FileSystemServiceStub(channel)
                prepare_response = stub.Prepare(vote_request)
                prepare_responses.append(prepare_response)

        # 检查所有Prepare响应
        if all(response.success for response in prepare_responses):
            # 阶段二：向所有次节点发送Commit请求
            for secondary_node in secondary_nodes:
                print(f"Committing {secondary_node}")
                with grpc.insecure_channel(secondary_node) as channel:
                    stub = file_system_pb2_grpc.FileSystemServiceStub(channel)
                    commit_response = stub.Commit(request)

            current_data = self.data_storage[file_path]
            # 更新数据存储，简单示例中直接替换指定偏移处的数据
            updated_data = current_data[:offset] + data + current_data[offset + len(data):]
            self.data_storage[file_path] = updated_data
            return file_system_pb2.FileResponse(success=True, message=f"write completed")
        else:
            # 如果有任何Prepare请求失败，通知客户端写入失败
            return file_system_pb2.FileResponse(success=False, message=f"write failed: prepare failed")

    def Prepare(self, request, context):
        # 进行简化，都返回可以写入 实际要进行判断
        return file_system_pb2.FileResponse(success=True, message=f"Vote_Commit")

    def Commit(self, request, context):
        file_path = request.file_path
        offset = request.offset
        data = request.data

        # 在此处处理次节点收到的写请求
        if file_path not in self.data_storage:
            self.data_storage[file_path] = b""
        current_data = self.data_storage[file_path]
        # 更新数据存储，简单示例中直接替换指定偏移处的数据
        updated_data = current_data[:offset] + data + current_data[offset + len(data):]
        self.data_storage[file_path] = updated_data

        # 返回复制成功的信息
        return file_system_pb2.FileResponse(success=True, message="Copy successful")

    def ReadData(self, request, context):
        file_path = request.file_path
        if file_path not in self.data_storage:
            return file_system_pb2.DataResponse(data=b"")

        offset = request.offset
        data = self.data_storage[file_path][offset:]
        return file_system_pb2.DataResponse(data=data)

    def send_heartbeat(self):
        while True:
            time.sleep(10)  # 定期发送心跳消息给NameNode
            print("Sending heartbeat to NameNode")
            with grpc.insecure_channel(self.name_node_address) as channel:
                stub = file_system_pb2_grpc.FileSystemServiceStub(channel)
                response = stub.Heartbeat(file_system_pb2.HeartbeatRequest(data_node_address=self.data_node_address))
                # print("Received heartbeat response from NameNode:", response.status)


if __name__ == '__main__':
    name_node_address = 'localhost:50051'  # 请替换成实际的NameNode地址
    data_node_address = 'localhost:50052'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_node = DataNode(data_node_address, name_node_address)
    file_system_pb2_grpc.add_FileSystemServiceServicer_to_server(data_node, server)
    server.add_insecure_port('[::]:50052')
    server.start()

    heartbeat_thread = threading.Thread(target=data_node.send_heartbeat, daemon=True)
    heartbeat_thread.start()

    server.wait_for_termination()
