import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class MyDialog (QtWidgets.QDialog):

	def __init__(self):
		super().__init__()

		# tabWidget requires a widget as a tab container
		# parent -> QTabWidget -> QWidget(sub. QGroupBox) -> QLayout
		self.setWindowTitle("Project Wizard")

		mainLayout = QtWidgets.QGridLayout(self)

		self.createProfileGroupBox()
		self.createDesignGroupBox()
		self.createCollateralGroupBox()

		mainLayout.addWidget(self.profileGroupBox, 1, 1)
		mainLayout.addWidget(self.designGroupBox, 1, 2)
		mainLayout.addWidget(self.collateralGroupBox, 2, 1, 1, 2)


		self.setLayout(mainLayout)

	def createProfileGroupBox(self):


		self.projectLineEdit = QtWidgets.QLineEdit(self)
		self.projectLineEdit.setClearButtonEnabled(True)
		self.projectLineEdit.setPlaceholderText("project name")
		self.projectLineEdit.textChanged.connect(self.projectNameChanged)

		self.fabComboBox = QtWidgets.QComboBox()
		self.fabComboBox.addItems(["TSMC", "SEC"])
		#fabComboBox.setEditable(True)
		
		self.nodeComboBox = QtWidgets.QComboBox()
		self.nodeComboBox.addItems(["12nm", "10nm", "8nm", "7nm", "5nm"])


		self.rowHeightComboBox = QtWidgets.QComboBox()
		self.rowHeightComboBox.addItems(["8P59", "9P55","11P45","9", "12"])

		self.toolComboBox = QtWidgets.QComboBox()
		self.toolComboBox.addItems(["INNOVUS", "ICC2"])

		profileLayout = QtWidgets.QFormLayout()
		profileLayout.addRow("Project", self.projectLineEdit)
		profileLayout.addRow("Fab", self.fabComboBox)
		profileLayout.addRow("Node", self.nodeComboBox)
		profileLayout.addRow("Row Height (tr)", self.rowHeightComboBox)
		profileLayout.addRow("Tool", self.toolComboBox)


		#tab1GroupBox = QtWidgets.QGroupBox("blala")			
		self.profileGroupBox = QtWidgets.QGroupBox()
		self.profileGroupBox.setLayout(profileLayout)
		self.profileGroupBox.setTitle("&Profile")


		
	def createDesignGroupBox(self):

		# self.blockLineEdit = QtWidgets.QLineEdit(self)
		# self.blockLineEdit.setClearButtonEnabled(True)
		# self.blockLineEdit.setPlaceholderText("block name")
		modelRoot = QtGui.QStandardItem("chip top")
		modelRoot.setCheckable(True)
		# modelRoot.appendRow(QtGui.QStandardItem("model child1"))

		self.blockListModel = QtGui.QStandardItemModel(self)
		self.blockListModel.setItem(0, 0, modelRoot)
		#self.blockListModel.setHorizontalHeaderLabels(["Root", "L1", "L2"])
		self.blockListModel.setHorizontalHeaderLabels(["Blabababa"])
		#self.blockListSELModel = QtCore.QItemSelectionModel(self)

		self.blockListView = QtWidgets.QTreeView(self)
		self.blockListView.setModel(self.blockListModel)
		self.blockListView.setTreePosition(-1)
		self.blockListView.setAnimated(True)
		self.blockListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.blockListView.customContextMenuRequested.connect(self.blockListMenu)
		#self.blockListView.setHeaderHidden(True)
		
		insertKey = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Insert), self.blockListView)
		insertKey.activated.connect(self.addAct_toggled)

		deleteKey = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self.blockListView)
		deleteKey.activated.connect(self.delAct_toggled)

		designLayout = QtWidgets.QFormLayout()
		# designLayout.addRow("&Block", self.blockLineEdit)
		designLayout.addRow(self.blockListView)

		self.designGroupBox = QtWidgets.QGroupBox()
		self.designGroupBox.setLayout(designLayout)
		self.designGroupBox.setTitle("&Design")
		
	def createCollateralGroupBox(self):

		### tech file ###
		self.techfileLineEdit = QtWidgets.QLineEdit()
		self.techfileLineEdit.setClearButtonEnabled(True)
		self.techfileLineEdit.setPlaceholderText("technology file")
		
		tfSearchButton = QtWidgets.QPushButton("...", self)
		tfSearchButton.clicked.connect(self.tfSearchButton_clicked)

		### tech file ###

		collateralLayout = QtWidgets.QGridLayout()
		collateralLayout.addWidget(QtWidgets.QLabel("Tech"), 0, 0)
		collateralLayout.addWidget(self.techfileLineEdit, 0, 1, 1, 2)
		collateralLayout.addWidget(tfSearchButton, 0, 3)
		collateralLayout.setColumnStretch(1, 1)



		self.collateralGroupBox = QtWidgets.QGroupBox(self)
		self.collateralGroupBox.setLayout(collateralLayout)
		self.collateralGroupBox.setTitle("&Collateral")

	def createMMMCGroupBox(self):
		pass


