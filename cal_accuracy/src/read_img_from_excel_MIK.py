#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import zipfile
import io

def read_img_from_excel_MIK(xlsx_filename, img_path):
    """
    read img from excel, treat xlsx file as zip
    """

    with zipfile.ZipFile(xlsx_filename) as inzip:
        for info in inzip.infolist():
            name = info.filename
            content = inzip.read(info)
            if name.endswith((".png", ".jpeg", ".gif")):
                prefix_list = xlsx_filename.split("\\")
                prefix_name = prefix_list[-4] + "_" + prefix_list[-3] + "_" + prefix_list[-2] + "_"
                # fmt = name.split(".")[-1]
                img_name = img_path + prefix_name + name.split("/")[-1]
                img = Image.open(io.BytesIO(content))
                img.save(str(img_name))
                print("Success save ", img_name)
                # outb = io.BytesIO()
                # img.save(outb, fmt)
    inzip.close()
