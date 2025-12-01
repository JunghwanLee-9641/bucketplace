import json
import logging
from typing import Optional

import requests


def send_teams_message(webhook_url: str, *, title: Optional[str] = None, text: str) -> bool:
    """
    Microsoft Teams Incoming Webhook 으로 메시지를 전송한다.
    title/text 만으로도 전송 가능하다.
    """
    if not webhook_url:
        logging.warning("Teams Webhook URL 이 설정되지 않아 메시지를 전송하지 않습니다.")
        return False

    payload = {"text": text}
    if title:
        payload["title"] = title

    try:
        response = requests.post(
            webhook_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=10,
        )
        response.raise_for_status()
        logging.info("Teams 에 테스트 결과 메시지를 전송했습니다.")
        return True
    except Exception as exc:
        logging.error("Teams 메시지 전송 실패: %s", exc)
        return False


def send_test_summary_to_teams(
    webhook_url: str,
    *,
    suite: str,
    total: int,
    success: int,
    duration_seconds: float,
    file_results: Optional[list[tuple[str, bool]]] = None,
) -> bool:
    """테스트 요약 메시지를 Teams 로 보낸다."""
    text = (
        f"테스트 스위트 `{suite}` 실행 완료\n"
        f"- 성공: {success}\n"
        f"- 전체: {total}\n"
        f"- 소요 시간: {duration_seconds:.1f}s"
    )
    if file_results:
        detail_lines = [
            f"- {name}: {'✅' if ok else '❌'}"
            for name, ok in file_results
        ]
        detail_text = "\n".join(detail_lines)
        text = f"{text}\n\n테스트 파일 결과:\n{detail_text}"

    return send_teams_message(
        webhook_url,
        title=f"[{suite.upper()}] 테스트 결과",
        text=text,
    )
