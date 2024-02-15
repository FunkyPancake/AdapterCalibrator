# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QGridLayout, QLCDNumber, QLabel, QLayout,
    QLineEdit, QMainWindow, QPlainTextEdit, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(624, 250)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(624, 0))
        MainWindow.setMaximumSize(QSize(625, 250))
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMaximumSize(QSize(625, 250))
        self.centralwidget.setAutoFillBackground(False)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetFixedSize)
        self.pass_fail_label = QLabel(self.centralwidget)
        self.pass_fail_label.setObjectName(u"pass_fail_label")
        font = QFont()
        font.setBold(True)
        self.pass_fail_label.setFont(font)
        self.pass_fail_label.setFrameShape(QFrame.Box)
        self.pass_fail_label.setFrameShadow(QFrame.Plain)
        self.pass_fail_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.pass_fail_label, 5, 8, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 1, 4, 5, 1)

        self.connect_tutton = QPushButton(self.centralwidget)
        self.connect_tutton.setObjectName(u"connect_tutton")

        self.gridLayout_3.addWidget(self.connect_tutton, 5, 0, 1, 1)

        self.cal_h_t_num = QLCDNumber(self.centralwidget)
        self.cal_h_t_num.setObjectName(u"cal_h_t_num")

        self.gridLayout_3.addWidget(self.cal_h_t_num, 5, 6, 1, 1)

        self.tol_sb = QDoubleSpinBox(self.centralwidget)
        self.tol_sb.setObjectName(u"tol_sb")
        self.tol_sb.setSingleStep(0.100000000000000)

        self.gridLayout_3.addWidget(self.tol_sb, 3, 1, 1, 2)

        self.cal_h_m_num = QLCDNumber(self.centralwidget)
        self.cal_h_m_num.setObjectName(u"cal_h_m_num")
        self.cal_h_m_num.setSegmentStyle(QLCDNumber.Filled)

        self.gridLayout_3.addWidget(self.cal_h_m_num, 5, 7, 1, 1)

        self.vsup_pb = QProgressBar(self.centralwidget)
        self.vsup_pb.setObjectName(u"vsup_pb")
        self.vsup_pb.setMinimum(-100)
        self.vsup_pb.setMaximum(100)
        self.vsup_pb.setValue(0)

        self.gridLayout_3.addWidget(self.vsup_pb, 3, 8, 1, 1)

        self.vsup_ideal_num = QLCDNumber(self.centralwidget)
        self.vsup_ideal_num.setObjectName(u"vsup_ideal_num")
        self.vsup_ideal_num.setSmallDecimalPoint(False)
        self.vsup_ideal_num.setDigitCount(5)
        self.vsup_ideal_num.setMode(QLCDNumber.Dec)
        self.vsup_ideal_num.setProperty("value", 5.000000000000000)
        self.vsup_ideal_num.setProperty("intValue", 5)

        self.gridLayout_3.addWidget(self.vsup_ideal_num, 3, 6, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 2, 5, 1, 1)

        self.cal_l_t_num = QLCDNumber(self.centralwidget)
        self.cal_l_t_num.setObjectName(u"cal_l_t_num")

        self.gridLayout_3.addWidget(self.cal_l_t_num, 4, 6, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)

        self.can_if_combo_box = QComboBox(self.centralwidget)
        self.can_if_combo_box.setObjectName(u"can_if_combo_box")

        self.gridLayout_3.addWidget(self.can_if_combo_box, 2, 1, 1, 2)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.label.setFont(font1)

        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 4)

        self.vsup_meas_num = QLCDNumber(self.centralwidget)
        self.vsup_meas_num.setObjectName(u"vsup_meas_num")
        self.vsup_meas_num.setSmallDecimalPoint(False)

        self.gridLayout_3.addWidget(self.vsup_meas_num, 3, 7, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 4, 5, 1, 1)

        self.cal_pb = QProgressBar(self.centralwidget)
        self.cal_pb.setObjectName(u"cal_pb")
        self.cal_pb.setMinimum(-100)
        self.cal_pb.setValue(0)

        self.gridLayout_3.addWidget(self.cal_pb, 4, 8, 1, 1)

        self.id_line_edit = QLineEdit(self.centralwidget)
        self.id_line_edit.setObjectName(u"id_line_edit")
        sizePolicy2.setHeightForWidth(self.id_line_edit.sizePolicy().hasHeightForWidth())
        self.id_line_edit.setSizePolicy(sizePolicy2)
        self.id_line_edit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.id_line_edit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.id_line_edit, 2, 6, 1, 2)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy2.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy2)
        self.label_6.setFont(font1)

        self.gridLayout_3.addWidget(self.label_6, 1, 5, 1, 4)

        self.cal_l_m_num = QLCDNumber(self.centralwidget)
        self.cal_l_m_num.setObjectName(u"cal_l_m_num")

        self.gridLayout_3.addWidget(self.cal_l_m_num, 4, 7, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 4, 0, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 3, 5, 1, 1)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 3, 0, 1, 1)

        self.db_path_line_edit = QLineEdit(self.centralwidget)
        self.db_path_line_edit.setObjectName(u"db_path_line_edit")

        self.gridLayout_3.addWidget(self.db_path_line_edit, 4, 1, 1, 2)

        self.status_indicator = QLabel(self.centralwidget)
        self.status_indicator.setObjectName(u"status_indicator")
        self.status_indicator.setFont(font)
        self.status_indicator.setLayoutDirection(Qt.LeftToRight)
        self.status_indicator.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.status_indicator, 5, 1, 1, 3)

        self.cal_status = QLabel(self.centralwidget)
        self.cal_status.setObjectName(u"cal_status")
        self.cal_status.setFont(font)
        self.cal_status.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.cal_status, 2, 8, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.log_text = QPlainTextEdit(self.centralwidget)
        self.log_text.setObjectName(u"log_text")

        self.gridLayout.addWidget(self.log_text, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Calibrator", None))
        self.pass_fail_label.setText(QCoreApplication.translate("MainWindow", u"PassFail", None))
        self.connect_tutton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.vsup_pb.setFormat(QCoreApplication.translate("MainWindow", u"%v", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"ID", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"CAN IF", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Config", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Cal Points", None))
        self.cal_pb.setFormat(QCoreApplication.translate("MainWindow", u"%v", None))
        self.id_line_edit.setText(QCoreApplication.translate("MainWindow", u"id", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Results", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"DB path", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"V supply", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Max tolerance", None))
        self.status_indicator.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.cal_status.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

