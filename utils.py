import os
import sys
import logging
import time
from pathlib import Path
from colorama import init, Fore, Style

# Инициализация colorama для кроссплатформенной работы с цветами
init(autoreset=True)


def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('office_tweaks.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def print_success(message):
    """Вывод успешного сообщения"""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message):
    """Вывод сообщения об ошибке"""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_warning(message):
    """Вывод предупреждения"""
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def print_info(message):
    """Вывод информационного сообщения"""
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")


def print_banner(version):
    """Вывод баннера программы"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{'=' * 50}")
    print(f"=== Office Tweaks v{version} ===")
    print(f"{'=' * 50}")


def validate_number_input(input_str, min_val, max_val):
    """Валидация числового ввода"""
    try:
        number = int(input_str)
        if min_val <= number <= max_val:
            return True, number
        else:
            return False, f"Число должно быть в диапазоне от {min_val} до {max_val}"
    except ValueError:
        return False, "Пожалуйста, введите целое число"


def get_file_size(file_path):
    """Получение размера файла в читаемом формате"""
    try:
        size = os.path.getsize(file_path)
        return get_file_size_from_bytes(size)
    except:
        return "unknown size"


def get_file_size_from_bytes(size_bytes):
    """Получение читаемого формата размера из байтов"""
    try:
        size = size_bytes
        units = ['B', 'KB', 'MB', 'GB']
        unit_index = 0

        while size >= 1024.0 and unit_index < len(units) - 1:
            size /= 1024.0
            unit_index += 1

        return f"{size:.2f} {units[unit_index]}"
    except:
        return "unknown size"


def confirm_action(message):
    """Подтверждение действия пользователем"""
    while True:
        response = input(f"{message} (y/n): ").lower().strip()
        if response in ['y', 'yes', 'д', 'да']:
            return True
        elif response in ['n', 'no', 'н', 'нет']:
            return False
        else:
            print_error("Пожалуйста, введите 'y' или 'n'")


def show_progress(current, total, description="Обработка"):
    """Простой прогресс-бар"""
    percent = (current / total) * 100 if total > 0 else 100
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)

    print(f"\r{description}: |{bar}| {current}/{total} ({percent:.1f}%)", end='', flush=True)

    if current == total:
        print()


def print_summary(success_count, total_count, total_savings=0, total_original_size=0):
    """Вывод сводки обработки"""
    print(f"\n{'=' * 50}")
    print("Сводка обработки:")
    print(f"  Успешно обработано: {success_count}/{total_count}")

    if success_count < total_count:
        print(f"  Не удалось обработать: {total_count - success_count}")

    if total_original_size > 0 and total_savings > 0:
        total_savings_percent = (total_savings / total_original_size) * 100
        print(f"  Общая экономия места: {get_file_size_from_bytes(total_savings)} ({total_savings_percent:.1f}%)")
    print(f"{'=' * 50}")