class INSERT():
	def inserisci(self):
		try:
			import psycopg2
		except ImportError, e:
			QMessageBox.information(self.iface.mainWindow(), "hey", "Couldn't import Python module 'psycopg2' for communication with PostgreSQL database. Without it you won't be able to run PostGIS manager.")
			return