import streamlit as st
from datetime import datetime
import json
import os
import html
import hashlib

# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Order & Bill Trà Sữa",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "menu_data.json"
ORDER_HISTORY_FILE = "order_history.json"


# ============================================================
# CẤU HÌNH ADMIN
# ============================================================
#
# Ưu tiên lấy mật khẩu từ Streamlit Secrets.
#
# Khi deploy Streamlit Cloud:
#
# [admin]
# username = "admin"
# password = "123456"
#
# Nếu chưa cấu hình Secrets:
# Username mặc định: admin
# Password mặc định: 123456
#
# ============================================================

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "123456"


def get_admin_username():
    try:
        return st.secrets["admin"]["username"]
    except Exception:
        return DEFAULT_ADMIN_USERNAME


def get_admin_password():
    try:
        return st.secrets["admin"]["password"]
    except Exception:
        return DEFAULT_ADMIN_PASSWORD


ADMIN_USERNAME = get_admin_username()
ADMIN_PASSWORD = get_admin_password()


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
/* =========================================================
   VIBRANT BERRY & PASSION — CUTE / GEN Z
   Primary: #E11D48
   Secondary: #881337
   Background: #FFF1F2
   Surface: #FFFFFF
   Text Primary: #111827
   Text Secondary: #6B7280
   ========================================================= */

:root {
    --berry: #E11D48;
    --berry-dark: #881337;
    --berry-soft: #FFF1F2;
    --berry-light: #FFE4E6;
    --berry-border: #FECDD3;
    --surface: #FFFFFF;
    --text: #111827;
    --muted: #6B7280;
}

.stApp {
    background: linear-gradient(135deg, #FFF1F2 0%, #FFF8F9 45%, #FFE4E6 100%);
    color: var(--text);
}

.main {
    background: transparent;
}

.block-container {
    max-width: 1380px;
    padding-top: 1.25rem;
    padding-bottom: 3.5rem;
}

/* Tăng độ rõ của chữ */
h1, h2, h3, h4, h5, h6 {
    color: var(--text) !important;
    font-weight: 850 !important;
}

h1 {
    text-align: center;
    font-size: 2.35rem !important;
    letter-spacing: -0.7px;
}

h2, h3 {
    color: var(--berry-dark) !important;
}

p, label, .stMarkdown, .stCaption {
    color: var(--muted);
}

/* HEADER */
.app-header {
    background: rgba(255,255,255,.96);
    border: 1px solid var(--berry-border);
    border-left: 7px solid var(--berry);
    border-radius: 22px;
    padding: 22px 26px;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px rgba(136,19,55,.08);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #881337 0%, #9F1239 48%, #4C0519 100%);
    border-right: 1px solid #BE123C;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,.09);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 14px;
    padding: 9px 11px;
    margin: 4px 0;
    transition: .15s ease;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(225,29,72,.55);
    transform: translateX(2px);
}

/* CUTE ICON / BADGE */
.cute-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 14px;
    background: linear-gradient(135deg, #FFE4E6, #FFF1F2);
    border: 1px solid #FECDD3;
    box-shadow: 0 5px 12px rgba(225,29,72,.12);
    font-size: 24px;
    vertical-align: middle;
    margin-right: 9px;
}

.cute-title {
    display: flex;
    align-items: center;
    color: var(--berry-dark);
    font-size: 22px;
    font-weight: 900;
    margin-bottom: 5px;
}

.cute-subtitle {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.6;
}

/* ORDER BUILDER */
.order-builder {
    background: rgba(255,255,255,.97);
    border: 1px solid var(--berry-border);
    border-top: 5px solid var(--berry);
    border-radius: 20px;
    padding: 22px;
    margin: 12px 0 20px;
    box-shadow: 0 10px 28px rgba(136,19,55,.08);
}

.builder-title {
    color: var(--berry-dark);
    font-size: 21px;
    font-weight: 900;
}

.item-config-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF8F9 100%);
    border: 1px solid var(--berry-border);
    border-left: 5px solid var(--berry);
    border-radius: 18px;
    padding: 16px;
    margin: 13px 0 4px;
    box-shadow: 0 6px 18px rgba(225,29,72,.07);
}

.item-config-title {
    color: var(--text);
    font-weight: 900;
    font-size: 18px;
}

/* ORDER CARDS */
.order-card, .menu-card {
    background: var(--surface);
    color: var(--text);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid var(--berry-border);
    margin-bottom: 14px;
    box-shadow: 0 6px 20px rgba(17,24,39,.06);
}

.order-card:hover, .menu-card:hover {
    border-color: #FB7185;
    box-shadow: 0 9px 24px rgba(225,29,72,.11);
}

.order-title {
    font-size: 19px;
    font-weight: 900;
    color: var(--berry-dark);
    margin-bottom: 8px;
}

.order-detail {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.9;
}

.order-detail b { color: var(--text); }

/* TOTAL */
.total-box {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF1F2 100%);
    padding: 23px;
    border-radius: 20px;
    border: 2px solid var(--berry);
    text-align: center;
    margin-top: 18px;
    box-shadow: 0 9px 25px rgba(225,29,72,.12);
}

.total-money {
    font-size: 32px;
    font-weight: 950;
    color: var(--berry);
    margin: 6px 0;
}

/* PRICE + BADGES */
.price-text {
    color: var(--berry);
    font-size: 18px;
    font-weight: 900;
}

.badge-blue {
    display: inline-block;
    background: #FFE4E6;
    color: #9F1239 !important;
    border: 1px solid #FDA4AF;
    padding: 5px 11px;
    border-radius: 999px;
    font-weight: 850;
    font-size: 13px;
}

.badge-cute {
    display: inline-block;
    background: #FFF1F2;
    color: #881337 !important;
    border: 1px solid #FECDD3;
    border-radius: 999px;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: 800;
    margin: 2px;
}

/* INPUTS */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: var(--text) !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 11px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #9CA3AF !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--berry) !important;
    box-shadow: 0 0 0 2px rgba(225,29,72,.12) !important;
}

/* DROPDOWN / MULTISELECT TEXT */
div[data-baseweb="select"] * {
    color: var(--text) !important;
}

/* BUTTONS */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    border-radius: 12px !important;
    border: 1px solid var(--berry) !important;
    font-weight: 850 !important;
    min-height: 42px;
    transition: all .16s ease;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(135deg, #E11D48, #BE123C) !important;
    color: #FFFFFF !important;
    box-shadow: 0 5px 14px rgba(225,29,72,.22);
}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #BE123C, #9F1239) !important;
    transform: translateY(-1px);
}

.stDownloadButton > button {
    background: #FFFFFF !important;
    color: var(--berry-dark) !important;
}

.stDownloadButton > button:hover {
    background: #FFF1F2 !important;
}

/* ALERTS */
div[data-testid="stAlert"] {
    border-radius: 13px;
    border: 1px solid var(--berry-border);
}

/* EXPANDER / CONTAINERS */
div[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid var(--berry-border);
    border-radius: 14px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--berry-border) !important;
    border-radius: 14px !important;
    background: #FFFFFF;
}

