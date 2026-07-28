"""
Tool registry and schemas for Role 2: Tool & Spec Engineer.

This module defines deterministic, offline-friendly career guidance tools for
"Chatbot Dinh Huong Su Nghiep". Tools return strings so the ReAct app can append
results directly as Observations.
"""

from __future__ import annotations

import json
import sys
import unicodedata
from typing import Any


CAREER_DATABASE: dict[str, dict[str, Any]] = {
    "data analyst": {
        "display_name": "Data Analyst",
        "tasks": [
            "Làm sạch và phân tích dữ liệu kinh doanh",
            "Tạo dashboard, báo cáo và biểu đồ",
            "Đặt câu hỏi dữ liệu để hỗ trợ quyết định",
        ],
        "skills": ["Excel", "SQL", "Python cơ bản", "Data visualization", "Tư duy phân tích", "Giao tiếp với stakeholder"],
        "good_for": ["toán", "logic", "giải quyết vấn đề", "dữ liệu", "kinh doanh", "excel"],
        "watch_out": "Cần kiên nhẫn với dữ liệu bẩn và phải diễn giải kết quả rõ ràng cho người không chuyên.",
        "learning_paths": ["Excel nâng cao", "SQL", "Python/pandas", "Power BI hoặc Tableau", "Thống kê ứng dụng"],
        "portfolio_ideas": ["Dashboard doanh thu mẫu", "Phân tích dữ liệu khảo sát sinh viên", "Báo cáo insight từ dataset công khai"],
        "risk_notes": "Không đảm bảo mức lương hoặc việc làm; cần kiểm chứng bằng dự án thực tế và phản hồi mentor.",
    },
    "software engineer": {
        "display_name": "Software Engineer",
        "tasks": [
            "Thiết kế và xây dựng tính năng phần mềm",
            "Viết, kiểm thử và bảo trì code",
            "Phối hợp với product, design và QA",
        ],
        "skills": ["Lập trình", "Cấu trúc dữ liệu", "Git", "Testing", "Debugging", "Làm việc nhóm"],
        "good_for": ["toán", "logic", "xây dựng sản phẩm", "giải quyết vấn đề", "công nghệ", "lập trình"],
        "watch_out": "Cần học liên tục và chấp nhận debug nhiều lỗi nhỏ trong thời gian dài.",
        "learning_paths": ["Python hoặc JavaScript", "Git/GitHub", "Cấu trúc dữ liệu", "Web/API cơ bản", "Testing"],
        "portfolio_ideas": ["Ứng dụng quản lý việc học", "API quản lý công việc", "Website portfolio có form liên hệ"],
        "risk_notes": "Không nên chọn chỉ vì ngành đang hot; cần thử xây sản phẩm nhỏ để kiểm chứng mức phù hợp.",
    },
    "ux/ui designer": {
        "display_name": "UX/UI Designer",
        "tasks": [
            "Nghiên cứu nhu cầu người dùng",
            "Thiết kế wireframe, prototype và giao diện",
            "Kiểm thử trải nghiệm và cải tiến sản phẩm",
        ],
        "skills": ["Tư duy thiết kế", "Figma", "User research", "Visual design", "Kể chuyện", "Giao tiếp"],
        "good_for": ["vẽ", "kể chuyện", "sáng tạo", "công nghệ", "người dùng", "thẩm mỹ"],
        "watch_out": "Cần cân bằng gu thẩm mỹ với dữ liệu người dùng và mục tiêu kinh doanh.",
        "learning_paths": ["Design principles", "Figma", "UX research", "Prototyping", "Usability testing"],
        "portfolio_ideas": ["Redesign màn hình đăng ký", "Prototype app học tập", "Case study cải thiện trải nghiệm đặt lịch"],
        "risk_notes": "Không kết luận phù hợp tuyệt đối nếu chưa thử research, thiết kế và nhận phản hồi thực tế.",
    },
    "digital marketer": {
        "display_name": "Digital Marketer",
        "tasks": [
            "Lên kế hoạch nội dung và chiến dịch online",
            "Theo dõi chỉ số quảng cáo, SEO hoặc social media",
            "Thử nghiệm thông điệp để cải thiện chuyển đổi",
        ],
        "skills": ["Viết nội dung", "Phân tích chỉ số", "SEO", "Social media", "Thử nghiệm A/B", "Sáng tạo"],
        "good_for": ["viết", "kể chuyện", "sáng tạo", "kinh doanh", "mạng xã hội", "phân tích"],
        "watch_out": "Cần đo lường hiệu quả bằng dữ liệu, không chỉ dựa vào cảm tính sáng tạo.",
        "learning_paths": ["Content marketing", "SEO cơ bản", "Google Analytics", "Social ads", "Copywriting"],
        "portfolio_ideas": ["Kế hoạch nội dung 30 ngày", "Audit SEO website mẫu", "Mini campaign cho câu lạc bộ"],
        "risk_notes": "Kết quả chiến dịch phụ thuộc thị trường, ngân sách và cách triển khai.",
    },
    "ai engineer": {
        "display_name": "AI Engineer",
        "tasks": [
            "Xây dựng pipeline dữ liệu và mô hình ML/AI",
            "Đánh giá chất lượng mô hình",
            "Tích hợp AI vào sản phẩm hoặc quy trình",
        ],
        "skills": ["Python", "Toán", "Machine learning", "Data engineering", "Đánh giá mô hình", "MLOps cơ bản"],
        "good_for": ["toán", "logic", "ai", "dữ liệu", "nghiên cứu", "công nghệ"],
        "watch_out": "Cần nền tảng toán, lập trình và dữ liệu vững; không nên kỳ vọng thành thạo trong thời gian quá ngắn.",
        "learning_paths": ["Python", "Xác suất thống kê", "Machine learning cơ bản", "Deep learning nhập môn", "Triển khai mô hình"],
        "portfolio_ideas": ["Classifier ảnh đơn giản", "Chatbot FAQ có đánh giá", "Dự án dự đoán trên dataset công khai"],
        "risk_notes": "Không đảm bảo lương cao; năng lực thực tế và portfolio quan trọng hơn tên ngành.",
    },
    "business analyst": {
        "display_name": "Business Analyst",
        "tasks": [
            "Thu thập yêu cầu từ stakeholder",
            "Mô hình hóa quy trình và viết tài liệu yêu cầu",
            "Kết nối đội kinh doanh với đội kỹ thuật",
        ],
        "skills": ["Giao tiếp", "Phân tích quy trình", "Viết tài liệu", "SQL cơ bản", "Tư duy sản phẩm", "Đàm phán"],
        "good_for": ["kinh doanh", "giao tiếp", "giải quyết vấn đề", "quy trình", "phân tích", "công nghệ"],
        "watch_out": "Cần kiên nhẫn làm rõ yêu cầu mơ hồ và xử lý khác biệt giữa các bên.",
        "learning_paths": ["Business process modeling", "Requirement writing", "SQL cơ bản", "Agile/Scrum", "Product thinking"],
        "portfolio_ideas": ["Tài liệu yêu cầu cho app đặt phòng", "User story map", "Sơ đồ quy trình đăng ký môn học"],
        "risk_notes": "Không phải vai trò chỉ nói chuyện; cần phân tích chặt và ghi nhận yêu cầu chính xác.",
    },
    "doctor": {
        "display_name": "Bác sĩ / Nhóm ngành chăm sóc sức khỏe",
        "tasks": [
            "Khám, tư vấn và theo dõi sức khỏe người bệnh",
            "Phối hợp với đội ngũ y tế",
            "Học tập chuyên môn và tuân thủ đạo đức nghề nghiệp",
        ],
        "skills": ["Sinh học", "Hóa học", "Giao tiếp đồng cảm", "Kỷ luật học tập", "Chịu áp lực", "Đạo đức nghề nghiệp"],
        "good_for": ["sinh học", "chăm sóc người khác", "y tế", "kỷ luật", "học dài hạn"],
        "watch_out": "Nếu sợ máu, không thích Sinh học hoặc không muốn học dài hạn, cần cân nhắc kỹ và tìm hiểu các vai trò y tế ít tiếp xúc lâm sàng hơn.",
        "learning_paths": ["Sinh học và Hóa học nền tảng", "Tìm hiểu ngành y", "Shadowing hoặc phỏng vấn người trong nghề", "Kỹ năng giao tiếp với bệnh nhân"],
        "portfolio_ideas": ["Bài tìm hiểu hệ thống y tế", "Dự án truyền thông sức khỏe cộng đồng", "Nhật ký shadowing sau khi được cho phép"],
        "risk_notes": "Không dùng tool này để chẩn đoán tâm lý, cam kết trúng tuyển hoặc khẳng định 100% phù hợp.",
    },
}

