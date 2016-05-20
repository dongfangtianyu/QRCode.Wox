#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from wox import Wox, WoxAPI
import os
import sys
import hashlib
import logging

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='wox_qrcpde.log',
                    filemode='w')
try:
    import qrcode
    import Image
    HAS_QRCODE = True
except Exception, e:
    HAS_QRCODE = False


def md5(value):
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()


class WoxQRcode(Wox):

    def __init__(self):
        logging.debug("sys.argv: %s" % sys.argv[1])
        self.plugin_path = os.path.dirname(os.path.realpath(__file__))
        self.img_path = os.path.join(self.plugin_path, '.cahe')
        if not os.path.exists(self.img_path):
            os.mkdir(self.img_path)
        logging.debug("Im runing,plugin_path is '%s' , img_path is '%s'" % (self.plugin_path ,self.img_path))

        super(WoxQRcode, self).__init__()

    def query(self, query):
        logging.debug("method:query, parameters:%s " % query)

        results = []
        if HAS_QRCODE is not True:
            results.append({
                "Title": "Mak QR Code",
                "SubTitle": "ERROR: Can Not Import Module: qrcode ",
                "IcoPath":"Images/app.ico",
            })
        else:
            results.append({
                "Title": "Mak QR Code",
                "SubTitle": "Context: {}".format(query),
                "IcoPath": "Images/app.ico",
                "JsonRPCAction": {
                    "method": "makeQRImage",
                    "parameters": [query],
                    "dontHideAfterAction": True}

            })

        logging.debug("results = %s" % results)
        return results

    def makeQRImage(self, context):
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
        # WoxAPI.hide_app()
        # WoxAPI.change_query(['111'])
        return self.showQRImage(QRImagePath)

    def showQRImage(self, QRImagePath):
        logging.debug("starting show QRImage...")
        os.startfile(QRImagePath)

        logging.debug("show QRImage end")


if __name__ == "__main__":
    WoxQRcode()
