# -*- coding: utf-8 -*-
# @Author  : xky
# @Link    : https://lewistian.github.io/
# @Version : Python3.6
import shutil
from PyQt5 import QtWidgets
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDesktopWidget
from slr1 import slr1_analyse
from lexer.scanner import gen_tokens
from ui.mainwindows import Ui_mainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import re
import sys
import os

CWD = os.getcwd()
APP_ImagePath = CWD + os.sep + 'images'
APP_HtmlPath = CWD + os.sep + 'lib'


class MissevanKit(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MissevanKit, self).__init__(parent)

        self.setupUi(self)
        self.filename = ''
        self.tb_slr.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.tb_table.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.tb_quad.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.tb_vn.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.center()
        self.setTab1()
        self.setTab2()
        self.setTab4()

        self.tabWidget.setCurrentIndex(0)

    def center(self):  # 实现窗体在屏幕中央
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def setTab1(self):
        self.pb_analy_choose.clicked.connect(self.choose_input)
        self.pb_analy_start.clicked.connect(self.start_ana)
        # self.pb_analy_stop.clicked.connect()
        pass

    def setTab2(self):


        self.pb_slr_start.clicked.connect(self.gen_slr)
        self.pb_slr_quad.clicked.connect(self.gen_quad)
    def setTab4(self):
        self.webview = QWebEngineView()
        self.webview.load(QUrl('https://github.com/wscjxky/'))
        self.gridLayout_3.addWidget(self.webview)

    def gen_slr(self):
        input_str=self.te_slr_input.toPlainText()
        if not self.tb_vn.toPlainText():
            if input_str:
                slr_vn, slr_vt, slr_first, slr_follow, slr_table, slr_process, quad = slr1_analyse()
                print( slr_vn, slr_vt, slr_first, slr_follow, slr_table, slr_process, quad)
                if slr_vn and  slr_vt and  slr_first and  slr_follow and  slr_table and  slr_process and  quad:
                    self.tb_vn.setPlainText("FIRST集合：%s\nFollow集合：%s\n非终结符集合：%s\n终结符集合："
                                            "%s" % (slr_first, slr_follow,slr_vn, slr_vt))
                    self.tb_table.setPlainText(str(slr_table))
                    self.tb_slr.setPlainText(str(slr_process))
                    self.tb_quad.setPlainText(str(quad))
                    self.echo('分析成功')
    def gen_quad(self):
        slr_vn, slr_vt, slr_first, slr_follow, slr_table, slr_process, quad = slr1_analyse()
        if quad:
            self.tb_quad.setText(quad)

    def start_ana(self):
        if self.filename:
            tokens = gen_tokens(self.filename)
            if tokens:
                self.tb_analy_res.setText(tokens)
                self.echo('分析成功')

    def choose_input(self):
        self.filename = QFileDialog.getOpenFileName(self, "选择源c文件",
                                                    APP_StaicPath)[0]
        print(self.filename)
        if self.filename:
            self.te_filename.setPlainText(self.filename)
            with open(self.filename, 'r', encoding='utf8')as f:
                inputs = f.read()
                self.tb_analy_input.setText(inputs)
                self.echo('载入' + self.filename + '成功')
        else:
            self.echo("载入失败")

    def echo(self, value):
        '''显示对话框返回值'''
        box = QMessageBox(self)
        box.information(self, "操作成功", "{}\n".format(value),
                        QMessageBox.Ok)
        # box.setIcon(("D:/pycharmproject/red-green-blindness/demo/image/success_48px_1129030_easyicon.net.png"))


import qtmodern.windows

if __name__ == "__main__":
    app = QApplication(sys.argv)
    APP_StaicPath = os.pardir + os.sep + 'mid_result'
    # APP_ImagePath = APP_DirPath + os.sep + 'image'
    # APP_HtmlPath = APP_DirPath + os.sep + 'lib'
    win = MissevanKit()
    mw = qtmodern.windows.ModernWindow(win)
    mw.show()
    sys.exit(app.exec_())
