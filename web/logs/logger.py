import logging
import sys
import os
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""
    
    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m', # 紫色
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # 获取颜色
        color = self.COLORS.get(record.levelname, self.RESET)
        
        # 格式化时间
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        # 构建日志消息
        log_msg = f"{color}[{timestamp}] [{record.levelname}] {record.getMessage()}{self.RESET}"
        
        # 如果有异常信息，添加到日志中
        if record.exc_info:
            log_msg += "\n" + self.formatException(record.exc_info)
            
        return log_msg


def setup_logger(name='pyJianYingDraft_Web', level=logging.INFO):
    """设置彩色日志记录器"""
    logger = logging.getLogger(name)
    
    # 清除现有的处理器
    logger.handlers.clear()
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter())
    
    # 确保日志目录存在
    log_dir = os.path.dirname(__file__)
    log_file = os.path.join(log_dir, 'web_service.log')
    
    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # 添加处理器到日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(level)
    
    return logger


def log_request_info(logger, request):
    """记录请求信息"""
    logger.info(f"🌐 请求URL: {request.url}")
    logger.info(f"📝 请求方法: {request.method}")
    logger.info(f"🏠 客户端IP: {request.remote_addr}")
    logger.info(f"🔧 User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    if request.method in ['POST', 'PUT', 'PATCH']:
        if request.is_json:
            logger.info(f"📋 请求数据: {request.get_json()}")
        elif request.form:
            logger.info(f"📋 表单数据: {dict(request.form)}")
    
    if request.args:
        logger.info(f"🔍 查询参数: {dict(request.args)}")


def log_response_info(logger, response, execution_time=None):
    """记录响应信息"""
    logger.info(f"📤 响应状态码: {response.status_code}")
    if execution_time:
        logger.info(f"⏱️ 执行时间: {execution_time:.2f}ms")
    
    if response.status_code >= 400:
        logger.error(f"❌ 响应错误: {response.get_data(as_text=True)}")
    else:
        logger.info("✅ 请求处理成功")
