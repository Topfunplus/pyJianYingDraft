### 运行环境相关

- 技术栈：Django 4.2.1
- 运行环境：Python 3.12.3 pip 24.0
- 虚拟环境：venv
- 虚拟环境依赖包：requirements.txt
- 虚拟环境启动：.venv/Scripts/active.bat

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

#### 业务相关

http 路由配置：
/backend/api/views.py 配置控制器
/backend/api/urls.py 配置路由