hr { border-color: #FECDD3 !important; }

/* CHECKBOX / RADIO ACCENT */
.stRadio [data-baseweb="radio"] div:first-child,
.stCheckbox [data-baseweb="checkbox"] div:first-child {
    accent-color: var(--berry);
}

/* ADMIN / LOGIN */
.admin-box {
    background: #FFFFFF;
    border: 1px solid var(--berry-border);
    border-top: 5px solid var(--berry-dark);
    border-radius: 18px;
    padding: 25px;
    margin: 20px auto;
    max-width: 720px;
    box-shadow: 0 10px 28px rgba(136,19,55,.08);
}

.login-title {
    text-align: center;
    font-size: 28px;
    font-weight: 950;
    color: var(--berry-dark);
}

@media (max-width: 768px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    h1 { font-size: 1.8rem !important; }
    .total-money { font-size: 26px; }
    .order-builder { padding: 15px; }
}
</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# DỮ LIỆU MẶC ĐỊNH
# ============================================================

DEFAULT_DATA = {

    "categories": [

        {
            "id": 1,
            "name": "Trà sữa",
            "visible": True
        },

        {
            "id": 2,
            "name": "Trà trái cây",
            "visible": True
        },

        {
            "id": 3,
            "name": "Topping",
            "visible": True
        }

    ],

    "products": [

        {
            "id": 1,
            "category": "Trà sữa",
            "name": "Trà sữa truyền thống",
            "image": "",
            "price": 25000,
            "description": "Trà sữa truyền thống thơm béo",
            "status": "Còn hàng",
            "sizes": {
                "S": 0,
                "M": 5000,
                "L": 10000
            }
        },

        {
            "id": 2,
            "category": "Trà sữa",
            "name": "Trà sữa matcha",
            "image": "",
            "price": 30000,
            "description": "Trà sữa matcha thơm đậm vị",
            "status": "Còn hàng",
            "sizes": {
                "S": 0,
                "M": 5000,
                "L": 10000
            }
        },

        {
            "id": 3,
            "category": "Trà sữa",
            "name": "Trà sữa socola",
            "image": "",
            "price": 30000,
            "description": "Trà sữa socola",
            "status": "Còn hàng",
            "sizes": {
                "S": 0,
                "M": 5000,
                "L": 10000
            }
        },

        {
            "id": 4,
            "category": "Trà sữa",
            "name": "Trà sữa khoai môn",
            "image": "",
            "price": 30000,
            "description": "Khoai môn béo thơm",
            "status": "Còn hàng",
            "sizes": {
                "S": 0,
                "M": 5000,
                "L": 10000
            }
        },

        {
            "id": 5,
            "category": "Trà trái cây",
            "name": "Trà đào cam sả",
            "image": "",
            "price": 30000,
            "description": "Trà đào kết hợp cam và sả",
            "status": "Còn hàng",
            "sizes": {
                "S": 0,
                "M": 5000,
                "L": 10000
            }
        },

        {
            "id": 6,
            "category": "Trà trái cây",
            "name": "Trà vải",
            "image": "",
            "price": 28000,
            "description": "Trà vải thanh mát",
            "status": "Còn hàng",
            "sizes": {
                "S": 0,
                "M": 5000,
                "L": 10000
            }
        }

    ],

    "toppings": [

        {
            "id": 1,
            "name": "Trân châu đen",
            "price": 5000,
            "status": "Còn hàng",
            "visible": True
        },

        {
            "id": 2,
            "name": "Trân châu trắng",
            "price": 6000,
            "status": "Còn hàng",
            "visible": True
        },

        {
            "id": 3,
            "name": "Thạch trái cây",
            "price": 5000,
            "status": "Còn hàng",
            "visible": True
        },

        {
            "id": 4,
            "name": "Thạch phô mai",
            "price": 8000,
            "status": "Còn hàng",
            "visible": True
        },

        {
            "id": 5,
            "name": "Pudding trứng",
            "price": 7000,
            "status": "Còn hàng",
            "visible": True
        }

    ]

}


# ============================================================
# ĐỌC DỮ LIỆU
# ============================================================

def load_data():

    if not os.path.exists(DATA_FILE):

        with open(DATA_FILE, "w", encoding="utf-8") as file:

            json.dump(
                DEFAULT_DATA,
                file,
                ensure_ascii=False,
                indent=4
            )

        return DEFAULT_DATA

    try:

        with open(DATA_FILE, "r", encoding="utf-8") as file:

            return json.load(file)

    except Exception:

        return DEFAULT_DATA


# ============================================================
# LƯU DỮ LIỆU
# ============================================================

def save_data():

    with open(DATA_FILE, "w", encoding="utf-8") as file:

        json.dump(
            st.session_state.data,
            file,
            ensure_ascii=False,
            indent=4
        )


# ============================================================
# SESSION STATE
# ============================================================

if "data" not in st.session_state:

    st.session_state.data = load_data()


if "cart" not in st.session_state:

    st.session_state.cart = []


if "customer_name" not in st.session_state:

    st.session_state.customer_name = ""


if "order_id" not in st.session_state:

    st.session_state.order_id = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )


# ============================================================
# TRẠNG THÁI ADMIN
# ============================================================

if "admin_logged_in" not in st.session_state:

    st.session_state.admin_logged_in = False


if "editing_cart_index" not in st.session_state:

    st.session_state.editing_cart_index = None


# ============================================================
# HÀM LỊCH SỬ HÓA ĐƠN
# ============================================================

