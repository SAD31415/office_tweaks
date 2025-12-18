import os
from pathlib import Path
from utils import print_success, print_error, print_info, show_progress, print_summary


class DocumentConverter:
    def __init__(self, file_manager):
        self.file_manager = file_manager

    def pdf_to_docx(self, pdf_path, output_path=None):
        """Конвертация PDF в DOCX"""
        try:
            from pdf2docx import Converter

            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                print_error(f"Файл не найден: {pdf_path}")
                return False

            if output_path is None:
                output_path = pdf_path.with_suffix('.docx')
            else:
                output_path = Path(output_path)

            # Проверка существования выходного файла
            if output_path.exists():
                output_path = self.file_manager.get_unique_filename(output_path)

            print_info(f"Конвертация: {pdf_path.name} -> {output_path.name}")

            # Конвертация
            cv = Converter(str(pdf_path))
            cv.convert(str(output_path))
            cv.close()

            print_success(f"Конвертация завершена: {output_path.name}")
            return True

        except ImportError:
            print_error("Библиотека pdf2docx не установлена")
            print_info("Установите: pip install pdf2docx")
            return False
        except Exception as e:
            print_error(f"Ошибка конвертации PDF в DOCX: {str(e)}")
            return False

    def docx_to_pdf(self, docx_path, output_path=None):
        """Конвертация DOCX в PDF"""
        try:
            from docx2pdf import convert

            docx_path = Path(docx_path)
            if not docx_path.exists():
                print_error(f"Файл не найден: {docx_path}")
                return False

            if output_path is None:
                output_path = docx_path.with_suffix('.pdf')
            else:
                output_path = Path(output_path)

            # Проверка существования выходного файла
            if output_path.exists():
                output_path = self.file_manager.get_unique_filename(output_path)

            print_info(f"Конвертация: {docx_path.name} -> {output_path.name}")

            # Конвертация
            convert(str(docx_path), str(output_path))

            print_success(f"Конвертация завершена: {output_path.name}")
            return True

        except ImportError:
            print_error("Библиотека docx2pdf не установлена")
            print_info("Установите: pip install docx2pdf")
            print_info("Примечание: для работы требуется установленный Microsoft Word")
            return False
        except Exception as e:
            print_error(f"Ошибка конвертации DOCX в PDF: {str(e)}")
            print_info("Убедитесь, что Microsoft Word установлен и доступен")
            return False

    def convert_all_pdf_to_docx(self, directory=None):
        """Конвертация всех PDF файлов в DOCX"""
        if directory:
            self.file_manager.change_directory(directory)

        pdf_files = self.file_manager.list_pdf_files()
        if not pdf_files:
            print_info("PDF файлы не найдены в текущем каталоге")
            return 0, 0

        print_info(f"Найдено PDF файлов: {len(pdf_files)}")
        success_count = 0

        for i, pdf_file in enumerate(pdf_files, 1):
            show_progress(i, len(pdf_files), "Конвертация PDF -> DOCX")
            if self.pdf_to_docx(pdf_file):
                success_count += 1

        print_summary(success_count, len(pdf_files))
        return success_count, len(pdf_files)

    def convert_all_docx_to_pdf(self, directory=None):
        """Конвертация всех DOCX файлов в PDF"""
        if directory:
            self.file_manager.change_directory(directory)

        docx_files = self.file_manager.list_docx_files()
        if not docx_files:
            print_info("DOCX файлы не найдены в текущем каталоге")
            return 0, 0

        print_info(f"Найдено DOCX файлов: {len(docx_files)}")
        success_count = 0

        for i, docx_file in enumerate(docx_files, 1):
            show_progress(i, len(docx_files), "Конвертация DOCX -> PDF")
            if self.docx_to_pdf(docx_file):
                success_count += 1

        print_summary(success_count, len(docx_files))
        return success_count, len(docx_files)

    def convert_single_pdf_to_docx(self, pdf_path, output_path=None):
        """Конвертация одного PDF файла в DOCX"""
        return self.pdf_to_docx(pdf_path, output_path)

    def convert_single_docx_to_pdf(self, docx_path, output_path=None):
        """Конвертация одного DOCX файла в PDF"""
        return self.docx_to_pdf(docx_path, output_path)