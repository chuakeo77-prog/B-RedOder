import streamlit as st
from datetime import datetime
from pathlib import Path
import json
import html
import uuid
import copy
import os

# ============================================================
# CẤU HÌNH
# ============================================================
st.set_page_config(
    page_title="Order & Bill Trà Sữa",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path("menu_data.json")

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "123456"

# ============================================================
# CSS
# ============================================================
st.markdown(
    """
<style>
:root{
    --berry:#E11D48;
    --berry-dark:#881337;
    --berry-soft:#FFF1F2;
    --berry-light:#FFE4E6;
    --border:#FECDD3;
    --text:#111827;
    --muted:#64748B;
}
.stApp{
    background:linear-gradient(135deg,#FFF1F2 0%,#FFF8F9 50%,#FFE4E6 100%);
    color:var(--text);
}
.block-container{
    max-width:1400px;
    padding-top:1.2rem;
    padding-bottom:3rem;
}
h1,h2,h3,h4,h5,h6{
    color:var(--text)!important;
    font-weight:850!important;
}
h1{text-align:center;font-size:2.3rem!important;}
h2,h3{color:var(--berry-dark)!important;}
p,label,.stMarkdown,.stCaption{color:var(--muted);}
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#881337 0%,#9F1239 50%,#4C0519 100%);
}
section[data-testid="stSidebar"] *{color:#fff!important;}
section[data-testid="stSidebar"] .stRadio label{
    background:rgba(255,255,255,.08);
    border:1px solid rgba(255,255,255,.08);
    border-radius:12px;
    padding:8px 10px;
    margin:3px 0;
}
.card{
    background:#fff;
    border:1px solid var(--border);
    border-radius:18px;
    padding:18px;
    margin:10px 0;
    box-shadow:0 7px 22px rgba(136,19,55,.07);
}
.card-title{
    color:var(--berry-dark);
    font-size:19px;
    font-weight:900;
}
.total-box{
    background:linear-gradient(135deg,#fff,#fff1f2);
    border:2px solid var(--berry);
    border-radius:20px;
    padding:22px;
    text-align:center;
    margin:18px 0;
}
.total-money{
    color:var(--berry);
    font-size:31px;
    font-weight:950;
}
.badge{
    display:inline-block;
    background:#fff1f2;
    color:#9f1239!important;
    border:1px solid #fda4af;
    padding:5px 10px;
    border-radius:999px;
    font-size:12px;
    font-weight:800;
    margin:2px;
}
.price{
    color:var(--berry);
    font-weight:900;
    font-size:18px;
}
.stButton>button,.stDownloadButton>button,.stFormSubmitButton>button{
    border-radius:12px!important;
    font-weight:800!important;
    min-height:42px;
}
.stButton>button[kind="primary"],
.stFormSubmitButton>button[kind="primary"]{
    background:linear-gradient(135deg,#E11D48,#BE123C)!important;
    color:#fff!important;
    border:1px solid #E11D48!important;
}
.stTextInput input,.stNumberInput input,.stTextArea textarea,
.stSelectbox div[data-baseweb="select"]>div,
.stMultiSelect div[data-baseweb="select"]>div{
    background:#fff!important;
    color:#111827!important;
    border-radius:11px!important;
}
div[data-baseweb="select"] *{color:#111827!important;}
hr{border-color:#fecdd3!important;}
@media(max-width:768px){
    .block-container{padding-left:1rem;padding-right:1rem;}
    h1{font-size:1.8rem!important;}
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# DỮ LIỆU MẶC ĐỊNH
# ============================================================
DEFAULT_DATA = {
    "categories": [
        {"id": 1, "name": "Trà sữa", "visible": True},
        {"id": 2, "name": "Trà trái cây", "visible": True},
        {"id": 3, "name": "Topping", "visible": True},
    ],
    "products": [
        {
            "id": 1, "category": "Trà sữa",
            "name": "Trà sữa truyền thống", "image": "",
            "price": 25000,
            "description": "Trà sữa truyền thống thơm béo",
            "status": "Còn hàng", "sizes": {"S": 0, "M": 5000, "L": 10000},
        },
        {
            "id": 2, "category": "Trà sữa",
            "name": "Trà sữa matcha", "image": "",
            "price": 30000,
            "description": "Trà sữa matcha thơm đậm vị",
            "status": "Còn hàng", "sizes": {"S": 0, "M": 5000, "L": 10000},
        },
        {
            "id": 3, "category": "Trà sữa",
            "name": "Trà sữa socola", "image": "",
            "price": 30000,
            "description": "Trà sữa socola",
            "status": "Còn hàng", "sizes": {"S": 0, "M": 5000, "L": 10000},
        },
        {
            "id": 4, "category": "Trà sữa",
            "name": "Trà sữa khoai môn", "image": "",
            "price": 30000,
            "description": "Khoai môn béo thơm",
            "status": "Còn hàng", "sizes": {"S": 0, "M": 5000, "L": 10000},
        },
        {
            "id": 5, "category": "Trà trái cây",
            "name": "Trà đào cam sả", "image": "",
            "price": 30000,
            "description": "Trà đào kết hợp cam và sả",
            "status": "Còn hàng", "sizes": {"S": 0, "M": 5000, "L": 10000},
        },
        {
            "id": 6, "category": "Trà trái cây",
            "name": "Trà vải", "image": "",
            "price": 28000,
            "description": "Trà vải thanh mát",
            "status": "Còn hàng", "sizes": {"S": 0, "M": 5000, "L": 10000},
        },
    ],
    "toppings": [
        {"id": 1, "name": "Trân châu đen", "price": 5000, "status": "Còn hàng", "visible": True},
        {"id": 2, "name": "Trân châu trắng", "price": 6000, "status": "Còn hàng", "visible": True},
        {"id": 3, "name": "Thạch trái cây", "price": 5000, "status": "Còn hàng", "visible": True},
        {"id": 4, "name": "Thạch phô mai", "price": 8000, "status": "Còn hàng", "visible": True},
        {"id": 5, "name": "Pudding trứng", "price": 7000, "status": "Còn hàng", "visible": True},
    ],
    "invoices": [],
}

# ============================================================
# HÀM DỮ LIỆU
# ============================================================
def deep_default():
    return copy.deepcopy(DEFAULT_DATA)


def normalize_data(data):
    if not isinstance(data, dict):
        data = deep_default()

    for key in ("categories", "products", "toppings", "invoices"):
        if key not in data or not isinstance(data[key], list):
            data[key] = []

    if not data["categories"]:
        data["categories"] = copy.deepcopy(DEFAULT_DATA["categories"])

    if not data["products"]:
        data["products"] = copy.deepcopy(DEFAULT_DATA["products"])

    if not data["toppings"]:
        data["toppings"] = copy.deepcopy(DEFAULT_DATA["toppings"])

    for product in data["products"]:
        product.setdefault("image", "")
        product.setdefault("description", "")
        product.setdefault("status", "Còn hàng")
        product.setdefault("price", 0)
        product.setdefault("sizes", {"S": 0, "M": 5000, "L": 10000})
        for size in ("S", "M", "L"):
            product["sizes"].setdefault(size, 0)

    for topping in data["toppings"]:
        topping.setdefault("visible", True)
        topping.setdefault("status", "Còn hàng")
        topping.setdefault("price", 0)

    return data


def load_data():
    if not DATA_FILE.exists():
        data = deep_default()
        save_data_to_disk(data)
        return data

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return normalize_data(data)
    except Exception:
        # Không làm app chết nếu JSON bị hỏng.
        # Tạo bản backup rồi dùng dữ liệu mặc định.
        try:
            backup = DATA_FILE.with_suffix(".broken.json")
            DATA_FILE.replace(backup)
        except Exception:
            pass
        data = deep_default()
        save_data_to_disk(data)
        return data


def save_data_to_disk(data):
    temp = DATA_FILE.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    temp.replace(DATA_FILE)


def save_data():
    save_data_to_disk(st.session_state.data)


def get_next_id(items):
    ids = []
    for item in items:
        try:
            ids.append(int(item.get("id", 0)))
        except Exception:
            pass
    return max(ids, default=0) + 1


def money(value):
    try:
        return f"{float(value):,.0f} VNĐ".replace(",", ".")
    except Exception:
        return "0 VNĐ"


def now_text():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def new_order_id():
    return datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4())[:4].upper()


def safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


# ============================================================
# ADMIN
# ============================================================
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
# SESSION STATE
# ============================================================
if "data" not in st.session_state:
    st.session_state.data = load_data()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "order_id" not in st.session_state:
    st.session_state.order_id = new_order_id()

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "active_page" not in st.session_state:
    st.session_state.active_page = "🛒 Đặt hàng"

if "editing_cart_index" not in st.session_state:
    st.session_state.editing_cart_index = None

if "editing_invoice_id" not in st.session_state:
    st.session_state.editing_invoice_id = None

if "editing_paid_invoice_id" not in st.session_state:
    st.session_state.editing_paid_invoice_id = None

# ============================================================
# CART
# ============================================================
def calculate_item_total(item):
    product_price = safe_int(item.get("price"))
    size_price = safe_int(item.get("size_price"))
    quantity = max(1, safe_int(item.get("quantity"), 1))
    topping_price = sum(
        safe_int(t.get("price"))
        for t in item.get("toppings", [])
    )
    return (product_price + size_price + topping_price) * quantity


def calculate_cart_total(cart=None):
    items = st.session_state.cart if cart is None else cart
    return sum(calculate_item_total(item) for item in items)


def reset_order():
    st.session_state.cart = []
    st.session_state.customer_name = ""
    st.session_state.order_id = new_order_id()
    st.session_state.editing_cart_index = None
    st.session_state.editing_paid_invoice_id = None


def clone_toppings(toppings):
    return [
        {
            "id": t.get("id"),
            "name": t.get("name", ""),
            "price": safe_int(t.get("price")),
        }
        for t in toppings
    ]


# ============================================================
# HÓA ĐƠN
# ============================================================
def build_invoice_from_cart(status="Đã thanh toán", old_invoice=None):
    timestamp = now_text()
    invoice = {
        "id": old_invoice.get("id") if old_invoice else st.session_state.order_id,
        "order_id": old_invoice.get("order_id") if old_invoice else st.session_state.order_id,
        "customer_name": st.session_state.customer_name.strip() or "Khách lẻ",
        "created_at": old_invoice.get("created_at", timestamp) if old_invoice else timestamp,
        "updated_at": timestamp,
        "status": status,
        "edit_count": safe_int(old_invoice.get("edit_count")) if old_invoice else 0,
        "items": copy.deepcopy(st.session_state.cart),
        "total": calculate_cart_total(),
    }
    return invoice


def save_paid_invoice():
    invoice = build_invoice_from_cart()
    existing = st.session_state.data["invoices"]

    # Nếu cùng order_id đã tồn tại thì cập nhật thay vì tạo bản trùng.
    replaced = False
    for i, old in enumerate(existing):
        if old.get("order_id") == invoice["order_id"]:
            invoice["created_at"] = old.get("created_at", invoice["created_at"])
            invoice["edit_count"] = safe_int(old.get("edit_count"))
            existing[i] = invoice
            replaced = True
            break

    if not replaced:
        existing.append(invoice)

    save_data()
    return invoice


def get_invoice(order_id):
    for invoice in st.session_state.data["invoices"]:
        if invoice.get("order_id") == order_id:
            return invoice
    return None


def load_invoice_to_cart(invoice, for_edit=True):
    st.session_state.cart = copy.deepcopy(invoice.get("items", []))
    st.session_state.customer_name = invoice.get("customer_name", "")
    st.session_state.order_id = invoice.get("order_id", new_order_id())
    st.session_state.editing_paid_invoice_id = invoice.get("order_id") if for_edit else None
    st.session_state.editing_cart_index = None


def update_existing_paid_invoice(order_id):
    invoice = get_invoice(order_id)
    if invoice is None:
        return False

    invoice["items"] = copy.deepcopy(st.session_state.cart)
    invoice["customer_name"] = st.session_state.customer_name.strip() or "Khách lẻ"
    invoice["total"] = calculate_cart_total()
    invoice["updated_at"] = now_text()
    invoice["status"] = "Đã thanh toán - Đã chỉnh sửa"
    invoice["edit_count"] = safe_int(invoice.get("edit_count")) + 1

    save_data()
    return True


def delete_invoice(order_id):
    st.session_state.data["invoices"] = [
        x for x in st.session_state.data["invoices"]
        if x.get("order_id") != order_id
    ]
    save_data()


def invoice_txt(invoice):
    lines = [
        "=" * 64,
        "                 HÓA ĐƠN TRÀ SỮA",
        "=" * 64,
        f"Mã đơn: {invoice.get('order_id', '')}",
        f"Khách hàng: {invoice.get('customer_name', 'Khách lẻ')}",
        f"Ngày tạo: {invoice.get('created_at', '')}",
        f"Cập nhật: {invoice.get('updated_at', '')}",
        f"Trạng thái: {invoice.get('status', '')}",
        "-" * 64,
    ]

    for i, item in enumerate(invoice.get("items", []), 1):
        topping_text = ", ".join(
            t.get("name", "") for t in item.get("toppings", [])
        ) or "Không"
        lines.extend([
            f"{i}. {item.get('name', '')}",
            f"   Size: {item.get('size', '')}",
            f"   Số lượng: {item.get('quantity', 1)}",
            f"   Đường: {item.get('sugar', 100)}%",
            f"   Đá: {item.get('ice', 100)}%",
            f"   Topping: {topping_text}",
            f"   Ghi chú: {item.get('notes', '') or 'Không'}",
            f"   Thành tiền: {money(calculate_item_total(item))}",
            "-" * 64,
        ])

    lines.extend([
        f"TỔNG THANH TOÁN: {money(invoice.get('total', 0))}",
        "=" * 64,
        "              CẢM ƠN QUÝ KHÁCH!",
        "=" * 64,
    ])
    return "\n".join(lines).encode("utf-8")


def invoice_html(invoice):
    rows = ""
    for i, item in enumerate(invoice.get("items", []), 1):
        toppings = ", ".join(
            t.get("name", "") for t in item.get("toppings", [])
        ) or "Không"
        rows += f"""
        <tr>
            <td>{i}</td>
            <td>{html.escape(str(item.get("name", "")))}</td>
            <td>{html.escape(str(item.get("size", "")))}</td>
            <td>{item.get("quantity", 1)}</td>
            <td>{item.get("sugar", 100)}%</td>
            <td>{item.get("ice", 100)}%</td>
            <td>{html.escape(toppings)}</td>
            <td>{html.escape(str(item.get("notes", "") or "Không"))}</td>
            <td>{money(calculate_item_total(item))}</td>
        </tr>
        """

    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>Hóa đơn {html.escape(str(invoice.get("order_id", "")))}</title>
<style>
body{{font-family:Arial,sans-serif;margin:30px;color:#111827}}
h1{{text-align:center;color:#881337}}
table{{width:100%;border-collapse:collapse}}
th,td{{border:1px solid #aaa;padding:8px;text-align:center}}
th{{background:#ffe4e6}}
.total{{text-align:right;font-size:24px;font-weight:bold;margin-top:20px;color:#e11d48}}
</style>
</head>
<body>
<h1>🧋 HÓA ĐƠN TRÀ SỮA</h1>
<p><b>Mã đơn:</b> {html.escape(str(invoice.get("order_id","")))}</p>
<p><b>Khách hàng:</b> {html.escape(str(invoice.get("customer_name","Khách lẻ")))}</p>
<p><b>Ngày tạo:</b> {html.escape(str(invoice.get("created_at","")))}</p>
<p><b>Cập nhật:</b> {html.escape(str(invoice.get("updated_at","")))}</p>
<p><b>Trạng thái:</b> {html.escape(str(invoice.get("status","")))}</p>
<table>
<thead>
<tr><th>#</th><th>Món</th><th>Size</th><th>SL</th><th>Đường</th><th>Đá</th><th>Topping</th><th>Ghi chú</th><th>Thành tiền</th></tr>
</thead>
<tbody>{rows}</tbody>
</table>
<div class="total">TỔNG: {money(invoice.get("total",0))}</div>
<p style="text-align:center"><b>Cảm ơn quý khách!</b></p>
</body>
</html>""".encode("utf-8")


# ============================================================
# ADMIN LOGIN
# ============================================================
def render_admin_login():
    st.header("🔐 ĐĂNG NHẬP ADMIN")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    username = st.text_input("👤 Tên đăng nhập", key="login_username")
    password = st.text_input("🔑 Mật khẩu", type="password", key="login_password")

    if st.button("🔐 ĐĂNG NHẬP", type="primary", use_container_width=True):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.success("Đăng nhập Admin thành công.")
            st.rerun()
        else:
            st.error("❌ Username hoặc mật khẩu không đúng.")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# CHỌN / THÊM MÓN
# ============================================================
def render_add_products():
    st.subheader("🛒 THÊM MÓN VÀO ĐƠN")

    visible_categories = [
        c["name"] for c in st.session_state.data["categories"]
        if c.get("visible", True)
    ]

    if not visible_categories:
        st.warning("Chưa có danh mục đang hiển thị.")
        return

    selected_categories = st.multiselect(
        "📂 Danh mục",
        visible_categories,
        default=visible_categories[:1],
        key="order_categories",
    )

    available_products = [
        p for p in st.session_state.data["products"]
        if p.get("category") in selected_categories
        and p.get("status") == "Còn hàng"
    ]

    if not available_products:
        st.info("Hãy chọn danh mục có món còn hàng.")
        return

    labels = [
        f"{p['name']} • {p['category']} • {money(p['price'])}"
        for p in available_products
    ]
    label_map = dict(zip(labels, available_products))

    selected_labels = st.multiselect(
        "🧋 Chọn một hoặc nhiều món",
        labels,
        key="order_products",
    )

    selected_products = [label_map[x] for x in selected_labels]

    if not selected_products:
        st.info("Chưa chọn món.")
        return

    configured = []

    for idx, product in enumerate(selected_products):
        st.markdown(
            f'<div class="card"><div class="card-title">🧋 {idx+1}. {html.escape(product["name"])}</div>'
            f'<div>{html.escape(product.get("description",""))}</div></div>',
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            size = st.radio(
                "📏 Size",
                ["S", "M", "L"],
                horizontal=True,
                key=f"add_size_{product['id']}",
            )

        with c2:
            quantity = st.number_input(
                "🔢 Số lượng",
                min_value=1,
                max_value=100,
                value=1,
                step=1,
                key=f"add_qty_{product['id']}",
            )

        with c3:
            sugar = st.selectbox(
                "🍬 Đường",
                [100, 70, 50, 30, 10, 0],
                format_func=lambda x: f"{x}%",
                key=f"add_sugar_{product['id']}",
            )

        ice = st.select_slider(
            "🧊 Lượng đá",
            options=[0, 30, 50, 70, 100],
            value=70,
            format_func=lambda x: f"{x}%",
            key=f"add_ice_{product['id']}",
        )

        available_toppings = [
            t for t in st.session_state.data["toppings"]
            if t.get("visible", True) and t.get("status") == "Còn hàng"
        ]
        topping_labels = [
            f"{t['name']} (+{money(t['price'])})"
            for t in available_toppings
        ]
        topping_map = dict(zip(topping_labels, available_toppings))

        selected_top_labels = st.multiselect(
            "🍓 Topping",
            topping_labels,
            key=f"add_top_{product['id']}",
        )
        selected_toppings = [
            topping_map[x] for x in selected_top_labels
        ]

        notes = st.text_input(
            "💬 Ghi chú",
            placeholder="Ví dụ: ít ngọt, để riêng topping...",
            key=f"add_note_{product['id']}",
        )

        size_price = safe_int(product.get("sizes", {}).get(size, 0))

        item = {
            "name": product["name"],
            "price": safe_int(product["price"]),
            "size": size,
            "size_price": size_price,
            "quantity": safe_int(quantity, 1),
            "sugar": sugar,
            "ice": ice,
            "toppings": clone_toppings(selected_toppings),
            "notes": notes.strip(),
        }
        configured.append(item)

        st.caption(
            f"💗 {product['name']} • {quantity} ly • "
            f"{money(calculate_item_total(item))}"
        )

    st.markdown(
        f'<div class="total-box"><div>Tạm tính</div>'
        f'<div class="total-money">{money(calculate_cart_total(configured))}</div></div>',
        unsafe_allow_html=True,
    )

    if st.button(
        f"🛒 THÊM {len(configured)} MÓN VÀO ĐƠN",
        type="primary",
        use_container_width=True,
        key="add_configured",
    ):
        st.session_state.cart.extend(configured)
        st.success(f"Đã thêm {len(configured)} món.")
        st.rerun()


# ============================================================
# SỬA MÓN TRONG GIỎ
# ============================================================
def render_cart_item_editor(index):
    if index < 0 or index >= len(st.session_state.cart):
        st.session_state.editing_cart_index = None
        return

    item = st.session_state.cart[index]
    st.subheader(f"✏️ SỬA MÓN {index + 1}: {item['name']}")

    products = st.session_state.data["products"]
    product = next(
        (p for p in products if p["name"] == item["name"]),
        None,
    )

    if product is None:
        st.warning("Món này không còn trong menu. Bạn vẫn có thể chỉnh số lượng/ghi chú.")
        product = {
            "sizes": {"S": 0, "M": 0, "L": 0},
            "price": item.get("price", 0),
        }

    sizes = ["S", "M", "L"]
    current_size = item.get("size", "S")
    if current_size not in sizes:
        current_size = "S"

    size = st.radio(
        "📏 Size",
        sizes,
        index=sizes.index(current_size),
        horizontal=True,
        key=f"edit_cart_size_{index}",
    )
    quantity = st.number_input(
        "🔢 Số lượng",
        min_value=1,
        max_value=100,
        value=max(1, safe_int(item.get("quantity"), 1)),
        key=f"edit_cart_qty_{index}",
    )
    sugar_options = [100, 70, 50, 30, 10, 0]
    current_sugar = safe_int(item.get("sugar"), 100)
    if current_sugar not in sugar_options:
        current_sugar = 100
    sugar = st.selectbox(
        "🍬 Đường",
        sugar_options,
        index=sugar_options.index(current_sugar),
        format_func=lambda x: f"{x}%",
        key=f"edit_cart_sugar_{index}",
    )

    ice_options = [0, 30, 50, 70, 100]
    current_ice = safe_int(item.get("ice"), 70)
    if current_ice not in ice_options:
        current_ice = 70
    ice = st.select_slider(
        "🧊 Đá",
        options=ice_options,
        value=current_ice,
        format_func=lambda x: f"{x}%",
        key=f"edit_cart_ice_{index}",
    )

    toppings = [
        t for t in st.session_state.data["toppings"]
        if t.get("visible", True) and t.get("status") == "Còn hàng"
    ]
    top_labels = [f"{t['name']} (+{money(t['price'])})" for t in toppings]
    top_map = {f"{t['name']} (+{money(t['price'])}):": t for t in toppings}

    existing_names = {t.get("name") for t in item.get("toppings", [])}
    default_labels = [
        label for label, t in zip(top_labels, toppings)
        if t.get("name") in existing_names
    ]

    selected_labels = st.multiselect(
        "🍓 Topping",
        top_labels,
        default=default_labels,
        key=f"edit_cart_top_{index}",
    )

    selected_toppings = []
    for label in selected_labels:
        name = label.split(" (+", 1)[0]
        found = next((t for t in toppings if t.get("name") == name), None)
        if found:
            selected_toppings.append(found)

    notes = st.text_input(
        "💬 Ghi chú",
        value=item.get("notes", ""),
        key=f"edit_cart_note_{index}",
    )

    new_item = {
        "name": item["name"],
        "price": safe_int(item.get("price")),
        "size": size,
        "size_price": safe_int(product.get("sizes", {}).get(size, item.get("size_price", 0))),
        "quantity": safe_int(quantity, 1),
        "sugar": sugar,
        "ice": ice,
        "toppings": clone_toppings(selected_toppings),
        "notes": notes.strip(),
    }

    st.info(f"Thành tiền mới: {money(calculate_item_total(new_item))}")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 LƯU MÓN", type="primary", use_container_width=True):
            st.session_state.cart[index] = new_item
            st.session_state.editing_cart_index = None
            st.success("Đã cập nhật món.")
            st.rerun()
    with c2:
        if st.button("↩️ HỦY", use_container_width=True):
            st.session_state.editing_cart_index = None
            st.rerun()


# ============================================================
# ĐẶT HÀNG
# ============================================================
def render_order_page():
    st.header("🛒 TẠO ĐƠN HÀNG")

    if st.session_state.editing_paid_invoice_id:
        invoice = get_invoice(st.session_state.editing_paid_invoice_id)
        if invoice:
            st.warning(
                f"✏️ Đang chỉnh sửa hóa đơn đã thanh toán: "
                f"**{invoice.get('order_id')}**"
            )
            if st.button("❌ HỦY CHỈNH SỬA HÓA ĐƠN"):
                reset_order()
                st.rerun()

    st.session_state.customer_name = st.text_input(
        "🐰 Tên khách hàng",
        value=st.session_state.customer_name,
        placeholder="Nhập tên khách hàng...",
        key="customer_name_input",
    )

    render_add_products()

    st.divider()
    st.header("🧾 GIỎ HÀNG")

    if not st.session_state.cart:
        st.info("Chưa có món trong đơn.")
        return

    if st.session_state.editing_cart_index is not None:
        render_cart_item_editor(st.session_state.editing_cart_index)
        st.divider()

    for i, item in enumerate(st.session_state.cart):
        toppings = ", ".join(
            t.get("name", "") for t in item.get("toppings", [])
        ) or "Không"

        with st.container(border=True):
            st.markdown(
                f'<div class="card-title">🧋 {i+1}. {html.escape(item["name"])}</div>',
                unsafe_allow_html=True,
            )
            st.write(
                f"📏 Size {item.get('size')} • "
                f"🔢 {item.get('quantity')} ly • "
                f"🍬 Đường {item.get('sugar')}% • "
                f"🧊 Đá {item.get('ice')}%"
            )
            st.write(f"🍓 Topping: {toppings}")
            st.write(f"💬 Ghi chú: {item.get('notes') or 'Không'}")
            st.markdown(
                f'<div class="price">💰 {money(calculate_item_total(item))}</div>',
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2)
            with c1:
                if st.button(
                    "✏️ SỬA MÓN",
                    key=f"cart_edit_{i}",
                    use_container_width=True,
                ):
                    st.session_state.editing_cart_index = i
                    st.rerun()
            with c2:
                if st.button(
                    "🗑️ XÓA MÓN",
                    key=f"cart_delete_{i}",
                    use_container_width=True,
                ):
                    st.session_state.cart.pop(i)
                    if st.session_state.editing_cart_index == i:
                        st.session_state.editing_cart_index = None
                    st.rerun()

    total = calculate_cart_total()

    st.markdown(
        f'<div class="total-box"><div>👤 Khách hàng: <b>{html.escape(st.session_state.customer_name or "Khách lẻ")}</b></div>'
        f'<div>🧾 Số dòng món: <b>{len(st.session_state.cart)}</b></div>'
        f'<div class="total-money">💰 {money(total)}</div>'
        f'<div>TỔNG THANH TOÁN</div></div>',
        unsafe_allow_html=True,
    )

    # Nếu đang sửa hóa đơn đã thanh toán
    if st.session_state.editing_paid_invoice_id:
        st.subheader("💾 LƯU THAY ĐỔI HÓA ĐƠN")

        if st.button(
            "💾 CẬP NHẬT HÓA ĐƠN ĐÃ THANH TOÁN",
            type="primary",
            use_container_width=True,
        ):
            order_id = st.session_state.editing_paid_invoice_id
            if update_existing_paid_invoice(order_id):
                st.success(
                    f"Đã cập nhật hóa đơn {order_id}. "
                    "Mã đơn được giữ nguyên."
                )
                st.session_state.editing_paid_invoice_id = None
                st.session_state.editing_cart_index = None
                st.rerun()
            else:
                st.error("Không tìm thấy hóa đơn cần cập nhật.")
        return

    st.subheader("💳 THANH TOÁN")

    if st.button(
        f"💳 XÁC NHẬN ĐÃ THANH TOÁN — {money(total)}",
        type="primary",
        use_container_width=True,
    ):
        invoice = save_paid_invoice()
        st.success(
            f"✅ Thanh toán thành công! Mã hóa đơn: {invoice['order_id']}"
        )

        st.download_button(
            "📄 TẢI HÓA ĐƠN TXT",
            data=invoice_txt(invoice),
            file_name=f"hoa_don_{invoice['order_id']}.txt",
            mime="text/plain",
            use_container_width=True,
            key=f"download_after_pay_{invoice['order_id']}",
        )

        # Giữ lại hóa đơn gần nhất để người dùng có thể sửa sau thanh toán.
        st.session_state.last_paid_order_id = invoice["order_id"]

    last_paid_id = st.session_state.get("last_paid_order_id")
    if last_paid_id:
        invoice = get_invoice(last_paid_id)
        if invoice:
            st.divider()
            st.subheader("✏️ SỬA HÓA ĐƠN VỪA THANH TOÁN")
            st.caption(
                f"Mã đơn gần nhất: {last_paid_id} • "
                f"Trạng thái: {invoice.get('status')}"
            )
            if st.button(
                "✏️ MỞ HÓA ĐƠN GẦN NHẤT ĐỂ SỬA",
                use_container_width=True,
            ):
                load_invoice_to_cart(invoice, True)
                st.rerun()

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🆕 TẠO ĐƠN MỚI", use_container_width=True):
            reset_order()
            st.rerun()
    with c2:
        if st.button("🧹 XÓA TOÀN BỘ GIỎ", use_container_width=True):
            st.session_state.cart = []
            st.session_state.editing_cart_index = None
            st.rerun()


# ============================================================
# LỊCH SỬ HÓA ĐƠN ADMIN
# ============================================================
def render_invoice_history():
    if not st.session_state.admin_logged_in:
        st.error("🔒 Chức năng này chỉ dành cho Admin.")
        return

    st.header("🧾 LỊCH SỬ HÓA ĐƠN")
    invoices = st.session_state.data["invoices"]

    if not invoices:
        st.info("Chưa có hóa đơn nào được thanh toán.")
        return

    total_revenue = sum(safe_int(x.get("total")) for x in invoices)
    edited_count = sum(1 for x in invoices if safe_int(x.get("edit_count")) > 0)

    a, b, c = st.columns(3)
    a.metric("🧾 Số hóa đơn", len(invoices))
    b.metric("💰 Tổng doanh thu", money(total_revenue))
    c.metric("✏️ Đã chỉnh sửa", edited_count)

    st.divider()

    search = st.text_input(
        "🔎 Tìm hóa đơn theo mã đơn hoặc tên khách hàng",
        placeholder="Ví dụ: 20261008 hoặc Nguyễn Văn A",
    ).strip().lower()

    filtered = []
    for invoice in reversed(invoices):
        text = (
            str(invoice.get("order_id", "")) + " " +
            str(invoice.get("customer_name", ""))
        ).lower()
        if not search or search in text:
            filtered.append(invoice)

    st.caption(f"Hiển thị {len(filtered)} / {len(invoices)} hóa đơn")

    for invoice in filtered:
        order_id = invoice.get("order_id", "")
        title = (
            f"🧾 {order_id} • "
            f"{invoice.get('customer_name', 'Khách lẻ')} • "
            f"{money(invoice.get('total', 0))}"
        )

        with st.expander(title):
            st.write(f"**Ngày tạo:** {invoice.get('created_at', '')}")
            st.write(f"**Cập nhật:** {invoice.get('updated_at', '')}")
            st.write(f"**Trạng thái:** {invoice.get('status', '')}")
            st.write(f"**Số lần chỉnh sửa:** {invoice.get('edit_count', 0)}")

            for i, item in enumerate(invoice.get("items", []), 1):
                topping_text = ", ".join(
                    t.get("name", "") for t in item.get("toppings", [])
                ) or "Không"
                st.markdown(
                    f"**{i}. {item.get('name')}** — "
                    f"Size {item.get('size')} — "
                    f"{item.get('quantity')} ly — "
                    f"Đường {item.get('sugar')}% — "
                    f"Đá {item.get('ice')}% — "
                    f"Topping: {topping_text} — "
                    f"**{money(calculate_item_total(item))}**"
                )

            st.markdown(
                f'<div class="total-box"><div class="total-money">{money(invoice.get("total",0))}</div></div>',
                unsafe_allow_html=True,
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.download_button(
                    "📄 TẢI TXT",
                    data=invoice_txt(invoice),
                    file_name=f"hoa_don_{order_id}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key=f"hist_txt_{order_id}",
                )

            with c2:
                if st.button(
                    "✏️ SỬA ĐƠN",
                    key=f"hist_edit_{order_id}",
                    use_container_width=True,
                ):
                    load_invoice_to_cart(invoice, True)
                    st.session_state.active_page = "🛒 Đặt hàng"
                    st.rerun()

            with c3:
                if st.button(
                    "🗑️ XÓA",
                    key=f"hist_delete_{order_id}",
                    use_container_width=True,
                ):
                    delete_invoice(order_id)
                    st.success("Đã xóa hóa đơn.")
                    st.rerun()

    st.divider()

    st.subheader("🗑️ QUẢN LÝ DỮ LIỆU LỊCH SỬ")

    if st.button(
        "🗑️ XÓA TOÀN BỘ LỊCH SỬ HÓA ĐƠN",
        use_container_width=True,
    ):
        st.session_state.confirm_delete_history = True

    if st.session_state.get("confirm_delete_history", False):
        st.warning("⚠️ Thao tác này sẽ xóa toàn bộ lịch sử hóa đơn.")
        x, y = st.columns(2)
        with x:
            if st.button("⚠️ XÁC NHẬN XÓA", type="primary", use_container_width=True):
                st.session_state.data["invoices"] = []
                st.session_state.confirm_delete_history = False
                save_data()
                st.success("Đã xóa toàn bộ lịch sử.")
                st.rerun()
        with y:
            if st.button("HỦY", use_container_width=True):
                st.session_state.confirm_delete_history = False
                st.rerun()


# ============================================================
# QUẢN LÝ DANH MỤC
# ============================================================
def render_categories():
    if not st.session_state.admin_logged_in:
        st.error("🔒 Chỉ Admin.")
        return

    st.header("📋 QUẢN LÝ DANH MỤC")

    with st.form("new_category"):
        name = st.text_input("Tên danh mục")
        submit = st.form_submit_button("➕ TẠO DANH MỤC", type="primary")

    if submit:
        name = name.strip()
        if not name:
            st.error("Tên danh mục không được để trống.")
        elif any(c["name"].lower() == name.lower() for c in st.session_state.data["categories"]):
            st.error("Danh mục đã tồn tại.")
        else:
            st.session_state.data["categories"].append({
                "id": get_next_id(st.session_state.data["categories"]),
                "name": name,
                "visible": True,
            })
            save_data()
            st.success("Đã tạo danh mục.")
            st.rerun()

    st.divider()

    for category in list(st.session_state.data["categories"]):
        with st.container(border=True):
            st.write(f"### 📂 {category['name']}")
            c1, c2, c3 = st.columns(3)

            with c1:
                new_name = st.text_input(
                    "Tên",
                    value=category["name"],
                    key=f"cat_name_{category['id']}",
                )

            with c2:
                if st.button(
                    "👁️ ẨN" if category.get("visible", True) else "👁️ HIỆN",
                    key=f"cat_vis_{category['id']}",
                    use_container_width=True,
                ):
                    category["visible"] = not category.get("visible", True)
                    save_data()
                    st.rerun()

            with c3:
                if st.button(
                    "💾 LƯU",
                    key=f"cat_save_{category['id']}",
                    use_container_width=True,
                ):
                    old = category["name"]
                    new = new_name.strip()
                    if not new:
                        st.error("Tên không được để trống.")
                    else:
                        category["name"] = new
                        for product in st.session_state.data["products"]:
                            if product.get("category") == old:
                                product["category"] = new
                        save_data()
                        st.success("Đã cập nhật.")
                        st.rerun()

            if st.button(
                "🗑️ XÓA DANH MỤC",
                key=f"cat_del_{category['id']}",
                use_container_width=True,
            ):
                used = any(
                    p.get("category") == category["name"]
                    for p in st.session_state.data["products"]
                )
                if used:
                    st.error("Không thể xóa vì đang có món thuộc danh mục này.")
                else:
                    st.session_state.data["categories"].remove(category)
                    save_data()
                    st.rerun()


# ============================================================
# QUẢN LÝ MÓN
# ============================================================
def render_products():
    if not st.session_state.admin_logged_in:
        st.error("🔒 Chỉ Admin.")
        return

    st.header("🍹 QUẢN LÝ MÓN")

    categories = [c["name"] for c in st.session_state.data["categories"]]
    if not categories:
        st.warning("Hãy tạo danh mục trước.")
        return

    with st.form("new_product"):
        st.subheader("➕ THÊM MÓN")

        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Tên món")
            category = st.selectbox("Danh mục", categories)
            price = st.number_input("Giá cơ bản", min_value=0, value=25000, step=1000)
            description = st.text_area("Mô tả")
        with c2:
            image = st.text_input("URL hình ảnh")
            status = st.selectbox("Trạng thái", ["Còn hàng", "Hết hàng"])
            s = st.number_input("Size S (+)", min_value=0, value=0, step=1000)
            m = st.number_input("Size M (+)", min_value=0, value=5000, step=1000)
            l = st.number_input("Size L (+)", min_value=0, value=10000, step=1000)

        submit = st.form_submit_button("➕ THÊM MÓN", type="primary")

    if submit:
        name = name.strip()
        if not name:
            st.error("Vui lòng nhập tên món.")
        else:
            st.session_state.data["products"].append({
                "id": get_next_id(st.session_state.data["products"]),
                "category": category,
                "name": name,
                "image": image.strip(),
                "price": price,
                "description": description.strip(),
                "status": status,
                "sizes": {"S": s, "M": m, "L": l},
            })
            save_data()
            st.success("Đã thêm món.")
            st.rerun()

    st.divider()

    for product in list(st.session_state.data["products"]):
        with st.expander(f"🧋 {product['name']} — {money(product['price'])}"):
            if product.get("image"):
                try:
                    st.image(product["image"], width=180)
                except Exception:
                    pass

            c1, c2 = st.columns(2)
            with c1:
                new_name = st.text_input(
                    "Tên món",
                    value=product["name"],
                    key=f"prod_name_{product['id']}",
                )
                cat_index = categories.index(product["category"]) if product["category"] in categories else 0
                new_category = st.selectbox(
                    "Danh mục",
                    categories,
                    index=cat_index,
                    key=f"prod_cat_{product['id']}",
                )
                new_price = st.number_input(
                    "Giá",
                    min_value=0,
                    value=safe_int(product["price"]),
                    step=1000,
                    key=f"prod_price_{product['id']}",
                )

            with c2:
                new_image = st.text_input(
                    "URL hình",
                    value=product.get("image", ""),
                    key=f"prod_img_{product['id']}",
                )
                status_options = ["Còn hàng", "Hết hàng"]
                status_index = 0 if product.get("status") == "Còn hàng" else 1
                new_status = st.selectbox(
                    "Trạng thái",
                    status_options,
                    index=status_index,
                    key=f"prod_status_{product['id']}",
                )
                new_desc = st.text_area(
                    "Mô tả",
                    value=product.get("description", ""),
                    key=f"prod_desc_{product['id']}",
                )

            s1, s2, s3 = st.columns(3)
            with s1:
                new_s = st.number_input(
                    "Size S +",
                    min_value=0,
                    value=safe_int(product.get("sizes", {}).get("S")),
                    step=1000,
                    key=f"prod_s_{product['id']}",
                )
            with s2:
                new_m = st.number_input(
                    "Size M +",
                    min_value=0,
                    value=safe_int(product.get("sizes", {}).get("M")),
                    step=1000,
                    key=f"prod_m_{product['id']}",
                )
            with s3:
                new_l = st.number_input(
                    "Size L +",
                    min_value=0,
                    value=safe_int(product.get("sizes", {}).get("L")),
                    step=1000,
                    key=f"prod_l_{product['id']}",
                )

            b1, b2 = st.columns(2)
            with b1:
                if st.button(
                    "💾 LƯU THAY ĐỔI",
                    key=f"prod_save_{product['id']}",
                    type="primary",
                    use_container_width=True,
                ):
                    product["name"] = new_name.strip()
                    product["category"] = new_category
                    product["price"] = new_price
                    product["image"] = new_image.strip()
                    product["status"] = new_status
                    product["description"] = new_desc.strip()
                    product["sizes"] = {"S": new_s, "M": new_m, "L": new_l}
                    save_data()
                    st.success("Đã cập nhật món.")
                    st.rerun()

            with b2:
                if st.button(
                    "🗑️ XÓA MÓN",
                    key=f"prod_del_{product['id']}",
                    use_container_width=True,
                ):
                    st.session_state.data["products"].remove(product)
                    save_data()
                    st.success("Đã xóa món.")
                    st.rerun()


# ============================================================
# QUẢN LÝ TOPPING
# ============================================================
def render_toppings():
    if not st.session_state.admin_logged_in:
        st.error("🔒 Chỉ Admin.")
        return

    st.header("🥤 QUẢN LÝ TOPPING")

    with st.form("new_topping"):
        name = st.text_input("Tên topping")
        price = st.number_input("Giá", min_value=0, value=5000, step=1000)
        status = st.selectbox("Trạng thái", ["Còn hàng", "Hết hàng"])
        submit = st.form_submit_button("➕ THÊM TOPPING", type="primary")

    if submit:
        name = name.strip()
        if not name:
            st.error("Tên topping không được để trống.")
        else:
            st.session_state.data["toppings"].append({
                "id": get_next_id(st.session_state.data["toppings"]),
                "name": name,
                "price": price,
                "status": status,
                "visible": True,
            })
            save_data()
            st.success("Đã thêm topping.")
            st.rerun()

    st.divider()

    for topping in list(st.session_state.data["toppings"]):
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                name_new = st.text_input(
                    "Tên",
                    value=topping["name"],
                    key=f"top_name_{topping['id']}",
                )
            with c2:
                price_new = st.number_input(
                    "Giá",
                    min_value=0,
                    value=safe_int(topping["price"]),
                    step=1000,
                    key=f"top_price_{topping['id']}",
                )
            with c3:
                status_new = st.selectbox(
                    "Trạng thái",
                    ["Còn hàng", "Hết hàng"],
                    index=0 if topping["status"] == "Còn hàng" else 1,
                    key=f"top_status_{topping['id']}",
                )

            a, b, c = st.columns(3)
            with a:
                if st.button(
                    "💾 LƯU",
                    key=f"top_save_{topping['id']}",
                    use_container_width=True,
                ):
                    topping["name"] = name_new.strip()
                    topping["price"] = price_new
                    topping["status"] = status_new
                    save_data()
                    st.rerun()
            with b:
                if st.button(
                    "👁️ ẨN" if topping.get("visible", True) else "👁️ HIỆN",
                    key=f"top_vis_{topping['id']}",
                    use_container_width=True,
                ):
                    topping["visible"] = not topping.get("visible", True)
                    save_data()
                    st.rerun()
            with c:
                if st.button(
                    "🗑️ XÓA",
                    key=f"top_del_{topping['id']}",
                    use_container_width=True,
                ):
                    st.session_state.data["toppings"].remove(topping)
                    save_data()
                    st.rerun()


# ============================================================
# TÀI KHOẢN ADMIN
# ============================================================
def render_admin_account():
    if not st.session_state.admin_logged_in:
        st.error("🔒 Chỉ Admin.")
        return

    st.header("⚙️ TÀI KHOẢN ADMIN")
    st.write(f"👤 **Username:** {ADMIN_USERNAME}")
    st.info(
        "Nếu bạn chưa cấu hình Streamlit Secrets, tài khoản mặc định là "
        "`admin / 123456`."
    )

    st.code(
        '[admin]\nusername = "admin"\npassword = "MAT_KHAU_CUA_BAN"',
        language="toml",
    )


# ============================================================
# SIDEBAR
# ============================================================
st.title("🧋 HÓA ĐƠN TRÀ SỮA")
st.caption("Order • Thanh toán • Sửa đơn • Lịch sử hóa đơn • Quản lý Admin")

st.sidebar.title("📌 MENU")

if st.session_state.admin_logged_in:
    menu_options = [
        "🛒 Đặt hàng",
        "🧾 Lịch sử hóa đơn",
        "📋 Quản lý danh mục",
        "🍹 Quản lý món",
        "🥤 Quản lý topping",
        "⚙️ Tài khoản Admin",
    ]
else:
    menu_options = [
        "🛒 Đặt hàng",
        "🔐 Đăng nhập Admin",
    ]

if st.session_state.active_page not in menu_options:
    st.session_state.active_page = menu_options[0]

menu = st.sidebar.radio(
    "Chọn chức năng",
    menu_options,
    key="active_page",
)

if st.session_state.admin_logged_in:
    st.sidebar.success("🔓 ADMIN MODE")
    st.sidebar.write(f"👤 {ADMIN_USERNAME}")
    if st.sidebar.button("🚪 ĐĂNG XUẤT", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.session_state.active_page = "🛒 Đặt hàng"
        st.rerun()
else:
    st.sidebar.info("👤 USER MODE")

st.sidebar.divider()
st.sidebar.caption("🧋 Milk Tea Order & Billing")

# ============================================================
# ROUTER
# ============================================================
if menu == "🛒 Đặt hàng":
    render_order_page()

elif menu == "🔐 Đăng nhập Admin":
    render_admin_login()

elif menu == "🧾 Lịch sử hóa đơn":
    render_invoice_history()

elif menu == "📋 Quản lý danh mục":
    render_categories()

elif menu == "🍹 Quản lý món":
    render_products()

elif menu == "🥤 Quản lý topping":
    render_toppings()

elif menu == "⚙️ Tài khoản Admin":
    render_admin_account()
