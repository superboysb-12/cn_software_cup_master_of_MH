import csv
import os
import datetime
from multiprocessing import Pool, Manager, cpu_count, TimeoutError
from util import APK

# 获取当前时间并生成文件名
current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
error_file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + "_errors.csv"


def check_non_empty(*args):
    for string in args:
        if string:
            return True
    return False


apk_folder = "..\\dataset\\test"


def process_apk(apk_info):
    apk_path, dirname = apk_info
    try:
        apk = APK(apk_path)
        name = apk.get_app_name()
        permissions = apk.get_permissions()
        packagename = apk.get_package()
        version = apk.get_androidversion_code()
        signature = apk.get_signature_names()

        if check_non_empty(name, permissions, packagename, version, signature):
            return [name, permissions, packagename, version, signature, dirname], None
    except Exception as e:
        return None, [apk_path, str(e)]

    return None, None


def worker(apk_info):
    return process_apk(apk_info)


def write_to_csv(file_name, rows, encoding):
    with open(file_name, "a", newline='', encoding=encoding, errors='replace') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


def main():
    # 收集所有APK路径
    apk_paths = []
    for dirname in os.listdir(apk_folder):
        path_dir = os.path.join(apk_folder, dirname)
        for apk_name in os.listdir(path_dir):
            apk_path = os.path.join(path_dir, apk_name)
            apk_paths.append((apk_path, dirname))

    manager = Manager()
    results_queue = manager.Queue()
    errors_queue = manager.Queue()

    # 使用多进程池来处理APK文件
    num_workers = cpu_count()  # 使用CPU核心数量
    with Pool(processes=num_workers) as pool:
        results = pool.imap_unordered(worker, apk_paths)

        batch_size = 100
        batch_results = []
        batch_errors = []

        for apk_info in apk_paths:
            try:
                result, error = results.next(timeout=60)  # 设置超时时间为60秒
                if result:
                    batch_results.append(result)
                elif error:
                    batch_errors.append(error)

                if len(batch_results) >= batch_size:
                    write_to_csv(file_name, batch_results, encoding='gbk')
                    batch_results.clear()

                if len(batch_errors) >= batch_size:
                    write_to_csv(error_file_name, batch_errors, encoding='gbk')
                    batch_errors.clear()
            except TimeoutError:
                # 跳过超时任务
                batch_errors.append([apk_info[0], "Processing timeout"])

        # 写入剩余的结果
        if batch_results:
            write_to_csv(file_name, batch_results, encoding='gbk')

        if batch_errors:
            write_to_csv(error_file_name, batch_errors, encoding='gbk')


if __name__ == "__main__":
    # 初始化CSV文件
    with open(file_name, "w", newline='', encoding='gbk') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "permissions", "get_package", "version_name", "signature", "type"])

    with open(error_file_name, "w", newline='', encoding='gbk') as errorfile:
        error_writer = csv.writer(errorfile)
        error_writer.writerow(["apk_path", "error"])

    main()
