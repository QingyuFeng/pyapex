# PYAPEX v1.0 用户手册

开发者：冯青郁 

更新时间: Dec 31, 2020



[TOC]

## APEX模型简介

链接：https://mp.weixin.qq.com/s/6O9qQurWrEBkyRn6KMyCVA

当今我国乃至世界上都面临着严重的水环境污染问题。这些水环境污染的成因主要包括生产、生活和畜牧养殖等排放的废水产生的“点源”，以及由于降雨产流、大气沉降、地下水渗漏等过程产生的污染，由于这类污染面积广、来源不确定，又称为“面源”污染。无论是“点源”还是“面源”污染，都将污染物从陆地排到河道、湖泊、海洋等收纳水体，进而产生富营养化等次生环境问题，最终人们的生产、生活、娱乐等活动以及自然界的动植物生长。

<img src="https://mmbiz.qpic.cn/mmbiz_png/XdyFAXuuOFTMjic0LnyurPPVZwsdl1X6zQUKrCR1ibuJbNziaGicTMeyNF79nw6QicPFIViaGj0gIskBAoIdtW2R9bRA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1" alt="Image" style="zoom:50%;" />

美国伊利湖（Lake Erie）旁告诫人们注意蓝藻有毒的公告牌 摄影：冯青郁

由于水是污染物流动的重要载体，因此在水污染治理中都是以流域为单元进行的。一个流域就是一个集水区，也就是在降雨发生的时候雨水汇集的区域。流域多成嵌套结构，也就是包含若干个子流域（图2的红色线条圈起来的范围，蓝色代表水形成径流之后可能的汇集路径，可以称为集水汇流路径，因为有时候并不是真的有一条河在哪里，只是降雨发生的时候产生的径流由于地形原因会经蓝色线条而流动）。子流域就是一个更小的集水区。以流域为单元，可以帮助我们判断水在地表和通过土壤进行流动的过程。然后可以计算水在地表流动过程中可能产生的土壤侵蚀的多少，之后又可以刻画水中溶解的污染物以及水流所携带的泥沙上吸附的污染物的多少。知道了水流、土壤颗粒和污染物在流域和子流域内随水流移动的多少和位置，就便于我们判断污染物的来源和路径，为治理污染物提供重要的依据。

