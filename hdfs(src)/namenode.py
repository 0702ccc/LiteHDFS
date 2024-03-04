import os
import threading
from concurrent import futures
import random

import grpc
import file_system_pb2_grpc
import file_system_pb2
import time


class FileLock:
    def __init__(self):
        self.readers = set()
        self.writer = None
        self.lock_timeout = None
        self.lock_time = time.time()  # 初始化锁的时间


class DirectoryNode:
    def __init__(self, name):
        self.name = name
        self.children = {}

    def add_child(self, child_name):
        if child_name not in self.children:
            self.children[child_name] = DirectoryNode(child_name)

    def remove_child(self, child_name):
        if child_name in self.children:
            del self.children[child_name]

    def get_child(self, child_name):
        return self.children.get(child_name)

    def list_children(self):
        return list(self.children.keys())


class NameNode(file_system_pb2_grpc.FileSystemServiceServicer):
    def __init__(self):
        # 文件元数据
        self.file_metadata = {}
        # 目录结构
        self.directory_structure = DirectoryNode("")
        # 用于存储活动的DataNode信息
        self.data_nodes = {}
        # 用于存储文件锁信息
        self.file_locks = {}
        # 锁的超时时间，单位秒
        self.lock_timeout = 60
        # 加载 SecondaryNameNode 中的元数据
        self.load_metadata_from_secondary_name_node()

    def load_metadata_from_secondary_name_node(self):
        secondary_name_node_address = 'localhost:50060'
        # 创建到 SecondaryNameNode 的 gRPC stub
        secondary_name_node_stub = file_system_pb2_grpc.FileSystemServiceStub(
            grpc.insecure_channel(secondary_name_node_address))
        # 使用 gRPC 调用 SecondaryNameNode 获取元数据
        response = secondary_name_node_stub.GetMetadata(file_system_pb2.FileRequest())
        # 将元数据加载到 NameNode 中并创建目录
        self.file_metadata = {metadata.file_path: metadata for metadata in response.metadata}

        # 根据元数据构建目录结构
        self.directory_structure = DirectoryNode("")
        for file_path in self.file_metadata:
            components = file_path.split("/")
            current_node = self.directory_structure
            for component in components:
                if component:
                    child_node = current_node.get_child(component)
                    if child_node is None:
                        # 如果子节点不存在，则创建一个新的子节点
                        current_node.add_child(component)
                        child_node = current_node.get_child(component)
                    current_node = child_node

        # # 打印目录结构
        # def print_directory_structure(node, indent=""):
        #     print(f"{indent}{node.name}")
        #     for child_name, child_node in node.children.items():
        #         print_directory_structure(child_node, indent + "  ")
        #
        # print("Directory Structure:")
        # print_directory_structure(self.directory_structure)

    def GetMetadata(self, request, context):
        # 返回 NameNode 中保存的元数据信息
        metadata_list = list(self.file_metadata.values())
        return file_system_pb2.MetadataResponse(metadata=metadata_list)

    def traverse_directory(self, path):
        current_node = self.directory_structure
        components = path.split("/")
        for component in components:
            if component:
                current_node = current_node.get_child(component)
                if current_node is None:
                    return None
        return current_node

    def GetFileMetadata(self, request, context):
        file_path = request.file_path
        if file_path not in self.file_metadata:
            print(f"File '{file_path}' not found.")
            return file_system_pb2.FileMetadataResponse()
        metadata = self.file_metadata[file_path]
        print(f"File '{file_path}' metadata retrieved: {metadata}")
        return file_system_pb2.FileMetadataResponse(metadata=metadata)

    def GetFileVersion(self, request, context):
        file_path = request.file_path

        # 获取文件所在的目录
        directory = os.path.dirname(file_path)
        parent_node = self.traverse_directory(directory)

        if parent_node is not None:
            # 判断文件路径是否已经存在
            if parent_node.get_child(os.path.basename(file_path)):
                # 文件已存在，返回文件版本
                file_metadata = self.file_metadata[file_path]
                return file_system_pb2.FileVersion(success=True, version=file_metadata.version)
            else:
                print(f"File '{file_path}' not found.")
                return file_system_pb2.FileVersion(success=False)
        else:
            print(f"Directory '{directory}' not found.")
            return file_system_pb2.FileVersion(success=False)

    def CreateFile(self, request, context):
        file_path = request.file_path
        owner = request.owner
        permissions = request.permissions
        if file_path in self.file_metadata:  # 如果该文件已经存在
            print(f"File '{file_path}' already exists.")
            return file_system_pb2.FileResponse(success=False, message="File already exists.")

        # 获取文件所在的目录
        directory = os.path.dirname(file_path)
        parent_node = self.traverse_directory(directory)

        if parent_node is not None:
            # 更新目录结构
            parent_node.add_child(os.path.basename(file_path))
            self.file_metadata[file_path] = file_system_pb2.FileMetadata(file_path=file_path, size=0, owner=owner,
                                                                         permissions=permissions, version=0)

            print(f"File '{file_path}' created successfully.")
            return file_system_pb2.FileResponse(success=True, message=f"File '{file_path}' created successfully.")
        else:
            print(f"Directory '{directory}' not found.")
            return file_system_pb2.FileResponse(success=False, message=f"Directory '{directory}' not found.")

    def DeleteFile(self, request, context):
        file_path = request.file_path
        if file_path not in self.file_metadata:
            print(f"File '{file_path}' not found.")
            return file_system_pb2.FileResponse(success=False, message=f"File '{file_path}' not found.")
        # 删除文件的块信息
        del self.file_metadata[file_path]
        # 获取文件所在的目录
        directory = os.path.dirname(file_path)
        parent_node = self.traverse_directory(directory)
        if parent_node is not None:
            # 更新目录结构
            parent_node.remove_child(os.path.basename(file_path))
            print(f"File '{file_path}' deleted successfully.")
            return file_system_pb2.FileResponse(success=True, message=f"File '{file_path}' deleted successfully.")
        else:
            print(f"Directory '{directory}' not found.")
            return file_system_pb2.FileResponse(success=False, message=f"Directory '{directory}' not found.")

    def RenameFile(self, request, context):
        old_path = request.old_path
        new_path = request.new_path
        if old_path not in self.file_metadata:
            print(f"File '{old_path}' not found.")
            return file_system_pb2.FileResponse(success=False, message=f"File '{old_path}' not found.")
        parent_node = self.traverse_directory(os.path.dirname(old_path))
        if parent_node is not None:  # 更新目录结构，修改元数据
            parent_node.remove_child(os.path.basename(old_path))
            parent_node.add_child(os.path.basename(new_path))
            file_metadata = self.file_metadata.pop(old_path)
            file_metadata.file_path = new_path
            self.file_metadata[new_path] = file_metadata
            print(f"File '{old_path}' renamed to '{new_path}' successfully.")
            return file_system_pb2.FileResponse(success=True,
                                                message=f"File '{old_path}' renamed to '{new_path}' successfully.")
        else:
            print(f"Parent directory not found: {os.path.dirname(old_path)}")
            return file_system_pb2.FileResponse(success=False,
                                                message=f"Parent directory not found: {os.path.dirname(old_path)}")

    def ListFiles(self, request, context):
        directory = request.directory
        directory_node = self.traverse_directory(directory)
        if directory_node is not None:
            files = directory_node.list_children()
            print(f"Files in directory '{directory}': {files}")
            return file_system_pb2.FileListResponse(files=files)
        else:
            print(f"Directory '{directory}' not found.")
            return file_system_pb2.FileListResponse()

    def MakeDirectory(self, request, context):
        directory = request.directory
        new_directory = request.new_directory
        parent_node = self.traverse_directory(directory)
        if parent_node is not None:
            parent_node.add_child(new_directory)
            print(f"Directory '{new_directory}' created successfully.parent name is {parent_node.name}")
            return file_system_pb2.FileResponse(success=True, message="Directory created successfully.")
        else:
            print(f"Parent directory '{directory}' not found.")
            return file_system_pb2.FileResponse(success=False, message="Parent directory not found.")

    def Heartbeat(self, request, context):
        # 处理DataNode的心跳信息
        data_node_address = request.data_node_address
        print(f"Received heartbeat from DataNode at {data_node_address}")
        # 在实际情况中，你可能还会更新DataNode的状态或其他信息
        self.data_nodes[data_node_address] = time.time()  # 更新时间戳
        # 返回心跳响应
        return file_system_pb2.HeartbeatResponse(status="OK")

    def clean_expired_data_nodes(self):
        # 定期清理过期的DataNode信息
        while True:
            time.sleep(60)  # 每隔60秒清理一次
            current_time = time.time()
            expired_nodes = [addr for addr, timestamp in self.data_nodes.items() if
                             current_time - timestamp > 60]  # 假设超过60秒没有心跳就认为过期
            for addr in expired_nodes:
                del self.data_nodes[addr]

    # def ChooseDataNodes(self, file_path, num_replicas):
    #     # 在实际生产环境中，你可能需要更复杂的逻辑来选择DataNode
    #     available_nodes = list(self.data_nodes.keys())
    #     selected_nodes = random.sample(available_nodes, min(num_replicas, len(available_nodes)))
    #     return

    def ChooseDataNodes(self, file_path, num_replicas):
        # 在实际生产环境中，需要更复杂的逻辑来选择DataNode
        # 获取文件元数据
        if file_path in self.file_metadata:
            file_metadata = self.file_metadata[file_path]
            if file_metadata and file_metadata.data_node_addresses:
                # 如果文件元数据中已有DataNodes信息，返回这些DataNodes
                selected_nodes = file_metadata.data_node_addresses
            else:
                # 否则，随机选择DataNodes
                available_nodes = list(self.data_nodes.keys())
                selected_nodes = random.sample(available_nodes, min(num_replicas, len(available_nodes)))
            return selected_nodes
        else:
            print(f"File '{file_path}' not found.")
            return

    def WriteFile(self, request, context):
        # 从客户端接收写入请求
        file_path = request.file_path
        num_replicas = 3  # 假设每个数据块有3个副本
        # 获取文件所在的目录
        directory = os.path.dirname(file_path)
        parent_node = self.traverse_directory(directory)
        if parent_node is not None:
            # 判断文件路径是否已经存在
            if parent_node.get_child(os.path.basename(file_path)):
                # 文件已存在，返回DataNode地址
                data_nodes = self.ChooseDataNodes(file_path, num_replicas)
                print(f"File '{file_path}' write process initiated.")
                return file_system_pb2.DataNodeListResponse(success=True, data_node_addresses=data_nodes)
            else:
                print(f"file '{file_path}' not found.")
                return file_system_pb2.DataNodeListResponse(success=False, message="filepath not found.")
        else:
            print(f"Directory '{directory}' not found.")
            return file_system_pb2.DataNodeListResponse(success=False, message="Parent directory not found.")

    def ClientWriteComplete(self, request, context):
        # 处理客户端写入完成的消息
        file_path = request.file_path
        data_node_addresses = request.nodes
        version = request.version
        print(f"write message for file '{file_path}' at DataNode； {data_node_addresses}")
        # 更新元数据
        new_metadata = file_system_pb2.FileMetadata(
            file_path=file_path,
            size=self.file_metadata[file_path].size,
            data_node_addresses=data_node_addresses,
            owner=self.file_metadata[file_path].owner,
            permissions=self.file_metadata[file_path].permissions,
            version=version,
        )
        # 更新字典中的元数据
        self.file_metadata[file_path] = new_metadata
        return file_system_pb2.FileResponse(success=True, message="Write complete message processed.")

    def GetDatanode(self, request, context):  # 返回存有对应文件的数据节点
        file_path = request.file_path
        if file_path not in self.file_metadata:
            return file_system_pb2.DataNodeListResponse(success=False, message="No such File.")
        data_node_addresses = self.file_metadata[file_path].data_node_addresses
        if data_node_addresses:
            return file_system_pb2.DataNodeListResponse(success=True, data_node_addresses=data_node_addresses)
        else:
            return file_system_pb2.DataNodeListResponse(success=False, message="No available datanode get")

    def ChangePermissions(self, request, context):
        file_path = request.file_path
        owner = request.owner
        new_permissions = request.permissions
        # 根据 file_path 获取文件元数据
        file_metadata = self.file_metadata[file_path]
        if not file_metadata:
            return file_system_pb2.FileResponse(success=False, message="File not found.")
        if owner == "1" or owner == file_metadata.owner:
            # 在这里根据实际需要修改文件权限
            file_metadata.permissions = new_permissions
            return file_system_pb2.FileResponse(success=True, message="Permissions changed successfully.")
        else:
            return file_system_pb2.FileResponse(success=False, message="Permissions denied.")

    def AddGroup(self, request, context):
        file_path = request.file_path
        user = request.owner
        # 根据 file_path 获取文件元数据
        file_metadata = self.file_metadata[file_path]
        if not file_metadata:
            return file_system_pb2.FileResponse(success=False, message="File not found.")
            # 在这里根据实际需要修改文件权限
        file_metadata.group.append(user)
        return file_system_pb2.FileResponse(success=True, message="User added successfully.")

    def CheckPermission(self, file_path, user):
        file_metadata = self.file_metadata[file_path]
        permission = file_metadata.permissions
        if user == file_metadata.owner:
            binary_permission = bin(int(permission[0]))[2:].zfill(3)
        elif user in file_metadata.group:
            binary_permission = bin(int(permission[1]))[2:].zfill(3)
        else:
            binary_permission = bin(int(permission[2]))[2:].zfill(3)
        return binary_permission

    def LockFile(self, request, context):
        file_path = request.file_path
        user = request.owner
        lock_type = request.type
        if file_path not in self.file_locks:
            self.file_locks[file_path] = FileLock()
        lock = self.file_locks[file_path]
        lock.lock_time = time.time()  # 更新锁的时间
        if lock_type == "read":
            permission = self.CheckPermission(file_path, user)
            if permission[0] == "1":
                if lock.writer is None or lock.writer == user:
                    lock.readers.add(user)
                    return file_system_pb2.FileResponse(success=True,
                                                        message=f"File opened successfully with {lock_type} lock.")
                else:
                    return file_system_pb2.FileResponse(success=False,
                                                        message="File is writen by another user,can not read.")
            else:
                return file_system_pb2.FileResponse(success=False, message="Permission denied.")
        elif lock_type == "write":
            permission = self.CheckPermission(file_path, user)
            if permission[1] == "1":
                if (lock.readers == {user} or not lock.readers) and (lock.writer is None or lock.writer == user):
                    lock.writer = user
                    return file_system_pb2.FileResponse(success=True,
                                                        message=f"File opened successfully with {lock_type} lock.")
                else:
                    return file_system_pb2.FileResponse(success=False,
                                                        message="File is read by other user, can not write.")
            else:
                return file_system_pb2.FileResponse(success=False, message="Permission denied.")
        return file_system_pb2.FileResponse(success=False, message="File is locked by another user.")

    def UnlockFile(self, request, context):
        file_path = request.file_path
        user = request.owner
        if self.unlock_file(file_path, user):
            return file_system_pb2.FileResponse(success=True, message="File closed successfully.")
        else:
            return file_system_pb2.FileResponse(success=False, message="File is not locked by user.")

    def unlock_file(self, file_path, user):
        if file_path in self.file_locks:
            lock = self.file_locks[file_path]
            if user in lock.readers:
                lock.readers.remove(user)
            if lock.writer == user:
                lock.writer = None
            return True
        return False

    def clean_expired_locks(self):
        while True:
            time.sleep(5)  # 每隔5秒清理一次
            current_time = time.time()
            for file_path, lock in list(self.file_locks.items()):
                if current_time - lock.lock_time > self.lock_timeout:
                    self.unlock_file(file_path, lock.writer)
                    for reader in lock.readers.copy():
                        self.unlock_file(file_path, reader)


if __name__ == '__main__':
    name_node = NameNode()  # 创建一个 NameNode 实例
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_system_pb2_grpc.add_FileSystemServiceServicer_to_server(name_node, server)
    server.add_insecure_port('[::]:50051')
    print("Server listening on port 50051")
    server.start()

    # 启动定期清理线程
    cleaning_thread = threading.Thread(target=name_node.clean_expired_data_nodes, daemon=True)
    cleaning_thread.start()
    lock_cleaning_thread = threading.Thread(target=name_node.clean_expired_locks, daemon=True)
    lock_cleaning_thread.start()

    server.wait_for_termination()
