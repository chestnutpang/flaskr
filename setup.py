from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    # packages 告诉 python 包所包含的文件夹，find_packages 自动找到这些文件夹
    packages=find_packages(),
    # 为了包含其他文件夹，如静态文件与模板文件的文件夹，需设置 include_package_data
    include_package_date=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'celery'
    ],
)
# python 还需要 MANIFEST.in 文件来说明这些文件又哪些
