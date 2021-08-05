import sys

import numpy as np
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from scipy.stats import norm

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

        chart = QChart()
        series = QLineSeries()

        series.append(1,3)
        series.append(2,4)

        chart.addSeries(series)
        chart.setTitle('Example')
        chart.createDefaultAxes()

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
