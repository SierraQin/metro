# coding=utf-8

import os
import time

import cairosvg
import httpx
import pikepdf


URL_API = "https://gitee.com/api/v5/repos/sierraqin/metro/commits?path=src%2FMTR2.svg&page=1&per_page=1"
PATH_SRC = "../src/MTR2.svg"
PATH_OUTPUT = "../ignore/"


buildDate = time.strftime("%y%m%d", time.localtime())
buildVer = httpx.get(URL_API).json()[0]["sha"][:7]
buildName = "MTR"+buildDate+"_dev-"+buildVer

svgPath = PATH_OUTPUT+buildName+"_temp.svg"
pdfPath = PATH_OUTPUT+buildName+"_temp.pdf"


for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if "MTR" in name and "_dev-" in name:
            os.remove(os.path.join(root, name))


cairosvg.svg2svg(url=PATH_SRC, write_to=svgPath)
cairosvg.svg2pdf(url=svgPath, write_to=pdfPath)


pdf = pikepdf.open(pdfPath)


with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
    meta["dc:title"] = "北京市轨道交通线路配置图"
    meta["dc:description"] = "北京地铁路网配线图"
    meta["dc:creator"] = ["SierraQin"]
    #meta["xmp:CreatorTool"] = "CairoSVG 2.5.2 (https://cairosvg.org)"
    meta["xmp:CreatorTool"] = "cairo 1.15.12 (http://www.cairographics.org/)"
    meta["pdf:Producer"] = "pikepdf 4.3.1 (https://github.com/pikepdf/pikepdf)"
    meta["{http://creativecommons.org/ns#}license"] = "http://creativecommons.org/licenses/by-sa/4.0/"
    meta["{http://creativecommons.org/ns#}attributionName"] = ["SierraQin"]
    meta["{http://creativecommons.org/ns#}morePermissions"] = "https://gitee.com/SierraQin/metro/blob/master/LICENSE"
    meta["{http://ns.adobe.com/xap/1.0/rights/}WebStatement"] = "https://gitee.com/SierraQin/metro"
    meta["{http://ns.adobe.com/xap/1.0/rights/}UsageTerms"] = "This work is licensed under a &lt;a rel=&#34;license&#34; href=&#34;http://creativecommons.org/licenses/by/4.0/&#34;&gt;Creative Commons Attribution 4.0 International License&lt;/a&gt;."
    meta["{http://ns.adobe.com/xap/1.0/rights/}Marked"] = "True"


pdf.save(PATH_OUTPUT+buildName+".pdf")


for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if "MTR" in name and "temp" in name:
            os.remove(os.path.join(root, name))