def load_order_history():

    if not os.path.exists(ORDER_HISTORY_FILE):
        return []

    try:
        with open(ORDER_HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_order_history(history):

    with open(ORDER_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)


def make_order_snapshot():

    return {
        "order_id": st.session_state.order_id,
        "customer_name": st.session_state.customer_name or "Khách lẻ",
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "total": calculate_cart_total(),
        "items": json.loads(json.dumps(st.session_state.cart, ensure_ascii=False)),
    }


def save_current_order_to_history():

    if not st.session_state.cart:
        return False, "Đơn hàng chưa có món."

    history = load_order_history()
    snapshot = make_order_snapshot()

    updated = False
    for index, order in enumerate(history):
        if str(order.get("order_id")) == str(snapshot["order_id"]):
            snapshot["created_at"] = order.get("created_at", snapshot["created_at"])
            history[index] = snapshot
            updated = True
            break

    if not updated:
        history.insert(0, snapshot)

    save_order_history(history)
    return True, "Đã lưu hóa đơn vào lịch sử."


def delete_order_from_history(order_id):

    history = load_order_history()
    new_history = [
        order for order in history
        if str(order.get("order_id")) != str(order_id)
    ]

    if len(new_history) == len(history):
        return False

    save_order_history(new_history)
    return True


# ============================================================
# HÀM ĐỊNH DẠNG TIỀN
# ============================================================

def money(value):

    return f"{value:,.0f} VNĐ".replace(",", ".")


# ============================================================
# ID TỰ ĐỘNG
# ============================================================

def get_next_id(items):

    if not items:

        return 1

    return max(
        item["id"]
        for item in items
    ) + 1


# ============================================================
# TÍNH TIỀN MỘT MÓN
# ============================================================

def calculate_item_total(item):

    product_price = item["price"]

    size_price = item["size_price"]

    topping_price = sum(
        topping["price"]
        for topping in item["toppings"]
    )

    return (
        product_price
        + size_price
        + topping_price
    ) * item["quantity"]


# ============================================================
# TÍNH TỔNG BILL
# ============================================================

def calculate_cart_total():

    return sum(
        calculate_item_total(item)
        for item in st.session_state.cart
    )


# ============================================================
# RESET ĐƠN
# ============================================================

def reset_order():

    st.session_state.cart = []
    st.session_state.customer_name = ""
    st.session_state.order_id = datetime.now().strftime("%Y%m%d%H%M%S")
    st.session_state.editing_cart_index = None


# ============================================================
# LOGIN ADMIN
# ============================================================

def admin_login():

    st.markdown(
        '<div class="admin-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-title">🔐 ADMIN LOGIN</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.info(
        "Khu vực này dành riêng cho quản trị viên."
    )

    username = st.text_input(
        "👤 Tên đăng nhập",
        placeholder="Nhập username..."
    )

    password = st.text_input(
        "🔑 Mật khẩu",
        type="password",
        placeholder="Nhập mật khẩu..."
    )

    login_button = st.button(
        "🔐 ĐĂNG NHẬP ADMIN",
        type="primary",
        use_container_width=True
    )

    if login_button:

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            st.session_state.admin_logged_in = True

            st.success(
                "Đăng nhập Admin thành công!"
            )

            st.rerun()

        else:

            st.error(
                "❌ Tên đăng nhập hoặc mật khẩu không đúng."
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# ĐĂNG XUẤT ADMIN
# ============================================================

def admin_logout():

    st.session_state.admin_logged_in = False

    st.success("Đã đăng xuất Admin.")

    st.rerun()


# ============================================================
# TẠO HÓA ĐƠN TXT
# ============================================================

def create_txt_invoice():

    now = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    lines = []

    lines.append("=" * 60)

    lines.append(
        "              HÓA ĐƠN TRÀ SỮA"
    )

    lines.append("=" * 60)

    lines.append(
        f"Mã đơn: {st.session_state.order_id}"
    )

    lines.append(
        f"Thời gian: {now}"
    )

    lines.append(
        f"Khách hàng: "
        f"{st.session_state.customer_name or 'Khách lẻ'}"
    )

    lines.append("-" * 60)

    for index, item in enumerate(
        st.session_state.cart,
        1
    ):

        lines.append(
            f"{index}. {item['name']} - Size {item['size']}"
        )

        lines.append(
            f"   Số lượng: {item['quantity']}"
        )

        lines.append(
            f"   Đường: {item['sugar']}%"
        )

        lines.append(
            f"   Đá: {item['ice']}%"
        )

        if item["toppings"]:

            topping_text = ", ".join(
                topping["name"]
                for topping in item["toppings"]
            )

            lines.append(
                f"   Topping: {topping_text}"
            )

        else:

            lines.append(
                "   Topping: Không"
            )

        lines.append(
            f"   Ghi chú: "
            f"{item['notes'] or 'Không'}"
        )

        unit_price = (
            item["price"]
            + item["size_price"]
        )

        lines.append(
            f"   Đơn giá: {money(unit_price)}"
        )

        lines.append(
            f"   Thành tiền: "
            f"{money(calculate_item_total(item))}"
        )

        lines.append("-" * 60)

    lines.append(
        f"TỔNG THANH TOÁN: "
        f"{money(calculate_cart_total())}"
    )

    lines.append("=" * 60)

    lines.append(
        "       Cảm ơn quý khách!"
    )

    lines.append("=" * 60)

    return "\n".join(lines).encode("utf-8")


# ============================================================
# TẠO HÓA ĐƠN HTML
# ============================================================

def create_html_invoice():

    now = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    rows = ""

    for index, item in enumerate(
        st.session_state.cart,
        1
    ):

        toppings = ", ".join(
            topping["name"]
            for topping in item["toppings"]
        ) if item["toppings"] else "Không"

        rows += f"""
        <tr>
            <td>{index}</td>
            <td>{html.escape(item['name'])}</td>
            <td>{item['size']}</td>
            <td>{item['quantity']}</td>
            <td>{item['sugar']}%</td>
            <td>{item['ice']}%</td>
            <td>{html.escape(toppings)}</td>
            <td>{html.escape(item['notes'] or 'Không')}</td>
            <td>{money(calculate_item_total(item))}</td>
        </tr>
        """

    customer = html.escape(
        st.session_state.customer_name
        or "Khách lẻ"
    )

    invoice_html = f"""
<!DOCTYPE html>

<html lang="vi">

<head>

<meta charset="UTF-8">

<title>Hóa đơn trà sữa</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 30px;
}}

h1 {{
    text-align: center;
    color: #8B4513;
}}

.info {{
    margin-bottom: 20px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    border: 1px solid #999;
    padding: 8px;
    text-align: center;
}}

th {{
    background: #f5d5c5;
}}

.total {{
    text-align: right;
    font-size: 24px;
    font-weight: bold;
    margin-top: 20px;
}}

</style>

</head>

<body>

<h1>🧋 HÓA ĐƠN TRÀ SỮA</h1>

<div class="info">

<b>Mã đơn:</b>
{st.session_state.order_id}

<br>

<b>Thời gian:</b>
{now}

<br>

<b>Khách hàng:</b>
{customer}

</div>

<table>

<thead>

<tr>

<th>#</th>

<th>Món</th>

<th>Size</th>

<th>SL</th>

<th>Đường</th>

<th>Đá</th>

<th>Topping</th>

<th>Ghi chú</th>

<th>Thành tiền</th>

</tr>

</thead>

<tbody>

{rows}

</tbody>

</table>

<div class="total">

TỔNG THANH TOÁN:
{money(calculate_cart_total())}

</div>

<br>

<center>

<b>Cảm ơn quý khách đã sử dụng dịch vụ!</b>

</center>

</body>

</html>
"""

    return invoice_html.encode("utf-8")


# ============================================================
# HEADER
# ============================================================

st.title("🧋 HÓA ĐƠN TRÀ SỮA")

st.caption(
    "Hệ thống Order • Tính Bill • Quản lý món • Xuất hóa đơn"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📌 MENU")


# ============================================================
# MENU DÀNH CHO NGƯỜI DÙNG
# ============================================================

if st.session_state.admin_logged_in:

    st.sidebar.success(
        "🔓 ADMIN ĐANG ĐĂNG NHẬP"
    )

    st.sidebar.write(
        f"👤 {ADMIN_USERNAME}"
    )

    menu_options = [
        "🛒 Đặt hàng",
        "🧾 Lịch sử hóa đơn",
        "📋 Quản lý danh mục",
        "🍹 Quản lý món",
        "🥤 Quản lý topping",
        "⚙️ Tài khoản Admin"
    ]

else:

    menu_options = [
        "🛒 Đặt hàng",
        "🔐 Đăng nhập Admin"
    ]


menu = st.sidebar.radio(
    "Chọn chức năng",
    menu_options
)


# ============================================================
# NÚT ĐĂNG XUẤT
# ============================================================

if st.session_state.admin_logged_in:

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Đăng xuất Admin",
        use_container_width=True
    ):

        admin_logout()


# ============================================================
# ============================================================
# 1. ĐĂNG NHẬP ADMIN
# ============================================================
# ============================================================

if menu == "🔐 Đăng nhập Admin":

    st.header("🔐 ĐĂNG NHẬP QUẢN TRỊ")

    admin_login()


# ============================================================
# ============================================================
# 2. ĐẶT HÀNG
# ============================================================
# ============================================================

elif menu == "🛒 Đặt hàng":

    st.header("💗 TẠO ĐƠN HÀNG")

    # --------------------------------------------------------
    # THÔNG TIN KHÁCH HÀNG
    # --------------------------------------------------------
    customer_name = st.text_input(
        "🐰 Tên khách hàng",
        value=st.session_state.customer_name,
        placeholder="Nhập tên khách hàng..."
    )
    st.session_state.customer_name = customer_name

    st.markdown(
        "<div class='badge-cute'>🌷 Chọn món yêu thích • Tùy chỉnh theo gu • Order thật cute ✨</div>",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # BỘ TẠO ĐƠN NHIỀU MÓN
    # --------------------------------------------------------
    st.markdown(
        """
        <div class="order-builder">
            <div class="cute-title"><span class="cute-icon">🧋</span>Chọn nhiều món trong một lần Order 💕</div>
            <div class="cute-subtitle">Có thể chọn nhiều danh mục và nhiều món cùng lúc. Sau đó cấu hình riêng cho từng món 💕</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    visible_categories = [
        category["name"]
        for category in st.session_state.data["categories"]
        if category.get("visible", True)
    ]

    if not visible_categories:
        st.warning("Hiện chưa có danh mục đang hiển thị.")
    else:
        selected_categories = st.multiselect(
            "🩷 Danh mục — chọn nhiều",
            visible_categories,
            default=[visible_categories[0]],
            help="Chọn một hoặc nhiều danh mục để hiển thị các món tương ứng."
        )

        available_products = [
            product
            for product in st.session_state.data["products"]
            if product.get("category") in selected_categories
            and product.get("status") == "Còn hàng"
        ]

        if not selected_categories:
            st.info("Hãy chọn ít nhất một danh mục.")
        elif not available_products:
            st.warning("Các danh mục đã chọn hiện chưa có món còn hàng.")
        else:
            product_labels = [
                f"{product['name']} • {product['category']} • {money(product['price'])}"
                for product in available_products
            ]
            label_to_product = dict(zip(product_labels, available_products))

            selected_product_labels = st.multiselect(
                "🌸 Chọn món — có thể chọn nhiều món",
                product_labels,
                help="Bạn có thể chọn 2, 3, 5... món trong cùng một lần Order."
            )

            selected_products = [
                label_to_product[label]
                for label in selected_product_labels
            ]

            if selected_products:
                st.markdown(
                    f"<span class='badge-blue'>Đã chọn {len(selected_products)} món</span>",
                    unsafe_allow_html=True
                )

                configured_items = []

                for product_index, product in enumerate(selected_products):
                    st.markdown(
                        f"""
                        <div class="item-config-card">
                            <div class="item-config-title">🧋 {product_index + 1}. {html.escape(product['name'])}</div>
                            <div class="cute-subtitle" style="margin-top:4px;">{html.escape(product.get('description', '') or 'Không có mô tả')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    image_col, config_col = st.columns([1, 3])

                    with image_col:
                        if product.get("image"):
                            try:
                                st.image(product["image"], use_container_width=True)
                            except Exception:
                                pass

                        st.markdown(
                            f"<div class='price-text'>Từ {money(product['price'])}</div>",
                            unsafe_allow_html=True
                        )

                    with config_col:
                        size = st.radio(
                            "🎀 Size",
                            ["S", "M", "L"],
                            horizontal=True,
                            key=f"multi_size_{product['id']}"
                        )

                        size_price = product.get("sizes", {}).get(size, 0)
                        current_price = product["price"] + size_price

                        c1, c2, c3 = st.columns(3)

                        with c1:
                            quantity = st.number_input(
                                "🐻 Số lượng",
                                min_value=1,
                                max_value=100,
                                value=1,
                                step=1,
                                key=f"multi_qty_{product['id']}"
                            )

                        with c2:
                            sugar = st.selectbox(
                                "🍬 Đường",
                                [100, 70, 50, 30, 10, 0],
                                format_func=lambda value: f"{value}%",
                                key=f"multi_sugar_{product['id']}"
                            )

                        with c3:
                            ice = st.selectbox(
                                "🧊 Đá",
                                [100, 70, 50, 30, 10, 0],
                                format_func=lambda value: f"{value}%",
                                key=f"multi_ice_{product['id']}"
                            )

                        st.caption(f"Giá Size {size}: {money(current_price)} / ly")

                        available_toppings = [
                            topping
                            for topping in st.session_state.data["toppings"]
                            if topping.get("visible", True)
                            and topping.get("status") == "Còn hàng"
                        ]

                        topping_options = {
                            f"{topping['name']} (+{money(topping['price'])})": topping
                            for topping in available_toppings
                        }

                        selected_topping_labels = st.multiselect(
                            "🍓 Topping — có thể chọn nhiều",
                            list(topping_options.keys()),
                            key=f"multi_toppings_{product['id']}"
                        )

                        selected_toppings = [
                            topping_options[label]
                            for label in selected_topping_labels
                        ]

                        notes_options = [
                            "Nhiều sữa",
                            "Không lấy ống hút",
                            "Uống tại chỗ",
                            "Mang về"
                        ]

                        selected_notes = st.multiselect(
                            "💌 Ghi chú nhanh",
                            notes_options,
                            key=f"multi_notes_{product['id']}"
                        )

                        custom_note = st.text_input(
                            "💬 Ghi chú riêng",
                            placeholder="Ví dụ: ít ngọt hơn, để riêng topping...",
                            key=f"multi_custom_note_{product['id']}"
                        )

                        notes = ", ".join(selected_notes)
                        if custom_note.strip():
                            notes = f"{notes}, {custom_note.strip()}" if notes else custom_note.strip()

                    preview_item = {
                        "name": product["name"],
                        "price": product["price"],
                        "size": size,
                        "size_price": size_price,
                        "quantity": quantity,
                        "sugar": sugar,
                        "ice": ice,
                        "toppings": selected_toppings,
                        "notes": notes
                    }

                    preview_total = calculate_item_total(preview_item)
                    configured_items.append(preview_item)

                    st.info(
                        f"💗 {product['name']} • {quantity} ly • Thành tiền: **{money(preview_total)}**"
                    )
                    st.divider()

                # ------------------------------------------------
                # TỔNG XEM TRƯỚC CÁC MÓN ĐÃ CHỌN
                # ------------------------------------------------
                selected_total = sum(
                    calculate_item_total(item)
                    for item in configured_items
                )

                st.markdown(
                    f"""
                    <div class="total-box">
                        <div style="color:#475569;">🛍️ {len(configured_items)} món đã chọn</div>
                        <div class="total-money">{money(selected_total)}</div>
                        <div style="color:#475569;">Tổng tạm tính trước khi thêm vào đơn</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    f"🛒 THÊM TẤT CẢ {len(configured_items)} MÓN VÀO ĐƠN 💕",
                    type="primary",
                    use_container_width=True,
                    key="add_all_selected_products"
                ):
                    st.session_state.cart.extend(configured_items)
                    st.success(
                        f"Đã thêm {len(configured_items)} món vào đơn hàng!"
                    )
                    st.rerun()
            else:
                st.info("Chưa chọn món. Hãy chọn nhiều món ở ô phía trên để cấu hình.")

    # ========================================================
    # CHI TIẾT ĐƠN HÀNG
    # ========================================================
    st.divider()
    st.header("🧾 CHI TIẾT ĐƠN HÀNG 💗")

    if not st.session_state.cart:
        st.info("Chưa có món trong đơn. Hãy chọn nhiều món ở khu vực phía trên.")
    else:
        for index, item in enumerate(st.session_state.cart):
            item_total = calculate_item_total(item)

            toppings_text = ", ".join(
                topping["name"] for topping in item["toppings"]
            ) if item["toppings"] else "Không"

            st.markdown(
                f"""
                <div class="order-card">
                    <div class="order-title">🧋 {index + 1}. {html.escape(item['name'])}</div>
                    <div class="order-detail">
                        📏 <b>Size:</b> {item['size']}<br>
                        🔢 <b>Số lượng:</b> {item['quantity']}<br>
                        🍬 <b>Đường:</b> {item['sugar']}%<br>
                        🧊 <b>Đá:</b> {item['ice']}%<br>
                        🧋 <b>Topping:</b> {html.escape(toppings_text)}<br>
                        📝 <b>Ghi chú:</b> {html.escape(item['notes'] or 'Không')}<br>
                        💰 <b>Thành tiền:</b> {money(item_total)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            edit_col, delete_col = st.columns([5, 1])

            with edit_col:
                if st.button(
                    "✏️ CHỈNH SỬA MÓN NÀY",
                    key=f"edit_cart_{index}",
                    use_container_width=True
                ):
                    st.session_state.editing_cart_index = index
                    st.rerun()

            with delete_col:
                if st.button(
                    "🗑️ Xóa món",
                    key=f"delete_cart_{index}",
                    use_container_width=True
                ):
                    st.session_state.cart.pop(index)
                    if st.session_state.editing_cart_index == index:
                        st.session_state.editing_cart_index = None
                    elif (
                        st.session_state.editing_cart_index is not None
                        and st.session_state.editing_cart_index > index
                    ):
                        st.session_state.editing_cart_index -= 1
                    st.rerun()

            if st.session_state.editing_cart_index == index:
                st.markdown(
                    """
                    <div class="item-config-card">
                        <div class="item-config-title">✏️ Chỉnh sửa món trong đơn</div>
                        <div class="cute-subtitle">Thay đổi size, số lượng, đường, đá, topping hoặc ghi chú rồi bấm lưu.</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                edit_col1, edit_col2, edit_col3 = st.columns(3)

                with edit_col1:
                    edit_size = st.selectbox(
                        "🎀 Size",
                        ["S", "M", "L"],
                        index=["S", "M", "L"].index(item.get("size", "S"))
                        if item.get("size", "S") in ["S", "M", "L"] else 0,
                        key=f"edit_size_{index}"
                    )

                with edit_col2:
                    edit_quantity = st.number_input(
                        "🐻 Số lượng",
                        min_value=1,
                        max_value=100,
                        value=int(item.get("quantity", 1)),
                        step=1,
                        key=f"edit_qty_{index}"
                    )

                with edit_col3:
                    sugar_options = [100, 70, 50, 30, 10, 0]
                    edit_sugar = st.selectbox(
                        "🍬 Đường",
                        sugar_options,
                        index=sugar_options.index(item.get("sugar", 100))
                        if item.get("sugar", 100) in sugar_options else 0,
                        format_func=lambda value: f"{value}%",
                        key=f"edit_sugar_{index}"
                    )

                ice_options = [100, 70, 50, 30, 10, 0]
                edit_ice = st.selectbox(
                    "🧊 Đá",
                    ice_options,
                    index=ice_options.index(item.get("ice", 100))
                    if item.get("ice", 100) in ice_options else 0,
                    format_func=lambda value: f"{value}%",
                    key=f"edit_ice_{index}"
                )

                available_toppings = [
                    topping
                    for topping in st.session_state.data["toppings"]
                    if topping.get("visible", True)
                    and topping.get("status") == "Còn hàng"
                ]

                topping_options = {
                    f"{topping['name']} (+{money(topping['price'])})": topping
                    for topping in available_toppings
                }

                existing_topping_names = {
                    topping.get("name") for topping in item.get("toppings", [])
                }

                default_topping_labels = [
                    label for label, topping in topping_options.items()
                    if topping.get("name") in existing_topping_names
                ]

                edit_topping_labels = st.multiselect(
                    "🍓 Topping — có thể chọn nhiều",
                    list(topping_options.keys()),
                    default=default_topping_labels,
                    key=f"edit_toppings_{index}"
                )

                edit_toppings = [
                    topping_options[label] for label in edit_topping_labels
                ]

                edit_notes = st.text_area(
                    "💬 Ghi chú",
                    value=item.get("notes", ""),
                    key=f"edit_notes_{index}",
                    placeholder="Ví dụ: ít ngọt hơn, để riêng topping..."
                )

                new_size_price = item.get("size_price", 0)
                for product in st.session_state.data["products"]:
                    if product.get("name") == item.get("name"):
                        new_size_price = product.get("sizes", {}).get(edit_size, new_size_price)
                        break

                new_item = {
                    "name": item["name"],
                    "price": item["price"],
                    "size": edit_size,
                    "size_price": new_size_price,
                    "quantity": edit_quantity,
                    "sugar": edit_sugar,
                    "ice": edit_ice,
                    "toppings": edit_toppings,
                    "notes": edit_notes.strip()
                }

                st.info(
                    f"💗 Thành tiền mới: **{money(calculate_item_total(new_item))}**"
                )

                save_edit_col, cancel_edit_col = st.columns(2)

                with save_edit_col:
                    if st.button(
                        "💾 LƯU THAY ĐỔI MÓN",
                        type="primary",
                        use_container_width=True,
                        key=f"save_edit_cart_{index}"
                    ):
                        st.session_state.cart[index] = new_item
                        st.session_state.editing_cart_index = None
                        st.rerun()

                with cancel_edit_col:
                    if st.button(
                        "↩️ HỦY CHỈNH SỬA",
                        use_container_width=True,
                        key=f"cancel_edit_cart_{index}"
                    ):
                        st.session_state.editing_cart_index = None
                        st.rerun()

        total = calculate_cart_total()

        st.markdown(
            f"""
            <div class="total-box">
                <div style="color:#475569;">👤 Khách hàng: <b style="color:#0F172A;">{html.escape(st.session_state.customer_name or 'Khách lẻ')}</b></div>
                <div style="margin-top:8px; color:#475569;">🧾 Số món: <b style="color:#0F172A;">{len(st.session_state.cart)}</b></div>
                <div class="total-money">💰 {money(total)}</div>
                <div style="color:#475569;">TỔNG SỐ TIỀN CẦN THANH TOÁN</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()
        st.subheader("💾 LƯU & XUẤT HÓA ĐƠN")

        save_col, txt_col, html_col, new_col = st.columns(4)

        with save_col:
            if st.button(
                "💾 LƯU HÓA ĐƠN",
                type="primary",
                use_container_width=True,
                key="save_invoice_history"
            ):
                saved, message = save_current_order_to_history()
                if saved:
                    st.success(message)
                else:
                    st.error(message)

        with txt_col:
            txt_data = create_txt_invoice()
            st.download_button(
                "📄 Tải TXT",
                data=txt_data,
                file_name=f"hoa_don_{st.session_state.order_id}.txt",
                mime="text/plain",
                use_container_width=True
            )

        with html_col:
            html_data = create_html_invoice()
            st.download_button(
                "🌐 Tải HTML",
                data=html_data,
                file_name=f"hoa_don_{st.session_state.order_id}.html",
                mime="text/html",
                use_container_width=True
            )

        with new_col:
            if st.button(
                "🗑️ TẠO ĐƠN MỚI",
                use_container_width=True,
                key="new_order_button"
            ):
                reset_order()
                st.rerun()


elif menu == "🧾 Lịch sử hóa đơn":

    if not st.session_state.admin_logged_in:
        st.error("🔒 Bạn phải đăng nhập Admin.")
        st.stop()

    st.header("🧾 LỊCH SỬ HÓA ĐƠN")
    st.success("🔓 Chỉ Admin mới có quyền xem, tải và xóa lịch sử hóa đơn.")

    history = load_order_history()

    if not history:
        st.info("📭 Chưa có hóa đơn nào được lưu. Hãy vào Đặt hàng và bấm \"💾 LƯU HÓA ĐƠN\".")
    else:
        total_revenue = sum(float(order.get("total", 0)) for order in history)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🧾 Số hóa đơn", len(history))
        with col2:
            st.metric("💰 Tổng doanh thu", money(total_revenue))
        with col3:
            st.metric("🛍️ Tổng số món", sum(len(order.get("items", [])) for order in history))

        search_text = st.text_input(
            "🔎 Tìm hóa đơn",
            placeholder="Nhập mã đơn hoặc tên khách hàng..."
        ).strip().lower()

        filtered_history = []
        for order in history:
            order_id = str(order.get("order_id", ""))
            customer = str(order.get("customer_name", ""))
            if not search_text or search_text in order_id.lower() or search_text in customer.lower():
                filtered_history.append(order)

        st.caption(f"Đang hiển thị {len(filtered_history)} / {len(history)} hóa đơn")

        for order in filtered_history:
            order_id = str(order.get("order_id", ""))
            customer = order.get("customer_name", "Khách lẻ")
            created_at = order.get("created_at", "")
            total = float(order.get("total", 0))
            items = order.get("items", [])

            with st.expander(
                f"🧾 {order_id}  •  👤 {customer}  •  💰 {money(total)}  •  {created_at}"
            ):
                for item_index, item in enumerate(items, 1):
                    toppings = ", ".join(
                        topping.get("name", "") for topping in item.get("toppings", [])
                    ) or "Không"
                    st.markdown(
                        f"""
                        <div class="order-card">
                            <div class="order-title">🧋 {item_index}. {html.escape(str(item.get('name', 'Món')))}</div>
                            <div class="order-detail">
                                📏 <b>Size:</b> {item.get('size', 'S')} &nbsp;•&nbsp;
                                🔢 <b>SL:</b> {item.get('quantity', 1)}<br>
                                🍬 <b>Đường:</b> {item.get('sugar', 100)}% &nbsp;•&nbsp;
                                🧊 <b>Đá:</b> {item.get('ice', 100)}%<br>
                                🧋 <b>Topping:</b> {html.escape(toppings)}<br>
                                📝 <b>Ghi chú:</b> {html.escape(str(item.get('notes', '') or 'Không'))}<br>
                                💰 <b>Thành tiền:</b> {money(calculate_item_total(item))}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(f"### 💰 Tổng thanh toán: **{money(total)}**")

                action_col1, action_col2, action_col3 = st.columns(3)

                invoice_lines = [
                    "=" * 60,
                    "                 HÓA ĐƠN TRÀ SỮA",
                    "=" * 60,
                    f"Mã đơn: {order_id}",
                    f"Thời gian: {created_at}",
                    f"Khách hàng: {customer}",
                    "-" * 60,
                ]

                for item_index, item in enumerate(items, 1):
                    toppings = ", ".join(
                        topping.get("name", "") for topping in item.get("toppings", [])
                    ) or "Không"
                    invoice_lines.extend([
                        f"{item_index}. {item.get('name', 'Món')} - Size {item.get('size', 'S')}",
                        f"   Số lượng: {item.get('quantity', 1)}",
                        f"   Đường: {item.get('sugar', 100)}%",
                        f"   Đá: {item.get('ice', 100)}%",
                        f"   Topping: {toppings}",
                        f"   Ghi chú: {item.get('notes', '') or 'Không'}",
                        f"   Thành tiền: {money(calculate_item_total(item))}",
                        "-" * 60,
                    ])

                invoice_lines.extend([
                    f"TỔNG THANH TOÁN: {money(total)}",
                    "=" * 60,
                    "             Cảm ơn quý khách!",
                    "=" * 60,
                ])

                with action_col1:
                    st.download_button(
                        "📄 TẢI HÓA ĐƠN",
                        data="\n".join(invoice_lines).encode("utf-8"),
                        file_name=f"hoa_don_{order_id}.txt",
                        mime="text/plain",
                        use_container_width=True,
                        key=f"download_history_{order_id}"
                    )

                with action_col2:
                    if st.button(
                        "✏️ SỬA HÓA ĐƠN",
                        use_container_width=True,
                        key=f"edit_history_{order_id}"
                    ):
                        st.session_state.cart = json.loads(json.dumps(items, ensure_ascii=False))
                        st.session_state.customer_name = customer if customer != "Khách lẻ" else ""
                        st.session_state.order_id = order_id
                        st.session_state.editing_cart_index = None
                        st.success("Đã đưa hóa đơn vào phần Đặt hàng để chỉnh sửa.")
                        st.info("Hãy chọn menu 🛒 Đặt hàng ở thanh bên để chỉnh sửa và lưu lại.")

                with action_col3:
                    if st.button(
                        "🗑️ XÓA HÓA ĐƠN",
                        use_container_width=True,
                        key=f"delete_history_{order_id}"
                    ):
                        delete_order_from_history(order_id)
                        st.success("Đã xóa hóa đơn khỏi lịch sử.")
                        st.rerun()

        st.divider()
        if st.button(
            "🗑️ XÓA TOÀN BỘ LỊCH SỬ HÓA ĐƠN",
            use_container_width=True,
            key="delete_all_history"
        ):
            save_order_history([])
            st.success("Đã xóa toàn bộ lịch sử hóa đơn.")
            st.rerun()


elif menu == "📋 Quản lý danh mục":

    if not st.session_state.admin_logged_in:

        st.error(
            "🔒 Bạn phải đăng nhập Admin."
        )

        st.stop()

    st.header(
        "📋 QUẢN LÝ DANH MỤC"
    )

    st.success(
        "🔓 Bạn đang sử dụng quyền quản trị."
    )

    # --------------------------------------------------------
    # THÊM DANH MỤC
    # --------------------------------------------------------

    st.subheader(
        "➕ TẠO DANH MỤC MỚI"
    )

    new_category = st.text_input(
        "Tên danh mục",
        placeholder=(
            "Ví dụ: Cà phê, Đá xay..."
        )
    )

    if st.button(
        "➕ TẠO DANH MỤC",
        type="primary"
    ):

        new_category = new_category.strip()

        if not new_category:

            st.error(
                "Vui lòng nhập tên danh mục."
            )

        elif any(
            category["name"].lower()
            == new_category.lower()
            for category
            in st.session_state.data["categories"]
        ):

            st.error(
                "Danh mục đã tồn tại."
            )

        else:

            st.session_state.data[
                "categories"
            ].append(
                {
                    "id": get_next_id(
                        st.session_state.data[
                            "categories"
                        ]
                    ),
                    "name": new_category,
                    "visible": True
                }
            )

            save_data()

            st.success(
                "Đã tạo danh mục."
            )

            st.rerun()

    st.divider()

    # --------------------------------------------------------
    # DANH SÁCH DANH MỤC
    # --------------------------------------------------------

    st.subheader(
        "📂 DANH SÁCH DANH MỤC"
    )

    for category in st.session_state.data[
        "categories"
    ]:

        with st.container(
            border=True
        ):

            col1, col2, col3 = st.columns(
                [4, 2, 2]
            )

            with col1:

                st.write(
                    f"### 📂 {category['name']}"
                )

            with col2:

                if category["visible"]:

                    st.success(
                        "👁️ Đang hiển thị"
                    )

                else:

                    st.warning(
                        "🙈 Đang ẩn"
                    )

            with col3:

                button_text = (
                    "🙈 Ẩn danh mục"
                    if category["visible"]
                    else "👁️ Hiện danh mục"
                )

                if st.button(
                    button_text,
                    key=(
                        f"toggle_category_"
                        f"{category['id']}"
                    ),
                    use_container_width=True
                ):

                    category["visible"] = (
                        not category["visible"]
                    )

                    save_data()

                    st.rerun()

            edit_name = st.text_input(
                "Sửa tên danh mục",
                value=category["name"],
                key=(
                    f"edit_category_"
                    f"{category['id']}"
                )
            )

            edit_col1, edit_col2 = st.columns(
                2
            )

            with edit_col1:

                if st.button(
                    "💾 LƯU TÊN",
                    key=(
                        f"save_category_"
                        f"{category['id']}"
                    ),
                    use_container_width=True
                ):

                    old_name = category[
                        "name"
                    ]

                    new_name = edit_name.strip()

                    if not new_name:

                        st.error(
                            "Tên danh mục không được để trống."
                        )

                    else:

                        category["name"] = new_name

                        for product in (
                            st.session_state.data[
                                "products"
                            ]
                        ):

                            if product[
                                "category"
                            ] == old_name:

                                product[
                                    "category"
                                ] = new_name

                        save_data()

                        st.success(
                            "Đã cập nhật danh mục."
                        )

                        st.rerun()

            with edit_col2:

                if st.button(
                    "🗑️ XÓA DANH MỤC",
                    key=(
                        f"delete_category_"
                        f"{category['id']}"
                    ),
                    use_container_width=True
                ):

                    used = any(
                        product["category"]
                        == category["name"]
                        for product
                        in st.session_state.data[
                            "products"
                        ]
                    )

                    if used:

                        st.error(
                            "Không thể xóa danh mục "
                            "vì đang có món thuộc danh mục này."
                        )

                    else:

                        st.session_state.data[
                            "categories"
                        ].remove(
                            category
                        )

                        save_data()

                        st.success(
                            "Đã xóa danh mục."
                        )

                        st.rerun()


# ============================================================
# ============================================================
# 4. QUẢN LÝ MÓN - CHỈ ADMIN
# ============================================================
# ============================================================

elif menu == "🍹 Quản lý món":

    if not st.session_state.admin_logged_in:

        st.error(
            "🔒 Bạn phải đăng nhập Admin."
        )

        st.stop()

    st.header(
        "🍹 QUẢN LÝ MÓN"
    )

    st.success(
        "🔓 Quyền Admin đang hoạt động."
    )

    categories = [
        category["name"]
        for category
        in st.session_state.data[
            "categories"
        ]
    ]

    if not categories:

        st.warning(
            "Hãy tạo danh mục trước."
        )

    else:

        # ----------------------------------------------------
        # THÊM MÓN
        # ----------------------------------------------------

        st.subheader(
            "➕ THÊM MÓN MỚI"
        )

        with st.form(
            "add_product_form"
        ):

            col1, col2 = st.columns(
                2
            )

            with col1:

                product_name = st.text_input(
                    "Tên món"
                )

                category = st.selectbox(
                    "Danh mục",
                    categories
                )

                base_price = st.number_input(
                    "Giá bán cơ bản",
                    min_value=0,
                    value=25000,
                    step=1000
                )

                description = st.text_area(
                    "Mô tả món"
                )

            with col2:

                image_url = st.text_input(
                    "URL hình ảnh",
                    placeholder="https://..."
                )

                status = st.selectbox(
                    "Trạng thái món",
                    [
                        "Còn hàng",
                        "Hết hàng"
                    ]
                )

                st.write(
                    "**Giá chênh lệch theo Size**"
                )

                size_s = st.number_input(
                    "Size S (+)",
                    min_value=0,
                    value=0,
                    step=1000
                )

                size_m = st.number_input(
                    "Size M (+)",
                    min_value=0,
                    value=5000,
                    step=1000
                )

                size_l = st.number_input(
                    "Size L (+)",
                    min_value=0,
                    value=10000,
                    step=1000
                )

            submitted = st.form_submit_button(
                "➕ THÊM MÓN",
                type="primary"
            )

        if submitted:

            product_name = product_name.strip()

            if not product_name:

                st.error(
                    "Vui lòng nhập tên món."
                )

            else:

                new_product = {

                    "id": get_next_id(
                        st.session_state.data[
                            "products"
                        ]
                    ),

                    "category": category,

                    "name": product_name,

                    "image": image_url.strip(),

                    "price": base_price,

                    "description": description.strip(),

                    "status": status,

                    "sizes": {

                        "S": size_s,

                        "M": size_m,

                        "L": size_l

                    }

                }

                st.session_state.data[
                    "products"
                ].append(
                    new_product
                )

                save_data()

                st.success(
                    "Đã thêm món mới."
                )

                st.rerun()

    st.divider()

    # --------------------------------------------------------
    # DANH SÁCH MÓN
    # --------------------------------------------------------

    st.subheader(
        "📋 DANH SÁCH MÓN"
    )

    for product in st.session_state.data[
        "products"
    ]:

        with st.expander(
            f"🧋 {product['name']} "
            f"– {money(product['price'])}"
        ):

            image_col, info_col = st.columns(
                [1, 3]
            )

            with image_col:

                if product["image"]:

                    try:

                        st.image(
                            product["image"],
                            use_container_width=True
                        )

                    except Exception:

                        pass

            with info_col:

                st.write(
                    f"**Danh mục:** "
                    f"{product['category']}"
                )

                st.write(
                    f"**Giá cơ bản:** "
                    f"{money(product['price'])}"
                )

                st.write(
                    f"**Size S:** "
                    f"+{money(product['sizes']['S'])}"
                )

                st.write(
                    f"**Size M:** "
                    f"+{money(product['sizes']['M'])}"
                )

                st.write(
                    f"**Size L:** "
                    f"+{money(product['sizes']['L'])}"
                )

                if product["status"] == "Còn hàng":

                    st.success(
                        "🟢 CÒN HÀNG"
                    )

                else:

                    st.error(
                        "🔴 HẾT HÀNG"
                    )

                st.write(
                    product["description"]
                )

            st.divider()

            st.markdown(
                "### ✏️ CHỈNH SỬA MÓN"
            )

            edit_col1, edit_col2 = st.columns(
                2
            )

            with edit_col1:

                edit_name = st.text_input(
                    "Tên món",
                    value=product["name"],
                    key=(
                        f"edit_name_"
                        f"{product['id']}"
                    )
                )

                current_category_index = 0

                if (
                    product["category"]
                    in categories
                ):

                    current_category_index = (
                        categories.index(
                            product["category"]
                        )
                    )

                edit_category = st.selectbox(
                    "Danh mục",
                    categories,
                    index=current_category_index,
                    key=(
                        f"edit_category_product_"
                        f"{product['id']}"
                    )
                )

                edit_price = st.number_input(
                    "Giá cơ bản",
                    min_value=0,
                    value=int(
                        product["price"]
                    ),
                    step=1000,
                    key=(
                        f"edit_price_"
                        f"{product['id']}"
                    )
                )

            with edit_col2:

                edit_image = st.text_input(
                    "URL hình ảnh",
                    value=product["image"],
                    key=(
                        f"edit_image_"
                        f"{product['id']}"
                    )
                )

                edit_status = st.selectbox(
                    "Trạng thái",
                    [
                        "Còn hàng",
                        "Hết hàng"
                    ],
                    index=(
                        0
                        if product["status"]
                        == "Còn hàng"
                        else 1
                    ),
                    key=(
                        f"edit_status_"
                        f"{product['id']}"
                    )
                )

                edit_description = st.text_area(
                    "Mô tả",
                    value=product[
                        "description"
                    ],
                    key=(
                        f"edit_description_"
                        f"{product['id']}"
                    )
                )

            st.write(
                "**Giá chênh lệch Size**"
            )

            size_col1, size_col2, size_col3 = (
                st.columns(3)
            )

            with size_col1:

                edit_s = st.number_input(
                    "Size S +",
                    min_value=0,
                    value=int(
                        product[
                            "sizes"
                        ]["S"]
                    ),
                    step=1000,
                    key=(
                        f"edit_s_"
                        f"{product['id']}"
                    )
                )

            with size_col2:

                edit_m = st.number_input(
                    "Size M +",
                    min_value=0,
                    value=int(
                        product[
                            "sizes"
                        ]["M"]
                    ),
                    step=1000,
                    key=(
                        f"edit_m_"
                        f"{product['id']}"
                    )
                )

            with size_col3:

                edit_l = st.number_input(
                    "Size L +",
                    min_value=0,
                    value=int(
                        product[
                            "sizes"
                        ]["L"]
                    ),
                    step=1000,
                    key=(
                        f"edit_l_"
                        f"{product['id']}"
                    )
                )

            save_col, delete_col = st.columns(
                2
            )

            with save_col:

                if st.button(
                    "💾 LƯU THAY ĐỔI",
                    key=(
                        f"save_product_"
                        f"{product['id']}"
                    ),
                    type="primary",
                    use_container_width=True
                ):

                    product["name"] = (
                        edit_name.strip()
                    )

                    product["category"] = (
                        edit_category
                    )

                    product["price"] = (
                        edit_price
                    )

                    product["image"] = (
                        edit_image.strip()
                    )

                    product["status"] = (
                        edit_status
                    )

                    product[
                        "description"
                    ] = edit_description.strip()

                    product["sizes"] = {

                        "S": edit_s,

                        "M": edit_m,

                        "L": edit_l

                    }

                    save_data()

                    st.success(
                        "Đã cập nhật món."
                    )

                    st.rerun()

            with delete_col:

                if st.button(
                    "🗑️ XÓA MÓN",
                    key=(
                        f"delete_product_"
                        f"{product['id']}"
                    ),
                    use_container_width=True
                ):

                    st.session_state.data[
                        "products"
                    ].remove(
                        product
                    )

                    save_data()

                    st.success(
                        "Đã xóa món."
                    )

                    st.rerun()


# ============================================================
# ============================================================
# 5. QUẢN LÝ TOPPING - CHỈ ADMIN
# ============================================================
# ============================================================

elif menu == "🥤 Quản lý topping":

    if not st.session_state.admin_logged_in:

        st.error(
            "🔒 Bạn phải đăng nhập Admin."
        )

        st.stop()

    st.header(
        "🥤 QUẢN LÝ TOPPING"
    )

    st.success(
        "🔓 Quyền Admin đang hoạt động."
    )

    # --------------------------------------------------------
    # THÊM TOPPING
    # --------------------------------------------------------

    st.subheader(
        "➕ THÊM TOPPING"
    )

    with st.form(
        "add_topping_form"
    ):

        topping_name = st.text_input(
            "Tên topping"
        )

        topping_price = st.number_input(
            "Giá topping",
            min_value=0,
            value=5000,
            step=1000
        )

        topping_status = st.selectbox(
            "Trạng thái",
            [
                "Còn hàng",
                "Hết hàng"
            ]
        )

        topping_submit = st.form_submit_button(
            "➕ THÊM TOPPING",
            type="primary"
        )

    if topping_submit:

        topping_name = topping_name.strip()

        if not topping_name:

            st.error(
                "Vui lòng nhập tên topping."
            )

        else:

            new_topping = {

                "id": get_next_id(
                    st.session_state.data[
                        "toppings"
                    ]
                ),

                "name": topping_name,

                "price": topping_price,

                "status": topping_status,

                "visible": True

            }

            st.session_state.data[
                "toppings"
            ].append(
                new_topping
            )

            save_data()

            st.success(
                "Đã thêm topping."
            )

            st.rerun()

    st.divider()

    # --------------------------------------------------------
    # DANH SÁCH TOPPING
    # --------------------------------------------------------

    st.subheader(
        "📋 DANH SÁCH TOPPING"
    )

    for topping in st.session_state.data[
        "toppings"
    ]:

        with st.expander(
            f"🧋 {topping['name']} "
            f"– {money(topping['price'])}"
        ):

            edit_name = st.text_input(
                "Tên topping",
                value=topping["name"],
                key=(
                    f"top_name_"
                    f"{topping['id']}"
                )
            )

            edit_price = st.number_input(
                "Giá",
                min_value=0,
                value=int(
                    topping["price"]
                ),
                step=1000,
                key=(
                    f"top_price_"
                    f"{topping['id']}"
                )
            )

            edit_status = st.selectbox(
                "Trạng thái",
                [
                    "Còn hàng",
                    "Hết hàng"
                ],
                index=(
                    0
                    if topping["status"]
                    == "Còn hàng"
                    else 1
                ),
                key=(
                    f"top_status_"
                    f"{topping['id']}"
                )
            )

            col1, col2, col3 = st.columns(
                3
            )

            with col1:

                if st.button(
                    "💾 LƯU",
                    key=(
                        f"save_top_"
                        f"{topping['id']}"
                    ),
                    use_container_width=True
                ):

                    topping["name"] = (
                        edit_name.strip()
                    )

                    topping["price"] = (
                        edit_price
                    )

                    topping["status"] = (
                        edit_status
                    )

                    save_data()

                    st.success(
                        "Đã cập nhật topping."
                    )

                    st.rerun()

            with col2:

                visible_text = (
                    "🙈 ẨN"
                    if topping["visible"]
                    else "👁️ HIỆN"
                )

                if st.button(
                    visible_text,
                    key=(
                        f"visible_top_"
                        f"{topping['id']}"
                    ),
                    use_container_width=True
                ):

                    topping["visible"] = (
                        not topping["visible"]
                    )

                    save_data()

                    st.rerun()

            with col3:

                if st.button(
                    "🗑️ XÓA",
                    key=(
                        f"delete_top_"
                        f"{topping['id']}"
                    ),
                    use_container_width=True
                ):

                    st.session_state.data[
                        "toppings"
                    ].remove(
                        topping
                    )

                    save_data()

                    st.success(
                        "Đã xóa topping."
                    )

                    st.rerun()


# ============================================================
# ============================================================
# 6. TÀI KHOẢN ADMIN
# ============================================================
# ============================================================

elif menu == "⚙️ Tài khoản Admin":

    if not st.session_state.admin_logged_in:

        st.error(
            "🔒 Bạn phải đăng nhập Admin."
        )

        st.stop()

    st.header(
        "⚙️ TÀI KHOẢN ADMIN"
    )

    st.success(
        "🔓 Bạn đang đăng nhập với quyền Admin."
    )

    st.write(
        f"👤 **Username:** {ADMIN_USERNAME}"
    )

    st.write(
        "🔐 **Mật khẩu:** ********"
    )

    st.info(
        """
        Mật khẩu được lấy từ Streamlit Secrets.

        Nếu bạn chưa thiết lập Secrets,
        hệ thống đang sử dụng tài khoản test mặc định.
        """
    )

    st.divider()

    st.subheader(
        "🚪 Đăng xuất"
    )

    if st.button(
        "🚪 ĐĂNG XUẤT ADMIN",
        type="primary"
    ):

        admin_logout()


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

if st.session_state.admin_logged_in:

    st.sidebar.success(
        "🔓 ADMIN MODE"
    )

else:

    st.sidebar.info(
        "👤 USER MODE"
    )

st.sidebar.caption(
    "🧋 Milk Tea Order & Billing"
)

st.sidebar.caption(
    "Order • Tính bill • Lịch sử hóa đơn • Admin"
)
