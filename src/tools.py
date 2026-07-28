"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
"""

from typing import List, Dict, Optional


# ---------------------------------------------------------------------------
# 1. search_careers
# ---------------------------------------------------------------------------
def search_careers(keywords: str, filters: Optional[Dict] = None) -> Dict:
    """
    Tìm kiếm danh sách nghề nghiệp phù hợp với từ khóa/bộ lọc.

    Args:
        keywords: Từ khóa tìm kiếm, vd: "công nghệ thông tin", "thiết kế".
        filters: Dict tùy chọn, vd:
            {
                "industry": "IT",
                "salary_min": 10000000,
                "location": "Hà Nội"
            }

    Returns:
        {
            "careers": [
                {
                    "career_id": "swe_001",
                    "title": "Software Engineer",
                    "description": "...",
                    "avg_salary": "15-30 triệu",
                    "required_skills": ["Python", "Git", "SQL"],
                    "growth_outlook": "Cao"
                },
                ...
            ]
        }
    """
    filters = filters or {}
    # TODO: thay bằng query database/API thật
    return {
        "careers": [
            {
                "career_id": "sample_001",
                "title": f"[Placeholder] Nghề liên quan đến '{keywords}'",
                "description": "Mô tả chi tiết công việc...",
                "avg_salary": "10-20 triệu",
                "required_skills": ["Skill A", "Skill B"],
                "growth_outlook": "Trung bình",
            }
        ]
    }


# ---------------------------------------------------------------------------
# 2. match_careers
# ---------------------------------------------------------------------------
def match_careers(user_profile: Dict, career_list: Optional[List[Dict]] = None) -> Dict:
    """
    So khớp hồ sơ người dùng với danh sách nghề nghiệp, trả về xếp hạng phù hợp.

    Args:
        user_profile: Dict hồ sơ người dùng, vd:
            {
                "skills": ["Python", "giao tiếp"],
                "interests": ["công nghệ", "sáng tạo"],
                "personality_type": "INTJ",
                "education": "Đại học CNTT"
            }
        career_list: Danh sách nghề để so khớp (nếu None, agent tự lấy từ search_careers).

    Returns:
        {
            "ranked_careers": [
                {
                    "title": "Software Engineer",
                    "match_score": 87,
                    "reasoning": "Phù hợp do kỹ năng Python và sở thích công nghệ..."
                },
                ...
            ]
        }
    """
    career_list = career_list or []
    # TODO: thay bằng logic scoring thật (embedding similarity, rule-based, ML model...)
    ranked = []
    for career in career_list:
        ranked.append({
            "title": career.get("title", "Unknown"),
            "match_score": 75,  # placeholder
            "reasoning": "Điểm phù hợp dựa trên kỹ năng và sở thích trùng khớp (placeholder logic)."
        })
    return {"ranked_careers": ranked}


# ---------------------------------------------------------------------------
# 3. get_career_profile
# ---------------------------------------------------------------------------
def get_career_profile(career_id: str) -> Dict:
    """
    Lấy thông tin chi tiết đầy đủ về một nghề nghiệp cụ thể.

    Args:
        career_id: Mã định danh nghề nghiệp, vd: "swe_001".

    Returns:
        {
            "career_id": "swe_001",
            "title": "Software Engineer",
            "description": "Mô tả đầy đủ...",
            "avg_salary": "15-30 triệu",
            "required_skills": ["Python", "Git", "SQL"],
            "career_path": ["Junior Dev", "Senior Dev", "Tech Lead", "CTO"],
            "related_majors": ["Khoa học máy tính", "Kỹ thuật phần mềm"],
            "growth_outlook": "Cao",
            "day_to_day": "Mô tả công việc hàng ngày..."
        }
    """
    # TODO: thay bằng query database thật theo career_id
    return {
        "career_id": career_id,
        "title": "Placeholder Career",
        "description": "Thông tin chi tiết chưa được kết nối database.",
        "avg_salary": "N/A",
        "required_skills": [],
        "career_path": [],
        "related_majors": [],
        "growth_outlook": "N/A",
        "day_to_day": "N/A",
    }


# ---------------------------------------------------------------------------
# 4. recommend_learning_path
# ---------------------------------------------------------------------------
def recommend_learning_path(current_status: Dict, target_career: str, timeframe: Optional[str] = None) -> Dict:
    """
    Đề xuất lộ trình học tập/phát triển kỹ năng để đạt được nghề nghiệp mục tiêu.

    Args:
        current_status: Dict mô tả tình trạng hiện tại, vd:
            {
                "education_level": "THPT",
                "current_skills": ["Excel cơ bản"],
                "experience_years": 0
            }
        target_career: Tên nghề nghiệp mục tiêu, vd: "Data Analyst".
        timeframe: Khung thời gian mong muốn, vd: "1 năm", "2 năm" (tùy chọn).

    Returns:
        {
            "target_career": "Data Analyst",
            "milestones": [
                {
                    "stage": "Tháng 1-3",
                    "action": "Học SQL và Excel nâng cao",
                    "resources": ["Khóa học X", "Sách Y"]
                },
                {
                    "stage": "Tháng 4-6",
                    "action": "Học Python cho phân tích dữ liệu",
                    "resources": ["Khóa học Z"]
                },
                ...
            ],
            "estimated_duration": "6-12 tháng"
        }
    """
    # TODO: thay bằng logic sinh roadmap thật (rule-based hoặc gọi LLM để generate)
    return {
        "target_career": target_career,
        "milestones": [
            {
                "stage": "Giai đoạn 1",
                "action": f"Xây nền tảng kỹ năng cơ bản cho '{target_career}'",
                "resources": ["Khóa học placeholder"],
            },
            {
                "stage": "Giai đoạn 2",
                "action": "Thực hành qua dự án thực tế",
                "resources": ["Portfolio project"],
            },
        ],
        "estimated_duration": timeframe or "6-12 tháng",
    }


# ---------------------------------------------------------------------------
# Danh sách các tool được đăng ký để Agent sử dụng
# ---------------------------------------------------------------------------
AVAILABLE_TOOLS = {
    "search_careers": search_careers,
    "match_careers": match_careers,
    "get_career_profile": get_career_profile,
    "recommend_learning_path": recommend_learning_path,
}