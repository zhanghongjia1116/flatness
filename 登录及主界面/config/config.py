from pydantic_settings import BaseSettings


# 创建一个配置设置类，继承自 Pydantic 的 BaseSettings 类
class Settings(BaseSettings):
    # 调试标志，指示是否启用调试模式
    DEBUG: bool = True

    # 应用程序的标题
    TITLE: str = "首钢二期板形上线"

    # MySQL 数据库连接参数
    MYSQL_USERNAME: str = "root"
    MYSQL_PASSWORD: str = "11166316"
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = 'mysql'


# 创建 Settings 类的实例，用于获取配置项的值
settings = Settings()
