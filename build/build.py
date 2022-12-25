# coding=utf-8

import os
import zipfile
from datetime import datetime

import cairosvg
import httpx
import pikepdf
import pytz

URL_API = "https://api.github.com/repos/SierraQin/metro/commits?path=src%2FMTR2.svg"
PATH_SRC = "../src/MTR2.svg"
PATH_LICENSE = "../LICENSE"
PATH_OUTPUT = "../build/"


buildTime = pytz.timezone(
    "Asia/Shanghai").localize(datetime.now()).replace(microsecond=0).isoformat()
commitInfo = httpx.get(URL_API).json()[0]
buildVer = commitInfo["sha"]
commitDate = commitInfo["commit"]["committer"]["date"]
commitDate = commitDate[2:4]+commitDate[5:7]+commitDate[8:10]
buildName = "MTR"+commitDate+"_dev-"+buildVer[:7]

svgTempPath = PATH_OUTPUT+buildName+"_temp.svg"
pdfTempPath = PATH_OUTPUT+buildName+"_temp.pdf"
pdfPath = PATH_OUTPUT+buildName+".pdf"
txtPath = PATH_OUTPUT+"readme.txt"
zipPath = PATH_OUTPUT+buildName+".zip"


for root, dirs, files in os.walk(PATH_OUTPUT, topdown=False):
    for name in files:
        if "MTR" in name and "_dev-" in name:
            os.remove(os.path.join(root, name))


cairosvg.svg2svg(url=PATH_SRC, write_to=svgTempPath)
cairosvg.svg2pdf(url=svgTempPath, write_to=pdfTempPath)


pdf = pikepdf.open(pdfTempPath)


with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
    meta["dc:title"] = "北京市轨道交通线路配置图"
    meta["dc:description"] = "北京地铁路网配线图 开发版"+buildVer[:7]
    meta["dc:creator"] = ["SierraQin"]
    #meta["xmp:CreatorTool"] = "CairoSVG 2.5.2 (https://cairosvg.org)"
    meta["xmp:CreatorTool"] = "cairo 1.15.12 (https://www.cairographics.org)"
    meta["xmp:CreateDate"] = commitInfo["commit"]["committer"]["date"]
    meta["xmp:ModifyDate"] = buildTime
    meta["pdf:Producer"] = "pikepdf 4.3.1 (https://github.com/pikepdf/pikepdf)"
    meta["{http://creativecommons.org/ns#}license"] = "http://creativecommons.org/licenses/by-sa/4.0/"
    meta["{http://creativecommons.org/ns#}attributionName"] = ["SierraQin"]
    meta["{http://creativecommons.org/ns#}morePermissions"] = "https://github.com/SierraQin/metro/blob/master/LICENSE"
    meta["{http://ns.adobe.com/xap/1.0/rights/}WebStatement"] = "https://github.com/SierraQin/metro"
    meta["{http://ns.adobe.com/xap/1.0/rights/}UsageTerms"] = "This work is licensed under a &lt;a rel=&#34;license&#34; href=&#34;http://creativecommons.org/licenses/by/4.0/&#34;&gt;Creative Commons Attribution 4.0 International License&lt;/a&gt;."
    meta["{http://ns.adobe.com/xap/1.0/rights/}Marked"] = "True"


pdf.save(PATH_OUTPUT+buildName+".pdf")


txt = ""
txt += "提交编号："+buildVer+"\n提交时间："+commitInfo["commit"]["committer"]["date"]
txt += "\n提交描述："+commitInfo["commit"]["message"]
txt += "\n构建名称："+buildName+"\n构建时间："+buildTime
txt += '''



本压缩包内包含以下文件：
readme.txt
  本文件。由计算机程序自动生成。
LICENSE
  项目使用授权协议文本。由creativecommons.org生成。
'''
txt += buildName+".pdf"
txt += '''
  开发版本配线图PDF文件。由计算机程序自动生成。



请注意：您当前正在阅读的版本为开发版本。开发版本旨在方便用户查看配线图当前的开发绘
制进度，不属于本项目的发行版范畴。由于开发版本属于过程性版本，因此其中可能存在较多
的错误或瑕疵。同时，由于该版本文件由计算机程序自动导出，未经人工校审，可能存在意料
之外的错误。值得注意的是，开发版本中可能会存在临时性或过程性内容，同时部分正式版内
容也可能会被暂时隐藏。开发版本不代表下个正式版本的最终效果，并可能会与其存在较大的
差异。欲使用正式版配线图，请您访问项目主页进行下载。

项目主页：
https://github.com/SierraQin/metro



生成此文件的流水线使用了下列工具：
cairo     1.15.12  MPL-1.1   www.cairographics.org
CairoSVG  2.5.2    LGPL-3.0  cairosvg.org
pikepdf   4.3.1    MPL-2.0   github.com/pikepdf/pikepdf
'''


txtFile = open(txtPath, "w")
txtFile.write(txt)
txtFile.close()


zipFile = zipfile.ZipFile(zipPath, "w")
zipFile.write(pdfPath, arcname=buildName+".pdf")
zipFile.write(txtPath, arcname="readme.txt")
zipFile.write(PATH_LICENSE, arcname="LICENSE")
zipFile.close()


for root, dirs, files in os.walk(PATH_OUTPUT, topdown=False):
    for name in files:
        if "readme.txt" in name or "temp" in name:
            os.remove(os.path.join(root, name))
