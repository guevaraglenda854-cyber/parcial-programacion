import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt

# ==========================================
# 1. INSPECCIÓN DE DATOS CON PANDAS
# ==========================================
def analizar_datos(file_path):
    print("="*60)
    print("         ANÁLISIS E INSPECCIÓN DE DATOS (PANDAS)")
    print("="*60)
    
    # Carga de datos
    df = pd.read_csv(file_path)
    
    print("\n--- 1. Primeras filas del DataFrame ---")
    print(df.head())
    
    print("\n--- 2. Estructura y Tipos de Datos (info) ---")
    df.info()
    
    print("\n--- 3. Estadísticas Básicas de Variables Numéricas ---")
    print(df.describe())
    
    print("\n--- 4. Conteo de Productos por Sucursal ---")
    print(df['Sucursal'].value_counts())
    
    print("\n--- 5. Valor Total de Inventario por Sucursal (USD) ---")
    df['Valor_Total'] = df['Cantidad_Stock'] * df['Precio_Unitario_USD']
    valor_sucursal = df.groupby('Sucursal')['Valor_Total'].sum()
    print(valor_sucursal)
    print("="*60 + "\n")
    
    return df

# ==========================================
# 2. INTERFAZ GRÁFICA EN PYQT5 CON MATPLOTLIB
# ==========================================
class VentanaInventario(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sistema de Gestión e Inspección de Inventario - UGB")
        self.setGeometry(100, 100, 1100, 700)

        # Layout Principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout_principal = QHBoxLayout(main_widget)

        # Panel Izquierdo: Tabla de Datos
        panel_izquierdo = QVBoxLayout()
        label_tabla = QLabel("<b>Inventario General por Sucursal</b>")
        label_tabla.setStyleSheet("font-size: 14px;")
        panel_izquierdo.addWidget(label_tabla)

        self.tabla = QTableWidget()
        self.cargar_datos_tabla()
        panel_izquierdo.addWidget(self.tabla)

        # Panel Derecho: Gráficos de Matplotlib
        panel_derecho = QVBoxLayout()
        label_graficos = QLabel("<b>Visualización Analítica del Inventario</b>")
        label_graficos.setStyleSheet("font-size: 14px;")
        panel_derecho.addWidget(label_graficos)

        # Matplotlib Figure y Canvas
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 8))
        self.canvas = FigureCanvas(self.figure)
        panel_derecho.addWidget(self.canvas)

        # Botón de actualización
        btn_graficar = QPushButton("Actualizar / Cargar Gráficos")
        btn_graficar.setStyleSheet("background-color: #003366; color: white; padding: 8px; font-weight: bold;")
        btn_graficar.clicked.connect(self.generar_graficos)
        panel_derecho.addWidget(btn_graficar)

        # Agregar paneles al layout principal
        layout_principal.addLayout(panel_izquierdo, stretch=1)
        layout_principal.addLayout(panel_derecho, stretch=1)

        # Generar gráficos al inicio
        self.generar_graficos()

    def cargar_datos_tabla(self):
        self.tabla.setRowCount(len(self.df))
        self.tabla.setColumnCount(len(self.df.columns))
        self.tabla.setHorizontalHeaderLabels(self.df.columns)

        for row in range(len(self.df)):
            for col in range(len(self.df.columns)):
                item = QTableWidgetItem(str(self.df.iloc[row, col]))
                item.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(row, col, item)

        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def generar_graficos(self):
        self.ax1.clear()
        self.ax2.clear()

        # Gráfico 1: Cantidad de Stock Total por Sucursal
        stock_sucursal = self.df.groupby('Sucursal')['Cantidad_Stock'].sum()
        stock_sucursal.plot(kind='bar', ax=self.ax1, color='#1f77b4')
        self.ax1.set_title('Stock Total disponible por Sucursal', fontsize=10, fontweight='bold')
        self.ax1.set_ylabel('Unidades')
        self.ax1.set_xlabel('')
        self.ax1.tick_params(axis='x', rotation=30)
        self.ax1.grid(axis='y', linestyle='--', alpha=0.7)

        # Gráfico 2: Valor del Inventario por Categoría
        self.df['Valor_Total'] = self.df['Cantidad_Stock'] * self.df['Precio_Unitario_USD']
        valor_categoria = self.df.groupby('Categoria')['Valor_Total'].sum()
        valor_categoria.plot(kind='pie', ax=self.ax2, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99'])
        self.ax2.set_title('Distribución Valor ($) de Inventario por Categoría', fontsize=10, fontweight='bold')
        self.ax2.set_ylabel('')

        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    archivo_csv = 'inventario.csv'
    try:
        # 1. Inspección en consola
        df_datos = analizar_datos(archivo_csv)
        
        # 2. Iniciar aplicación GUI
        app = QApplication(sys.argv)
        ventana = VentanaInventario(df_datos)
        ventana.show()
        sys.exit(app.exec_())
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_csv}'. Asegúrate de que esté en la misma carpeta.")