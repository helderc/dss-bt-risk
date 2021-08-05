import sys

import numpy as np
from scipy.stats import norm

import qtmodern.styles
import qtmodern.windows
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtChart import QChart, QChartView, QBarSet, QValueAxis, QPercentBarSeries, QBarCategoryAxis
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import Qt


from bayesiannet import BayesianNet


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #self._model = GraphModel()
        uic.loadUi("mainwindow.ui", self)

        # Generate checkboxes based on length of data in model
        # for datapoint in range(self._model.datapoints):
        #     self.tempCheck = QtWidgets.QCheckBox(self.scenarioGroupBox)
        #     self.tempCheck.setFont(QtGui.QFont('SansSerif', 13))
        #     self.tempCheck.setObjectName(str(datapoint))
        #     self.tempCheck.toggled.connect(self.updateGraph)
        #     self.verticalLayout.addWidget(self.tempCheck, alignment=QtCore.Qt.AlignTop)
        #     self.tempCheck.setText(
        #         QtCore.QCoreApplication.translate(
        #             "MainWindow", f"Scenario {datapoint+1}"
        #         )
        #     )

        self.bnet = BayesianNet()

        # TODO: Automate creation/population of sets
        sets = []

        # Testing barchart
        set0 = QBarSet("PofS")
        set1 = QBarSet("Bob")
        set2 = QBarSet("Tom")
        set3 = QBarSet("Logan")
        set4 = QBarSet("Karim")


        set0 << 8 << 55 << 0 << 0 << 0 << 0 << 0 << 0 << 0#= self.bnet.doInference(self.bnet.bn, 'PofS').toarray() * 100
        set1 << 2 << 45 << 0 << 4 << 0 << 0 << 0 << 0 << 0
        set2 << 0 << 0 << 8 << 13 << 8 << 0 << 0 << 0 << 0
        set3 << 0 << 0 << 7 << 3 << 4 << 0 << 0 << 0 << 0
        set4 << 0 << 0 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0

        series = QPercentBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)

        #series2 = QPercentBarSeries()
        

        chart = QChart()
        #chart.setTheme(QChart.ChartThemeQt)
        chart.addSeries(series)
        #chart.addSeries(series2)
        chart.setTitle("DSS - Diamond Princess cruise ship")

        font = QFont()
        font.setPixelSize(14)
        font.setBold(True)

        chart.setTitleFont(font)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ['Age', 'Gender', 'PofS', 'IPR', 'FNR', 'FPR', 'CovS', 'TPos', 'IFR']
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsAngle(-45)
        axisX.setTitleText('Variables')
        #chart.createDefaultAxes()
        chart.addAxis(axisX, Qt.AlignBottom)
        

        axisY = QValueAxis()
        axisY.setRange(0,100)
        axisY.setTickCount(11)
        axisY.setLabelFormat('%d')
        axisY.setTickType(QValueAxis.TicksFixed)
        axisY.setTitleText('Percentage')

        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        # TODO: Y-axis set tick interval 10
        # TODO: Y-axis horizontal lines

        chart.legend().setVisible(False)
        chart.legend().setAlignment(Qt.AlignBottom)

        
        #chartView = QChartView(chart)
        #chartView.setRenderHint(QPainter.Antialiasing)

        self.widget.setChart(chart) 

        # connecting signals to slots
        self.sldrAge.valueChanged.connect(self.SliderChanged)
        self.actionExit.triggered.connect(self.Exit)
        self.actionAbout.triggered.connect(self.About)
        self.actionAbout_Qt.triggered.connect(self.AboutQt)
        #self.simulationStopButton.clicked.connect(self.SIRWidget.thread_cancel)
        # NOTE: stop button will literally just kill entire main window

    def SliderChanged(self, v):
        self.lblAge.setText(f'Age: {v}')

    def About(self):
        QMessageBox.about(self,
                    'About...',
                    'by Helder')

    def AboutQt(self):
        QMessageBox.aboutQt(self)

    def Exit(self):
        # QtWidgets.qApp.quit
        self.close()

    # TODO: Maybe this will be necessary when plotting new graphs
    def updateGraph(self):
        """Updates graph respective to status of toggled checkbox.

        Retrieves sender (toggled checkbox) reference and if it is checked, retrieves data from model 
        and passes it to drawLine(). If not checked, references line respective to checkbox and removes
        it.
        """
        checkbox = self.sender()
        checkboxNumber = int(checkbox.objectName())
        if checkbox.isChecked():
            peak = self._model.get_peak(checkboxNumber)
            duration = self._model.get_duration(checkboxNumber)
            self.drawLine(peak=peak, checkboxNumber=checkboxNumber, duration=duration)
        else:
            for line in self.graphWidget.canvas.ax.lines:
                if line.get_label() == f"Scenario {checkboxNumber+1}":
                    self.graphWidget.canvas.ax.lines.remove(line)
            # TODO: Resize after removal of line
        self.graphWidget.canvas.ax.legend()
        # NOTE: Legend is not ordered, not too sure if worth addressing or not.
        self.graphWidget.canvas.draw()

    def drawLine(self, peak, checkboxNumber, duration=100.0):
        """Generates gaussian wave based off given peak and duration data in order to model disease spread. 

        Processes gaussian wave off peak and duration data, passes x and y arrays to MplWidget.plot(). 
        Assigns labels to lines for referenced removal.

        Parameters
        ----------
        peak : float
            Desired peak (%) of wave
        duration : float, optional
            Desired duration of wave (days), by default 100.0
        """
        X = np.linspace(0, duration, 100)
        y = norm.pdf(X, duration / 2, duration / 6)
        y = peak / max(y) * y  # Stretches curve to reach peak point
        self.graphWidget.plot(X, y, label=f"Scenario {checkboxNumber+1}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main = qtmodern.windows.ModernWindow(main)
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
