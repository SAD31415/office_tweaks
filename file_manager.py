import os
import shutil
from pathlib import Path
from utils import print_success, print_error, print_warning, print_info, confirm_action


class FileManager:
    def __init__(self, workdir=None):
        if workdir:
            self.current_directory = Path(workdir).resolve()
        else:
            self.current_directory = Path.cwd()

    def get_current_directory(self):
        """Получить текущий рабочий каталог"""
        return self.current_directory

    def change_directory(self, new_path):
        """Сменить рабочий каталог"""
        try:
            if not new_path:
                print_error("Путь не может быть пустым")
                return False

            path = Path(new_path)
            if not path.exists():
                print_error(f"Каталог '{new_path}' не существует")
                return False

            if not path.is_dir():
                print_error(f"'{new_path}' не является каталогом")
                return False

            # Проверка прав доступа
            if not os.access(path, os.R_OK | os.W_OK):
                print_error("Недостаточно прав для доступа к каталогу")
                return False

            self.current_directory = path.resolve()
            print_success(f"Рабочий каталог изменен на: {self.current_directory}")
            return True

        except Exception as e:
            print_error(f"Ошибка при смене каталога: {str(e)}")
            return False

    def list_files_by_extension(self, extensions):
        """Получить список файлов по расширениям"""
        files = []
        for ext in extensions:
            pattern = f"*.{ext.lstrip('.')}"
            files.extend(self.current_directory.glob(pattern))

        # Убираем дубликаты и сортируем
        files = sorted(set(files), key=lambda x: x.name.lower())
        return [f for f in files if f.is_file()]

    def list_pdf_files(self):
        """Список PDF файлов"""
        return self.list_files_by_extension(['pdf'])

    def list_docx_files(self):
        """Список DOCX файлов"""
        return self.list_files_by_extension(['docx'])

    def list_image_files(self):
        """Список изображений"""
        return self.list_files_by_extension(['jpg', 'jpeg', 'png', 'gif'])

    def get_file_size(self, file_path):
        """Получение размера файла в читаемом формате"""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
            return f"{size:.2f} TB"
        except:
            return "unknown size"

    def delete_files_by_pattern(self, pattern_type, pattern, directory=None):
        """Удаление файлов по шаблону"""
        try:
            if directory:
                target_dir = Path(directory)
            else:
                target_dir = self.current_directory

            if not target_dir.exists():
                print_error(f"Каталог '{target_dir}' не существует")
                return False

            files_to_delete = []

            for file_path in target_dir.iterdir():
                if not file_path.is_file():
                    continue

                filename = file_path.name.lower()
                pattern_lower = pattern.lower()

                if pattern_type == 'startswith' and filename.startswith(pattern_lower):
                    files_to_delete.append(file_path)
                elif pattern_type == 'endswith' and filename.endswith(pattern_lower):
                    files_to_delete.append(file_path)
                elif pattern_type == 'contains' and pattern_lower in filename:
                    files_to_delete.append(file_path)
                elif pattern_type == 'extension' and filename.endswith('.' + pattern_lower.lstrip('.')):
                    files_to_delete.append(file_path)

            if not files_to_delete:
                print_info("Файлы, соответствующие критерию, не найдены")
                return False

            return files_to_delete

        except Exception as e:
            print_error(f"Ошибка при поиске файлов: {str(e)}")
            return []

    def execute_deletion(self, files_to_delete):
        """Выполнить удаление файлов"""
        deleted_count = 0
        for file_path in files_to_delete:
            try:
                file_path.unlink()
                print_success(f"Удален: {file_path.name}")
                deleted_count += 1
            except Exception as e:
                print_error(f"Ошибка при удалении {file_path.name}: {str(e)}")

        print_success(f"Удалено файлов: {deleted_count}/{len(files_to_delete)}")
        return deleted_count

    def get_unique_filename(self, original_path):
        """Получить уникальное имя файла"""
        path = Path(original_path)
        if not path.exists():
            return path

        counter = 1
        while True:
            new_name = f"{path.stem}_{counter}{path.suffix}"
            new_path = path.parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1

    def create_backup_folder(self):
        """Создать папку для резервных копий"""
        backup_dir = self.current_directory / "backup"
        backup_dir.mkdir(exist_ok=True)
        return backup_dir

    def validate_path(self, path_str):
        """Проверка существования пути"""
        path = Path(path_str)
        if not path.exists():
            print_error(f"Путь не существует: {path_str}")
            return False
        return True