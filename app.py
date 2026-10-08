import streamlit as st
from datetime import datetime
import json
import os
import html
import hashlib
from copy import deepcopy

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

# ============================================================
# ADMIN
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
# CSS - VIBRANT BERRY & PASSION
# ============================================================
st.markdown("""
<style>
:root {
    --berry:#E11D48;
    --berry-dark:#881337;
    --berry-soft:#FFF1F2;
    --berry-light:#FFE4E6;
    --berry-border:#FECDD3;
    --surface:#FFFFFF;
    --text:#111827;
    --muted:#6B7280;
}
.stApp {
    background:linear-gradient(135deg,#FFF1F2 0%,#FFF8F9 45%,#FFE4E6 100%);
    color:var(--text);
}
.block-container {
    max-width:1380px;
    padding-top:1.25rem;
    padding-bottom:3.5rem;
}
h1,h2,h3,h4,h5,h6 {
    color:var(--text)!important;
    font-weight:850!important;
}
h1 {
    text-align:center;
    font-size:2.35rem!important;
    letter-spacing:-.7px;
}
h2,h3 { color:var(--berry-dark)!important; }
p,label,.stMarkdown,.stCaption { color:var(--muted); }

.app-header {
    background:rgba(255,255,255,.96);
    border:1px solid var(--berry-border);
    border-left:7px solid var(--berry);
    border-radius:22px;
    padding:22px 26px;
    margin-bottom:22px;
    box-shadow:0 10px 30px rgba(136,19,55,.08);
}
section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#881337 0%,#9F1239 48%,#4C0519 100%);
    border-right:1px solid #BE123C;
}
section[data-testid="stSidebar"] * { color:#FFFFFF!important; }
section[data-testid="stSidebar"] .stRadio label {
    background:rgba(255,255,255,.09);
    border:1px solid rgba(255,255,255,.08);
    border-radius:14px;
    padding:9px 11px;
    margin:4px 0;
}
.cute-icon {
    display:inline-flex;
    align-items:center;
    justify-content:center;
    width:44px;
    height:44px;
    border-radius:14px;
    background:linear-gradient(135deg,#FFE4E6,#FFF1F2);
    border:1px solid #FECDD3;
    box-shadow:0 5px 12px rgba(225,29,72,.12);
    font-size:24px;
    vertical-align:middle;
    margin-right:9px;
}
.cute-title {
    display:flex;
    align-items:center;
    color:var(--berry-dark);
    font-size:22px;
    font-weight:900;
    margin-bottom:5px;
}
.cute-subtitle { color:var(--muted);font-size:14px;line-height:1.6; }
.order-builder {
    background:rgba(255,255,255,.97);
    border:1px solid var(--berry-border);
    border-top:5px solid var(--berry);
    border-radius:20px;
    padding:22px;
    margin:12px 0 20px;
    box-shadow:0 10px 28px rgba(136,19,55,.08);
}
.item-config-card {
    background:linear-gradient(135deg,#FFFFFF 0%,#FFF8F9 100%);
    border:1px solid var(--berry-border);
    border-left:5px solid var(--berry);
    border-radius:18px;
    padding:16px;
    margin:13px 0 4px;
    box-shadow:0 6px 18px rgba(225,29,72,.07);
}
.item-config-title { color:var(--text);font-weight:900;font-size:18px; }
.order-card,.menu-card {
    background:#FFFFFF;
    color:var(--text);
    padding:18px;
    border-radius:18px;
    border:1px solid var(--berry-border);
    margin-bottom:14px;
    box-shadow:0 6px 20px rgba(17,24,39,.06);
}
.order-title { font-size:19px;font-weight:900;color:var(--berry-dark);margin-bottom:8px; }
.order-detail { color:var(--muted);font-size:14px;line-height:1.9; }
.order-detail b { color:var(--text); }
.total-box {
    background:linear-gradient(135deg,#FFFFFF 0%,#FFF1F2 100%);
    padding:23px;
    border-radius:20px;
    border:2px solid var(--berry);
    text-align:center;
    margin-top:18px;
    box-shadow:0 9px 25px rgba(225,29,72,.12);
}
.total-money { font-size:32px;font-weight:950;color:var(--berry);margin:6px 0; }
.price-text { color:var(--berry);font-size:18px;font-weight:900; }
.badge-blue {
    display:inline-block;
    background:#FFE4E6;
    color:#9F1239!important;
    border:1px solid #FDA4AF;
    padding:5px 11px;
    border-radius:999px;
    font-weight:850;
    font-size:13px;
}
.badge-cute {
    display:inline-block;
    background:#FFF1F2;
    color:#881337!important;
    border:1px solid #FECDD3;
    border-radius:999px;
    padding:5px 10px;
    font-size:12px;
    font-weight:800;
    margin:2px;
}
.stTextInput input,.stNumberInput input,.stTextArea textarea,
.stSelectbox div[data-baseweb="select"]>div,
.stMultiSelect div[data-baseweb="select"]>div {
    background:#FFFFFF!important;
    color:var(--text)!important;
    border:1px solid #D1D5DB!important;
    border-radius:11px!important;
}
.stTextInput input::placeholder,.stTextArea textarea::placeholder { color:#9CA3AF!important; }
div[data-baseweb="select"] * { color:var(--text)!important; }
.stButton>button,.stDownloadButton>button,.stFormSubmitButton>button {
    border-radius:12px!important;
    border:1px solid var(--berry)!important;
    font-weight:850!important;
    min-height:42px;
}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"] {
    background:linear-gradient(135deg,#E11D48,#BE123C)!important;
    color:#FFFFFF!important;
    box-shadow:0 5px 14px rgba(225,29,72,.22);
}
.stDownloadButton>button { background:#FFFFFF!important;color:var(--berry-dark)!important; }
div[data-testid="stExpander"] {
    background:#FFFFFF;
    border:1px solid var(--berry-border);
    border-radius:14px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color:var(--berry-border)!important;
    border-radius:14px!important;
    background:#FFFFFF;
}
hr { border-color:#FECDD3!important; }
.admin-box {
    background:#FFFFFF;
    border:1px solid var(--berry-border);
    border-top:5px solid var(--berry-dark);
    border-radius:18px;
    padding:25px;
    margin:20px auto;
    max-width:720px;
    box-shadow:0 10px 28px rgba(136,19,55,.08);
}
.login-title {
    text-align:center;
    font-size:28px;
    font-weight:950;
    color:var(--berry-dark);
}
.history-card {
    background:#FFFFFF;
    border:1px solid var(--berry-border);
    border-left:6px solid var(--berry);
    border-radius:16px;
    padding:16px;
    margin-bottom:12px;
    box-shadow:0 6px 18px rgba(17,24,39,.05);
}
.paid-badge {
    display:inline-block;
    background:#DCFCE7;
    color:#166534!important;
    border:1px solid #86EFAC;
    padding:5px 10px;
    border-radius:999px;
    font-weight:800;
}
.edited-badge {
    display:inline-block;
    background:#FEF3C7;
    color:#92400E!important;
    border:1px solid #FCD34D;
    padding:5px 10px;
    border-radius:999px;
    font-weight:800;
}
@media(max-width:768px) {
    .block-container { padding-left:1rem;padding-right:1rem; }
    h1 { font-size:1.8rem!important; }
    .total-money { font-size:26px; }
    .order-builder { padding:15px; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DỮ LIỆU MẶC ĐỊNH
# ============================================================
DEFAULT_DATA = {
    "categories": [
        {"id":1,"name":"Trà sữa","visible":True},
        {"id":2,"name":"Trà trái cây","visible":True},
        {"id":3,"name":"Topping","visible":True}
    ],
    "products": [
        {"id":1,"category":"Trà sữa","name":"Trà sữa truyền thống","image":"","price":25000,
         "description":"Trà sữa truyền thống thơm béo","status":"Còn hàng","sizes":{"S":0,"M":5000,"L":10000}},
        {"id":2,"category":"Trà sữa","name":"Trà sữa matcha","image":"","price":30000,
         "description":"Trà sữa matcha thơm đậm vị","status":"Còn hàng","sizes":{"S":0,"M":5000,"L":10000}},
        {"id":3,"category":"Trà sữa","name":"Trà sữa socola","image":"","price":30000,
         "description":"Trà sữa socola","status":"Còn hàng","sizes":{"S":0,"M":5000,"L":10000}},
        {"id":4,"category":"Trà sữa","name":"Trà sữa khoai môn","image":"","price":30000,
         "description":"Khoai môn béo thơm","status":"Còn hàng","sizes":{"S":0,"M":5000,"L":10000}},
        {"id":5,"category":"Trà trái cây","name":"Trà đào cam sả","image":"","price":30000,
         "description":"Trà đào kết hợp cam và sả","status":"Còn hàng","sizes":{"S":0,"M":5000,"L":10000}},
        {"id":6,"category":"Trà trái cây","name":"Trà vải","image":"","price":28000,
         "description":"Trà vải thanh mát","status":"Còn hàng","sizes":{"S":0,"M":5000,"L":10000}}
    ],
    "toppings": [
        {"id":1,"name":"Trân châu đen","price":5000,"status":"Còn hàng","visible":True},
        {"id":2,"name":"Trân châu trắng","price":6000,"status":"Còn hàng","visible":True},
        {"id":3,"name":"Thạch trái cây","price":5000,"status":"Còn hàng","visible":True},
        {"id":4,"name":"Thạch phô mai","price":8000,"status":"Còn hàng","visible":True},
        {"id":5,"name":"Pudding trứng","price":7000,"status":"Còn hàng","visible":True}
    ],
    "invoices": []
}

# ============================================================
# DỮ LIỆU
# ============================================================
def normalize_data(data):
    """Bổ sung các khóa mới để code vẫn chạy với menu_data.json cũ."""
    if not isinstance(data, dict):
        data = deepcopy(DEFAULT_DATA)

    for key in ["categories","products","toppings","invoices"]:
        if key not in data or not isinstance(data[key], list):
            data[key] = deepcopy(DEFAULT_DATA[key])

    for product in data["products"]:
        product.setdefault("image","")
        product.setdefault("description","")
        product.setdefault("status","Còn hàng")
        product.setdefault("sizes",{"S":0,"M":5000,"L":10000})
        for size in ["S","M","L"]:
            product["sizes"].setdefault(size,0)

    for topping in data["toppings"]:
        topping.setdefault("visible",True)
        topping.setdefault("status","Còn hàng")

    return data


def load_data():
    if not os.path.exists(DATA_FILE):
        data = deepcopy(DEFAULT_DATA)
        with open(DATA_FILE,"w",encoding="utf-8") as file:
            json.dump(data,file,ensure_ascii=False,indent=4)
        return data

    try:
        with open(DATA_FILE,"r",encoding="utf-8") as file:
            return normalize_data(json.load(file))
    except Exception:
        return deepcopy(DEFAULT_DATA)


def save_data():
    with open(DATA_FILE,"w",encoding="utf-8") as file:
        json.dump(st.session_state.data,file,ensure_ascii=False,indent=4)


# ============================================================
# SESSION
# ============================================================
if "data" not in st.session_state:
    st.session_state.data = load_data()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "order_id" not in st.session_state:
    st.session_state.order_id = datetime.now().strftime("%Y%m%d%H%M%S")

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "editing_invoice_id" not in st.session_state:
    st.session_state.editing_invoice_id = None

if "last_paid_invoice_id" not in st.session_state:
    st.session_state.last_paid_invoice_id = None

# ============================================================
# TIỆN ÍCH
# ============================================================
def money(value):
    return f"{int(value):,} VNĐ".replace(",", ".")


def get_next_id(items):
    if not items:
        return 1
    return max(int(item.get("id",0)) for item in items) + 1


def calculate_item_total(item):
    product_price = float(item.get("price",0))
    size_price = float(item.get("size_price",0))
    topping_price = sum(float(t.get("price",0)) for t in item.get("toppings",[]))
    return int((product_price + size_price + topping_price) * int(item.get("quantity",1)))


def calculate_cart_total():
    return sum(calculate_item_total(item) for item in st.session_state.cart)


def reset_order():
    st.session_state.cart = []
    st.session_state.customer_name = ""
    st.session_state.order_id = datetime.now().strftime("%Y%m%d%H%M%S")
    st.session_state.editing_invoice_id = None


def find_invoice(invoice_id):
    for invoice in st.session_state.data["invoices"]:
        if str(invoice.get("id")) == str(invoice_id):
            return invoice
    return None


def snapshot_current_order(status="Đã thanh toán"):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return {
        "id": st.session_state.order_id,
        "customer_name": st.session_state.customer_name.strip() or "Khách lẻ",
        "created_at": now,
        "updated_at": now,
        "status": status,
        "items": deepcopy(st.session_state.cart),
        "total": calculate_cart_total(),
        "edit_count": 0
    }


def save_paid_invoice():
    """Lưu đơn đã thanh toán vào lịch sử."""
    invoice = snapshot_current_order("Đã thanh toán")
    old = find_invoice(invoice["id"])

    if old:
        invoice["created_at"] = old.get("created_at", invoice["created_at"])
        invoice["edit_count"] = old.get("edit_count",0)
        index = st.session_state.data["invoices"].index(old)
        st.session_state.data["invoices"][index] = invoice
    else:
        st.session_state.data["invoices"].append(invoice)

    save_data()
    st.session_state.last_paid_invoice_id = invoice["id"]
    return invoice


def start_edit_invoice(invoice_id):
    invoice = find_invoice(invoice_id)
    if not invoice:
        st.error("Không tìm thấy hóa đơn.")
        return False

    st.session_state.cart = deepcopy(invoice.get("items",[]))
    st.session_state.customer_name = invoice.get("customer_name","Khách lẻ")
    st.session_state.order_id = str(invoice["id"])
    st.session_state.editing_invoice_id = str(invoice["id"])
    return True


def update_invoice_from_cart():
    invoice = find_invoice(st.session_state.editing_invoice_id)
    if not invoice:
        return False

    invoice["items"] = deepcopy(st.session_state.cart)
    invoice["customer_name"] = st.session_state.customer_name.strip() or "Khách lẻ"
    invoice["total"] = calculate_cart_total()
    invoice["updated_at"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    invoice["edit_count"] = int(invoice.get("edit_count",0)) + 1
    invoice["status"] = "Đã thanh toán - Đã chỉnh sửa"
    save_data()
    return True


def invoice_to_txt(invoice):
    lines = [
        "="*64,
        "                    HÓA ĐƠN TRÀ SỮA",
        "="*64,
        f"Mã đơn: {invoice.get('id','')}",
        f"Thời gian tạo: {invoice.get('created_at','')}",
        f"Cập nhật: {invoice.get('updated_at',invoice.get('created_at',''))}",
        f"Khách hàng: {invoice.get('customer_name','Khách lẻ')}",
        f"Trạng thái: {invoice.get('status','')}",
        "-"*64
    ]

    for index,item in enumerate(invoice.get("items",[]),1):
        toppings = ", ".join(t["name"] for t in item.get("toppings",[])) or "Không"
        lines += [
            f"{index}. {item.get('name','')} - Size {item.get('size','S')}",
            f"   Số lượng: {item.get('quantity',1)}",
            f"   Đường: {item.get('sugar',100)}%",
            f"   Đá: {item.get('ice',100)}%",
            f"   Topping: {toppings}",
            f"   Ghi chú: {item.get('notes','') or 'Không'}",
            f"   Thành tiền: {money(calculate_item_total(item))}",
            "-"*64
        ]

    lines += [
        f"TỔNG THANH TOÁN: {money(invoice.get('total',0))}",
        "="*64,
        "              Cảm ơn quý khách!",
        "="*64
    ]
    return "\n".join(lines).encode("utf-8")


def invoice_to_html(invoice):
    rows = ""
    for index,item in enumerate(invoice.get("items",[]),1):
        toppings = ", ".join(t["name"] for t in item.get("toppings",[])) or "Không"
        rows += f"""
        <tr>
            <td>{index}</td>
            <td>{html.escape(str(item.get('name','')))}</td>
            <td>{html.escape(str(item.get('size','S')))}</td>
            <td>{item.get('quantity',1)}</td>
            <td>{item.get('sugar',100)}%</td>
            <td>{item.get('ice',100)}%</td>
            <td>{html.escape(toppings)}</td>
            <td>{html.escape(str(item.get('notes','') or 'Không'))}</td>
            <td>{money(calculate_item_total(item))}</td>
        </tr>
        """

    customer = html.escape(str(invoice.get("customer_name","Khách lẻ")))
    invoice_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Hóa đơn {html.escape(str(invoice.get('id','')))}</title>
<style>
body{{font-family:Arial,sans-serif;margin:30px;color:#111827}}
h1{{text-align:center;color:#881337}}
table{{width:100%;border-collapse:collapse}}
th,td{{border:1px solid #999;padding:8px;text-align:center}}
th{{background:#FFE4E6}}
.total{{text-align:right;font-size:24px;font-weight:bold;margin-top:20px;color:#E11D48}}
</style>
</head>
<body>
<h1>🧋 HÓA ĐƠN TRÀ SỮA</h1>
<p><b>Mã đơn:</b> {invoice.get('id','')}</p>
<p><b>Thời gian:</b> {invoice.get('created_at','')}</p>
<p><b>Cập nhật:</b> {invoice.get('updated_at',invoice.get('created_at',''))}</p>
<p><b>Khách hàng:</b> {customer}</p>
<p><b>Trạng thái:</b> {html.escape(str(invoice.get('status','')))}</p>
<table>
<thead><tr>
<th>#</th><th>Món</th><th>Size</th><th>SL</th><th>Đường</th>
<th>Đá</th><th>Topping</th><th>Ghi chú</th><th>Thành tiền</th>
</tr></thead>
<tbody>{rows}</tbody>
</table>
<div class="total">TỔNG THANH TOÁN: {money(invoice.get('total',0))}</div>
<center><b>Cảm ơn quý khách đã sử dụng dịch vụ!</b></center>
</body>
</html>"""
    return invoice_html.encode("utf-8")


# ============================================================
# LOGIN
# ============================================================
def admin_login():
    st.markdown('<div class="admin-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 ADMIN LOGIN</div>', unsafe_allow_html=True)
    st.info("Khu vực này dành riêng cho quản trị viên.")

    username = st.text_input("👤 Tên đăng nhập", placeholder="Nhập username...")
    password = st.text_input("🔑 Mật khẩu", type="password", placeholder="Nhập mật khẩu...")

    if st.button("🔐 ĐĂNG NHẬP ADMIN", type="primary", use_container_width=True):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.success("Đăng nhập Admin thành công!")
            st.rerun()
        else:
            st.error("❌ Tên đăng nhập hoặc mật khẩu không đúng.")

    st.markdown("</div>", unsafe_allow_html=True)


def admin_logout():
    st.session_state.admin_logged_in = False
    st.success("Đã đăng xuất Admin.")
    st.rerun()


# ============================================================
# HEADER / SIDEBAR
# ============================================================
st.title("🧋 HÓA ĐƠN TRÀ SỮA")
st.caption("Hệ thống Order • Tính Bill • Quản lý món • Lịch sử hóa đơn • Admin")

st.sidebar.title("📌 MENU")

if st.session_state.admin_logged_in:
    st.sidebar.success("🔓 ADMIN ĐANG ĐĂNG NHẬP")
    st.sidebar.write(f"👤 {ADMIN_USERNAME}")
    menu_options = [
        "🛒 Đặt hàng",
        "🧾 Lịch sử hóa đơn",
        "📋 Quản lý danh mục",
        "🍹 Quản lý món",
        "🥤 Quản lý topping",
        "⚙️ Tài khoản Admin"
    ]
else:
    menu_options = ["🛒 Đặt hàng", "🔐 Đăng nhập Admin"]

menu = st.sidebar.radio("Chọn chức năng", menu_options)

if st.session_state.admin_logged_in:
    st.sidebar.divider()
    if st.sidebar.button("🚪 Đăng xuất Admin", use_container_width=True):
        admin_logout()

# ============================================================
# ĐĂNG NHẬP ADMIN
# ============================================================
if menu == "🔐 Đăng nhập Admin":
    st.header("🔐 ĐĂNG NHẬP QUẢN TRỊ")
    admin_login()

# ============================================================
# ĐẶT HÀNG
# ============================================================
elif menu == "🛒 Đặt hàng":
    st.header("💗 TẠO ĐƠN HÀNG")

    # --------------------------------------------------------
    # Nếu đang sửa hóa đơn đã thanh toán
    # --------------------------------------------------------
    if st.session_state.editing_invoice_id:
        editing = find_invoice(st.session_state.editing_invoice_id)
        if editing:
            st.warning(
                f"✏️ Bạn đang sửa hóa đơn đã thanh toán "
                f"#{editing['id']}. Sau khi lưu, hóa đơn cũ sẽ được cập nhật."
            )
            c1,c2 = st.columns(2)
            with c1:
                st.info(f"Khách hàng: {editing.get('customer_name','Khách lẻ')}")
            with c2:
                st.info(f"Tổng hiện tại: {money(calculate_cart_total())}")

            if st.button("❌ HỦY CHỈNH SỬA", use_container_width=True):
                reset_order()
                st.rerun()

    customer_name = st.text_input(
        "🐰 Tên khách hàng",
        value=st.session_state.customer_name,
        placeholder="Nhập tên khách hàng..."
    )
    st.session_state.customer_name = customer_name

    st.markdown(
        "<span class='badge-cute'>🌷 Chọn món yêu thích • Tùy chỉnh theo gu • Order thật cute ✨</span>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="order-builder">
        <div class="cute-title"><span class="cute-icon">🧋</span>Chọn nhiều món trong một lần Order 💕</div>
        <div class="cute-subtitle">Có thể chọn nhiều món, chỉnh size, đường, đá, topping và ghi chú riêng.</div>
    </div>
    """, unsafe_allow_html=True)

    visible_categories = [
        c["name"] for c in st.session_state.data["categories"]
        if c.get("visible",True)
    ]

    if not visible_categories:
        st.warning("Hiện chưa có danh mục đang hiển thị.")
    else:
        selected_categories = st.multiselect(
            "🩷 Danh mục — chọn nhiều",
            visible_categories,
            default=[visible_categories[0]]
        )

        available_products = [
            p for p in st.session_state.data["products"]
            if p.get("category") in selected_categories
            and p.get("status") == "Còn hàng"
        ]

        if not selected_categories:
            st.info("Hãy chọn ít nhất một danh mục.")
        elif not available_products:
            st.warning("Các danh mục đã chọn hiện chưa có món còn hàng.")
        else:
            product_labels = [
                f"{p['name']} • {p['category']} • {money(p['price'])}"
                for p in available_products
            ]
            label_to_product = dict(zip(product_labels,available_products))

            selected_product_labels = st.multiselect(
                "🌸 Chọn món — có thể chọn nhiều món",
                product_labels
            )

            selected_products = [label_to_product[x] for x in selected_product_labels]

            if selected_products:
                st.markdown(
                    f"<span class='badge-blue'>Đã chọn {len(selected_products)} món</span>",
                    unsafe_allow_html=True
                )
                configured_items = []

                for product_index,product in enumerate(selected_products):
                    st.markdown(
                        f"""
                        <div class="item-config-card">
                            <div class="item-config-title">🧋 {product_index+1}. {html.escape(product['name'])}</div>
                            <div class="cute-subtitle">{html.escape(product.get('description','') or 'Không có mô tả')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    image_col,config_col = st.columns([1,3])

                    with image_col:
                        if product.get("image"):
                            try:
                                st.image(product["image"],use_container_width=True)
                            except Exception:
                                pass
                        st.markdown(
                            f"<div class='price-text'>Từ {money(product['price'])}</div>",
                            unsafe_allow_html=True
                        )

                    with config_col:
                        size = st.radio(
                            "🎀 Size",["S","M","L"],
                            horizontal=True,
                            key=f"multi_size_{product['id']}"
                        )
                        size_price = product.get("sizes",{}).get(size,0)
                        current_price = product["price"] + size_price

                        c1,c2,c3 = st.columns(3)
                        with c1:
                            quantity = st.number_input(
                                "🐻 Số lượng",1,100,1,1,
                                key=f"multi_qty_{product['id']}"
                            )
                        with c2:
                            sugar = st.selectbox(
                                "🍬 Đường",[100,70,50,30,10,0],
                                format_func=lambda v:f"{v}%",
                                key=f"multi_sugar_{product['id']}"
                            )
                        with c3:
                            ice = st.selectbox(
                                "🧊 Đá",[100,70,50,30,10,0],
                                format_func=lambda v:f"{v}%",
                                key=f"multi_ice_{product['id']}"
                            )

                        st.caption(f"Giá Size {size}: {money(current_price)} / ly")

                        available_toppings = [
                            t for t in st.session_state.data["toppings"]
                            if t.get("visible",True) and t.get("status")=="Còn hàng"
                        ]
                        topping_options = {
                            f"{t['name']} (+{money(t['price'])})":t
                            for t in available_toppings
                        }

                        selected_topping_labels = st.multiselect(
                            "🍓 Topping — có thể chọn nhiều",
                            list(topping_options.keys()),
                            key=f"multi_toppings_{product['id']}"
                        )
                        selected_toppings = [
                            topping_options[x] for x in selected_topping_labels
                        ]

                        selected_notes = st.multiselect(
                            "💌 Ghi chú nhanh",
                            ["Nhiều sữa","Không lấy ống hút","Uống tại chỗ","Mang về"],
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

                    configured_items.append({
                        "name":product["name"],
                        "price":product["price"],
                        "size":size,
                        "size_price":size_price,
                        "quantity":quantity,
                        "sugar":sugar,
                        "ice":ice,
                        "toppings":deepcopy(selected_toppings),
                        "notes":notes
                    })

                    st.info(
                        f"💗 {product['name']} • {quantity} ly • Thành tiền: **{money(calculate_item_total(configured_items[-1]))}**"
                    )
                    st.divider()

                selected_total = sum(calculate_item_total(x) for x in configured_items)

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
                    use_container_width=True
                ):
                    st.session_state.cart.extend(configured_items)
                    st.success(f"Đã thêm {len(configured_items)} món vào đơn hàng!")
                    st.rerun()
            else:
                st.info("Chưa chọn món. Hãy chọn món ở ô phía trên để cấu hình.")

    # --------------------------------------------------------
    # CHI TIẾT ĐƠN
    # --------------------------------------------------------
    st.divider()
    st.header("🧾 CHI TIẾT ĐƠN HÀNG 💗")

    if not st.session_state.cart:
        st.info("Chưa có món trong đơn.")
    else:
        for index,item in enumerate(st.session_state.cart):
            item_total = calculate_item_total(item)
            toppings_text = ", ".join(t["name"] for t in item.get("toppings",[])) or "Không"

            st.markdown(
                f"""
                <div class="order-card">
                    <div class="order-title">🧋 {index+1}. {html.escape(item['name'])}</div>
                    <div class="order-detail">
                        📏 <b>Size:</b> {item['size']}<br>
                        🔢 <b>Số lượng:</b> {item['quantity']}<br>
                        🍬 <b>Đường:</b> {item['sugar']}%<br>
                        🧊 <b>Đá:</b> {item['ice']}%<br>
                        🍓 <b>Topping:</b> {html.escape(toppings_text)}<br>
                        📝 <b>Ghi chú:</b> {html.escape(item.get('notes','') or 'Không')}<br>
                        💰 <b>Thành tiền:</b> {money(item_total)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            _,delete_col = st.columns([6,1])
            with delete_col:
                if st.button("🗑️ Xóa món",key=f"delete_cart_{index}",use_container_width=True):
                    st.session_state.cart.pop(index)
                    st.rerun()

        total = calculate_cart_total()

        st.markdown(
            f"""
            <div class="total-box">
                <div style="color:#475569;">👤 Khách hàng:
                    <b style="color:#0F172A;">{html.escape(st.session_state.customer_name or 'Khách lẻ')}</b>
                </div>
                <div style="margin-top:8px;color:#475569;">🧾 Số món:
                    <b style="color:#0F172A;">{len(st.session_state.cart)}</b>
                </div>
                <div class="total-money">💰 {money(total)}</div>
                <div style="color:#475569;">TỔNG SỐ TIỀN CẦN THANH TOÁN</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # ----------------------------------------------------
        # THANH TOÁN / CẬP NHẬT
        # ----------------------------------------------------
        if st.session_state.editing_invoice_id:
            st.subheader("✏️ CẬP NHẬT ĐƠN ĐÃ THANH TOÁN")
            st.info(
                "Sau khi cập nhật, lịch sử sẽ giữ nguyên mã đơn và ghi nhận số lần chỉnh sửa."
            )

            c1,c2 = st.columns(2)
            with c1:
                if st.button(
                    "💾 LƯU THAY ĐỔI ĐƠN ĐÃ THANH TOÁN",
                    type="primary",
                    use_container_width=True
                ):
                    if update_invoice_from_cart():
                        st.success("✅ Đã cập nhật hóa đơn thành công!")
                        st.session_state.last_paid_invoice_id = st.session_state.editing_invoice_id
                        st.session_state.editing_invoice_id = None
                        st.rerun()

            with c2:
                if st.button("❌ HỦY SỬA ĐƠN",use_container_width=True):
                    reset_order()
                    st.rerun()
        else:
            st.subheader("💳 THANH TOÁN")
            st.caption("Bấm nút thanh toán để lưu hóa đơn vào lịch sử. Hóa đơn vẫn có thể được sửa sau khi thanh toán.")

            if st.button(
                f"💳 XÁC NHẬN THANH TOÁN • {money(total)}",
                type="primary",
                use_container_width=True
            ):
                invoice = save_paid_invoice()
                st.success(
                    f"🎉 Thanh toán thành công! Mã hóa đơn: #{invoice['id']}"
                )

                txt_data = invoice_to_txt(invoice)
                html_data = invoice_to_html(invoice)

                c1,c2,c3 = st.columns(3)
                with c1:
                    st.download_button(
                        "📄 Tải hóa đơn TXT",
                        txt_data,
                        file_name=f"hoa_don_{invoice['id']}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with c2:
                    st.download_button(
                        "🌐 Tải hóa đơn HTML",
                        html_data,
                        file_name=f"hoa_don_{invoice['id']}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                with c3:
                    if st.button("🆕 TẠO ĐƠN MỚI",use_container_width=True):
                        reset_order()
                        st.rerun()

        # ----------------------------------------------------
        # SỬA ĐƠN VỪA THANH TOÁN
        # ----------------------------------------------------
        if st.session_state.last_paid_invoice_id and not st.session_state.editing_invoice_id:
            recent_invoice = find_invoice(st.session_state.last_paid_invoice_id)
            if recent_invoice:
                st.divider()
                st.subheader("✏️ SỬA ĐƠN VỪA THANH TOÁN")
                st.write(
                    f"Hóa đơn gần nhất: **#{recent_invoice['id']}** • "
                    f"Tổng: **{money(recent_invoice['total'])}**"
                )
                if st.button(
                    "✏️ MỞ HÓA ĐƠN GẦN NHẤT ĐỂ SỬA",
                    use_container_width=True
                ):
                    start_edit_invoice(recent_invoice["id"])
                    st.rerun()

        st.divider()
        st.subheader("📤 XUẤT HÓA ĐƠN HIỆN TẠI")

        current_invoice = snapshot_current_order(
            "Đang chỉnh sửa" if st.session_state.editing_invoice_id else "Chưa thanh toán"
        )
        txt_data = invoice_to_txt(current_invoice)
        html_data = invoice_to_html(current_invoice)

        c1,c2 = st.columns(2)
        with c1:
            st.download_button(
                "📄 Tải hóa đơn TXT",
                txt_data,
                file_name=f"hoa_don_{st.session_state.order_id}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with c2:
            st.download_button(
                "🌐 Tải hóa đơn HTML",
                html_data,
                file_name=f"hoa_don_{st.session_state.order_id}.html",
                mime="text/html",
                use_container_width=True
            )

        if st.button("🗑️ TẠO ĐƠN MỚI",use_container_width=True):
            reset_order()
            st.rerun()

# ============================================================
# LỊCH SỬ HÓA ĐƠN - ADMIN
# ============================================================
elif menu == "🧾 Lịch sử hóa đơn":
    if not st.session_state.admin_logged_in:
        st.error("🔒 Bạn phải đăng nhập Admin.")
        st.stop()

    st.header("🧾 LỊCH SỬ HÓA ĐƠN")
    invoices = st.session_state.data["invoices"]

    if not invoices:
        st.info("Chưa có hóa đơn nào được lưu.")
    else:
        # Thống kê
        total_revenue = sum(int(x.get("total",0)) for x in invoices)
        total_orders = len(invoices)
        edited_orders = sum(1 for x in invoices if "chỉnh sửa" in x.get("status","").lower())

        a,b,c = st.columns(3)
        a.metric("🧾 Tổng hóa đơn",total_orders)
        b.metric("💰 Tổng doanh thu",money(total_revenue))
        c.metric("✏️ Hóa đơn đã sửa",edited_orders)

        st.divider()

        # Bộ lọc
        search = st.text_input(
            "🔎 Tìm theo mã đơn hoặc tên khách hàng",
            placeholder="Ví dụ: 20261008123456 hoặc Nguyễn Văn A"
        )

        filtered = [
            x for x in reversed(invoices)
            if not search.strip()
            or search.lower() in str(x.get("id","")).lower()
            or search.lower() in str(x.get("customer_name","")).lower()
        ]

        st.write(f"Hiển thị **{len(filtered)} / {len(invoices)}** hóa đơn.")

        for invoice in filtered:
            invoice_id = str(invoice.get("id",""))
            status = invoice.get("status","Đã thanh toán")
            badge = (
                '<span class="edited-badge">✏️ ĐÃ CHỈNH SỬA</span>'
                if "chỉnh sửa" in status.lower()
                else '<span class="paid-badge">✅ ĐÃ THANH TOÁN</span>'
            )

            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="history-card">
                        <div style="font-size:20px;font-weight:900;color:#881337;">
                            🧾 Hóa đơn #{html.escape(invoice_id)}
                        </div>
                        <div style="margin-top:7px;">{badge}</div>
                        <div style="margin-top:10px;color:#475569;">
                            👤 Khách hàng: <b>{html.escape(str(invoice.get('customer_name','Khách lẻ')))}</b><br>
                            🕒 Tạo lúc: <b>{html.escape(str(invoice.get('created_at','')))}</b><br>
                            🔄 Cập nhật: <b>{html.escape(str(invoice.get('updated_at',invoice.get('created_at',''))))}</b><br>
                            🧋 Số món: <b>{len(invoice.get('items',[]))}</b><br>
                            ✏️ Số lần sửa: <b>{invoice.get('edit_count',0)}</b><br>
                            💰 Tổng tiền: <b style="color:#E11D48;font-size:18px;">{money(invoice.get('total',0))}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                c1,c2,c3,c4 = st.columns(4)

                with c1:
                    if st.button("👁️ XEM CHI TIẾT",key=f"view_history_{invoice_id}",use_container_width=True):
                        st.session_state[f"show_invoice_{invoice_id}"] = not st.session_state.get(f"show_invoice_{invoice_id}",False)

                with c2:
                    if st.button("✏️ SỬA ĐƠN",key=f"edit_history_{invoice_id}",use_container_width=True):
                        start_edit_invoice(invoice_id)
                        st.success("Đã chuyển hóa đơn sang chế độ chỉnh sửa.")
                        st.rerun()

                with c3:
                    st.download_button(
                        "📄 TXT",
                        invoice_to_txt(invoice),
                        file_name=f"hoa_don_{invoice_id}.txt",
                        mime="text/plain",
                        key=f"download_txt_{invoice_id}",
                        use_container_width=True
                    )

                with c4:
                    if st.button("🗑️ XÓA",key=f"delete_history_{invoice_id}",use_container_width=True):
                        st.session_state.data["invoices"] = [
                            x for x in st.session_state.data["invoices"]
                            if str(x.get("id")) != invoice_id
                        ]
                        save_data()
                        st.success(f"Đã xóa hóa đơn #{invoice_id}.")
                        st.rerun()

                if st.session_state.get(f"show_invoice_{invoice_id}",False):
                    st.markdown("#### 📋 Chi tiết món")
                    for i,item in enumerate(invoice.get("items",[]),1):
                        toppings = ", ".join(t["name"] for t in item.get("toppings",[])) or "Không"
                        st.write(
                            f"**{i}. {item.get('name','')}** — "
                            f"Size {item.get('size','S')} — "
                            f"{item.get('quantity',1)} ly — "
                            f"Đường {item.get('sugar',100)}% — "
                            f"Đá {item.get('ice',100)}% — "
                            f"Topping: {toppings} — "
                            f"**{money(calculate_item_total(item))}**"
                        )

        st.divider()
        st.subheader("🗑️ QUẢN LÝ LỊCH SỬ")

        c1,c2 = st.columns(2)

        with c1:
            all_history_txt = "\n\n".join(
                invoice_to_txt(x).decode("utf-8")
                for x in reversed(invoices)
            )
            st.download_button(
                "📥 TẢI TOÀN BỘ LỊCH SỬ (.TXT)",
                all_history_txt.encode("utf-8"),
                file_name="lich_su_hoa_don.txt",
                mime="text/plain",
                use_container_width=True
            )

        with c2:
            if st.button(
                "🗑️ XÓA TOÀN BỘ LỊCH SỬ",
                use_container_width=True
            ):
                st.session_state.data["invoices"] = []
                save_data()
                st.success("Đã xóa toàn bộ lịch sử hóa đơn.")
                st.rerun()

# ============================================================
# QUẢN LÝ DANH MỤC
# ============================================================
elif menu == "📋 Quản lý danh mục":
    if not st.session_state.admin_logged_in:
        st.error("🔒 Bạn phải đăng nhập Admin.")
        st.stop()

    st.header("📋 QUẢN LÝ DANH MỤC")

    new_category = st.text_input(
        "Tên danh mục",
        placeholder="Ví dụ: Cà phê, Đá xay..."
    )

    if st.button("➕ TẠO DANH MỤC",type="primary"):
        new_category = new_category.strip()
        if not new_category:
            st.error("Vui lòng nhập tên danh mục.")
        elif any(c["name"].lower()==new_category.lower() for c in st.session_state.data["categories"]):
            st.error("Danh mục đã tồn tại.")
        else:
            st.session_state.data["categories"].append({
                "id":get_next_id(st.session_state.data["categories"]),
                "name":new_category,
                "visible":True
            })
            save_data()
            st.success("Đã tạo danh mục.")
            st.rerun()

    st.divider()
    for category in st.session_state.data["categories"]:
        with st.container(border=True):
            c1,c2,c3 = st.columns([4,2,2])
            with c1:
                st.write(f"### 📂 {category['name']}")
            with c2:
                st.success("👁️ Đang hiển thị") if category["visible"] else st.warning("🙈 Đang ẩn")
            with c3:
                text = "🙈 Ẩn" if category["visible"] else "👁️ Hiện"
                if st.button(text,key=f"toggle_cat_{category['id']}",use_container_width=True):
                    category["visible"] = not category["visible"]
                    save_data()
                    st.rerun()

            edit_name = st.text_input(
                "Sửa tên danh mục",
                value=category["name"],
                key=f"edit_cat_{category['id']}"
            )
            c1,c2 = st.columns(2)
            with c1:
                if st.button("💾 LƯU TÊN",key=f"save_cat_{category['id']}",use_container_width=True):
                    old = category["name"]
                    new = edit_name.strip()
                    if not new:
                        st.error("Tên danh mục không được để trống.")
                    else:
                        category["name"] = new
                        for p in st.session_state.data["products"]:
                            if p["category"] == old:
                                p["category"] = new
                        save_data()
                        st.rerun()
            with c2:
                if st.button("🗑️ XÓA DANH MỤC",key=f"del_cat_{category['id']}",use_container_width=True):
                    used = any(p["category"]==category["name"] for p in st.session_state.data["products"])
                    if used:
                        st.error("Không thể xóa vì đang có món thuộc danh mục này.")
                    else:
                        st.session_state.data["categories"].remove(category)
                        save_data()
                        st.rerun()

# ============================================================
# QUẢN LÝ MÓN
# ============================================================
elif menu == "🍹 Quản lý món":
    if not st.session_state.admin_logged_in:
        st.error("🔒 Bạn phải đăng nhập Admin.")
        st.stop()

    st.header("🍹 QUẢN LÝ MÓN")

    categories = [c["name"] for c in st.session_state.data["categories"]]

    if categories:
        st.subheader("➕ THÊM MÓN MỚI")
        with st.form("add_product_form"):
            c1,c2 = st.columns(2)
            with c1:
                product_name = st.text_input("Tên món")
                category = st.selectbox("Danh mục",categories)
                base_price = st.number_input("Giá bán cơ bản",0,10000000,25000,1000)
                description = st.text_area("Mô tả món")
            with c2:
                image_url = st.text_input("URL hình ảnh",placeholder="https://...")
                status = st.selectbox("Trạng thái",["Còn hàng","Hết hàng"])
                size_s = st.number_input("Size S (+)",0,1000000,0,1000)
                size_m = st.number_input("Size M (+)",0,1000000,5000,1000)
                size_l = st.number_input("Size L (+)",0,1000000,10000,1000)

            submitted = st.form_submit_button("➕ THÊM MÓN",type="primary")

        if submitted:
            product_name = product_name.strip()
            if not product_name:
                st.error("Vui lòng nhập tên món.")
            else:
                st.session_state.data["products"].append({
                    "id":get_next_id(st.session_state.data["products"]),
                    "category":category,
                    "name":product_name,
                    "image":image_url.strip(),
                    "price":base_price,
                    "description":description.strip(),
                    "status":status,
                    "sizes":{"S":size_s,"M":size_m,"L":size_l}
                })
                save_data()
                st.success("Đã thêm món mới.")
                st.rerun()
    else:
        st.warning("Hãy tạo danh mục trước.")

    st.divider()
    st.subheader("📋 DANH SÁCH MÓN")

    for product in st.session_state.data["products"]:
        with st.expander(f"🧋 {product['name']} – {money(product['price'])}"):
            image_col,info_col = st.columns([1,3])
            with image_col:
                if product.get("image"):
                    try:
                        st.image(product["image"],use_container_width=True)
                    except Exception:
                        pass
            with info_col:
                st.write(f"**Danh mục:** {product['category']}")
                st.write(f"**Giá:** {money(product['price'])}")
                st.write(f"**Size S/M/L:** +{money(product['sizes']['S'])} / +{money(product['sizes']['M'])} / +{money(product['sizes']['L'])}")
                st.write(f"**Trạng thái:** {product['status']}")
                st.write(product.get("description",""))

            st.markdown("### ✏️ CHỈNH SỬA MÓN")
            c1,c2 = st.columns(2)
            with c1:
                edit_name = st.text_input("Tên món",product["name"],key=f"pn_{product['id']}")
                edit_category = st.selectbox(
                    "Danh mục",categories,
                    index=categories.index(product["category"]) if product["category"] in categories else 0,
                    key=f"pc_{product['id']}"
                )
                edit_price = st.number_input("Giá cơ bản",0,10000000,int(product["price"]),1000,key=f"pp_{product['id']}")
            with c2:
                edit_image = st.text_input("URL hình ảnh",product.get("image",""),key=f"pi_{product['id']}")
                edit_status = st.selectbox(
                    "Trạng thái",["Còn hàng","Hết hàng"],
                    index=0 if product["status"]=="Còn hàng" else 1,
                    key=f"ps_{product['id']}"
                )
                edit_description = st.text_area("Mô tả",product.get("description",""),key=f"pd_{product['id']}")

            s1,s2,s3 = st.columns(3)
            with s1:
                edit_s = st.number_input("Size S +",0,1000000,int(product["sizes"]["S"]),1000,key=f"pns_{product['id']}")
            with s2:
                edit_m = st.number_input("Size M +",0,1000000,int(product["sizes"]["M"]),1000,key=f"pnm_{product['id']}")
            with s3:
                edit_l = st.number_input("Size L +",0,1000000,int(product["sizes"]["L"]),1000,key=f"pnl_{product['id']}")

            c1,c2 = st.columns(2)
            with c1:
                if st.button("💾 LƯU THAY ĐỔI",key=f"save_p_{product['id']}",type="primary",use_container_width=True):
                    product.update({
                        "name":edit_name.strip(),
                        "category":edit_category,
                        "price":edit_price,
                        "image":edit_image.strip(),
                        "status":edit_status,
                        "description":edit_description.strip(),
                        "sizes":{"S":edit_s,"M":edit_m,"L":edit_l}
                    })
                    save_data()
                    st.success("Đã cập nhật món.")
                    st.rerun()
            with c2:
                if st.button("🗑️ XÓA MÓN",key=f"del_p_{product['id']}",use_container_width=True):
                    st.session_state.data["products"].remove(product)
                    save_data()
                    st.rerun()

# ============================================================
# QUẢN LÝ TOPPING
# ============================================================
elif menu == "🥤 Quản lý topping":
    if not st.session_state.admin_logged_in:
        st.error("🔒 Bạn phải đăng nhập Admin.")
        st.stop()

    st.header("🥤 QUẢN LÝ TOPPING")

    with st.form("add_topping_form"):
        topping_name = st.text_input("Tên topping")
        topping_price = st.number_input("Giá topping",0,1000000,5000,1000)
        topping_status = st.selectbox("Trạng thái",["Còn hàng","Hết hàng"])
        topping_submit = st.form_submit_button("➕ THÊM TOPPING",type="primary")

    if topping_submit:
        topping_name = topping_name.strip()
        if not topping_name:
            st.error("Vui lòng nhập tên topping.")
        else:
            st.session_state.data["toppings"].append({
                "id":get_next_id(st.session_state.data["toppings"]),
                "name":topping_name,
                "price":topping_price,
                "status":topping_status,
                "visible":True
            })
            save_data()
            st.success("Đã thêm topping.")
            st.rerun()

    st.divider()
    for topping in st.session_state.data["toppings"]:
        with st.expander(f"🧋 {topping['name']} – {money(topping['price'])}"):
            name = st.text_input("Tên topping",topping["name"],key=f"tn_{topping['id']}")
            price = st.number_input("Giá",0,1000000,int(topping["price"]),1000,key=f"tp_{topping['id']}")
            status = st.selectbox(
                "Trạng thái",["Còn hàng","Hết hàng"],
                index=0 if topping["status"]=="Còn hàng" else 1,
                key=f"ts_{topping['id']}"
            )

            c1,c2,c3 = st.columns(3)
            with c1:
                if st.button("💾 LƯU",key=f"save_t_{topping['id']}",use_container_width=True):
                    topping["name"] = name.strip()
                    topping["price"] = price
                    topping["status"] = status
                    save_data()
                    st.rerun()
            with c2:
                text = "🙈 ẨN" if topping["visible"] else "👁️ HIỆN"
                if st.button(text,key=f"vis_t_{topping['id']}",use_container_width=True):
                    topping["visible"] = not topping["visible"]
                    save_data()
                    st.rerun()
            with c3:
                if st.button("🗑️ XÓA",key=f"del_t_{topping['id']}",use_container_width=True):
                    st.session_state.data["toppings"].remove(topping)
                    save_data()
                    st.rerun()

# ============================================================
# TÀI KHOẢN ADMIN
# ============================================================
elif menu == "⚙️ Tài khoản Admin":
    if not st.session_state.admin_logged_in:
        st.error("🔒 Bạn phải đăng nhập Admin.")
        st.stop()

    st.header("⚙️ TÀI KHOẢN ADMIN")
    st.success("🔓 Bạn đang đăng nhập với quyền Admin.")
    st.write(f"👤 **Username:** {ADMIN_USERNAME}")
    st.write("🔐 **Mật khẩu:** ********")
    st.info(
        "Mật khẩu được lấy từ Streamlit Secrets. "
        "Nếu chưa thiết lập Secrets, tài khoản test mặc định là admin / 123456."
    )

    st.divider()
    if st.button("🚪 ĐĂNG XUẤT ADMIN",type="primary"):
        admin_logout()

# ============================================================
# FOOTER
# ============================================================
st.sidebar.divider()
st.sidebar.success("🔓 ADMIN MODE") if st.session_state.admin_logged_in else st.sidebar.info("👤 USER MODE")
st.sidebar.caption("🧋 Milk Tea Order & Billing")
st.sidebar.caption("Order • Tính bill • Lịch sử • Quản lý món • Admin")