ALIASES = {
    "data analyst": "data analyst",
    "phan tich du lieu": "data analyst",
    "phân tích dữ liệu": "data analyst",
    "software engineer": "software engineer",
    "lap trinh vien": "software engineer",
    "lập trình viên": "software engineer",
    "ux ui designer": "ux/ui designer",
    "ux/ui designer": "ux/ui designer",
    "thiet ke ux": "ux/ui designer",
    "thiết kế ux": "ux/ui designer",
    "digital marketer": "digital marketer",
    "marketing so": "digital marketer",
    "marketing số": "digital marketer",
    "ai engineer": "ai engineer",
    "ky su ai": "ai engineer",
    "kỹ sư ai": "ai engineer",
    "business analyst": "business analyst",
    "phan tich nghiep vu": "business analyst",
    "phân tích nghiệp vụ": "business analyst",
    "doctor": "doctor",
    "bac si": "doctor",
    "bác sĩ": "doctor",
    "healthcare": "doctor",
    "y te": "doctor",
    "y tế": "doctor",
}

UNSAFE_OR_INJECTION_PATTERNS = [
    "bo qua tat ca quy tac",
    "bỏ qua tất cả quy tắc",
    "ignore all rules",
    "100% phu hop",
    "100% phù hợp",
    "dam bao viec lam",
    "đảm bảo việc làm",
    "luong cao chac chan",
    "lương cao chắc chắn",
]


