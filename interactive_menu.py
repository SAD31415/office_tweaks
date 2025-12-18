import os
from utils import print_success, print_error, print_info, print_warning, validate_number_input, print_banner


class InteractiveMenu:
    def __init__(self, file_manager, converter, image_processor):
        self.file_manager = file_manager
        self.converter = converter
        self.image_processor = image_processor
        self.version = "2.0"

    def display_menu(self):
        """Отображение главного меню"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner(self.version)
        print(f"Текущий каталог: {self.file_manager.get_current_directory()}")
        print(f"{'=' * 50}")
        print("Выберите действие:")
        print("0. Сменить рабочий каталог")
        print("1. Преобразовать PDF в Docx")
        print("2. Преобразовать Docx в PDF")
        print("3. Произвести сжатие изображений")
        print("4. Удалить группу файлов")
        print("5. Выход")
        print(f"{'=' * 50}")

    def change_directory_menu(self):
        """Меню смены рабочего каталога"""
        print_info(f"Текущий каталог: {self.file_manager.get_current_directory()}")
        new_path = input("Введите новый путь к каталогу (или Enter для отмены): ").strip()

        if new_path:
            self.file_manager.change_directory(new_path)
        else:
            print_info("Операция отменена")

        input("\nНажмите Enter для продолжения...")

    def pdf_to_docx_menu(self):
        """Меню конвертации PDF в DOCX"""
        pdf_files = self.file_manager.list_pdf_files()

        if not pdf_files:
            print_info("PDF файлы не найдены в текущем каталоге")
            input("\nНажмите Enter для продолжения...")
            return

        print_info("Список PDF файлов:")
        for i, pdf_file in enumerate(pdf_files, 1):
            size = self.file_manager.get_file_size(pdf_file)
            print(f"  {i}. {pdf_file.name} ({size})")

        print("\nВведите:")
        print("  0 - конвертировать все файлы")
        print("  -1 - отмена")
        print("  номер файла - конвертировать выбранный файл")

        while True:
            choice = input("\nВаш выбор: ").strip()
            valid, result = validate_number_input(choice, -1, len(pdf_files))

            if valid:
                if result == -1:
                    print_info("Операция отменена")
                    break
                elif result == 0:
                    self.converter.convert_all_pdf_to_docx()
                    break
                else:
                    selected_file = pdf_files[result - 1]
                    self.converter.pdf_to_docx(selected_file)
                    break
            else:
                print_error(result)

        input("\nНажмите Enter для продолжения...")

    def docx_to_pdf_menu(self):
        """Меню конвертации DOCX в PDF"""
        docx_files = self.file_manager.list_docx_files()

        if not docx_files:
            print_info("DOCX файлы не найдены в текущем каталоге")
            input("\nНажмите Enter для продолжения...")
            return

        print_info("Список DOCX файлов:")
        for i, docx_file in enumerate(docx_files, 1):
            size = self.file_manager.get_file_size(docx_file)
            print(f"  {i}. {docx_file.name} ({size})")

        print("\nВведите:")
        print("  0 - конвертировать все файлы")
        print("  -1 - отмена")
        print("  номер файла - конвертировать выбранный файл")

        while True:
            choice = input("\nВаш выбор: ").strip()
            valid, result = validate_number_input(choice, -1, len(docx_files))

            if valid:
                if result == -1:
                    print_info("Операция отменена")
                    break
                elif result == 0:
                    self.converter.convert_all_docx_to_pdf()
                    break
                else:
                    selected_file = docx_files[result - 1]
                    self.converter.docx_to_pdf(selected_file)
                    break
            else:
                print_error(result)

        input("\nНажмите Enter для продолжения...")

    def compress_images_menu(self):
        """Меню сжатия изображений"""
        image_files = self.file_manager.list_image_files()

        if not image_files:
            print_info("Изображения не найдены в текущем каталоге")
            input("\nНажмите Enter для продолжения...")
            return

        print_info("Список изображений:")
        for i, image_file in enumerate(image_files, 1):
            size = self.file_manager.get_file_size(image_file)
            print(f"  {i}. {image_file.name} ({size})")

        print("\nВведите:")
        print("  0 - обработать все файлы")
        print("  -1 - отмена")
        print("  номер файла - обработать выбранный файл")

        while True:
            choice = input("\nВаш выбор: ").strip()
            valid, result = validate_number_input(choice, -1, len(image_files))

            if valid:
                if result == -1:
                    print_info("Операция отменена")
                    break
                else:
                    while True:
                        quality_input = input("Введите качество сжатия (1-100, по умолчанию 85): ").strip()
                        if not quality_input:
                            quality = 85
                            break
                        try:
                            quality = int(quality_input)
                            if 1 <= quality <= 100:
                                break
                            else:
                                print_error("Качество должно быть в диапазоне от 1 до 100")
                        except ValueError:
                            print_error("Пожалуйста, введите целое число")

                    if result == 0:
                        self.image_processor.compress_all_images(quality=quality)
                    else:
                        selected_file = image_files[result - 1]
                        self.image_processor.compress_image(selected_file, quality)
                    break
            else:
                print_error(result)

        input("\nНажмите Enter для продолжения...")

    def delete_files_menu(self):
        """Меню удаления файлов"""
        print("Выберите критерий удаления:")
        print("1. Удалить файлы, начинающиеся на...")
        print("2. Удалить файлы, заканчивающиеся на...")
        print("3. Удалить файлы, содержащие...")
        print("4. Удалить файлы по расширению")
        print("5. Отмена")

        while True:
            choice = input("\nВаш выбор: ").strip()
            valid, result = validate_number_input(choice, 1, 5)

            if valid:
                if result == 5:
                    print_info("Операция отменена")
                    break
                else:
                    pattern = input("Введите шаблон для поиска: ").strip()
                    if not pattern:
                        print_error("Шаблон не может быть пустым")
                        continue

                    pattern_types = {
                        1: 'startswith',
                        2: 'endswith',
                        3: 'contains',
                        4: 'extension'
                    }

                    files_to_delete = self.file_manager.delete_files_by_pattern(
                        pattern_types[result], pattern
                    )

                    if files_to_delete:
                        print_info(f"Найдено файлов для удаления: {len(files_to_delete)}")
                        for i, file_path in enumerate(files_to_delete, 1):
                            size = self.file_manager.get_file_size(file_path)
                            print(f"  {i}. {file_path.name} ({size})")

                        from utils import confirm_action
                        if confirm_action("Вы уверены, что хотите удалить эти файлы?"):
                            self.file_manager.execute_deletion(files_to_delete)
                        else:
                            print_info("Удаление отменено")
                    break
            else:
                print_error(result)

        input("\nНажмите Enter для продолжения...")

    def run(self):
        """Главный цикл программы"""
        try:
            while True:
                self.display_menu()
                choice = input("Ваш выбор: ").strip()

                valid, result = validate_number_input(choice, 0, 5)

                if valid:
                    if result == 0:
                        self.change_directory_menu()
                    elif result == 1:
                        self.pdf_to_docx_menu()
                    elif result == 2:
                        self.docx_to_pdf_menu()
                    elif result == 3:
                        self.compress_images_menu()
                    elif result == 4:
                        self.delete_files_menu()
                    elif result == 5:
                        print_success("До свидания!")
                        break
                else:
                    print_error(result)
                    input("\nНажмите Enter для продолжения...")

        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем")
        except Exception as e:
            print_error(f"Критическая ошибка: {str(e)}")
            input("\nНажмите Enter для выхода...")