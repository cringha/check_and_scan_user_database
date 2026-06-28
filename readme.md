

## 将用户身份证、证书、合同等转用户截图 

export-user-info-to-images.py

```shell

usage: export-user-info-to-images.py [-h] [-i INPUT_XLSX] [-d USER_DATABASE] [-s OUTPUT_USER_IMAGES]
                                     [--sheet-name-user SHEET_NAME_USER] [--col-user-name COL_USER_NAME] [-c]
                                     [-t DOCX_TEMPLATE_FILE] [-o OUTPUT_DOCX_FILE]

转换用户身份证、证书、合同等转用户截图工具

options:
  -h, --help            show this help message and exit
  -i INPUT_XLSX, --input-xlsx INPUT_XLSX
                        输入Xlsx文件
  -d USER_DATABASE, --user-database USER_DATABASE
                        输入用户文件根目录
  -s OUTPUT_USER_IMAGES, --output-user-images OUTPUT_USER_IMAGES
                        输出截图文件根目录
  --sheet-name-user SHEET_NAME_USER
                        User sheet name
  --col-user-name COL_USER_NAME
                        user column name
  -c, --convert         将截图转换为DOCX文档
  -t DOCX_TEMPLATE_FILE, --docx-template-file DOCX_TEMPLATE_FILE
                        docx template filename
  -o OUTPUT_DOCX_FILE, --output-docx-file OUTPUT_DOCX_FILE
                        输出docx文件


```

## 将用户身份证、证书、合同截图转换为DOCX文档

export-user-image-to-docx.py 


```shell

将用户身份证、证书、合同截图转换为DOCX文档

options:
  -h, --help            show this help message and exit
  -i INPUT_XLSX, --input-xlsx INPUT_XLSX
                        输入Xlsx文件
  --user-snapshot-types USER_SNAPSHOT_TYPES
                        输入用户截图类型, '身份证', '毕业证', '资质证书', '合同', '社保'
  -s USER_SNAPSHOT_ROOT, --user-snapshot-root USER_SNAPSHOT_ROOT
                        输入用户截图文件根目录
  -x USER_SS_SNAPSHOT_ROOT, --user-ss-snapshot-root USER_SS_SNAPSHOT_ROOT
                        输入用户社保截图文件根目录
  --sheet-name-user SHEET_NAME_USER
                        User sheet name
  --sheet-name-project SHEET_NAME_PROJECT
                        project sheet name
  --sheet-name-duty SHEET_NAME_DUTY
                        duty sheet name
  --col-user-name COL_USER_NAME
                        user column name
  -t DOCX_TEMPLATE_FILE, --docx-template-file DOCX_TEMPLATE_FILE
                        docx template filename
  -o OUTPUT_DOCX_FILE, --output-docx-file OUTPUT_DOCX_FILE
                        输出docx文件


```
