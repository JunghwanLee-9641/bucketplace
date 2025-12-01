from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from appium.options.ios import XCUITestOptions

import Config.config as config
from TestBase.AppDownload import download_latest_file
from Pages.page_Login import LoginPage

import re
import xml.etree.ElementTree as ET
import os, subprocess, signal
import time
import requests, json, sys

local_folder = config.LOCAL_FOLDER

class DeviceSetup:
    _appium_ports = {}  # 시뮬레이터별 Appium 포트 저장
    _simulators = {}    # 실행 중인 시뮬레이터 정보 저장
    _appium_processes = {}  # Appium 서버 프로세스 저장
    _artifact_downloaded = False  # NAS에서 앱을 한 번만 내려받도록 제어
    
    def __init__(self, device, port=4723, *, udid=None, is_simulator=True, os_version=None):
        # 환경 변수로부터 device, port 값을 가져오기 (없으면 기본값 사용)
        if not device:
            device = os.environ.get("DEVICE_NAME", "iPhone 15 Pro")
        if not port:
            port = int(os.environ.get("PORT", "4723"))
        if not udid:
            udid = os.environ.get("UDID")
        self.port = port
        self.device = device
        self.udid = udid
        self.is_simulator = is_simulator
        self.os_version = os_version
        self.driver = None
        
        if not DeviceSetup._artifact_downloaded:
            download_latest_file()
            DeviceSetup._artifact_downloaded = True

        # Appium 서버 실행
        if not self.check_appium_server(port):
            print(f"🚀 Appium 서버가 실행되지 않아 시작합니다... (포트: {port})")
            self.start_appium(port)
        else:
            print(f"✅ Appium 서버가 이미 실행 중입니다. (포트: {port})")
        
        # 디바이스 유형에 따라 세션 구성
        if self.is_simulator and os.environ.get("BOOT_SIMULATOR", "true") == "true":
            self.driver = self.start_appium_with_simulator(device)
        elif not self.is_simulator:
            self.driver = self.start_appium_with_real_device()
        
        # 실행 정보 저장
        DeviceSetup._appium_ports[device] = port

    @staticmethod
    def _server_config():
        return getattr(config, "APPIUM_SERVER_CONFIG", {})

    @classmethod
    def _appium_host(cls):
        return cls._server_config().get("host", "127.0.0.1")

    @classmethod
    def _build_server_url(cls, port: int) -> str:
        host = cls._appium_host()
        if host.startswith("http://") or host.startswith("https://"):
            base = host.rstrip("/")
        else:
            base = f"http://{host}"
        if base.endswith(f":{port}"):
            return base
        return f"{base}:{port}"

    @staticmethod    
    def start_appium(port=4723):
        """지정된 포트로 Appium 서버 실행"""
        try:
            # 해당 포트의 이전 프로세스 종료
            DeviceSetup.stop_appium(port)
            time.sleep(2)
            
            # Appium 서버 시작
            server_cfg = DeviceSetup._server_config()
            log_dir = server_cfg.get("log_dir")
            log_path = None
            if log_dir:
                log_dir = os.path.abspath(log_dir)
                os.makedirs(log_dir, exist_ok=True)
                log_path = os.path.join(log_dir, f'appium_{port}.log')
            else:
                log_path = os.path.abspath(f'./logs/appium_{port}.log')
                os.makedirs(os.path.dirname(log_path), exist_ok=True)

            print(f"🚀 Appium 서버 시작 (포트: {port})")
            appium_cmd = [
                'appium',
                '--port', str(port),
                '--log', log_path
            ]
            host = DeviceSetup._appium_host()
            if host:
                address = host
                if address.startswith("http://") or address.startswith("https://"):
                    address = address.split("://", 1)[1]
                address = address.split("/")[0]
                address = address.split(":")[0]
                if address:
                    appium_cmd += ['--address', address]
            if server_cfg.get("log_timestamp", True):
                appium_cmd.append('--log-timestamp')
            if server_cfg.get("local_timezone", True):
                appium_cmd.append('--local-timezone')
            if server_cfg.get("log_level"):
                appium_cmd += ['--log-level', server_cfg['log_level']]
            extra_args = server_cfg.get("extra_args") or []
            if extra_args:
                appium_cmd += extra_args

            process = subprocess.Popen(appium_cmd)
            DeviceSetup._appium_processes[port] = process
            time.sleep(5)  # Appium 서버가 시작될 때까지 대기
            return process
        except Exception as e:
            print(f"❌ Appium 실행 오류 (포트 {port}): {e}")
            return None

    @staticmethod
    def check_appium_server(port=4723):
        """지정된 포트의 Appium 서버가 실행 중인지 확인"""
        try:
            response = requests.get(f"{DeviceSetup._build_server_url(port)}/status", timeout=3)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def stop_appium(port=None):
        """지정된 포트의 Appium 서버 종료"""
        try:
            if port:
                if port in DeviceSetup._appium_processes:
                    process = DeviceSetup._appium_processes[port]
                    process.terminate()
                    process.wait(timeout=5)
                    del DeviceSetup._appium_processes[port]
                subprocess.run(f"kill -9 $(lsof -ti :{port}) || true", shell=True, check=False)
            else:
                # 모든 Appium 서버 종료
                for port, process in DeviceSetup._appium_processes.items():
                    process.terminate()
                    process.wait(timeout=5)
                DeviceSetup._appium_processes.clear()
                DeviceSetup._appium_ports.clear()
        except Exception as e:
            print(f"❌ Appium 종료 오류: {e}")

    @staticmethod
    def wait_for_appium_ready(port, timeout=60):
        start = time.time()
        while time.time() - start < timeout:
            try:
                r = requests.get(f"{DeviceSetup._build_server_url(port)}/status")
                if r.status_code == 200 and r.json().get("value", {}).get("ready"):
                    return True
            except Exception:
                pass
            time.sleep(1)
        return False

    @staticmethod
    def stop_simulator(device=None):
        """지정된 시뮬레이터 또는 모든 시뮬레이터 종료"""
        try:
            if device:
                udid = DeviceSetup.get_udid_from_name(device)
                if udid:
                # 시뮬레이터 상태 확인 using UDID
                    status = subprocess.check_output(['xcrun', 'simctl', 'list', 'devices']).decode()
                if udid in status and 'Booted' in status.split(udid)[1]:
                    subprocess.run(['xcrun', 'simctl', 'shutdown', udid], check=True)
                    print(f"✅ iOS 시뮬레이터가 종료되었습니다: {device}")
                else:
                    print(f"ℹ️ {device} 시뮬레이터가 이미 종료되어 있습니다.")
            else:
                subprocess.run(['xcrun', 'simctl', 'shutdown', 'all'], check=True)
                print("✅ 모든 iOS 시뮬레이터가 종료되었습니다.")
                DeviceSetup._simulators.clear()
        except subprocess.CalledProcessError as e:
            print(f"❌ 시뮬레이터 종료 오류: {e}")
        except Exception as e:
            print(f"❌ 시뮬레이터 종료 중 오류 발생: {e}")

    def rotate_device(self, orientation="LANDSCAPE"):
        """iOS 시뮬레이터를 가로/세로 모드로 변경"""
        if orientation.upper() == "LANDSCAPE":
            self.driver.orientation = "LANDSCAPE"
        else:
            self.driver.orientation = "PORTRAIT"
        time.sleep(5)

    @staticmethod
    def get_udid_from_name(simulator_name):
        """입력한 시뮬레이터 이름에 해당하는 UDID 가져오기"""
        try:
            result = subprocess.run(["xcrun", "simctl", "list", "devices"], capture_output=True, text=True, check=True)
            devices = result.stdout

            # 정규식으로 해당 시뮬레이터 이름과 UDID 추출
            pattern = rf"{re.escape(simulator_name)} \(([\w-]+)\) \(Booted\)|{re.escape(simulator_name)} \(([\w-]+)\) \(Shutdown\)"
            match = re.search(pattern, devices)

            if match:
                udid = match.group(1) or match.group(2)
                print(f"🔍 찾은 시뮬레이터: {simulator_name}, UDID: {udid}")
                return udid
            else:
                print(f"❌ '{simulator_name}'에 해당하는 시뮬레이터를 찾을 수 없습니다.")
                return None
        except subprocess.CalledProcessError as e:
            print(f"❌ UDID 검색 오류: {e}")
            return None
    
    def start_simulator(self, simulator_name):
        
        DeviceSetup.stop_simulator()

        """시뮬레이터 시작"""
        try:
            # 시뮬레이터 UDID 가져오기
            udid = self.get_udid_from_name(simulator_name)
            if not udid:
                print(f"❌ '{simulator_name}' 시뮬레이터를 찾을 수 없습니다.")
                return False

            # 시뮬레이터 상태 확인
            status = subprocess.check_output(['xcrun', 'simctl', 'list', 'devices', simulator_name]).decode()
            if 'Booted' in status:
                print(f"ℹ️ {simulator_name} 시뮬레이터가 이미 실행 중입니다.")
                return True
            
            # 기존 시뮬레이터 종료
            subprocess.run(['xcrun', 'simctl', 'shutdown', udid], check=False)
            time.sleep(2)
            
            # 시뮬레이터 실행
            print(f"🚀 시뮬레이터 실행: {simulator_name}")
            subprocess.run(['xcrun', 'simctl', 'boot', udid], check=True)
            time.sleep(15)  # 시뮬레이터가 완전히 시작될 때까지 대기 시간 증가
            
            # 시뮬레이터 상태 재확인
            status = subprocess.check_output(['xcrun', 'simctl', 'list', 'devices', simulator_name]).decode()
            if 'Booted' in status:
                print(f"✅ {simulator_name} 시뮬레이터가 성공적으로 시작되었습니다.")
                return True
            else:
                print(f"❌ {simulator_name} 시뮬레이터 시작 실패")
                return False
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 시뮬레이터 실행 실패: {e}")
            return False
        except Exception as e:
            print(f"❌ 시뮬레이터 실행 중 오류 발생: {e}")
            return False

    def start_appium_with_simulator(self, simulator_name):
        """시뮬레이터 이름을 받아 해당 UDID로 Appium 실행"""
        if not simulator_name:
            raise ValueError("시뮬레이터 이름이 지정되지 않았습니다.")
            
        udid = self.get_udid_from_name(simulator_name)
        if not udid:
            raise Exception(f"❌ '{simulator_name}'에 해당하는 시뮬레이터 UDID를 찾을 수 없습니다.")

        try:
            # 기존 시뮬레이터 종료
            print(f"🔄 {simulator_name} 시뮬레이터 초기화 중...")
            try:
                subprocess.run(['xcrun', 'simctl', 'shutdown', udid], check=False)
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ 시뮬레이터 종료 중 경고 (무시): {e}")
            
            # 시뮬레이터 초기화
            subprocess.run(['xcrun', 'simctl', 'erase', udid], check=True)
            time.sleep(5)
            
            # WebDriverAgent 설치 및 설정
            print("🔄 WebDriverAgent 설치 중...")
            wda_path = "/usr/local/lib/node_modules/appium/node_modules/appium-webdriveragent"
            
            # WebDriverAgent 빌드 전 정리
            subprocess.run(['rm', '-rf', f'{wda_path}/DerivedData'], check=False)
            subprocess.run(['rm', '-rf', f'{wda_path}/WebDriverAgent.xcodeproj/xcuserdata'], check=False)
            
            # WebDriverAgent 빌드
            build_result = subprocess.run([
                'xcodebuild', '-project', f'{wda_path}/WebDriverAgent.xcodeproj',
                '-scheme', 'WebDriverAgentRunner',
                '-destination', f'id={udid}',
                'clean', 'build', 'test',
                'CODE_SIGN_IDENTITY=""',
                'CODE_SIGNING_REQUIRED=NO',
                'CODE_SIGNING_ALLOWED=NO'
            ], capture_output=True, text=True)
            
            if build_result.returncode != 0:
                print(f"⚠️ WebDriverAgent 빌드 경고: {build_result.stderr}")
                # 빌드 실패 시에도 계속 진행
            
            time.sleep(5)
            
            # 시뮬레이터 시작
            print(f"🚀 {simulator_name} 시뮬레이터 시작 중...")
            subprocess.run(['xcrun', 'simctl', 'boot', udid], check=True)
            time.sleep(15)
            
            # 시뮬레이터 상태 확인
            status = subprocess.check_output(['xcrun', 'simctl', 'list', 'devices', simulator_name]).decode()
            if 'Booted' not in status:
                raise Exception(f"❌ {simulator_name} 시뮬레이터 시작 실패")
            
            # WebDriverAgent 권한 설정
            print("🔄 WebDriverAgent 권한 설정 중...")
            try:
                subprocess.run([
                    'xcrun', 'simctl', 'privacy', udid, 'grant', 'all',
                    'com.facebook.WebDriverAgentRunner.xctrunner'
                ], check=True)
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ WebDriverAgent 권한 설정 중 경고 (무시): {e}")
            
            # 앱 설치
            if not self.install_app_to_simulator(udid):
                raise Exception("❌ 앱 설치 실패: 시뮬레이터에 앱을 설치할 수 없습니다.")
            
            # Appium 설정
            options = XCUITestOptions()
            capabilities = config.SIMULATOR_CAPABILITIES.copy()
            capabilities.update(getattr(config, "SIMULATOR_SESSION_CAPABILITIES", {}))
            capabilities["appium:udid"] = udid
            capabilities["appium:wdaLocalPort"] = int(self.port) + 100
            capabilities.setdefault(
                "appium:derivedDataPath",
                os.path.expanduser("~/Library/Developer/Xcode/DerivedData/WebDriverAgent")
            )
            
            options.load_capabilities(capabilities)
            
            # Appium 서버 시작
            if not self.check_appium_server(self.port):
                self.start_appium(self.port)
                time.sleep(5)
            
            # Appium 드라이버 초기화
            print(f"🔄 Appium 드라이버 초기화 중... (포트: {self.port})")
            self.driver = webdriver.Remote(self._build_server_url(self.port), options=options)
            print(f"✅ Appium 연결 성공 (포트: {self.port})")
            time.sleep(15)
            
            # 화면 회전
            try:
                self.rotate_device("LANDSCAPE")
            except Exception as e:
                print("⚠️ 화면 회전 명령 실행 중 경고 (무시):", e)
            
            return self.driver
            
        except Exception as e:
            print(f"❌ {simulator_name} 설정 중 오류 발생: {e}")
            # 오류 발생 시 시뮬레이터 정리
            self.stop_simulator(simulator_name)
            self.stop_appium(self.port)
            raise

    def start_appium_with_real_device(self):
        """실제 iOS 기기에서 Appium 세션을 시작"""
        if not self.udid:
            raise ValueError("실제 기기 연결을 위해 UDID가 필요합니다.")

        capabilities = config.REAL_DEVICE_CAPABILITIES.copy()
        capabilities["appium:udid"] = self.udid or capabilities.get("appium:udid")
        capabilities["appium:deviceName"] = self.device or capabilities.get("appium:deviceName") or "iOS Device"

        platform_version = self.os_version or os.environ.get("PLATFORM_VERSION") or capabilities.get("appium:platformVersion")
        if platform_version:
            capabilities["appium:platformVersion"] = platform_version

        if not capabilities.get("appium:udid"):
            raise ValueError("실제 기기 UDID가 설정되지 않았습니다.")

        # 각 디바이스별 고유 WDA 포트 설정
        capabilities.setdefault("appium:wdaLocalPort", int(self.port) + 100)

        # 앱 경로나 번들 ID 설정
        if config.REAL_DEVICE_APP_PATH:
            capabilities["appium:app"] = config.REAL_DEVICE_APP_PATH
        else:
            # 앱 설치 없이 실행할 경우 bundleId 만으로 세션 유지
            capabilities["appium:bundleId"] = capabilities.get("appium:bundleId", "com.medit.m-express")

        options = XCUITestOptions()
        options.load_capabilities(capabilities)

        if not self.check_appium_server(self.port):
            self.start_appium(self.port)
            time.sleep(5)

        print(f"🔄 실제 기기와 Appium 세션 초기화 중... (기기: {self.device}, UDID: {self.udid}, 포트: {self.port})")
        self.driver = webdriver.Remote(self._build_server_url(self.port), options=options)
        print(f"✅ 실제 기기 연결 성공 (포트: {self.port})")
        time.sleep(5)
        return self.driver

    
    
    def install_app_to_simulator(self,simulator_udid):
        """
        다운로드 받은 MeditExpress.app 파일을 시뮬레이터에 설치합니다.
        simulator_udid: 시뮬레이터의 UDID (문자열)
        """
        app_path = os.path.join(local_folder, config.APP_NAME)
        if not os.path.exists(app_path):
            print(f"앱 파일이 존재하지 않습니다: {app_path}")
            return False
        
        # Retrieve bundle id from config, defaulting if not provided
        bundle_id = config.SIMULATOR_CAPABILITIES.get("appium:bundleId", "com.medit.m-express")
        
        try:
            # Attempt to uninstall the app if it's already installed
            print(f"기존에 설치된 앱이 있으면 삭제합니다: {bundle_id}")
            subprocess.run([
                "xcrun", "simctl", "uninstall", simulator_udid, bundle_id
            ], capture_output=True, text=True, check=True)
            print("기존 앱 삭제 성공")
        except subprocess.CalledProcessError as e:
            # If uninstall fails, it might be because the app is not installed; ignore the error
            print(f"앱 삭제 시도 중 오류 발생 (앱이 설치되어 있지 않을 수 있음): {e.stderr}")
        
        try:
            print(f"앱 설치 시작: {app_path} -> {simulator_udid}")
            # xcrun simctl install 명령어로 시뮬레이터에 앱 설치
            result = subprocess.run(
                ["xcrun", "simctl", "install", simulator_udid, app_path],
                capture_output=True, text=True, check=True
            )
            print("앱 설치 완료:", result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print("앱 설치 중 오류 발생:", e.stderr)
            return False

    @staticmethod
    def get_available_simulators():
        """Return a list of available simulators."""
        try:
            output = subprocess.check_output(['xcrun', 'simctl', 'list', 'devices', 'available', '-j'], text=True)
            devices_json = json.loads(output)
            simulators = []

            for runtime_group, devices in devices_json["devices"].items():
                # macOS, watchOS 등 비 iOS 런타임은 제외
                if "iOS" not in runtime_group:
                    continue
                for device in devices:
                    if device["isAvailable"]:
                        name = device.get("name", "")
                        # iOS 시뮬레이터만 사용하며 'My Mac' 항목은 제외
                        if name.lower() == "my mac":
                            continue
                        simulators.append({
                            "group": runtime_group,
                            "device": name,
                            "udid": device.get("udid"),
                            "is_simulator": True
                        })
            return DeviceSetup.assign_ports(simulators)
        except Exception as e:
            print(f"Error parsing available simulators: {e}")
            return []

    @staticmethod
    def get_connected_ios_devices():
        """연결된 실제 iOS 기기 목록을 반환"""
        try:
            result = subprocess.run(
                ['xcrun', 'xcdevice', 'list', '--json'],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            devices = json.loads(result.stdout)
        except FileNotFoundError:
            print("⚠️ 'xcrun xcdevice' 명령을 찾을 수 없습니다. Xcode Command Line Tools 설치 상태를 확인하세요.")
            return []
        except subprocess.CalledProcessError as e:
            print(f"⚠️ 실제 기기 목록 조회 실패: {e.stderr or e}")
            return []
        except json.JSONDecodeError:
            print("⚠️ 실제 기기 목록 파싱 중 오류가 발생했습니다.")
            return []
        except subprocess.TimeoutExpired:
            print("⚠️ 실제 기기 목록 조회가 시간 초과되었습니다.")
            return []

        physical_devices = []
        for device in devices:
            if device.get("simulator", False):
                continue
            if not device.get("available", False):
                continue

            name = device.get("name") or device.get("modelName") or "iOS Device"
            platform = (device.get("platform") or device.get("platformIdentifier") or "").lower()
            if "mac" in name.lower():
                continue
            if platform and not any(keyword in platform for keyword in ("ios", "iphone", "ipad")):
                continue
            udid = (
                device.get("identifier")
                or device.get("serialNumber")
                or device.get("udid")
            )
            if not udid:
                continue

            os_version = (
                device.get("operatingSystemVersion")
                or device.get("osVersion")
                or device.get("iosVersion")
            )

            physical_devices.append({
                "group": "physical",
                "device": name,
                "udid": udid,
                "os_version": os_version,
                "is_simulator": False
            })

        return DeviceSetup.assign_ports(physical_devices, start_port=config.DEFAULT_BASE_PORT + config.PORT_INCREMENT * config.MAX_SIMULATORS)

    @staticmethod
    def assign_ports(devices, start_port=None):
        """디바이스 목록에 Appium 포트를 순차적으로 할당"""
        if start_port is None:
            start_port = config.DEFAULT_BASE_PORT

        for idx, device in enumerate(devices):
            device["port"] = start_port + idx * config.PORT_INCREMENT
        return devices

    @staticmethod
    def setup_simulator(simulator_name):
        """Setup simulator by starting it."""
        success = DeviceSetup.start_simulator(simulator_name)
        if success:
            print(f"Simulator {simulator_name} setup successfully.")
        else:
            print(f"Failed to setup simulator {simulator_name}.")
        return success

    @staticmethod
    def run_device_tests(target, test_files, repeat_count=1):
        """
        디바이스(시뮬레이터/실제 기기)에서 테스트를 실행합니다.
        반복 횟수는 repeat_count 인자 또는 REPEAT_COUNT 환경 변수로 제어합니다.
        """
        report_dir = DeviceSetup.create_report_dir(f"{target['group']}_{target['device']}")
        is_simulator = target.get("is_simulator", True)
        device_setup = None

        try:
            os.environ["BOOT_SIMULATOR"] = "true" if is_simulator else "false"
            device_setup = DeviceSetup(
                target['device'],
                target['port'],
                udid=target.get("udid"),
                is_simulator=is_simulator,
                os_version=target.get("os_version")
            )
            if not test_files:
                print(f"⚠️ 테스트 파일이 비어 있습니다. 기본 테스트 경로 './Tests'를 사용합니다.")
                test_files = ['./Tests']

            device_label = "시뮬레이터" if is_simulator else "실제 기기"
            print(f"\n🔄 {target['device']} {device_label} 테스트 시작")
            if not DeviceSetup.wait_for_appium_ready(target['port']):
                print(f"❌ Appium 서버가 준비되지 않았습니다. 포트: {target['port']}")
                return False

            repeat_count_env = int(os.environ.get("REPEAT_COUNT", str(repeat_count)))
            final_results = []
            overall_ok = True
            for i in range(repeat_count_env):
                print(f"🔁 테스트 반복 실행 {i + 1}/{repeat_count_env}")
                file_results = DeviceSetup.run_tests_for_device(target, test_files)
                final_results.extend(file_results)
                iteration_ok = all(ok for _, ok in file_results)
                if not iteration_ok:
                    print(f"❌ 반복 {i + 1}에서 실패하여 중단")
                    overall_ok = False
                    break

            if overall_ok:
                print(f"✅ {target['device']} 테스트 완료")
            else:
                print(f"❌ {target['device']} 테스트 실패")

            time.sleep(10)
            return overall_ok, final_results

        except Exception as e:
            print(f"❌ {target['device']} 실행 중 오류 발생: {e}")
            return False

        finally:
            # 테스트 세션 종료 후 드라이버 종료
            if device_setup and getattr(device_setup, "driver", None):
                try:
                    device_setup.driver.quit()
                except Exception:
                    pass

    @staticmethod
    def run_simulator_tests(simulator, test_files, repeat_count=1):
        """기존 메서드와의 호환성을 위한 래퍼"""
        return DeviceSetup.run_device_tests(simulator, test_files, repeat_count)

    @staticmethod
    def run_tests_for_device(sim, test_files):
        """주어진 시뮬레이터에서 테스트 실행. 파일별 성공 여부 리스트 반환"""
        env = os.environ.copy()
        env["DEVICE_NAME"] = sim["device"]
        env["PORT"] = str(sim["port"])
        env["DEVICE_IS_SIMULATOR"] = "1" if sim.get("is_simulator", True) else "0"
        if sim.get("udid"):
            env["UDID"] = sim["udid"]
        if sim.get("os_version"):
            env["PLATFORM_VERSION"] = sim["os_version"]

        report_dir = DeviceSetup.create_report_dir()

        import re
        safe_device_name = re.sub(r'[^\w\-_\. ]', '_', sim["device"])
        # test_files에는 여러 개가 들어올 수 있으므로 리스트로 정규화한다.
        if not test_files:
            tests_to_run = ['./Tests']
        elif isinstance(test_files, (str, os.PathLike)):
            tests_to_run = [str(test_files)]
        else:
            tests_to_run = [str(path) for path in test_files]

        tests_to_run = sorted(tests_to_run)
        html_report = os.path.join(
            report_dir,
            f"report_{safe_device_name}.html"
        )
        junit_report = os.path.join(
            report_dir,
            f"junit_{safe_device_name}.xml"
        )

        print(f"▶️ {sim['device']}에서 테스트 실행: {' '.join(tests_to_run)}")
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    *tests_to_run,
                    f"--html={html_report}",
                    "--self-contained-html",
                    f"--junitxml={junit_report}",
                    "-v",
                ],
                env=env,
                check=True,
            )
            ok = True
        except subprocess.CalledProcessError:
            print(f"❌ 테스트 실패: {' '.join(tests_to_run)}")
            ok = False

        file_status = {path: ok for path in tests_to_run}
        if os.path.exists(junit_report):
            try:
                tree = ET.parse(junit_report)
                root = tree.getroot()
                per_file = {}
                for tc in root.iter("testcase"):
                    file_attr = tc.get("file")
                    if not file_attr:
                        continue
                    tc_ok = True
                    for child in tc:
                        if child.tag in ("failure", "error"):
                            tc_ok = False
                            break
                    per_file[file_attr] = per_file.get(file_attr, True) and tc_ok
                if per_file:
                    file_status.update(per_file)
            except Exception as exc:
                print(f"⚠️ JUnit 파싱 실패: {exc}")

        results = [(path, file_status.get(path, ok)) for path in tests_to_run]
        return results
    
    @staticmethod
    def create_report_dir(report_name="Report"):
        """Create a directory for test reports at meditExpress/Report"""
        # 현재 파일(DeviceSetup.py)의 위치를 기준으로 meditExpress 폴더 경로 계산
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # meditExpress
        report_dir = os.path.join(base_dir, report_name)

        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
            print(f"📂 Report directory created: {report_dir}")
        else:
            print(f"ℹ️ Report directory already exists: {report_dir}")
        return report_dir
    
    @staticmethod
    def cleanup_resources():
        """프로그램 종료 시 모든 리소스 정리"""
        print("\n리소스 정리 중...")
        DeviceSetup.stop_appium()
        DeviceSetup.stop_simulator()
