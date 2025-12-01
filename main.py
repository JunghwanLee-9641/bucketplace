import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
import subprocess

import Config.config as config
from TestBase.DeviceSetup import DeviceSetup


DEFAULT_TESTS = config.DEFAULT_TEST_PATHS


def parse_args():
    parser = argparse.ArgumentParser(
        description="오늘의집 QA 과제용: 설치/로그인/홈 진입 시나리오 자동화 실행기 (실제 iOS 기기 전용)"
    )
    parser.add_argument(
        "--tests",
        nargs="+",
        default=DEFAULT_TESTS,
        help="실행할 테스트 파일 경로 목록 (기본: Tests/test_Login.py)",
    )
    parser.add_argument(
        "--udid",
        default=os.environ.get("UDID"),
        help="대상 실기기 UDID (여러 기기 연결 시 필수)",
    )
    parser.add_argument(
        "--device-name",
        default=os.environ.get("DEVICE_NAME"),
        help="테스트에 사용할 기기 이름 라벨 (기본: 연결된 기기명)",
    )
    parser.add_argument(
        "--platform-version",
        default=os.environ.get("PLATFORM_VERSION"),
        help="iOS 버전 문자열 (예: 17.5, 미지정 시 연결된 기기 정보 사용)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", config.APPIUM_BASE_PORT)),
        help=f"Appium 서버 포트 (기본: {config.APPIUM_BASE_PORT})",
    )
    parser.add_argument(
        "--report-dir",
        default=config.DEFAULT_REPORT_DIR,
        help=f"pytest HTML/JUnit 리포트 저장 경로 (기본: {config.DEFAULT_REPORT_DIR})",
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="테스트 실행 전에 requirements.txt 의존성 설치",
    )
    return parser.parse_args()


def ensure_requirements():
    req = Path("requirements.txt")
    print("📦 requirements.txt 설치를 시작합니다...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req)])
    print("✅ 의존성 설치 완료")


def pick_device(args):
    return DeviceSetup.select_physical_device(
        udid=args.udid,
        device_name=args.device_name,
        platform_version=args.platform_version,
        port=args.port,
    )


def ensure_appium_running(port: int):
    if DeviceSetup.check_appium_server(port):
        print(f"✅ Appium 서버가 이미 실행 중입니다. (포트: {port})")
        return
    print(f"🚀 Appium 서버를 시작합니다... (포트: {port})")
    process = DeviceSetup.start_appium(port)
    if not process:
        raise SystemExit("❌ Appium 서버를 시작하지 못했습니다.")


def run_pytest(tests, env, report_dir: Path):
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = report_dir / f"report_{stamp}.html"
    junit_report = report_dir / f"junit_{stamp}.xml"

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        *tests,
        f"--html={html_report}",
        "--self-contained-html",
        f"--junitxml={junit_report}",
        "-v",
    ]

    print(f"▶️ pytest 실행: {' '.join(tests)}")
    subprocess.check_call(cmd, env=env)
    print(f"✅ 테스트 완료: HTML={html_report}, JUnit={junit_report}")


def build_env(device):
    env = os.environ.copy()
    env["DEVICE_IS_SIMULATOR"] = "0"
    env["UDID"] = device["udid"]
    env["DEVICE_NAME"] = device["device"]
    env["PORT"] = str(device["port"])
    if device.get("platform_version"):
        env["PLATFORM_VERSION"] = device["platform_version"]
    return env


def main():
    args = parse_args()

    if args.install_deps:
        ensure_requirements()

    tests = args.tests
    device = pick_device(args)

    print(
        f"\n=== 테스트 대상 기기 ===\n"
        f"- 이름: {device['device']}\n"
        f"- UDID: {device['udid']}\n"
        f"- iOS : {device.get('platform_version') or 'unknown'}\n"
        f"- 포트: {device['port']}\n"
    )

    # Appium 서버 준비
    ensure_appium_running(device["port"])

    # 환경 변수 준비 후 테스트 실행
    env = build_env(device)
    try:
        run_pytest(tests, env, Path(args.report_dir))
    finally:
        # 테스트 종료 후 Appium 프로세스 정리
        DeviceSetup.stop_appium(device["port"])


if __name__ == "__main__":
    main()
