### 运行环境相关

- 技术栈：Django 4.2.1
- 运行环境：Python 3.12.3 pip 24.0
- 虚拟环境：venv
- 虚拟环境依赖包：requirements.txt
- 虚拟环境启动：.venv/Scripts/active.bat

前提条件：这个操作将会使用 /backend/setup.py 安装依赖包

```shell
cd /backend
pip install -e .
```

启动 python 虚拟环境

```shell
cd backend
python -m venv .venv
```

使用 VScode / pycharm

```shell
./.venv/Scripts/active.bat
pip install -r requirements.txt
```

使用 pycharm
设置 python 解释器 选择 .venv

### 基本知识

1. `@dataclass` 注解
   自动添加 **init** 方法：
   当你使用 @dataclass 装饰一个类时，Python 会自动为这个类添加一个 **init** 方法，这个方法会根据类定义中的字段自动创建一个初始化方法。这样，你就不需要手动编写 **init** 方法来初始化类的实例了。
   自动添加 **repr** 方法：
   **repr** 方法用于返回一个对象的字符串表示。当你打印一个对象时，Python 会调用这个方法来生成一个字符串表示。使用 @dataclass 后，Python 会自动为类添加这个方法，使得对象的打印输出更加直观。
   自动添加 **eq** 方法：
   **eq** 方法用于比较两个对象是否相等。当你使用 == 操作符比较两个对象时，Python 会调用这个方法来判断它们是否相等。使用 @dataclass 后，Python 会自动为类添加这个方法，使得对象的比较更加方便。
   字段的默认值和类型检查：
   使用 @dataclass 定义的类中的字段可以指定默认值和类型。这样，当你创建类的实例时，如果省略了某些字段的值，Python 会使用默认值。此外，类型检查也可以帮助你确保字段的类型正确。

### 业务相关

http 路由配置：
/backend/api/views.py 配置控制器
/backend/api/urls.py 配置路由

### pyJianYingDraft SDK 相关

1. 本地素材相关
   在 /backend/pyJianYingDraft/local_material.py 中 导出了三个类 ，一个是对素材裁剪的封装，两个是对素材的导出封装
   `Crop_settings` 类 可以对素材进行裁剪 参数在构造函数中已经声明

2. 轨道相关
   在 /backend/pyJianYingDraft/track.py 中 导出了一个类 `Track_meta` 封装了素材的轨道操作

3. 片段说明

通用片段 /backend/pyJianYingDraft/segement.py 中 `Base_segment` 类定义了基本的片段操作 


### 功能汇总
1. 文本片段生成