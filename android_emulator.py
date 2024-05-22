import subprocess

# 创建模拟器
def create_emulator(emulator_name = "MyEmulator2",system_image = "system-images;android-30;google_apis;x86_64"):
    cmd = f"avdmanager create avd -n {emulator_name} -k {system_image}"
    subprocess.run(cmd, shell=True)

# 启动模拟器
def start_emulator(emulator_name = "MyEmulator"):
    pass
    #cmd = f"emulator -avd {emulator_name}"
    #subprocess.run(cmd, shell=True)
