# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import file_system_pb2 as file__system__pb2


class FileSystemServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateFile = channel.unary_unary(
                '/file_system.FileSystemService/CreateFile',
                request_serializer=file__system__pb2.FileRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.DeleteFile = channel.unary_unary(
                '/file_system.FileSystemService/DeleteFile',
                request_serializer=file__system__pb2.FileRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.RenameFile = channel.unary_unary(
                '/file_system.FileSystemService/RenameFile',
                request_serializer=file__system__pb2.RenameRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.GetFileMetadata = channel.unary_unary(
                '/file_system.FileSystemService/GetFileMetadata',
                request_serializer=file__system__pb2.FileRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileMetadataResponse.FromString,
                )
        self.WriteFile = channel.unary_unary(
                '/file_system.FileSystemService/WriteFile',
                request_serializer=file__system__pb2.FileRequest.SerializeToString,
                response_deserializer=file__system__pb2.DataNodeListResponse.FromString,
                )
        self.WriteData = channel.unary_unary(
                '/file_system.FileSystemService/WriteData',
                request_serializer=file__system__pb2.DataRequest_main.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.Commit = channel.unary_unary(
                '/file_system.FileSystemService/Commit',
                request_serializer=file__system__pb2.DataRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.ClientWriteComplete = channel.unary_unary(
                '/file_system.FileSystemService/ClientWriteComplete',
                request_serializer=file__system__pb2.DataRequest_main.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.ReadData = channel.unary_unary(
                '/file_system.FileSystemService/ReadData',
                request_serializer=file__system__pb2.DataRequest.SerializeToString,
                response_deserializer=file__system__pb2.DataResponse.FromString,
                )
        self.GetDatanode = channel.unary_unary(
                '/file_system.FileSystemService/GetDatanode',
                request_serializer=file__system__pb2.FileRequest.SerializeToString,
                response_deserializer=file__system__pb2.DataNodeListResponse.FromString,
                )
        self.GetFileVersion = channel.unary_unary(
                '/file_system.FileSystemService/GetFileVersion',
                request_serializer=file__system__pb2.FileRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileVersion.FromString,
                )
        self.Prepare = channel.unary_unary(
                '/file_system.FileSystemService/Prepare',
                request_serializer=file__system__pb2.FileRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.ListFiles = channel.unary_unary(
                '/file_system.FileSystemService/ListFiles',
                request_serializer=file__system__pb2.DirectoryRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileListResponse.FromString,
                )
        self.MakeDirectory = channel.unary_unary(
                '/file_system.FileSystemService/MakeDirectory',
                request_serializer=file__system__pb2.DirectoryRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.ChangeDirectory = channel.unary_unary(
                '/file_system.FileSystemService/ChangeDirectory',
                request_serializer=file__system__pb2.DirectoryRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.Heartbeat = channel.unary_unary(
                '/file_system.FileSystemService/Heartbeat',
                request_serializer=file__system__pb2.HeartbeatRequest.SerializeToString,
                response_deserializer=file__system__pb2.HeartbeatResponse.FromString,
                )
        self.ChangePermissions = channel.unary_unary(
                '/file_system.FileSystemService/ChangePermissions',
                request_serializer=file__system__pb2.FileRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.AddGroup = channel.unary_unary(
                '/file_system.FileSystemService/AddGroup',
                request_serializer=file__system__pb2.FileRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.LockFile = channel.unary_unary(
                '/file_system.FileSystemService/LockFile',
                request_serializer=file__system__pb2.LockRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.UnlockFile = channel.unary_unary(
                '/file_system.FileSystemService/UnlockFile',
                request_serializer=file__system__pb2.LockRequest.SerializeToString,
                response_deserializer=file__system__pb2.FileResponse.FromString,
                )
        self.GetMetadata = channel.unary_unary(
                '/file_system.FileSystemService/GetMetadata',
                request_serializer=file__system__pb2.FileRequest.SerializeToString,
                response_deserializer=file__system__pb2.MetadataResponse.FromString,
                )


class FileSystemServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateFile(self, request, context):
        """File metadata management
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RenameFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFileMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WriteFile(self, request, context):
        """Data storage
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WriteData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Commit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClientWriteComplete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReadData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDatanode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFileVersion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Prepare(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFiles(self, request, context):
        """Newly added file system operations
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MakeDirectory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChangeDirectory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Heartbeat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChangePermissions(self, request, context):
        """Permission set
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LockFile(self, request, context):
        """File Lock
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnlockFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMetadata(self, request, context):
        """copy namenode
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileSystemServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateFile': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateFile,
                    request_deserializer=file__system__pb2.FileRequest.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'DeleteFile': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteFile,
                    request_deserializer=file__system__pb2.FileRequest.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'RenameFile': grpc.unary_unary_rpc_method_handler(
                    servicer.RenameFile,
                    request_deserializer=file__system__pb2.RenameRequest.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'GetFileMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFileMetadata,
                    request_deserializer=file__system__pb2.FileRequest.FromString,
                    response_serializer=file__system__pb2.FileMetadataResponse.SerializeToString,
            ),
            'WriteFile': grpc.unary_unary_rpc_method_handler(
                    servicer.WriteFile,
                    request_deserializer=file__system__pb2.FileRequest.FromString,
                    response_serializer=file__system__pb2.DataNodeListResponse.SerializeToString,
            ),
            'WriteData': grpc.unary_unary_rpc_method_handler(
                    servicer.WriteData,
                    request_deserializer=file__system__pb2.DataRequest_main.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'Commit': grpc.unary_unary_rpc_method_handler(
                    servicer.Commit,
                    request_deserializer=file__system__pb2.DataRequest.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'ClientWriteComplete': grpc.unary_unary_rpc_method_handler(
                    servicer.ClientWriteComplete,
                    request_deserializer=file__system__pb2.DataRequest_main.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'ReadData': grpc.unary_unary_rpc_method_handler(
                    servicer.ReadData,
                    request_deserializer=file__system__pb2.DataRequest.FromString,
                    response_serializer=file__system__pb2.DataResponse.SerializeToString,
            ),
            'GetDatanode': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDatanode,
                    request_deserializer=file__system__pb2.FileRequest.FromString,
                    response_serializer=file__system__pb2.DataNodeListResponse.SerializeToString,
            ),
            'GetFileVersion': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFileVersion,
                    request_deserializer=file__system__pb2.FileRequest.FromString,
                    response_serializer=file__system__pb2.FileVersion.SerializeToString,
            ),
            'Prepare': grpc.unary_unary_rpc_method_handler(
                    servicer.Prepare,
                    request_deserializer=file__system__pb2.FileRequest.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'ListFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.ListFiles,
                    request_deserializer=file__system__pb2.DirectoryRequest.FromString,
                    response_serializer=file__system__pb2.FileListResponse.SerializeToString,
            ),
            'MakeDirectory': grpc.unary_unary_rpc_method_handler(
                    servicer.MakeDirectory,
                    request_deserializer=file__system__pb2.DirectoryRequest.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'ChangeDirectory': grpc.unary_unary_rpc_method_handler(
                    servicer.ChangeDirectory,
                    request_deserializer=file__system__pb2.DirectoryRequest.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'Heartbeat': grpc.unary_unary_rpc_method_handler(
                    servicer.Heartbeat,
                    request_deserializer=file__system__pb2.HeartbeatRequest.FromString,
                    response_serializer=file__system__pb2.HeartbeatResponse.SerializeToString,
            ),
            'ChangePermissions': grpc.unary_unary_rpc_method_handler(
                    servicer.ChangePermissions,
                    request_deserializer=file__system__pb2.FileRequest.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'AddGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.AddGroup,
                    request_deserializer=file__system__pb2.FileRequest.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'LockFile': grpc.unary_unary_rpc_method_handler(
                    servicer.LockFile,
                    request_deserializer=file__system__pb2.LockRequest.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'UnlockFile': grpc.unary_unary_rpc_method_handler(
                    servicer.UnlockFile,
                    request_deserializer=file__system__pb2.LockRequest.FromString,
                    response_serializer=file__system__pb2.FileResponse.SerializeToString,
            ),
            'GetMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMetadata,
                    request_deserializer=file__system__pb2.FileRequest.FromString,
                    response_serializer=file__system__pb2.MetadataResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'file_system.FileSystemService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FileSystemService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/CreateFile',
            file__system__pb2.FileRequest.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/DeleteFile',
            file__system__pb2.FileRequest.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RenameFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/RenameFile',
            file__system__pb2.RenameRequest.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFileMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/GetFileMetadata',
            file__system__pb2.FileRequest.SerializeToString,
            file__system__pb2.FileMetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def WriteFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/WriteFile',
            file__system__pb2.FileRequest.SerializeToString,
            file__system__pb2.DataNodeListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def WriteData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/WriteData',
            file__system__pb2.DataRequest_main.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Commit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/Commit',
            file__system__pb2.DataRequest.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClientWriteComplete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/ClientWriteComplete',
            file__system__pb2.DataRequest_main.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReadData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/ReadData',
            file__system__pb2.DataRequest.SerializeToString,
            file__system__pb2.DataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDatanode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/GetDatanode',
            file__system__pb2.FileRequest.SerializeToString,
            file__system__pb2.DataNodeListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFileVersion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/GetFileVersion',
            file__system__pb2.FileRequest.SerializeToString,
            file__system__pb2.FileVersion.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Prepare(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/Prepare',
            file__system__pb2.FileRequest.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/ListFiles',
            file__system__pb2.DirectoryRequest.SerializeToString,
            file__system__pb2.FileListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MakeDirectory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/MakeDirectory',
            file__system__pb2.DirectoryRequest.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ChangeDirectory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/ChangeDirectory',
            file__system__pb2.DirectoryRequest.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Heartbeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/Heartbeat',
            file__system__pb2.HeartbeatRequest.SerializeToString,
            file__system__pb2.HeartbeatResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ChangePermissions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/ChangePermissions',
            file__system__pb2.FileRequest.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/AddGroup',
            file__system__pb2.FileRequest.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LockFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/LockFile',
            file__system__pb2.LockRequest.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UnlockFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/UnlockFile',
            file__system__pb2.LockRequest.SerializeToString,
            file__system__pb2.FileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/file_system.FileSystemService/GetMetadata',
            file__system__pb2.FileRequest.SerializeToString,
            file__system__pb2.MetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
