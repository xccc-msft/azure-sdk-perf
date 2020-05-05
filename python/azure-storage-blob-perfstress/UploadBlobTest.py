import os

from azure.test.perfstress import PerfStressTest

from azure.storage.blob import ContainerClient as SyncContainerClient
from azure.storage.blob.aio import ContainerClient as AsyncContainerClient

class UploadBlobTest(PerfStressTest):
    container_name = PerfStressTest.NewGuid()
    blob_name = PerfStressTest.NewGuid()
    data = None

    async def GlobalSetupAsync(self):
        connection_string = os.environ.get("STORAGE_CONNECTION_STRING")
        if not connection_string:
            raise Exception("Undefined environment variable STORAGE_CONNECTION_STRING")

        type(self).container_client = SyncContainerClient.from_connection_string(conn_str=connection_string, container_name=self.container_name)
        
        type(self).async_container_client = AsyncContainerClient.from_connection_string(conn_str=connection_string, container_name=self.container_name)
        await type(self).async_container_client.__aenter__()

        type(self).container_client.create_container()

        self.data = b'a' * self.Arguments.size


    async def GlobalCleanupAsync(self):
        type(self).container_client.delete_container()

        await type(self).async_container_client.__aexit__()


    def Run(self):
        type(self).container_client.upload_blob(self.blob_name, self.data, overwrite=True)

    async def RunAsync(self):
        await type(self).async_container_client.upload_blob(self.blob_name, self.data, overwrite=True)

    @staticmethod
    def AddArguments(parser):
        parser.add_argument('-s', '--size', nargs='?', type=int, help='Size of blobs to upload.  Default is 10240.', default=10240)