### sub function ###

	def projectNameChanged(self, name):
		self.blockListModel.setHorizontalHeaderLabels([name])

	def tfSearchButton_clicked(self):
		fileName_tuple = QtWidgets.QFileDialog.getOpenFileName(self,
				"tech nology file",
				"/data/tool_lib/lib_tmp/SEC_8n_DK/LN08LPP_INNOVUS_S00-V1.2.1.1/LN08LPP_INNOVUS_S00-V1.2.1.1_SOURCE/TECH/LN08LPP_INNOVUS_S00-V1.2.1.1/10M_3Mx_5Dx_1Gx_1Iz_LB/11p45TR_HSDB/",
				"tf(*.tf);;tlef(*tlef);;tlef(*.lef);;all(*)")

		fileName = fileName_tuple[0]
		self.techfileLineEdit.insert(fileName)
		#debug# print(self.techfileLineEdit.text())

	def blockListMenu(self, position):

		addAct = QtWidgets.QAction(self)
		addAct.setText(self.tr("Add sub-block"))
		addAct.triggered.connect(self.addAct_toggled)


		delAct = QtWidgets.QAction(self)
		delAct.setText(self.tr("Del sub-block"))
		delAct.triggered.connect(self.delAct_toggled)

		reviewAct = QtWidgets.QAction(self)
		reviewAct.setText(self.tr("Show Hierarchy"))
		reviewAct.triggered.connect(self.reviewAct_toggled)

		menu = QtWidgets.QMenu()
		#menu.addAction(self.tr("Add sub-block"))
		#menu.addAction(self.tr("Delete"))
		menu.addAction(addAct)
		menu.addAction(delAct)
		menu.addAction(reviewAct)

		menu.exec_(self.blockListView.viewport().mapToGlobal(position))

	def addAct_toggled(self):
		text, okPressed = QtWidgets.QInputDialog.getText(self, "New Block", "Block Name", QtWidgets.QLineEdit.Normal, "")
		if okPressed and text != "":
			if self.blockListView.selectedIndexes():
				current_index = self.blockListView.selectedIndexes()[0]
			else:
				current_index = self.blockListModel.index(0,0)

			new_item = QtGui.QStandardItem(text)
			# new_item.setCheckable(True)

			current_item = self.blockListModel.itemFromIndex(current_index)
			current_item.appendRow(new_item)

			self.blockListView.setExpanded(current_index, True)

	def delAct_toggled(self):
		current_index = self.blockListView.currentIndex()
		current_item = self.blockListModel.itemFromIndex(current_index)
		btnPressed = QtWidgets.QMessageBox.question(self, "Delete Object", "Delete '" + current_item.text() + "'?")
		
		if btnPressed == QtWidgets.QMessageBox.Yes:
			parent = current_item.parent()
			parent.removeRow(current_item.row())


	def reviewAct_toggled(self):
		#print(self.blockListView.selectedIndexes())
		#print(self.blockListModel.itemFromIndex(self.blockListView.selectedIndexes()))
		current_index = self.blockListView.currentIndex()
		current_item = self.blockListModel.itemFromIndex(current_index)
		
		hier_list = []
		hier_list.append(current_item.text())
		tmp_item = current_item	

		while tmp_item.parent():
			hier_list.append(tmp_item.parent().text())
			tmp_item = tmp_item.parent()

		hier_list.reverse()
		
		output_text = ""	

		for hier in hier_list:
			index = hier_list.index(hier)
			hier = "--"*index +" " + hier + "\n"
			output_text += hier
		
		QtWidgets.QMessageBox.information(self, "Hierarchy", output_text)
		#popup_msgBox = QtWidgets.QMessageBox.information(self, "Hierarchy", output_text)
		#popup_msgBox = QtWidgets.QMessageBox.information(self, "Hierarchy", output_text, QtWidgets.QMessageBox.Discard)
		#popup_msgBox.setText(output_text)
		#print(popup_msgBox)
### sub function ###

if __name__ == '__main__':

	app = QtWidgets.QApplication([])

	dialog = MyDialog()
	dialog.show()

	app.exec_()
	sys.exit()

