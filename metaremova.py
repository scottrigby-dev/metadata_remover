from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import sys
import piexif

class ImageMetadataRemover(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Metadata Remover')
        self.setGeometry(100, 100, 600, 400)

        # Widgets
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)  # Now 'Qt' is defined
        self.image_path = None

        self.select_button = QPushButton('Select Image', self)
        self.select_button.clicked.connect(self.show_file_dialog)

        self.rename_label = QLabel('Enter New Name:', self)
        self.rename_lineedit = QLineEdit(self)

        self.remove_metadata_button = QPushButton('Remove Metadata', self)
        self.remove_metadata_button.clicked.connect(self.remove_metadata)

        # Layout
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.image_label)
        v_layout.addWidget(self.select_button)
        v_layout.addWidget(self.rename_label)
        v_layout.addWidget(self.rename_lineedit)
        v_layout.addWidget(self.remove_metadata_button)

        h_layout = QHBoxLayout(self)
        h_layout.addLayout(v_layout)

    def show_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.bmp *.jpeg *.gif)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.image_path = selected_files[0]
                self.show_image()

    def show_image(self):
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap.scaledToWidth(400))

    def remove_metadata(self):
        if self.image_path:
            new_name = self.rename_lineedit.text().strip()

            try:
                image = Image.open(self.image_path)

                # Remove EXIF data (including orientation information)
                exif_data = image.info.get('exif')
                if exif_data:
                    exif_dict = piexif.load(exif_data)
                    exif_dict.pop("thumbnail", None)
                    exif_bytes = piexif.dump(exif_dict)
                    image.info["exif"] = exif_bytes

                # Save the image without metadata and with the new name
                if new_name:
                    output_path = f'{new_name}.jpg'
                else:
                    output_path = 'output_image.jpg'

                image.save(output_path)

                print(f"Metadata removed successfully. Image saved at {output_path}")

            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Please select an image first.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageMetadataRemover()
    window.show()
    sys.exit(app.exec_())