![Image](https://mmbiz.qpic.cn/mmbiz_png/XdyFAXuuOFTMjic0LnyurPPVZwsdl1X6z5Lj9sMWJHNhgRzOq65ibv61CPdMibf2OGXcDJibAoLNmiaia9aHm6uVqftA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

图2 流域、子流域和集水汇流路径的概念展示

**APEX模型的应用场景**

在一个现实中的流域，通过足够多的人力和设备布设，是有可能精确测定在降雨发生时每个子流域和整个流域各个集水汇流路径上的水量大小，以及其携带的土壤颗粒和化学污染物的多少。然而，一般是没有这样的条件的，主要是受限于人力和物力的限制，特别是我们没有办法在所有的地方都放上监测设备来实时收集数据。就算我们有条件将所有的地方监测起来，当需要治理的时候，用什么样的方法效果最好呢？一般的治理下过包括源头控制、过程阻断技术和末端强化技术等几个类型。那么我们怎么知道选择哪一种措施、在什么地方布设这些措施以及不同措施之间的组合效果最好呢？这些问题通过常规的监测手段是没有办法完全回答的。还有一些问题包括，我们如何判断把流域内的草地换成农耕地，或者把耕地换成林地对这些污染物有什么样的影响呢？回答这些问题，就需要借助计算机模型的帮助。**为了解决估算流域水流和污染物流失这个问题，很多模型被开发出来，APEX就是其中一个。**

APEX模型的全称是Agricultural Policy Environmental eXtender，它是用来在小流域或者农场尺度预测土地管理措施、气候变化和最优化管理措施（Best Management Practice，BMP）等因素的变化对水文循环、土壤侵蚀和农业化学物的流失量的影响。该模型的开发始于十九世纪八十年代初由美国农业部（United States Department of Agriculture，USDA）农业研究中心（AgriculturalResearch Service，ARS）的EPIC（Erosion-Productivity Impact Calculator）模型。

在1993年，美国发起的《畜牧业与环境：国家先导项目》促使了APEX模型的开发，主要是用于解决不同农场尺度有机肥管理措施情景带来的水文水质效应。EPIC模型是一个田块尺度的模型，APEX模型的开发思路是**将汇流模块同EPIC模型耦合，使得该模型既能够在单个田块运行EPIC模型，又可以被应用于包含多个田块的一个小流域。*

自开发之后，该模型不断在各个水文、水质相关模块的到加强，比如于2004年将Century的碳循环模块的融入，最终形成了包含12个模块的模型。这些模块包括气象、水文、植物生长、杀虫剂流失、养分循环、土壤侵蚀运移、碳循环、土地管理措施、土壤温度、植物生长环境控制、经济投入分析、汇流等。在进行农场或者小流域进行模拟时，首先将模拟区域划分为若干个子田块或者子流域，其划分依据是每一个田块或者子流域需要有统一的土壤、土地利用、地形（坡度）条件。其次，在每一个田块或子流域使用EPIC模型计算每天的气象变化、各个水文组分（地表径流、土壤水分变化、壤中流等）、作物生长状况、土壤侵蚀、土壤中的碳氮磷等养分含量等状态的变化量。最后，将各个田块或子流域的模拟结果通过河道汇流的途径将泥沙和养分输移到小流域出口以获得整个流域的模拟结果。

在进行模型构建的时，需要的输入数据包括流域的地形（通常使用数字高程模型，Digital Elevation Model，DEM）、土壤（包含空间数据和分层属性数据）、气象、以及土地利用（包含土地覆盖和管理措施数据）等。由于APEX模型是使用Fortran语言编写的一个可执行文件，需要读取文本文档作为输入数据并对文本文档的格式有严格的要求。所需要的输入数据通常需要借助于ArcAPEX、WinAPEX等界面工具进行处理，形成APEX模型所需要的文本输入文件。

模型的输出数据包括各个田块或子流域和整个流域两个层面的水文组分、土壤流失和泥沙输移量、农业化学物的流失量等状态变量。为了适应当代大数据的发展，我们还开发了线上模型构建和运行平台，平台融合了在中国构建APEX模型所需要的基础数据库，大大简化了模型构建所需要的学习时间。同时为了满足研究者可能需要使用自己搜集的数据库的需求，提供pyapex线下版本，**独立运行，代码开源，不依赖于GIS软件**，使得大家能够方便快捷地在自己的研究区利用自己的数据构建APEX模型。让大家在专注面源污染问题的解决上可以节省时间，更关注于自己的研究，而不是花很多的时间和精力在模型构建上。

如果有兴趣的同学可以通过: http://159.226.240.209/rceesecomodelcloud.html获取。

![rceesEcoModelQRCode_Public](D:\gitrepositories\pyapex\mdimages\rceesEcoModelQRCode_Public.jpg)

生态中心内网需通过下面的二维码扫描进入：

![rceesEcoModelQRCode_Private](D:\gitrepositories\pyapex\mdimages\rceesEcoModelQRCode_Private.jpg)







## PYAPEX模型介绍

该软件主要功能是使用用户提供的土壤、土地利用、气象、耕作措施等数据构建APEX模型。模型提供了两种模型构建模式，流域模式和行政边界模式。在两种模式下，用户均需要提供土壤、土地利用、DEM和气象数据。在使用流域模式进行模型构建时，用户还需要提供流域的出口（该版本仅支持一个流域出口）。在使用行政边界模式进行模型构建时，用于需要提供行政边界的shapefile文件。软件的运行流程包括![flowchart](D:\gitrepositories\pyapex\mdimages\flowchart.jpg)

该软件的主要技术特点：

- 软件运行脱离了对ArcGIS和QGIS软件的依赖，用户可以使用商业化或者开源的GIS软件进行数据准备；
- 跨平台运行（Windows，Ubuntu1804已测试），便于扩展为平行运算。软件运行的流程如图1 所示。
- 软件模块化构建，用户可根据自己的需求进行个性化定制。



## PYAPEX模型使用过程

### 用户数据准备

正如简介中介绍，APEX模型构建需要土壤、土地利用、DEM、气象数据、流域出口（或者行政边界）。这里将对数据进行详细的介绍。

1. DEM：用于生成流域、计算各个流域的坡度、坡长和海拔等信息。
2. 土壤：主要用来参与水文、植被生长、土壤侵蚀、养分库状态变化等的计算。土壤信息主要需要两类数据：一类是空间数据，用于表示土壤的空间分布；另一类是土壤属性数据，主要包含空间数据所显示的每一种土壤的深度、分层数和每层厚度、每层的土壤容重、饱和导水率、土壤质地等参数信息。
3. 土地利用：主要用于表示地表的覆盖状况，参与地表覆盖植被类型、植被生长、地表粗糙度、水文、耕作等过程的模拟。同土壤信息一样，土地利用也需要两类信息，空间数据显示植被覆盖的空间分布，而属性数据则包括植被覆盖的作物类型、耕作管理制度等。
4. 说明：其中DEM、土壤和土地利用的空间数据需要准备为相同的分辨率和相同的投影。本软件仅接受通用横轴墨卡托投影（Universal Transverses Mercator projection, UTM）。用户在准备的时候需要将数据投影为相应的UTM区域。UTM区域分布图详见：https://i2.wp.com/tmackinnon.com/2005/images/utmworld.gif
5. 此外，正如上图所示，软件包含两种运行模式，流域模式和行政边界模式。流域模式下需要输入shapefile文件格式的流域出口（仅支持一个流域出口）。行政边界模式下需要输入shapefile文件格式的行政边界。两者同样需要被投影为同其他数据一致的UTM投影。
6. 气象数据：主要参与降雨、径流产生、土壤侵蚀、植被生长等过程的计算。所需要的气象指标包括降水、最高最低气温、相对湿度、风速和太阳辐射等信息。时间步长包含月统计气象信息和日观测气象数据。由于APEX模型是以天为时间步长进行计算的，如果用户有日观测气象数据，则可以准备日观测气象数据到APEX模型需要的格式参与计算。然而，这要求用户具备所有的气象参数且中间不能有缺失值。如果有缺失值或者缺少部分气象参数，则模型需要借助月统计气象数据作为天气发生器的输入数据用于生成日的气象估计值进行计算。



### 软件环境设置

该软件用python语言编写，需要在python编辑器中进行运行，目前尚未提供可视化用户界面。此外，软件运行需要借助开源的地理信息处理软件GDAL，以及一些python依赖的软件库，需要提前进行设置才能够成功运行。具体的设置步骤如下：（安装顺序很重要，请按照顺序安装。）

- Python：下载地址为https://www.python.org/ ，软件开发版本为3.7.6。目前不建议升级到最高版本，因为python的依赖包有些没有得到及时更新。安装好之后需要将安装路径添加到系统的环境变量中去。建议安装到系统安装路径（C:/Program Files/python37）。安装过程中需要使用pip，用于后续python包的安装。

- Microsoft Visual C++ redistributable (2015-2019)，下载地址为https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads目前仅支持64位版本，所以需要下载64位版本vc_redist.x64.exe。该软件为GDAL运行依赖软件。

- GDAL：下载地址为https://www.gisinternals.com/release.php 。需要下载2.4版本（2.4.0-2.4.4）。下载gdal-204-1911-x64-core.msi进行安装。**安装好之后需要将安装路径添加到系统的环境变量中去**。建议安装到默认安装路径。(GDAL_DATA: C:\Program Files\GDAL\gdal-data, path: C:\Program Files\GDAL)

- 安装python-gdal，在上述GDAL下载网页进行下载，需要下载对应于python 3.7的版本。通过下载python-gdal binding 安装文件进行安装，下载文件名称为（GDAL-2.4.4.win-amd64-py3.7.msi）。执行该步骤前要求将GDAL的路径在环境变量中设置好。

- 安装python 依赖包：所需要额外安装的依赖包包括：gdal（见步骤4）、numpy、pandas、sqlalchemy。安装步骤为打开命令提示符（有可能需要管理员账户打开），在命令行输入如下命令进行安装：

    ```
    pip install packageName
    ```

- 安装Microsoft MPI：下载地址为https://www.microsoft.com/en-us/download/details.aspx?id=57467 

- 推荐安装：Visual studio code，下载地址为：https://code.visualstudio.com/ 安装好之后可以打开visual studio或者其他用户选择的python开发环境，就可以进行软件的测试和使用。

- 如果用户有编辑土壤属性数据库的需求，可安装[SQLiteStudio](https://sqlitestudio.pl/) 软件进行查看和编辑。

说明：目前该软件未在Anaconda的python环境下进行测试。



当软件测试好之后，用户可以通过如下的方式进行测试，确保需要的软件环境都正确设置。

在Windows系统中，打开命令提示符，输入如下命令

```
# Test python:
C:\Users\qingy>python --version
Python 3.7.6

#　Test gdal
C:\Users\qingy>gdalinfo --version
GDAL 2.4.4, released 2020/01/08

# Test python-gdal
C:\Users\qingy>python
Python 3.7.6 (tags/v3.7.6:43364a7ae0, Dec 19 2019, 00:42:30) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>>from osgeo import gdal
>>>exit()

# Test other python packages
C:\Users\qingy>pip freeze
absl-py==0.10.0
aiohttp==3.6.2
aiohttp-cors==0.7.0
aioredis==1.3.1
argon2-cffi==20.1.0
astunparse==1.6.3
async-generator==1.10
async-timeout==3.0.1
attrs==20.2.0
backcall==0.2.0
beautifulsoup4==4.9.3
...

# Install python packages:
C:\Users\qingy>pip install packagename
...
```



### 软件运行流程

简单来讲，用于运行的具体步骤同上述流程图一致。具体的操作为：

1. 用户设置运行模式和输入数据的格式：通过编辑userinputs.py文件里的参数名来实现；

![userinputscreen](D:\gitrepositories\pyapex\mdimages\userinputscreen.png)

2. 初始化项目：主要是通过运行mainstep1_initiateProj.py来实现。该步骤主要是在apexprojects文件夹下构建以项目名称命名的项目文件夹（命名规则为project name +run mode，比如project name= demo，run mode = mode1，则会在apexprojects文件夹下创建名称为demomode1的文件夹），并在项目文件夹下创建3-5个子文件夹，分别为apextio、gislayers、taudemlayers。如果用户选择使用自己的气象数据（也就是在userinputs.py文件中设置useDlyWea为True），将会额外创建一个名为userdlyandlist的文件夹。如果用户选择使用自己的土地利用数据，将会额外创建一个名为userlulistopcfiles文件夹，用于存放用户准备的土地覆盖数据列表和ops文件。具体的日观测气象数据和土地利用覆盖数据准备步骤请参加下方相应部分。

![initialsetup](D:\gitrepositories\pyapex\mdimages\initialsetup.png)

3. **放入用户准备好的数据1GIS数据（必须执行）**：用户在上述准备的土壤、土地利用和DEM数据需要拷贝到gislayers文件夹中，如果有气象数据，日观测气象数据需要放置到userdlyandlist文件夹中。在本软件中包含了一套样例数据，样例数据存放于demodata文件夹。该文件夹中包含了一套可以运行的所有数据，包含土壤属性和日观测气象数据的样例。放好之后如下图：

![gislayers](D:\gitrepositories\pyapex\mdimages\gislayers.png)

4. **如果用户选择使用自己的日观测数据，则放入用户准备好的数据2-日观测气象**：该文件直接放置于apexprojects/project name +run mode/userdlyandlist文件夹下。如果用户准备了自己的日观测气象数据，则需要放置到userddlyandlist文件夹中。模型在运行时会检测是否该文件已存在，如果不存在或者格式不正确，将导致程序无法运行。这两个文件都为文本文档，可用Notepad++文本编辑器或其他进行编辑。

![dailyObsandList](D:\gitrepositories\pyapex\mdimages\dailyObsandList.png)

5. **如果用户选择使用自己的土壤数据库，则放入用户准备好的数据3：土壤属性数据**：该文件直接放置于apexprojects/project name +run mode文件夹下。土壤属性数据存放于SQL数据文件夹中，可使用SQLiteStudio软件进行编辑。本软件包含了一套有基于FAO土壤属性数据库构建的APEX中国土壤属性数据库，供用户使用。如果用户需要使用自己观测的数据库，则需要按照样例数据库（usersoil.db）的格式填入数据库的数值。在下述表格中，mukey将需要同土壤空间数据库的Tiff文件中的数值对应，并包含所有的tiff文件中的数值所对应的土壤号码，如果缺失，软件将无法运行。

    ![usersoildb](D:\gitrepositories\pyapex\mdimages\usersoildb.png)

    如果要添加新的土壤类型，可以通过点击上图中的绿色加号箭头

    ![usersoildbincertnewrow](D:\gitrepositories\pyapex\mdimages\usersoildbincertnewrow.png)

    ![usersoildbincertnewrow2](D:\gitrepositories\pyapex\mdimages\usersoildbincertnewrow2.png)

​		然后可以在其中手动输入对应的数据，每个参数的含义请参见APEX用户手册。

6. **如果用户选择使用自己的土地覆盖数据，则放入用户准备好的数据4：土地覆盖数据和OPS文件**：这些文件文件直接放置于apexprojects/project name +run mode/userlylistopcfiles文件夹下。土壤覆盖属性数据包含土地覆盖列表和OPS文件。其中土地覆盖列表数据名称为user_lumgtupn.csv，其中包含土地覆盖的信息、OPS文件名称以及各个土地覆盖下的土地利用相关参数和曼宁系数等数据，具体的参数准备过程详见下方介绍。而OPS文件则包含耕作管理措施的详细设置。userlylistopcfiles文件夹中的内容如下，用户可根据自己的数据进行命名，但是名称必须同user_lumgtupn.csv指定的名称一致，并且包含user_lumgtupn.csv文件中包含的所有OPC文件，如果有缺失，软件无法运行。

    ![opcfilelist](D:\gitrepositories\pyapex\mdimages\opcfilelist.png)

    user_lumgtupn.csv下的内容。该样例数据同样为软件默认的土壤覆盖类型和OPC文件名称。该命名规则为Global30土地利用数据的分类规则。如果用户选择不是用自己的土壤覆盖数据，软件将默认采用下图显示的土壤覆盖和OPC文件进行模拟。

    ![user_lumgtupn](D:\gitrepositories\pyapex\mdimages\user_lumgtupn.png)

    OPC文件截图显示

    ![opcfileexample](D:\gitrepositories\pyapex\mdimages\opcfileexample.png)

    注：1） 上述4、5、6三步位用户选择使用，使用时需要先在userinputs.py文件中对将使用日观测数据（useDlyWea）、自己的土壤数据库（useUserSoil）和使用自己的土地覆盖数据数据（userUserLUOPS）三个选项根据自己的需求设置为True。如果设置之后，软件将会按照上述路径寻找对应文件。如果没有，软件将无法正确运行。2）再进行模型初始化设置，也就是文件夹创建的时候，对于流域模式或者行政边界模式模拟都是一样的，唯一的区别就是apexprojects文件夹下对应用户新建的项目文件夹名称会有区别。

    

    7. 设置好数据之后，用户可以开始进行相应的模拟。
    8. 流域模式下，用户依次运行河道绘制（mode1step1_stream.py）、流域绘制（mode1step2_watershed.py）、和模型构建（mode1step3_setupapex.py）三个python文件进行模型构建。其中河道绘制仅仅使用DEM数据生成河道；流域绘制则需要用户输入的流域出口；而模型构建的主要工作包括从土壤、土地利用和DEM以及流域边界进行模型所需参数的抽取，这是将需要用户准备的日观测气象、土壤数据库和土地覆盖属性等数据。
        1. 
    9. 行政边界模式下，用户需要一次运行流域绘制（mode2step1_watershed.py）、模型构建（mode2step2_setupapex.py）两个步骤进行模型构建，同时可运行结果制图（mode2step3_mapping）将各个流域的年平均径流、土壤侵蚀、全氮和全磷信息抽取出来并制成流域图。流域模式当前不包含该功能，在后续的开发中会加入。





## 软件文件夹结构

1. userinputs.py文件：设置运行模式、项目名称、数目名称、河道绘制阈值等。
2. mainstep1_initiateProj.py文件：创建项目文件夹
3. mode1step1_stream.py文件：流域模式下绘制河道
4. mode1step2_watershed.py文件：流域模式下绘制流域
5. mode1step3_setupapex.py文件：流域模式下构建APEX模型
6. mode2step1_watershed.py文件：行政边界模式下绘制流域
7. mode2step2_setupapex.py文件：行政边界模式下构建APEX模型
8. mode2step3_mapping.py文件：行政边界模式下进行结果图绘制
9. apexprojects文件夹：存放用户构建的apex项目文件夹，每一个子文件夹代表一个APEX项目。
10. scripts文件夹：存放pyapex相关函数以及基础数据的的python文件
    1. apexdata：APEX基础输入数据库，包含模型自带的作物生长、耕作、农药、杀虫剂、模型参数等数据库。
    2. clinear：包含用于寻找站点附近最近气象站点位置和名称的程序
    3. json：包含用于APEX模型输入文件转换的模板文档JSON格式
    4. taudembins：存放TauDEM可执行命令的文件夹
    5. utm：包含用于投影转换为UTM的软件包
    6. apexfuncs.py：包含用于处理APEX模型输入输出文件的函数
    7. ascInfoBdy.py：包含用于将栅格数据转换为行政边界模式下运行APEX所需信息的函数
    8. ascInfoWSOlt.py：包含用于将栅格数据转换为流域模式下运行APEX所需信息的函数
    9. climfuncs.py：包含用于寻找最近气象战点，以及写入APEX所需气象参数文件的函数
    10. defaultFNFD.py：包含各个步骤下的生成文件的默认名称
    11. gdal_reclassify.py：包含对栅格数据进行重分类的函数
    12. gdalfuncs.py：包含调用GDAL命令的函数
    13. generalfuncs.py：包含一般性的处理函数，比如文件的删除与移动等
    14. globalsetting.py：包含全局变量设置，比如路径设置等
    15. mapUtil.py：包含结果抽取和输出结果地图制作的函数
    16. solfuncs.py：包含抽取土壤数据库中的数据以及写入APEX土壤参数文件的函数
    17. sqldbfuncs.py：包含链接SQL数据库的函数
    18. subWsInfoBdy.py：包含将ascinfoBdy.py文件生成的信息转换为APEX所需文件的函数
    19. subWsInfoWsOlt.py：包含将ascInfoWSOlt.py文件生成的信息转换为APEX所需文件的函数
    20. taudemfuncs.py：包含调用TauDEM命令的函数
    21. userinputs.py：包含用户输入的函数和变量





## 气象数据准备步骤

用户自己准备的气象数据主要是指日观测气象数据的准备，目前软件尚未完善对月统计观测数据的准备，如果用户需要，可以联系开发者进行功能完善。

日观测气象数据包含气象站点列表和各个站点的气象数据准备。每一个站点需要一个DLY文件。

注：用户输入的气象数据要求必须要有的为日降雨量。如果用户有其他的数据，则可以按照下面要求的列对应准备好。同时需要在userinputs.py文件中变量dailyWeaVar后设置对应的气象参数缩写。允许的输入见下面的代码。改组代码的意思为，如果用户输入为特定的参数prcp（日降雨量，mm），tmax（日最高气温，摄氏度），tmin（日最低气温，摄氏度），solar（日总太阳辐射量，MJ/m2），wind（日平均风速，m/s），rh（日相对湿度，fraction）。则将在APEXCONT文件中设置为对应的数值，用于告知模型用户输入了那些参数。如果没有参数，用户可以设置为-99或者0.00。由于APEXCONT设置好了，所以模型只会读取每一行对应位置的气象参数值。

```python
    if useDlyWea:
        if dailyWeaVar == ["prcp"]:
            contjs["weather"]["weather_in_var_ngn"] = "1"
        elif dailyWeaVar == ["prcp", "tmax", "tmin"]:
            contjs["weather"]["weather_in_var_ngn"] = "2"
        elif dailyWeaVar == ["prcp", "solar"]:
            contjs["weather"]["weather_in_var_ngn"] = "3"
        elif dailyWeaVar == ["prcp", "wind"]:
            contjs["weather"]["weather_in_var_ngn"] = "4"
        elif dailyWeaVar == ["prcp", "rh"]:
            contjs["weather"]["weather_in_var_ngn"] = "5"
        elif dailyWeaVar == ["prcp", "tmax", "tmin", "solar"]:
            contjs["weather"]["weather_in_var_ngn"] = "5"
        elif dailyWeaVar == ["prcp", "tmax", "tmin", "solar", "rh", "wind"]:
            contjs["weather"]["weather_in_var_ngn"] = "2345"
    else:
        contjs["weather"]["weather_in_var_ngn"] = "0"
```


### 气象站点列表文件准备

该软件的气象数据列表放置于scripts/clinear文件夹下，用户需要用文本文档打开exampleDlyList.db文件，如下

![cliStationList](D:\gitrepositories\pyapex\mdimages\cliStationList.png)

其中最主要的是中间四列。请勿修改格式，最简单的办法，就是通过复制第一行，然后新建一行，将样例中的"exampleObsPrcp";exampleObsPrcp;53.4667;122.3667;修改为用户指定站点的信息，分别为带双引号的站点名，不带双引号的站点名，纬度和经度。改好之后，保存即可。

### DLY文件准备

1. 使用Excel或其他工具准备好dly文件，格式如下图。DLY文件内部格式示意图，共9列，前三列分别为年、月、日，之后依次为太阳辐射、日最高气温、日最低气温、日降雨量、相对湿度和平均风速。。

    ![dlyfilescreen](D:\gitrepositories\pyapex\mdimages\dlyfilescreen.png)

2. 在准备过程中，用户可以通过使用Excel进行准备。在Excel中，首先将数据粘贴到表格中，然后通过设置单元格宽度来满足要求，9列分别要求的宽度为6，4，4，6，6，6，6，6，6。右键点击所选列（如列A）。选择设置列宽（W），打开列宽窗口，然后输入所需要的列宽。比如第一列A列为6个字符，输入数字6，点击确定即可。其他列依次设置。

    ![excellinewidth](D:\gitrepositories\pyapex\mdimages\excellinewidth.png)

    ![excellinewidth2](D:\gitrepositories\pyapex\mdimages\excellinewidth2.png)

    ![excellinewidth3](D:\gitrepositories\pyapex\mdimages\excellinewidth3.png)

3. 设置好之后，点击文件，另存为，选择带格式的文本文件（空格分隔）（*.prn），并设置好文件名称。最后将文件后缀改为DLY文件。

    ![excellinewidth4](D:\gitrepositories\pyapex\mdimages\excellinewidth4.png)

    ![excellinewidth5](D:\gitrepositories\pyapex\mdimages\excellinewidth5.png)



## 土地利用类型数据准备步骤

土地利用类型数据主要包含对user_lumgtupn.csv中的数据进行修改，并准备相应的OPC文件。其中user_lumgtupn.csv文件的各列意思为：

| 列名称                               | 说明                                                         |
| ------------------------------------ | ------------------------------------------------------------ |
| LanduseNo                            | 这是对应于土地利用空间数据landuse.tif属性表中各个栅格值的数字。土地空间数据属性表中包含的所有的数字都必须在这个列表中包含。 |
| LandCoverName                        | 土地利用属性表中数字对应的土地覆盖类型，比如10代表cropland或者cultivatedland。该数据需要根据用户自己的土地利用图进行设置。 |
| LandCoverGroup                       | 该属性对应于APEX 1501 user manual（用户手册）第79页Table 2.6中的土地利用类型一列。主要用于标注。 |
| OPCFileName                          | 土地覆盖所对应的OPC文件名称，非常重要。模型构建过程中，将依据表格中的OPC文件名称来读取各个土地覆盖的管理措施。所有对应的OPC文件都必须放置于apexprojects/project name +run mode/userlylistopcfiles文件夹下。 |
| APEXOPCNumber                        | 该列等于landuseNo一列。                                      |
| LUNOCV_Straight_Poor                 | 上述Table2.6中对应的耕作方式和水文条件下的Land Use Number 一列。用于结合水文土壤组（Hydrologic Soil Group），依据Table 2.6来确定各个子流域的初始径流曲线数（Curve Number）。 |
| LUNOCV_Straight_Good                 | 同上                                                         |
| LUNOCV_Contoured_Poor                | 同上                                                         |
| LUNOCV_Contoured_Good                | 同上                                                         |
| LUNOCV_ContouredTerraced_Poor        | 同上                                                         |
| LUNOCV_ContouredTerrace_Good         | 同上                                                         |
| UPN_Conventional_Tillage_No_ Residue | 该属性描述的是该土地覆盖下的地表曼宁系数值，确定依据为APEX 1501 user manual（用户手册）第48页Table 2.2中的地表曼宁系数表中的Type of surface一列。 |
| UPN_Conventional_Tillage_ Residue    | 同上                                                         |
| UPN_Chisel_Plow_No_Residue           | 同上                                                         |
| UPN_Chisel_Plow_Residue              | 同上                                                         |
| UPN_Fall_Disking_Residue             | 同上                                                         |
| UPN_No_Till_No_Residue               | 同上                                                         |
| UPN_No_Till_With_Residue_0to1ton     | 同上                                                         |
| UPN_No_Till_With_Residue_2to9ton     | 同上                                                         |

OPC文件中存储的是各个土地覆盖类型上的耕作管理措施，比如施肥、耕作、播种、收获、施农药等措施的具体日期和轮作信息。具体的准备方式详见APEX 1501 User Manual。目前该软件不提供界面化的文件制作方式。在后续开发中将会加入。

## Issues and fixes

### gdal_polynize.py not working

Ref: https://stackoverflow.com/questions/35500176/importerror-no-module-named-gdal

I was using python 3.7.9. But it does not work.

Currently, python 3.7.6 is sure to be working.