def _normalize(text: str) -> str:
    text = str(text or "").strip().lower()
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def _json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def _resolve_career_name(career_name: str) -> str | None:
    raw = str(career_name or "").strip()
    if not raw:
        return None
    normalized = _normalize(raw)
    for alias, key in ALIASES.items():
        if _normalize(alias) == normalized or _normalize(alias) in normalized:
            return key
    for key in CAREER_DATABASE:
        if _normalize(key) == normalized or _normalize(key) in normalized:
            return key
    return None


def _contains_unsafe_request(*parts: str) -> bool:
    combined = _normalize(" ".join(str(part or "") for part in parts))
    return any(_normalize(pattern) in combined for pattern in UNSAFE_OR_INJECTION_PATTERNS)


def _has_healthcare_contradiction(*parts: str) -> bool:
    combined = _normalize(" ".join(str(part or "") for part in parts))
    wants_healthcare = any(token in combined for token in ["bac si", "doctor", "y te", "healthcare"])
    has_mismatch = any(token in combined for token in ["so mau", "khong thich sinh", "khong thich sinh hoc"])
    return wants_healthcare and has_mismatch


def match_careers(interests: str, strengths: str = "", constraints: str = "") -> str:
    """
    Rank career options from user interests, strengths and constraints.

    Input schema:
    - interests: required free-text interests or preferred subjects.
    - strengths: optional free-text strengths.
    - constraints: optional constraints or dislikes.

    Output schema:
    JSON string: {"careers":[{"name", "fit_reason", "watch_out", "confidence"}], "notes": str}

    Error behavior:
    Returns "LOI: ..." for missing profile and "CANH_BAO: ..." for unsafe or contradictory requests.

    Side effects: none. The tool is deterministic and uses only local sample data.

    Example:
    match_careers("thích vẽ, kể chuyện và công nghệ", "sáng tạo", "")
    """
    if not str(interests or "").strip() and not str(strengths or "").strip():
        return "LOI: Chưa có đủ thông tin về sở thích hoặc điểm mạnh để gợi ý nghề nghiệp."

    if _contains_unsafe_request(interests, strengths, constraints):
        return "CANH_BAO: Yêu cầu có dấu hiệu ép kết luận tuyệt đối hoặc bỏ qua quy tắc; cần tư vấn bằng ngôn ngữ có điều kiện."

    if _has_healthcare_contradiction(interests, strengths, constraints):
        return "CANH_BAO: Đầu vào có mâu thuẫn với nhóm ngành chăm sóc sức khỏe; cần hỏi thêm trước khi kết luận."

    profile_text = _normalize(" ".join([interests, strengths]))
    constraint_text = _normalize(constraints)
    ranked: list[dict[str, Any]] = []

    for key, career in CAREER_DATABASE.items():
        matches = [term for term in career["good_for"] if _normalize(term) in profile_text]
        constraint_hits = [term for term in career["good_for"] if _normalize(term) in constraint_text]
        score = len(matches) * 2 - len(constraint_hits)
        if score <= 0 and key not in {"ux/ui designer", "data analyst", "software engineer"}:
            continue
        confidence = "cao" if score >= 4 else "trung bình" if score >= 2 else "thấp"
        ranked.append(
            {
                "name": career["display_name"],
                "fit_reason": "Phù hợp với " + (", ".join(matches) if matches else "một số tín hiệu sở thích ban đầu"),
                "watch_out": career["watch_out"],
                "confidence": confidence,
                "score": score,
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    careers = [{k: v for k, v in item.items() if k != "score"} for item in ranked[:3]]
    return _json(
        {
            "careers": careers,
            "notes": "Đây là gợi ý định hướng ban đầu, không phải kết luận chắc chắn về nghề nghiệp tương lai.",
        }
    )


def get_career_profile(career_name: str) -> str:
    """
    Retrieve deterministic profile data for a supported career.

    Input schema:
    - career_name: required career name or common alias, for example "Data Analyst".

    Output schema:
    JSON string with career, tasks, skills, learning_paths, portfolio_ideas and risk_notes.

    Error behavior:
    Returns "LOI: ..." when the career is missing or unsupported.

    Side effects: none.

    Example:
    get_career_profile("Data Analyst")
    """
    key = _resolve_career_name(career_name)
    if key is None:
        return "LOI: Chưa có tên nghề để tra cứu hồ sơ nghề nghiệp."
    if key not in CAREER_DATABASE:
        return f"LOI: Không tìm thấy hồ sơ nghề '{career_name}' trong bộ dữ liệu mẫu."

    career = CAREER_DATABASE[key]
    return _json(
        {
            "career": career["display_name"],
            "tasks": career["tasks"],
            "skills": career["skills"],
            "learning_paths": career["learning_paths"],
            "portfolio_ideas": career["portfolio_ideas"],
            "risk_notes": career["risk_notes"],
        }
    )


def recommend_learning_path(target_career: str, current_skills: str, duration_weeks: int = 8) -> str:
    """
    Produce a bounded learning roadmap from current skills to a target career.

    Input schema:
    - target_career: required supported career name or alias.
    - current_skills: required free-text list of current skills.
    - duration_weeks: optional integer from 1 to 24, default 8.

    Output schema:
    JSON string with target_career, duration_weeks, skill_gaps, weekly_plan and next_action.

    Error behavior:
    Returns "LOI: ..." for missing career/skills, unsupported career or invalid duration.
    Returns "CANH_BAO: ..." for unsafe certainty requests.

    Side effects: none.

    Example:
    recommend_learning_path("Data Analyst", "Excel cơ bản", 8)
    """
    if _contains_unsafe_request(target_career, current_skills):
        return "CANH_BAO: Không thể đảm bảo việc làm, lương hoặc mức độ phù hợp tuyệt đối; chỉ có thể đề xuất lộ trình học tham khảo."

    key = _resolve_career_name(target_career)
    if key is None or key not in CAREER_DATABASE:
        return f"LOI: Không tìm thấy hồ sơ nghề '{target_career}' trong bộ dữ liệu mẫu."

    if not str(current_skills or "").strip():
        return "LOI: Chưa có thông tin kỹ năng hiện tại để lập lộ trình học."

    try:
        weeks = int(duration_weeks)
    except (TypeError, ValueError):
        return f"LOI: Thời lượng học '{duration_weeks}' không hợp lệ; hãy dùng số tuần từ 1 đến 24."

    if weeks <= 0 or weeks > 24:
        return "LOI: Thời lượng học phải nằm trong khoảng 1 đến 24 tuần để lộ trình còn thực tế."

    career = CAREER_DATABASE[key]
    current = _normalize(current_skills)
    skill_gaps = [skill for skill in career["skills"] if _normalize(skill).split()[0] not in current]
    if not skill_gaps:
        skill_gaps = ["Thực hành dự án thực tế", "Nhận phản hồi từ mentor hoặc người trong ngành"]

    themes = career["learning_paths"] + career["portfolio_ideas"]
    weekly_plan = []
    for week in range(1, weeks + 1):
        theme = themes[(week - 1) % len(themes)]
        weekly_plan.append(
            {
                "week": week,
                "focus": theme,
                "output": "Ghi chú học tập hoặc sản phẩm nhỏ có thể đưa vào portfolio.",
            }
        )

    return _json(
        {
            "target_career": career["display_name"],
            "duration_weeks": weeks,
            "current_skills": current_skills,
            "skill_gaps": skill_gaps[:5],
            "weekly_plan": weekly_plan,
            "next_action": "Chọn 1 dự án nhỏ trong tuần đầu và xin phản hồi từ giáo viên, mentor hoặc người đang làm nghề.",
            "safety_note": "Lộ trình này là gợi ý tham khảo, không đảm bảo đầu vào, việc làm hoặc mức lương.",
        }
    )


AVAILABLE_TOOLS = {
    "match_careers": match_careers,
    "get_career_profile": get_career_profile,
    "recommend_learning_path": recommend_learning_path,
}


if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    print(match_careers("thích vẽ, kể chuyện và dùng công nghệ", "sáng tạo", ""))
    print(get_career_profile("Data Analyst"))
    print(recommend_learning_path("Data Analyst", "Excel cơ bản", 8))
