import os

from logs.logger import setup_logger
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# 导入python-dotenv来读取.env文件
try:
    from dotenv import load_dotenv

    # 加载.env文件，首先查找当前目录，然后查找上级目录
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"✅ 已加载环境变量文件: {env_path}")
    else:
        # 尝试在项目根目录查找
        root_env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
        if os.path.exists(root_env_path):
            load_dotenv(root_env_path)
            print(f"✅ 已加载环境变量文件: {root_env_path}")
        else:
            print("⚠️ 未找到.env文件，将使用默认配置")
except ImportError:
    print("⚠️ python-dotenv未安装，无法读取.env文件")

logger = setup_logger('Database')

# 数据库配置 - 从环境变量读取，提供默认值
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'username': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'jianying_draft'),
    'charset': 'utf8mb4'
}

# 打印配置信息（隐藏密码）
config_info = {k: v if k != 'password' else '*' * len(str(v)) for k, v in DATABASE_CONFIG.items()}
logger.info(f"📊 数据库配置: {config_info}")

# 构建数据库连接URL
DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}"
    f"/{DATABASE_CONFIG['database']}?charset={DATABASE_CONFIG['charset']}"
)

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=os.getenv('DB_ECHO', 'False').lower() == 'true'  # 从环境变量控制SQL日志
)

# 创建Session工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建Base类
Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库操作异常: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def test_connection():
    """测试数据库连接"""
    try:
        with engine.connect() as conn:
            # 使用text()包装SQL语句
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            logger.info("✅ 数据库连接成功")
            return True
    except Exception as e:
        logger.error(f"❌ 数据库连接失败: {e}")
        return False


def check_tables_exist():
    """检查数据库表是否存在"""
    try:
        with engine.connect() as conn:
            # 检查主要表是否存在
            tables_to_check = ['users', 'projects', 'assets']
            existing_tables = []

            for table in tables_to_check:
                result = conn.execute(text(f"SHOW TABLES LIKE '{table}'"))
                if result.fetchone():
                    existing_tables.append(table)

            logger.info(f"📋 已存在的表: {existing_tables}")

            if len(existing_tables) == len(tables_to_check):
                logger.info("✅ 所有必需的数据库表已存在")
                return True
            else:
                missing_tables = set(tables_to_check) - set(existing_tables)
                logger.warning(f"⚠️ 缺少数据库表: {missing_tables}")
                logger.warning("📝 请手动执行SQL脚本创建数据库表")
                return False

    except Exception as e:
        logger.error(f"❌ 检查数据库表失败: {e}")
        return False
