from setuptools import setup, find_packages


setup(
    name="nonebot_plugin_zyk_music",
    version="0.1.5.1",
    packages=find_packages(),
    author="ZSSLM",
    author_email="3119964735@qq.com",
    long_description="This is a simple plugin for nonebot2 to pick up music",
    url="https://github.com/ZYKsslm/nonebot_plugin_zyk_music",
    license="MIT License",
    install_requires=["fake_useragent", "httpx", "aiohttp", "colorama", "filetype", "nonebot2", "nonebot_adapter_onebot"],
    package_data={"nonebot_plugin_zyk_music": ["User-Agent.json"]}
)
