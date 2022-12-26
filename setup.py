from setuptools import setup, find_packages


setup(
    name="nonebot_plugin_zyk_music",
    version="0.1.3",
    packages=find_packages(),
    author="ZSSLM",
    author_email="3119964735@qq.com",
    long_description="This is a simple plugin to pick up music",
    url="https://github.com/ZYKsslm/nonebot_plugin_zyk_music",
    license="MIT License",
    install_requires=["fake_useragent", "httpx", "aiohttp", "colorama", "nonebot2", "nonebot_adapter_onebot"],
)
