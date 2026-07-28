"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
"""

def match_careers():
    pass
def get_career_profile():
    pass
def recommend_learning_path():
    pass

# Danh sách các tool được đăng ký để Agent sử dụng
AVAILABLE_TOOLS = {
    "match_careers": match_careers,
    "get_career_profile": get_career_profile,
    "recommend_learning_path": recommend_learning_path} 