import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import zipfile
import shutil
import re
from smb.SMBConnection import SMBConnection
from Config import config

# NAS 및 SMB 연결 정보
smb_server = config.SMB_SERVER
share_name = config.SHARE_NAME
remote_dir = config.REMOTE_DIR.rstrip("/")
local_folder  = config.LOCAL_FOLDER

# 인증 정보 (필요한 경우 수정)
username = config.USERNAME
password = config.PASSWORD
client_machine_name = config.CLIENT_MACHINE_NAME
server_name = config.SERVER_NAME
version_pattern = re.compile(r"^\d+(?:\.\d+)*$")


def get_human_readable_size(size, decimal_places=2):
    """
    바이트 단위의 입력 값을 사람이 읽기 좋은 크기 단위로 변환하여 문자열로 반환합니다.
    
    예) 1024 -> 1.00 KB, 1048576 -> 1.00 MB
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024
    return f"{size:.{decimal_places}f} PB"

class ProgressWriter:
    """
    다운로드 받은 바이트 수를 누적하면서 진행률을 출력하는 파일 래퍼 클래스입니다.
    
    파일에 데이터를 쓰면서 다운로드된 바이트와 전체 용량 정보를 사람이 보기 좋은
    단위로 출력합니다.
    """
    def __init__(self, file_obj, total_size):
        self.file_obj = file_obj
        self.total_size = total_size
        self.downloaded = 0

    def write(self, data):
        self.file_obj.write(data)
        self.downloaded += len(data)
        self._print_progress()

    def _print_progress(self):
        percent = (self.downloaded / self.total_size) * 100
        downloaded_hr = get_human_readable_size(self.downloaded)
        total_hr = get_human_readable_size(self.total_size)
        progress_line = (f"\r다운로드 중: {downloaded_hr} / {total_hr} "
                         f"({percent:.2f}%)")
        sys.stdout.write(progress_line)
        sys.stdout.flush()

    def flush(self):
        self.file_obj.flush()

    def close(self):
        self.file_obj.close()


def parse_version_tuple(name):
    """'1.0.4' 같은 문자열을 (1,0,4) 튜플로 변환"""
    if not version_pattern.match(name):
        return None
    try:
        return tuple(int(part) for part in name.split("."))
    except ValueError:
        return None


def resolve_latest_ios_dir(conn):
    """
    REMOTE_DIR 하위 버전 폴더 중 가장 큰 버전을 찾아 그 내부 iOS 경로를 반환
    """
    try:
        entries = conn.listPath(share_name, remote_dir)
    except Exception as e:
        print("베이스 디렉토리 목록을 가져오는 중 오류 발생:", e)
        return None

    version_dirs = []
    for entry in entries:
        if not entry.isDirectory or entry.filename in (".", ".."):
            continue
        version_tuple = parse_version_tuple(entry.filename)
        if version_tuple:
            version_dirs.append((version_tuple, entry.filename))

    if not version_dirs:
        print("❌ 버전 디렉토리를 찾을 수 없습니다. NAS 경로를 확인하세요.")
        return None

    latest_version_tuple, latest_dir = max(version_dirs, key=lambda item: item[0])
    latest_dir_path = os.path.join(remote_dir, latest_dir, "iOS").replace("\\", "/")
    print(f"✅ 최신 버전 디렉토리 선택: {latest_dir} (경로: {latest_dir_path})")
    return latest_dir_path


def download_latest_file():

    # SMBConnection 객체 생성 (NTLMv2 사용 권장)
    conn = SMBConnection(username, password, client_machine_name, server_name, use_ntlm_v2=True)
    if not conn.connect(smb_server, 445):
        print("NAS 연결에 실패하였습니다.")
        return

    # 최신 버전의 iOS 디렉토리 확인
    latest_ios_dir = resolve_latest_ios_dir(conn)
    if not latest_ios_dir:
        conn.close()
        return

    try:
        # 원격 디렉토리의 파일 목록 조회
        file_list = conn.listPath(share_name, latest_ios_dir)
    except Exception as e:
        print("디렉토리 목록을 가져오는 중 오류 발생:", e)
        conn.close()
        return

    # 디렉토리 항목과 '.' 및 '..' 제거
    files = [f for f in file_list if not f.isDirectory and f.filename not in (".", "..")]
    if not files:
        print("다운로드할 파일이 없습니다.")
        conn.close()
        return

    valid_extensions = ('.zip', '.app')

    # 시스템 파일 및 유효하지 않은 확장자 제외
    filtered_files = [
        f for f in files
        if f.filename.lower().endswith(valid_extensions) and not f.filename.startswith('.')
    ]

    if not filtered_files:
        print("❌ 유효한 .zip 또는 .app 파일을 찾을 수 없습니다.")
        return False

    # 가장 최근 파일 선택
    latest_file = max(filtered_files, key=lambda f: f.create_time)
    print("다운로드할 최신 파일:", latest_file.filename)

        # 로컬에 저장할 파일 전체 경로 생성
    local_file_path = os.path.join(local_folder, latest_file.filename)
    
    # .zip 파일인 경우
    if latest_file.filename.lower().endswith('.zip'):
        # 다운로드할 .zip 파일의 전체 경로
        zip_download_path = os.path.join(local_folder, latest_file.filename)
        # 동일한 파일이 존재하면, 파일 크기를 비교하여 다운로드를 생략
        if os.path.exists(zip_download_path):
            local_zip_size = os.path.getsize(zip_download_path)
            if local_zip_size == latest_file.file_size:
                print("동일한 .zip 파일이 이미 존재합니다. 다운로드를 생략합니다.")
                conn.close()
                return
        # 동일한 파일이 없거나 크기가 다르면, 로컬 폴더 내의 모든 .zip 파일 삭제
        for f in os.listdir(local_folder):
            if f.lower().endswith('.zip'):
                file_to_delete = os.path.join(local_folder, f)
                os.remove(file_to_delete)
                print(f"기존 zip 파일 삭제: {file_to_delete}")
    else:
        # .zip 파일이 아닌 경우 기존에 'MeditExpress.zip' 파일 삭제 (필요 시)
        base_name = 'MeditExpress'
        zip_path = os.path.join(local_folder, base_name + '.zip')
        if os.path.exists(zip_path):
            os.remove(zip_path)
            print(f"기존 zip 파일 삭제: {zip_path}")

    # 기존 .app 파일 삭제 처리
    app_path = os.path.join(local_folder, 'MeditExpress.app')
    if os.path.exists(app_path):
        if os.path.isdir(app_path):
            shutil.rmtree(app_path)
        else:
            os.remove(app_path)
        print(f"기존 app 파일 삭제: {app_path}")

    if os.path.exists(app_path):
        if os.path.isdir(app_path):
            shutil.rmtree(app_path)
        else:
            os.remove(app_path)
        print(f"기존 app 파일 삭제: {app_path}")

    # 전체 파일 크기 출력 (진행률 계산에 사용)
    total_size = latest_file.file_size
    print(f"전체 파일 크기: {get_human_readable_size(total_size)}")
    
    try:
        with open(local_file_path, "wb") as f:
            progress_writer = ProgressWriter(f, total_size)
            remote_file_path = os.path.join(latest_ios_dir, latest_file.filename).replace("\\", "/")
            conn.retrieveFile(share_name, remote_file_path, progress_writer)
        print("\n파일 다운로드 완료:", local_file_path)
    except Exception as e:
        print("\n파일 다운로드 중 오류 발생:", e)
        conn.close()
        return
    finally:
        conn.close()

    # 다운로드한 파일이 zip 파일일 경우 압축 해제 실행
    if zipfile.is_zipfile(local_file_path):
        try:
            with zipfile.ZipFile(local_file_path, "r") as zip_ref:
                extract_path = local_folder
                zip_ref.extractall(extract_path)
            print(f"압축 해제 완료: {extract_path}")
        except Exception as e:
            print("압축 해제 중 오류 발생:", e)
    else:
        print("다운로드한 파일은 zip 압축 파일이 아닙니다. 압축 해제를 생략합니다.")
