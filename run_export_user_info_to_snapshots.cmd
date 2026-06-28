@call .venv\Scripts\activate.bat
chcp 65001

REM 读取用户资料,将身份证、毕业证等PDF转换为 PNG 截图

REM 输入的Excel数据，只有一列用户名
SET INPUT_EXCEL=data\user-single-list.xlsx


REM 包含用户身份证、毕业证等文件的根目录 
SET INPUT_USER_DATABASE_ROOT="D:\用户身份证、毕业证、合同等信息"

REM 输出，社保截图文件的存放位置
SET OUTPUT_IMAGE_ROOT=.\output

python export-user-info-to-images.py -i %INPUT_EXCEL% -d %INPUT_USER_DATABASE_ROOT% --output-user-images %OUTPUT_IMAGE_ROOT% --sheet-name-user Users --col-user-name 人名  


@call .venv\Scripts\deactivate.bat