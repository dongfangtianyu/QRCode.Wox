#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from wox import Wox, WoxAPI
import os
import sys
import shutil
import hashlib
import logging

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='wox_qrcpde.log',
                    filemode='w')
try:
    import qrcode
    from PIL import Image
    HAS_QRCODE = True
except Exception as e:
    HAS_QRCODE = False


def md5(value):
    m = hashlib.md5()
    m.update(str(value).encode("utf-8"))
    return m.hexdigest()


class WoxQRcode(Wox):
    request_query = ''
    plugin_ico = "Images/pic.png"

    def __init__(self):
        logging.debug("sys.argv: %s" % sys.argv[1])

        self.plugin_path = os.path.dirname(os.path.realpath(__file__))
        self.img_path = os.path.join(self.plugin_path, '.cahe')
        if not os.path.exists(self.img_path):
            os.mkdir(self.img_path)

        logging.debug("Im runing,plugin_path is '%s' , img_path is '%s'" % (self.plugin_path ,self.img_path))

        super(WoxQRcode, self).__init__()

    def query(self, request_query):
        logging.debug("method:query, parameters:%s " % request_query)

        self.request_query = request_query
        results = []
        if request_query in 'clean':
            # clean cache img
            results.append(self.get_result('CLEAN_IMAGE_CACHE', request_query))

        if HAS_QRCODE is not True:
            # if not has qrcode module , plugin can not work
            results.append(self.get_result('NOT_HAS_QRCODE_MODULE', request_query))

        else:
            results.append(self.get_result('MAKE_QRCODE', request_query))

        logging.debug("results = %s" % results)
        return results

    def make_qr_image(self, context):
        logging.debug("starting make QRImage...")

        QRImageName = "qrcode_{}.jpg".format(md5(context))
        QRImagePath = os.path.join(self.img_path, QRImageName)
        logging.debug("QRImagePath is %s" % QRImagePath)

        if not os.path.exists(QRImagePath):
                logging.debug("QRImage file not exists,so need make")

                img = qrcode.make(context, border=1)
                img.save(QRImagePath)

                logging.debug("make QRImage ok, this file size is %s" % os.path.getsize(QRImagePath))
        else:
            logging.debug("has cache, use cache image")
        # Wox输入框可能会遮挡二维码
        WoxAPI.hide_app()
        return self.show_image(QRImagePath)

    def show_image(self, QRImagePath):
        logging.debug("starting show QRImage...")

        os.startfile(QRImagePath)

        logging.debug("show QRImage end")

    def clean_cache(self, contest):
        shutil.rmtree(self.img_path)
        WoxAPI.show_msg("Success", " clean up cache file done", self.plugin_ico)

    # messgae
    def get_result(self, key, request_query):
        messages = {
            'CLEAN_IMAGE_CACHE': {
                "Title": "Clean Cache",
                "SubTitle": "input 'clean', can clean this plugin cache",
                "IcoPath": self.plugin_ico,
                "JsonRPCAction": {
                    "method": "clean_cache",
                    "parameters": [request_query],
                    "dontHideAfterAction": True
                }
            },

            'NOT_HAS_QRCODE_MODULE': {
                "Title": "ERROR: ",
                "SubTitle": "Can Not Import Module: qrcode ",
                "IcoPath": self.plugin_ico,
            },

            'MAKE_QRCODE': {
                "Title": "Mak QR Code",
                "SubTitle": "Context: {}".format(request_query),
                "IcoPath": self.plugin_ico,
                "JsonRPCAction": {
                    "method": "make_qr_image",
                    "parameters": [request_query],
                    "dontHideAfterAction": False
                }
            }
        }

        return messages.get(key, {"Title": "Mak QR Code", "SubTitle": "Context: {}".format(request_query)})
if __name__ == "__main__":
    WoxQRcode()
