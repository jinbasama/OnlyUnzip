from typing import Union

_FAKE_PASSWORD = 'FAKEPASSWORD'


class ModelArchive:
    """压缩包处理模式，解压/测试"""

    class Extract:
        """解压"""
        value = 'extract'

    class Test:
        """测试"""
        value = 'test'


class ModelExtract:
    """解压模式，智能解压/解压到同名文件夹/直接解压"""

    class Smart:
        """智能解压"""
        value = 'smart'

    class SameFolder:
        """解压到同名文件夹"""
        value = 'same_folder'

    class Direct:
        """直接解压"""
        value = 'direct'


class ModelCoverFile:
    """文件覆盖模式，跳过/覆盖/重命名新文件/重命名旧文件/重命名（WinRAR内核只有单个重命名档）"""

    class Skip:
        """跳过"""
        text = '跳过重复文件'
        value = 'skip'
        switch = '-aos'
        switch_winrar = '-o-'

    class Overwrite:
        """覆盖"""
        text = '覆盖重复文件'
        value = 'overwrite'
        switch = '-aoa'
        switch_winrar = '-o+'

    class RenameNew:
        """重命名新文件"""
        text = '重命名新文件'
        value = 'rename_new'
        switch = '-aou'
        switch_winrar = '-or'

    class RenameOld:
        """重命名旧文件"""
        text = '重命名旧文件'
        value = 'rename_old'
        switch = '-aot'
        switch_winrar = '-or'

    class Rename:
        """重命名（WinRAR内核的独立档位，7z内核下等价于重命名新文件）"""
        text = '重命名'
        value = 'rename'
        switch = '-aou'
        switch_winrar = '-or'


class Kernel:
    """解压内核，7zip/WinRAR"""

    class SevenZip:
        """7-Zip（默认）"""
        text = '7-Zip'
        value = '7zip'

    class WinRAR:
        """WinRAR"""
        text = 'WinRAR'
        value = 'winrar'


# 内核取值与各内核支持的覆盖模式档位（列表顺序即设置页下拉框顺序）
TYPES_KERNEL = Union[Kernel.SevenZip, Kernel.WinRAR]

CLASSES_KERNEL = [Kernel.SevenZip, Kernel.WinRAR]

CLASSES_COVER_FILE = {Kernel.SevenZip.value: [ModelCoverFile.Overwrite, ModelCoverFile.Skip,
                                              ModelCoverFile.RenameNew, ModelCoverFile.RenameOld],
                      Kernel.WinRAR.value: [ModelCoverFile.Overwrite, ModelCoverFile.Skip,
                                            ModelCoverFile.Rename]}

CLASSES_COVER_FILE_ALL = [ModelCoverFile.Overwrite, ModelCoverFile.Skip,
                          ModelCoverFile.RenameNew, ModelCoverFile.RenameOld, ModelCoverFile.Rename]


def get_kernel_class(value: str):
    """根据内核取值获取对应的内核类，无效取值返回7-Zip"""
    for kernel_class in CLASSES_KERNEL:
        if kernel_class.value == value:
            return kernel_class
    return Kernel.SevenZip


def get_kernel_value(text: str) -> str:
    """根据内核文本获取内核取值，无效文本返回7-Zip的取值"""
    for kernel_class in CLASSES_KERNEL:
        if kernel_class.text == text:
            return kernel_class.value
    return Kernel.SevenZip.value


def get_cover_file_classes(kernel_value: str) -> list:
    """获取指定内核支持的覆盖模式类清单，无效取值返回7-Zip的档位"""
    return CLASSES_COVER_FILE.get(kernel_value, CLASSES_COVER_FILE[Kernel.SevenZip.value])


def get_cover_file_texts(kernel_value: str) -> list:
    """获取指定内核支持的覆盖模式文本清单"""
    return [cover_class.text for cover_class in get_cover_file_classes(kernel_value)]


def get_cover_file_class(text_or_value: str):
    """根据选项文本或取值获取覆盖模式类，无效值返回None"""
    for cover_class in CLASSES_COVER_FILE_ALL:
        if text_or_value in (cover_class.text, cover_class.value):
            return cover_class
    return None


def get_cover_file_display_text(cover_model, kernel_value: str) -> str:
    """获取覆盖模式在指定内核的下拉框中应显示的选项文本
    内核不支持的档位显示为命令行参数等价的档位（例如7z内核下的“重命名”显示为“重命名新文件”）
    :param cover_model: 覆盖模式类的实例"""
    cover_classes = get_cover_file_classes(kernel_value)
    for cover_class in cover_classes:
        if cover_class.text == cover_model.text:
            return cover_class.text
    for cover_class in cover_classes:
        if cover_class.switch == cover_model.switch:
            return cover_class.text
    return cover_classes[0].text


class ModelBreakFolder:
    """解散文件夹的模式"""

    class MoveBottom:
        """移动最底层的首个非空文件夹到顶层目录之外（并删除空的顶层目录）"""
        text = '移动底层文件夹'
        value = 'move_bottom'

    class MoveToTop:
        """移动最底层的首个非空文件夹下的文件到顶层目录之下（保持文件层级结构，并删除空的该底层文件夹）"""
        text = '移动到顶层目录'
        value = 'move_to_top'

    class MoveFiles:
        """移动所有文件到顶层目录之下（并删除空的子文件夹）"""
        text = '仅移动文件'
        value = 'move_files'


