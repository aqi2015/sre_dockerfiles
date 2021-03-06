"""
@File    : clinet.py
@Time    : 2020/7/17 2:30 下午
@Author  : Akiqi
@Email   : linqi03@beyondsoft.com
@Software: PyCharm
"""
import alluxio

from alluxio import option

map_chmod = {
    "0": "NONE",
    "1": "EXECUTE",
    "2": "WRITE",
    "3": "WRITE_EXECU TE",
    "4": "READ",
    "5": "READ_EXECUTE",
    "6": "READ_WRITE",
    "7": "ALL",
}


class Client():

    def __init__(self):
        pass

    def conn(self, host, port):
        self.conn = alluxio.Client(host, port)
        # self.opt = option.CreateDirectory(recursive=True)
        self.opt = None

    def create_dir(self, payload):
        """Create a directory in Alluxio.
        By default, the create directory operation enforces that the parent of
        the given path must exist and the path itself does not already exist.
        The directory will be created with access mode bits 'drwxr-xr-x'.
        The created directory will only exist in Alluxio and not in any of its
        under storages. You can change the behavior by setting optional
        parameters in kwargs.
        Args:
            payload (dict): Contains various parameters.
            path (str): The path of the directory to be created.
            opt (:class:`alluxio.option.CreateDirectory`): Options to be used when creating a directory.
        Raises:
            alluxio.exceptions.AlreadyExistsError: If there is already a file or directory at the given path.
            alluxio.exceptions.AlluxioError: For any other exceptions thrown by Alluxio servers.
                Check the error status for additional details.
            alluxio.exceptions.HTTPError: If the underlying HTTP client library raises an error.
        """
        path = payload.get("path")
        return self.conn.create_directory(path, self.opt)

    # 创建文件
    def create_file(self, payload):
        """Create a file in Alluxio.
        The file must not already exist and must be closed by calling
        :meth:`alluxio.Client.close`.
        A preferred way to write to a file is to use :meth:`.open`,
        see its documentation for details.
        Args:
            payload (dict): Contains various parameters.
            path (str): The Alluxio path.
            opt (:class:`alluxio.option.CreateFile`): Options to be used when creating a file.
        Returns:
            int: The file ID, which can be passed to :meth:`alluxio.Client.write` and :meth:`alluxio.Client.close`.
        Raises:
            alluxio.exceptions.AlreadyExistsError: If there is already a file or directory at the given path.
            alluxio.exceptions.InvalidArgumentError: If the path is invalid.
            alluxio.exceptions.AlluxioError: For any other exceptions thrown by Alluxio servers.
                Check the error status for additional details.
            alluxio.exceptions.HTTPError: If the underlying HTTP client library raises an error.
        Examples:
            Create a file and write a string to it both in Alluxio and the under storage,
            finally close it:
            # >>> opt = alluxio.option.CreateFile(write_type=wire.WRITE_TYPE_CACHE_THROUGH)
            # >>> file_id = create_file('/file', opt)
            # >>> writer = write(file_id)
            # >>> writer.write('data')
            # >>> writer.close()
            # >>> close(file_id)
        """
        path = payload.get("path")
        return self.conn.create_file(path, self.opt)
        # url = self._paths_url(path, 'create-file')
        # return self._post(url, opt).json()

    # 删除path
    def delete(self, payload):
        """Delete a directory or file in Alluxio.
        By default, if path is a directory which contains files or directories,
        this method will fail. You can change the behavior by setting optional
        parameters in kwargs.
        Args:
            payload (dict): Contains various parameters.
            path (str): The path of the directory or file to be deleted.
            opt (:class:`alluxio.option.Delete`): Options to be used when deleting a path.
        Raises:
            alluxio.exceptions.NotFoundError: If the path does not exist.
            alluxio.exceptions.AlluxioError: For any other exceptions thrown by Alluxio servers.
                Check the error status for additional details.
            alluxio.exceptions.HTTPError: If the underlying HTTP client library raises an error.
        """
        path = payload.get("path")
        return self.conn.delete(path, self.opt)

    # 查看path是否存在
    def exists(self, payload):
        """Check whether a path exists in Alluxio.
        Args:
            payload (dict): Contains various parameters.
            path (str): The Alluxio path.
            opt (:class:`alluxio.option.Exists`): Options to be used when checking whether a path exists.
        Returns:
            bool: True if the path exists, False otherwise.
        Raises:
            alluxio.exceptions.InvalidArgumentError: If the path is invalid.
            alluxio.exceptions.AlluxioError: For any other exceptions thrown by Alluxio servers.
                Check the error status for additional details.
            alluxio.exceptions.HTTPError: If the underlying HTTP client library raises an error.
        """
        path = payload.get("path")
        return self.conn.exists(path, self.opt)

    # 获取文件状态
    def get_status(self, payload):
        """Get the status of a file or directory at the given path.
        Args:
            payload (dict): Contains various parameters.
            path (str): The Alluxio path.
            opt (:class:`alluxio.option.GetStatus`): Options to be used when getting the status of a path.
        Returns:
            alluxio.wire.FileInfo: The information of the file or directory.
        Raises:
            alluxio.exceptions.NotFoundError: If the path does not exist.
            alluxio.exceptions.AlluxioError: For any other exceptions thrown by Alluxio servers.
                Check the error status for additional details.
            alluxio.exceptions.HTTPError: If the underlying HTTP client library raises an error.
        """
        path = payload.get("path")
        stat = self.conn.get_status(path)
        return stat.json()

    # 列出目录内容
    def list_status(self, payload):
        """List the status of a file or directory at the given path.
        Args:
            payload (dict): Contains various parameters.
            path (str): The Alluxio path, which should be a directory.
            opt (:class:`alluxio.option.ListStatus`): Options to be used when listing status.
        Returns:
            List of :class:`alluxio.wire.FileInfo`: List of information of
            files and direcotries under path.
        Raises:
            alluxio.exceptions.NotFoundError: If the path does not exist.
            alluxio.exceptions.AlluxioError: For any other exceptions thrown by Alluxio servers.
                Check the error status for additional details.
            alluxio.exceptions.HTTPError: If the underlying HTTP client library raises an error.
        """
        path = payload.get("path")
        return self.conn.list_status(path, self.opt)
        # root_stats = self.conn.list_status(d)
        # for stat in root_stats:
        #     print(pretty_json(stat.json()))

    def ls(self, payload):
        """List the names of the files and directories under path.
        To get more information of the files and directories under path, call
        :meth:`.list_status`.
        Args:
            payload (dict): Contains various parameters.
            path (str): The Alluxio path, which should be a directory.
            opt (:class:`alluxio.option.ListStatus`): Options to be used when listing status.
        Returns:
            List of str: A list of names of the files and directories under path.
        Raises:
            alluxio.exceptions.NotFoundError: If the path does not exist.
            alluxio.exceptions.AlluxioError: For any other exceptions thrown by Alluxio servers.
                Check the error status for additional details.
            alluxio.exceptions.HTTPError: If the underlying HTTP client library raises an error.
        """
        path = payload.get("path")
        return self.conn.ls(path, self.opt)

    # 读取文件前n行
    def read(self, payload):
        """Open a file for reading.
        It should be called using a with statement so that the reader or writer
        will be automatically closed.
        Args:
            payload (dict): Contains various parameters.
            path (str): The Alluxio file to be read from.
            num (str): The number of lines read from the file。
            opt: For reading, it is :class:`alluxio.option.OpenFile`.
        Raises:
            alluxio.exceptions.InvalidArgumentError: If the path is invalid.
            alluxio.exceptions.NotFoundError: If mode is 'r' but the path does not exist.
            alluxio.exceptions.AlreadyExistsError: If mode is 'w' but the path already exists.
            alluxio.exceptions.AlluxioError: For any other exceptions thrown by Alluxio servers.
                Check the error status for additional details.
            alluxio.exceptions.HTTPError: If the underlying HTTP client library raises an error.
        """
        file_name = payload.get("path")
        num = payload.get("num")
        count = 0
        content = str()
        with client.open(file_name, 'r') as f:
            for line in f:
                if count >= num:
                    break
                content += line
                count += 1
        return content

    # 文件重命名
    def rename(self, payload):
        """Rename path to dst in Alluxio.
        Args:
            payload (dict): Contains various parameters.
            path (str): The Alluxio path to be renamed.
            dst (str): The Alluxio path to be renamed to.
            opt (:class:`alluxio.option.Rename`): Options to be used when renaming a path.
        Raises:
            alluxio.exceptions.NotFoundError: If the path does not exist.
            alluxio.exceptions.AlluxioError: For any other exceptions thrown by Alluxio servers.
                Check the error status for additional details.
            alluxio.exceptions.HTTPError: If the underlying HTTP client library raises an error.
        """
        path = payload.get("path")
        dst = payload.get("dst")
        return self.conn.rename(path, dst, self.opt)

    # 设置文件或目录权限
    def set_attribute(self, payload):
        """Set attributes of a path in Alluxio.
        Args:
            payload (dict): Contains various parameters.
            path (str): The Alluxio path.
            opt (:class:`alluxio.option.SetAttribute`): Options to be used when setting attribute.
        Raises:
            alluxio.exceptions.NotFoundError: If the path does not exist.
            alluxio.exceptions.AlluxioError: For any other exceptions thrown by Alluxio servers.
                Check the error status for additional details.
            alluxio.exceptions.HTTPError: If the underlying HTTP client library raises an error.
        """
        path = payload.get("path")
        owner = payload.get("owner")
        group = payload.get("group")
        chmod = payload.get("chmod")

        owner_bits, group_bits, other_bits = map(lambda x: map_chmod.get(x), tuple(str(chmod)))
        opt = option.SetAttribute(
            owner=owner,
            group=group,
            mode=alluxio.wire.Mode(
                owner_bits=alluxio.wire.Bits(name=owner_bits),
                # NONE 0, EXECUTE 1, WRITE 2, WRITE_EXECUTE 3, READ 4, READ_EXECUTE 5, READ_WRITE 6, ALL 7
                group_bits=alluxio.wire.Bits(name=group_bits),
                other_bits=alluxio.wire.Bits(name=other_bits),
            ),
            # pinned=False,    # Whether the path is pinned in Alluxio, which means it should be kept in memory
            # recursive=False,
            # recursive=True,
            # ttl=-1,
            # ttl_action=alluxio.wire.TTLAction(name="TTL_ACTION_FREE")
        )

        return self.conn.set_attribute(path, opt)

    # 写文件
    def write_file(self, payload):
        """Open a file for writing.
        It should be called using a with statement so that the writer
        will be automatically closed.
        Args:
            payload (dict): Contains various parameters.
            path (str): The Alluxio file to be written from.
            opt: for writing, it is :class:`alluxio.option.CreateFile`.
        Raises:
            ValueError: If mode is neither 'w'.
            alluxio.exceptions.InvalidArgumentError: If the path is invalid.
            alluxio.exceptions.AlreadyExistsError: If mode is 'w' but the path already exists.
            alluxio.exceptions.AlluxioError: For any other exceptions thrown by Alluxio servers.
                Check the error status for additional details.
            alluxio.exceptions.HTTPError: If the underlying HTTP client library raises an error.
        Examples:
            Write a string to a file in Alluxio:
            # >>> with open('/file', 'w') as f:
            # >>>     f.write('data')
            Copy a file in local filesystem to a file in Alluxio and also persist
            it into Alluxio's under storage, note that the second :func"`open`
            is python's built-in function:
            # >>> opt = alluxio.option.CreateFile(write_type=wire.WRITE_TYPE_CACHE_THROUGH)
            # >>> with alluxio_client.open('/alluxio-file', 'w', opt) as alluxio_file:
            # >>>     with open('/local-file', 'rb') as local_file:
            # >>>         alluxio_file.write(local_file)
            # Read the first 10 bytes of a file from Alluxio:
            # >>> with open('/file', 'r') as f:
            # >>>     print f.read(10)
        """

        path = payload.get("path")
        content = payload.get("content")
        with self.conn.open(path, 'w') as f:
            r = f.write(content)
        return r
