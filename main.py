"""
간단한 테스트 실행 스크립트
실제 실행: pytest Tests/test_Login.py -v
"""

import sys
import subprocess
import Config.config as config


def main():
    """
    pytest를 사용하여 테스트를 실행합니다.
    
    사용 예시:
        python main.py                          # 모든 테스트 실행
        python main.py Tests/test_Login.py      # 특정 테스트 파일 실행
        python main.py --env Dev                # 서버 환경 지정
    """
    import argparse
    parser = argparse.ArgumentParser(description="테스트 실행")
    parser.add_argument(
        "tests",
        nargs="*",
        default=["Tests/"],
        help="실행할 테스트 경로 (기본: Tests/)"
    )
    parser.add_argument(
        "--env",
        default=config.Test_Server_Env,
        choices=["Dev", "Stage", "Operation"],
        help="서버 환경 설정"
    )
    args = parser.parse_args()
    
    # 서버 환경 설정
    config.Test_Server_Env = args.env
    
    # pytest 실행
    cmd = [sys.executable, "-m", "pytest", *args.tests, "-v"]
    
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