class ArchiveRole:
    """压缩包角色，普通压缩包/分卷压缩包（首个分卷）/分卷压缩包（非首个的成员）"""

    class Normal:
        """普通压缩包"""

    class VolumeFirst:
        """分卷压缩包（首个分卷）"""

    class VolumeMember:
        """分卷压缩包（非首个的成员）"""


class Model7zip:
    """7zip命令模式，l/t/x"""

    class L:
        """l，列表命令"""
        value = 'l'

    class T:
        """t，测试命令"""
        value = 't'

    class X:
        """x，解压命令"""
        value = 'x'


class Result7zip:
    """zip调用结果"""

    class Success:
        """成功"""
        return_code = 0
        return_text = '成功'  # success
        _7zip_return = 'No error'
        color = [0, 0, 0]
        result_state = '成功'

        def __init__(self, password: str = None):
            if not password or password == _FAKE_PASSWORD:
                password = '无密码'
            self.password = password

    class Skip:
        """跳过"""
        return_code = None
        return_text = '跳过'  # skip
        _7zip_return = 'Skip'
        color = [255, 215, 0]
        result_state = '跳过'

    class Warning:
        """非致命错误"""
        return_code = 1
        return_text = '文件被占用'  # file occupied一般情况下是文件被占用
        _7zip_return = 'Warning (Non fatal error(s)).'
        color = [128, 0, 0]
        result_state = '失败'

    class WrongPassword:
        """密码错误"""
        return_code = 2
        return_text = '未找到密码'  # wrong password
        _7zip_return = 'Fatal error'
        color = [178, 34, 34]
        result_state = '失败'

    class MissingVolume:
        """缺失分卷包"""
        return_code = 2
        return_text = '缺失分卷'  # missing volume
        _7zip_return = 'Fatal error'
        color = [205, 92, 92]
        result_state = '失败'

    class WrongFiletype:
        """错误的文件类型（不是压缩文件）"""
        return_code = 2
        return_text = '错误的文件类型'  # wrong filetype
        _7zip_return = 'Fatal error'
        color = [255, 99, 71]
        result_state = '失败'

    class UnknownError:
        """未知错误"""
        return_code = 2
        return_text = '未知错误'  # unknown error
        _7zip_return = 'Fatal error'
        color = [220, 20, 60]
        result_state = '失败'

        def __init__(self, error_text: str):
            self.error_text = error_text

    class ErrorCommand:
        """7zip命令行错误"""
        return_code = 7
        return_text = '错误的命令行'  # command line error
        _7zip_return = 'Command line error'
        color = [240, 128, 128]
        result_state = '失败'

        def __init__(self, error_text: str = None):
            """初始化
            :param error_text: 附加的错误说明（例如密码无法传入时对用户的提示）"""
            self.error_text = error_text

    class NotEnoughMemory:
        """没有足够的硬盘空间"""
        return_code = 8
        return_text = '磁盘空间不足'  # Not enough memory
        _7zip_return = 'Not enough memory for operation'
        color = [250, 128, 114]
        result_state = '失败'

    class UserStopped:
        """用户主动停止"""
        return_code = 255
        return_text = '用户终止操作'  # user stopped
        _7zip_return = 'User stopped the process_7zip'
        color = [255, 160, 122]
        result_state = '失败'


class Position:
    """位置"""

    class Left:
        """左端"""
        text = '最左端'

    class Right:
        """左端"""
        text = '最右端'


TYPES_MODEL_ARCHIVE = Union[ModelArchive.Extract, ModelArchive.Test]

TYPES_MODEL_EXTRACT = Union[ModelExtract.Smart, ModelExtract.SameFolder, ModelExtract.Direct]

TYPES_MODEL_COVER_FILE = Union[ModelCoverFile.Skip, ModelCoverFile.Overwrite,
ModelCoverFile.RenameNew, ModelCoverFile.RenameOld, ModelCoverFile.Rename]

TYPES_MODEL_BREAK_FOLDER = Union[ModelBreakFolder.MoveBottom, ModelBreakFolder.MoveToTop, ModelBreakFolder.MoveFiles]

TYPES_ARCHIVE_ROLE = Union[ArchiveRole.Normal, ArchiveRole.VolumeFirst, ArchiveRole.VolumeMember]

TYPES_MODEL_7ZIP = Union[Model7zip.L, Model7zip.T, Model7zip.X]

TYPES_RESULT_7ZIP = Union[Result7zip.Success, Result7zip.Skip,
Result7zip.Warning, Result7zip.WrongPassword,
Result7zip.MissingVolume, Result7zip.WrongFiletype,
Result7zip.UnknownError, Result7zip.ErrorCommand,
Result7zip.NotEnoughMemory, Result7zip.UserStopped]

TYPES_POSITION = Union[Position.Left, Position.Right]

CLASS_RESULT_7ZIP = [Result7zip.Success, Result7zip.Skip,
                     Result7zip.Warning, Result7zip.WrongPassword,
                     Result7zip.MissingVolume, Result7zip.WrongFiletype,
                     Result7zip.UnknownError, Result7zip.ErrorCommand,
                     Result7zip.NotEnoughMemory, Result7zip.UserStopped]

RESULT_STATE_ALL = '全部'
RESULT_STATES = [RESULT_STATE_ALL, Result7zip.Success.result_state, Result7zip.Warning.result_state,
                 Result7zip.Skip.result_state]
