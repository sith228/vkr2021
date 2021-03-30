import platform


class OsUtil(object):
    @staticmethod
    def is_windows():
        """
        Checks if the current OS is windows
        :return: true for windows
        """
        return platform.system().lower() == "windows"

    @staticmethod
    def is_macos():
        """
        Checks if the current OS is macOS
        :return:
        """
        return platform.system().lower() == "darwin"

    @staticmethod
    def is_linux():
        """
        Checks if the current OS is linux
        :return: true for linux
        """
        return platform.system().lower() == "linux"
