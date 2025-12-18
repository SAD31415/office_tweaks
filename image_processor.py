import os
from pathlib import Path
from utils import print_success, print_error, print_info, show_progress, print_summary


class ImageProcessor:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.pillow_available = self._check_pillow()

    def _check_pillow(self):
        """Проверка доступности Pillow"""
        try:
            from PIL import Image
            return True
        except ImportError:
            print_error("Pillow не установлен")
            print_info("Установите: pip install Pillow")
            return False

    def compress_image(self, image_path, quality=85, output_dir=None):
        """Сжатие изображения"""
        if not self.pillow_available:
            return False, 0, 0

        try:
            from PIL import Image

            image_path = Path(image_path)
            if not image_path.exists():
                print_error(f"Файл не найден: {image_path}")
                return False, 0, 0

            if output_dir is None:
                output_dir = image_path.parent

            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True)

            output_path = output_dir / f"compressed_{image_path.name}"

            # Проверка существования выходного файла
            if output_path.exists():
                output_path = self.file_manager.get_unique_filename(output_path)

            print_info(f"Сжатие: {image_path.name} (качество: {quality}%)")

            # Открытие и обработка изображения
            with Image.open(image_path) as img:
                original_size = os.path.getsize(image_path)

                # Конвертируем в RGB если нужно (для JPEG)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                # Параметры сохранения в зависимости от формата
                save_kwargs = {'quality': quality, 'optimize': True}
                if image_path.suffix.lower() == '.png':
                    save_kwargs = {'optimize': True}

                # Сохраняем изображение
                img.save(output_path, **save_kwargs)
                new_size = os.path.getsize(output_path)

                # Расчет экономии
                savings = original_size - new_size
                savings_percent = (savings / original_size) * 100 if original_size > 0 else 0

                print_success(f"Сжато успешно. Экономия: {savings_percent:.1f}%")

                return True, savings, savings_percent

        except Exception as e:
            print_error(f"Ошибка сжатия изображения {image_path.name}: {str(e)}")
            return False, 0, 0

    def compress_all_images(self, directory=None, quality=85):
        """Сжатие всех изображений"""
        if not self.pillow_available:
            return 0, 0, 0, 0

        if directory:
            self.file_manager.change_directory(directory)

        image_files = self.file_manager.list_image_files()
        if not image_files:
            print_info("Изображения не найдены в текущем каталоге")
            return 0, 0, 0, 0

        print_info(f"Найдено изображений: {len(image_files)} (качество: {quality}%)")
        success_count = 0
        total_savings = 0
        total_original_size = 0

        for i, image_file in enumerate(image_files, 1):
            show_progress(i, len(image_files), "Сжатие изображений")
            success, savings, percent = self.compress_image(image_file, quality)
            if success:
                success_count += 1
                total_savings += savings
                total_original_size += os.path.getsize(image_file)

        print_summary(success_count, len(image_files), total_savings, total_original_size)
        return success_count, len(image_files), total_savings, total_original_size

    def compress_single_image(self, image_path, quality=85, output_dir=None):
        """Сжатие одного изображения"""
        success, savings, percent = self.compress_image(image_path, quality, output_dir)
        return success