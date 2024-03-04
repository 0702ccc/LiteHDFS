import random
import grpc
import file_system_pb2_grpc
import file_system_pb2


class AutoSelectDataNodeClient:
    def __init__(self):
        self.client_id = "1"
        self.name_node_stub = self.create_name_node_stub()
        self.data_node_stub = None  # Initialize with None
        self.current_directory = ""  # Track the current working directory
        self.file_cache = {}  # 字典用于存储文件内容缓存

    def create_name_node_stub(self):
        channel = grpc.insecure_channel('localhost:50051')
        return file_system_pb2_grpc.FileSystemServiceStub(channel)

    def read_file_content(self, file_path, offset):
        # 尝试从缓存中获取文件内容
        cached_entry = self.file_cache.get(file_path)
        file_response = self.name_node_stub.GetFileVersion(file_system_pb2.FileRequest(file_path=file_path.strip()))
        file_version = file_response.version
        if cached_entry:
            cached_content = cached_entry["content"]
            cached_version = cached_entry["version"]
            if cached_version >= file_version:
                print("Cache hit")
                return cached_content[offset:]
        if file_version == 0:
            print("File is empty")
            self.file_cache[file_path] = {"content": b"", "version": file_version, "dirty": False}
            return None
        # 如果缓存中不存在，从 DataNode 获取文件内容
        response = self.name_node_stub.GetDatanode(
            file_system_pb2.FileRequest(file_path=file_path.strip(), owner=self.client_id))
        if response.success:
            data_node_addresses = response.data_node_addresses
            selected_data_node = random.choice(data_node_addresses)
            data_node_channel = grpc.insecure_channel(selected_data_node)
            data_node_stub = file_system_pb2_grpc.FileSystemServiceStub(data_node_channel)
            data_node_response = data_node_stub.ReadData(
                file_system_pb2.DataRequest(
                    file_path=file_path.strip(),
                    offset=int(offset),
                )
            )
            print(f"Cache miss, Reading data from datanode: {selected_data_node}")

            # 将获取到的文件内容放入缓存
            self.file_cache[file_path] = {"content": data_node_response.data, "version": file_version, "dirty": False}

            return data_node_response.data[offset:]
        else:
            print(f"Error: {response.message}.")
            return None

    def write_file_content(self, file_path, data, offset):
        # 将写入的数据放入缓存
        # 首先更新缓存中的内容，确保是在最新数据中写入
        self.read_file_content(file_path, offset)
        current_content = self.file_cache[file_path]["content"]
        new_content = current_content[:offset] + data
        self.file_cache[file_path]["content"] = new_content
        self.file_cache[file_path]["dirty"] = True

    def flush_cache(self, file_path):
        # 在这里实现将缓存中的数据刷写到实际的存储位置的逻辑
        # 可以调用相应的 gRPC 方法将数据传输到 DataNode
        if self.file_cache[file_path]["dirty"]:
            self.file_cache[file_path]["version"] += 1
        # 获取 DataNode 地址
        response = self.name_node_stub.WriteFile(
            file_system_pb2.FileRequest(file_path=file_path.strip(), owner=self.client_id))

        if response.success:
            data_node_addresses = response.data_node_addresses
            selected_data_node = data_node_addresses[0]  # 主节点选择策略还未实现

            # 建立选定 DataNode 的 gRPC stub
            data_node_channel = grpc.insecure_channel(selected_data_node)
            data_node_stub = file_system_pb2_grpc.FileSystemServiceStub(data_node_channel)

            # 刷写缓存中的数据到 DataNode
            data_node_response = data_node_stub.WriteData(
                file_system_pb2.DataRequest_main(
                    file_path=file_path.strip(),
                    data=self.file_cache[file_path]["content"],
                    offset=0,  # 从头开始写
                    nodes=data_node_addresses
                )
            )
            if data_node_response.success:
                print(f"Cache flush, Data successfully written to DataNode at {selected_data_node}")
                self.name_node_stub.ClientWriteComplete(
                    file_system_pb2.DataRequest_main(file_path=file_path.strip(), nodes=data_node_addresses,
                                                     version=self.file_cache[file_path]["version"]))
                # 关闭 DataNode 的 channel
                data_node_channel.close()
            else:
                print(f"Data written to DataNode at {selected_data_node} failed!!")
            # 关闭 DataNode 的 channel
        else:
            print(f"Error: {response.message}")

    def GetLock(self, file_path, type):
        response = self.name_node_stub.LockFile(
            file_system_pb2.LockRequest(file_path=file_path.strip(), owner=self.client_id, type=type))
        print("Get Lock Response:", response.message)
        return response.success

    def Unlock(self, file_path):
        cached_entry = self.file_cache.get(file_path)
        if cached_entry:
            self.flush_cache(file_path)
        response = self.name_node_stub.UnlockFile(
            file_system_pb2.LockRequest(file_path=file_path.strip(), owner=self.client_id))
        print("Close File Response:", response.message)
        return response.success

    def run(self):
        while True:
            print(f"Current working directory: {self.current_directory}")
            command = input("Enter a command (type 'help' for a list of commands): ")
            if command == "help":
                print("\nAvailable Commands:")
                print("1. create_file <file_path> <permission>")
                print("2. get_m <file_path>")
                print("3. open <file_path>")
                print("3.1 write <data> <offset>")
                print("3.2 read <offset>")
                print("3.3 close")
                print("4. rename_file <file_path> <file_path>")
                print("5. delete_file <file_path>")
                print("6. ls <directory>")
                print("7. mkdir <directory>")
                print("8. cd <directory>")
                print("9. cd.. ")
                print("10. chmod <file_path> <permissions>")
                print("11, usermod <file_path> <user_id>")
                print("12. exit")
            elif command.startswith("create_file"):
                _, file_path, permissions = command.split(maxsplit=2)
                file_path = f"{self.current_directory}/{file_path}"
                response = self.name_node_stub.CreateFile(
                    file_system_pb2.FileRequest(file_path=file_path.strip(), owner=self.client_id,
                                                permissions=permissions))
                print("Create File Response:", response.message)
            elif command.startswith("get_m"):
                _, file_path = command.split(maxsplit=1)
                file_path = f"{self.current_directory}/{file_path}"
                response = self.name_node_stub.GetFileMetadata(
                    file_system_pb2.FileRequest(file_path=file_path.strip()))
                print("File Metadata:", response.metadata)
            elif command.startswith("write_data"):
                _, file_path, data, offset = command.split(maxsplit=3)
                file_path = f"{self.current_directory}/{file_path}"
                # 使用缓存的 write_file_content 方法
                self.write_file_content(file_path, data.encode(), int(offset))

            elif command.startswith("read_data"):
                _, file_path, offset = command.split(maxsplit=2)
                file_path = f"{self.current_directory}/{file_path}"
                # 使用缓存的 read_file_content 方法
                file_content = self.read_file_content(file_path, int(offset))
                if file_content:
                    print("File Content:", file_content.decode('utf-8'))
                else:
                    print("Read data failed!!!")

            elif command.startswith("delete_file"):
                _, file_path = command.split(maxsplit=1)
                file_path = f"{self.current_directory}/{file_path}"
                response = self.name_node_stub.DeleteFile(file_system_pb2.FileRequest(file_path=file_path.strip()))
                print("Delete File Response:", response)

            elif command.startswith("rename_file"):
                _, old_path, new_path = command.split(maxsplit=2)
                old_path = f"{self.current_directory}/{old_path}"
                new_path = f"{self.current_directory}/{new_path}"
                if self.GetLock(old_path, "write"):
                    response = self.name_node_stub.RenameFile(
                        file_system_pb2.RenameRequest(old_path=old_path.strip(), new_path=new_path.strip())
                    )
                    print(response.message)
                    self.Unlock(old_path)

            elif command.startswith("ls"):
                _ = command.split(maxsplit=1)
                response = self.name_node_stub.ListFiles(
                    file_system_pb2.DirectoryRequest(directory=self.current_directory))
                if response.files:
                    print(f"Files in directory '{self.current_directory}': {response.files}")
                else:
                    print(f"No files found in directory '{self.current_directory}'.")

            elif command.startswith("mkdir"):
                _, directory = command.split(maxsplit=1)
                response = self.name_node_stub.MakeDirectory(
                    file_system_pb2.DirectoryRequest(directory=self.current_directory, new_directory=directory.strip()))
                print("Make Directory Response:", response)
            elif command == "cd..":
                self.current_directory = "/".join(self.current_directory.split("/")[:-1])
                print("Change Directory Success:", self.current_directory)
            elif command.startswith("cd"):
                _, directory = command.split(maxsplit=1)
                self.current_directory = f"{self.current_directory}/{directory.strip()}"
                print("Change Directory Success:", self.current_directory)

            elif command.startswith("chmod"):
                _, file_path, permissions = command.split(maxsplit=2)
                file_path = f"{self.current_directory}/{file_path}"
                # 在这里调用相应的 gRPC 接口以修改文件权限
                response = self.name_node_stub.ChangePermissions(
                    file_system_pb2.FileRequest(
                        file_path=file_path.strip(),
                        owner=self.client_id,
                        permissions=permissions
                    )
                )
                print("Change Permissions Response:", response.message)

            elif command.startswith("usermod"):
                _, file_path, user_id = command.split(maxsplit=2)
                file_path = f"{self.current_directory}/{file_path}"
                if self.client_id == "1":
                    response = self.name_node_stub.AddGroup(
                        file_system_pb2.FileRequest(
                            file_path=file_path.strip(),
                            owner=self.client_id
                        )
                    )
                    print(response.message)
                else:
                    print("Permission denied!!")

            elif command.startswith("open"):
                _, file_path = command.split(maxsplit=1)
                file_path = f"{self.current_directory}/{file_path}"
                if self.GetLock(file_path, "read"):
                    print(f"File '{file_path}' opened successfully.")
                    while True:
                        action = input("Select an action (read, write, close): ")
                        if action.startswith("read"):
                            _, offset = action.split(maxsplit=1)
                            file_content = self.read_file_content(file_path, int(offset))
                            if file_content:
                                print("File Content:", file_content.decode('utf-8'))
                            else:
                                print("Read data failed!!!")
                        elif action.startswith("write"):
                            if self.GetLock(file_path, "write"):
                                # 处理写操作
                                _, data, offset = action.split(maxsplit=2)
                                self.write_file_content(file_path, data.encode(), int(offset))

                        elif action == "close":
                            # 处理关闭文件操作
                            self.Unlock(file_path)
                            print("File closed.")
                            break
                        else:
                            print("Invalid action. Please choose 'read', 'write', or 'close'.")

            elif command == "exit":
                break

            else:
                print("Invalid command.")


if __name__ == '__main__':
    client = AutoSelectDataNodeClient()
    client.run()
