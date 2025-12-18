#!/usr/bin/env python3
"""
Office_Tweaks - Утилита для работы с документами и изображениями
"""

import os
import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import setup_logging, print_success, print_error, print_info, print_banner
from file_manager import FileManager
from converter import DocumentConverter
from image_processor import ImageProcessor
from cli_parser import CLIParser
from interactive_menu import InteractiveMenu
import logging


class OfficeTweaks:
    def __init__(self):
        setup_logging()
        self.version = "2.0"
        self.file_manager = None
        self.converter = None
        self.image_processor = None
        self.cli_parser = CLIParser()

        logging.info(f"Office_Tweaks v{self.version} запущен")

    def run_batch_mode(self, args):
        """Запуск пакетного режима"""
        print_banner(self.version)
        print_info("Пакетный режим обработки\n")

        # Инициализация менеджера файлов
        workdir = args.workdir if args.workdir else None
        self.file_manager = FileManager(workdir)

        print_info(f"Рабочий каталог: {self.file_manager.get_current_directory()}")

        # Инициализация обработчиков
        self.converter = DocumentConverter(self.file_manager)
        self.image_processor = ImageProcessor(self.file_manager)

        # Обработка операций
        if args.pdf2docx:
            self._handle_pdf2docx(args)
        elif args.docx2pdf:
            self._handle_docx2pdf(args)
        elif args.compress_images:
            self._handle_compress_images(args)
        elif args.delete:
            self._handle_delete(args)

    def _handle_pdf2docx(self, args):
        """Обработка конвертации PDF в DOCX"""
        if args.pdf2docx.lower() == 'all':
            print_info("Конвертация всех PDF файлов в DOCX...")
            success, total = self.converter.convert_all_pdf_to_docx(args.workdir)
            if success > 0:
                print_success(f"Успешно сконвертировано {success} из {total} файлов")
        else:
            print_info(f"Конвертация файла: {args.pdf2docx}")
            success = self.converter.convert_single_pdf_to_docx(args.pdf2docx, args.output)
            if success:
                print_success("Конвертация завершена успешно")

    def _handle_docx2pdf(self, args):
        """Обработка конвертации DOCX в PDF"""
        if args.docx2pdf.lower() == 'all':
            print_info("Конвертация всех DOCX файлов в PDF...")
            success, total = self.converter.convert_all_docx_to_pdf(args.workdir)
            if success > 0:
                print_success(f"Успешно сконвертировано {success} из {total} файлов")
        else:
            print_info(f"Конвертация файла: {args.docx2pdf}")
            success = self.converter.convert_single_docx_to_pdf(args.docx2pdf, args.output)
            if success:
                print_success("Конвертация завершена успешно")

    def _handle_compress_images(self, args):
        """Обработка сжатия изображений"""
        if not self.image_processor.pillow_available:
            print_error("Невозможно выполнить сжатие: Pillow не установлен")
            return

        if args.compress_images.lower() == 'all':
            print_info(f"Сжатие всех изображений (качество: {args.quality}%)...")
            success, total, savings, original = self.image_processor.compress_all_images(
                args.workdir, args.quality
            )
            if success > 0:
                print_success(f"Успешно сжато {success} из {total} изображений")
        else:
            print_info(f"Сжатие файла: {args.compress_images} (качество: {args.quality}%)")
            success = self.image_processor.compress_single_image(
                args.compress_images, args.quality, args.workdir
            )
            if success:
                print_success("Сжатие завершено успешно")

    def _handle_delete(self, args):
        """Обработка удаления файлов"""
        delete_dir = args.delete_dir if args.delete_dir else args.workdir
        if not delete_dir:
            delete_dir = self.file_manager.get_current_directory()

        print_info(f"Удаление файлов в каталоге: {delete_dir}")
        print_info(f"Режим: {args.delete_mode}, Шаблон: {args.delete_pattern}")

        files_to_delete = self.file_manager.delete_files_by_pattern(
            args.delete_mode, args.delete_pattern, delete_dir
        )

        if files_to_delete:
            print_info(f"Найдено файлов для удаления: {len(files_to_delete)}")
            for i, file_path in enumerate(files_to_delete, 1):
                size = self.file_manager.get_file_size(file_path)
                print(f"  {i}. {file_path.name} ({size})")

            from utils import confirm_action
            if confirm_action("Вы уверены, что хотите удалить эти файлы?"):
                deleted_count = self.file_manager.execute_deletion(files_to_delete)
                print_success(f"Удалено файлов: {deleted_count}/{len(files_to_delete)}")
            else:
                print_info("Удаление отменено")
        else:
            print_info("Файлы, соответствующие критерию, не найдены")

    def run_interactive_mode(self):
        """Запуск интерактивного режима"""
        # Инициализация компонентов
        self.file_manager = FileManager()
        self.converter = DocumentConverter(self.file_manager)
        self.image_processor = ImageProcessor(self.file_manager)

        # Запуск меню
        menu = InteractiveMenu(self.file_manager, self.converter, self.image_processor)
        menu.run()

    def run(self):
        """Главная точка входа"""
        try:
            # Парсинг аргументов
            args = self.cli_parser.parse_args()

            # Определение режима работы
            mode = self.cli_parser.get_operation_mode(args)

            if mode == 'interactive':
                self.run_interactive_mode()
            else:
                self.run_batch_mode(args)

        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем")
            logging.info("Программа прервана пользователем (Ctrl+C)")
        except SystemExit:
            # Игнорируем SystemExit от argparse
            pass
        except Exception as e:
            print_error(f"Критическая ошибка: {str(e)}")
            logging.error(f"Критическая ошибка: {str(e)}")
            sys.exit(1)


def main():
    """Точка входа в программу"""
    app = OfficeTweaks()
    app.run()


if __name__ == "__main__":
    main()