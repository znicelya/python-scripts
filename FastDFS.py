import traceback

from fdfs_client.client import Fdfs_client


class FDFS(object):
    def __init__(self):
        self.client_conf = {
            'host_tuple': ('host1', 'host2'),
            'port': 22122,
            'timeout': 30,
            'name': 'Tracker Pool'
        }
        self.client = self.create_client()

    def create_client(self):
        try:
            client = Fdfs_client(self.client_conf)
            return client
        except Exception as e:
            print("FastDFS Create file fail, {0}, {1}".format(e, traceback.print_exc()))
            return None

    def download(self, file_id):
        try:
            ret_download = self.client.download_to_buffer(file_id)
            return ret_download
        except Exception as e:
            print("FastDFS download file fail, {0}, {1}".format(e, traceback.print_exc()))
            return None

    def upload(self, file_name):
        try:
            ret_upload = self.client.upload_by_filename(file_name)
            return ret_upload
        except Exception as e:
            print("FastDFS upload file fail, {0}, {1}".format(e, traceback.print_exc()))
            return None

    def upload_by_buffer(self, buffer):
        try:
            ret_upload = self.client.upload_by_buffer(buffer, file_ext_name='png')
            return ret_upload
        except Exception as e:
            print("FastDFS upload file fail, {0}, {1}".format(e, traceback.print_exc()))
            return None

    def delete(self, file_id):
        try:
            ret_delete = self.client.delete_file(file_id)
            print(ret_delete)
            return True
        except Exception as e:
            print("FastDFS delete file fail, {0}, {1}".format(e, traceback.print_exc()))
            return False

