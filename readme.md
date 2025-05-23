1. 将项目下载至电脑上
2. 确保电脑上拥有py37, py38, py39, py310, py311（确保正确的在系统中能被搜索到）
3. 在你当前使用的python环境中（py37, py38, py39, py310, py311）任意一个都可以，下载tox工具包即

pip install tox

序列化对象生成（本项目已经预先提供一份序列化数据供使用）
1. 主目录下，刚才安装的python环境中，使用命令行，输入命令（可以通过修改“tox.ini”来完成环境调整与输出目录）

tox

经过以上四步，就已经完成对五种环境的的运行

2. 因为python35版本特殊性，无法直接使用tox运行，故需要额外在目录下，使用pyhton3.5的解释器进行命令运行（确保安装py35）即 

python yield_pkl.py --output-dir mac/py35


3. 在project_2的目录下将生成对应数据文件夹




1. Download the project to your computer
2. Make sure you have py37 , py38 , py39 , py310 , py311 on your computer (make sure the correct ones can be searched in the system)
3. In your current python environment ( py37 , py38 , py39 , py310 , py311 ) any one can download the tox toolkit

pip install tox

Serialized object generation (this project has provided a serialized data for use in advance)
1. Under the home directory, in the python environment that was just installed, use the command line and enter the command (you can modify "tox.ini" to complete the environment adjustment and output directory)
tox

After the above four steps, the operation of the five environments has been completed

2. Because of the particularity of the python35 version, it cannot be run directly with tox , so it is necessary to use the pyhton3.5 interpreter in the directory to run the command (make sure to install py35) that is

python yield_pkl.py --output-dir mac/py35


3. Corresponding data folders will be generated in the project_2 directory