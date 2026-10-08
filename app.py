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

.stApp {
    background-color: #fff8f5;
}

.main {
    background-color: #fff8f5;
}

h1, h2, h3 {
    color: #8B4513;
}

.order-card {
    background: white;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #ead8cf;
    margin-bottom: 15px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
}

.order-title {
    font-size: 21px;
    font-weight: bold;
    color: #8B4513;
}

.order-detail {
    font-size: 15px;
    line-height: 1.8;
}

.total-box {
    background: #fff0e8;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #d2691e;
    text-align: center;
    margin-top: 15px;
}

.total-money {
    font-size: 30px;
    font-weight: bold;
    color: #d35400;
}

.admin-box {
    background: #fff;
    border: 2px solid #8B4513;
    border-radius: 15px;
    padding: 25px;
    margin-top: 20px;
    margin-bottom: 20px;
}

.admin-success {
    background: #e8f5e9;
    border: 1px solid #81c784;
    padding: 12px;
    border-radius: 10px;
}

.menu-card {
    background: white;
    border-radius: 15px;
    padding: 15px;
    border: 1px solid #ead8cf;
    margin-bottom: 12px;
}

.price-text {
    color: #d35400;
    font-size: 18px;
    font-weight: bold;
}

.login-title {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: #8B4513;
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

    st.session_state.order_id = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )


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

    st.header("🛒 TẠO ĐƠN HÀNG")

    # --------------------------------------------------------
    # THÔNG TIN KHÁCH
    # --------------------------------------------------------

    customer_name = st.text_input(
        "👤 Tên khách hàng",
        value=st.session_state.customer_name,
        placeholder="Nhập tên khách hàng..."
    )

    st.session_state.customer_name = customer_name

    st.divider()

    # --------------------------------------------------------
    # THÊM MÓN
    # --------------------------------------------------------

    st.subheader("🥤 THÊM MÓN VÀO ĐƠN")

    visible_categories = [
        category["name"]
        for category in st.session_state.data["categories"]
        if category["visible"]
    ]

    if not visible_categories:

        st.warning(
            "Hiện chưa có danh mục món."
        )

    else:

        selected_category = st.selectbox(
            "📂 Danh mục",
            visible_categories
        )

        available_products = [
            product
            for product in st.session_state.data["products"]
            if product["category"] == selected_category
            and product["status"] == "Còn hàng"
        ]

        if not available_products:

            st.warning(
                "Danh mục này hiện chưa có món còn hàng."
            )

        else:

            product_names = [
                product["name"]
                for product in available_products
            ]

            selected_product_name = st.selectbox(
                "🧋 Chọn món",
                product_names
            )

            product = next(
                product
                for product in available_products
                if product["name"] == selected_product_name
            )

            image_col, info_col = st.columns(
                [1, 2]
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

                st.markdown(
                    f"### 🧋 {product['name']}"
                )

                st.write(
                    product["description"]
                )

                st.markdown(
                    f"### {money(product['price'])}"
                )

            # ------------------------------------------------
            # SIZE
            # ------------------------------------------------

            size = st.radio(
                "📏 Size",
                ["S", "M", "L"],
                horizontal=True
            )

            size_price = product[
                "sizes"
            ].get(
                size,
                0
            )

            current_price = (
                product["price"]
                + size_price
            )

            st.info(
                f"Giá Size {size}: "
                f"**{money(current_price)}**"
            )

            # ------------------------------------------------
            # SỐ LƯỢNG
            # ------------------------------------------------

            quantity = st.number_input(
                "🔢 Số lượng",
                min_value=1,
                max_value=100,
                value=1,
                step=1
            )

            # ------------------------------------------------
            # ĐƯỜNG
            # ------------------------------------------------

            sugar = st.selectbox(
                "🍬 Mức độ đường",
                [100, 70, 50, 30, 10, 0],
                format_func=lambda value:
                    f"{value}%"
            )

            # ------------------------------------------------
            # ĐÁ
            # ------------------------------------------------

            ice = st.selectbox(
                "🧊 Lượng đá",
                [100, 70, 50, 30, 10, 0],
                format_func=lambda value:
                    f"{value}%"
            )

            # ------------------------------------------------
            # TOPPING
            # ------------------------------------------------

            available_toppings = [
                topping
                for topping
                in st.session_state.data["toppings"]
                if topping["visible"]
                and topping["status"] == "Còn hàng"
            ]

            topping_options = {
                f"{topping['name']} "
                f"(+{money(topping['price'])})":
                topping
                for topping in available_toppings
            }

            selected_topping_labels = st.multiselect(
                "🧋 Topping – có thể chọn nhiều",
                list(topping_options.keys())
            )

            selected_toppings = [
                topping_options[label]
                for label in selected_topping_labels
            ]

            # ------------------------------------------------
            # GHI CHÚ
            # ------------------------------------------------

            st.markdown(
                "### 📝 GHI CHÚ RIÊNG"
            )

            notes_options = [
                "Nhiều sữa",
                "Không lấy ống hút",
                "Uống tại chỗ",
                "Mang về"
            ]

            selected_notes = st.multiselect(
                "Chọn ghi chú",
                notes_options
            )

            custom_note = st.text_input(
                "Ghi chú theo yêu cầu",
                placeholder=(
                    "Ví dụ: Ít ngọt hơn, "
                    "để riêng topping..."
                )
            )

            notes = ", ".join(
                selected_notes
            )

            if custom_note.strip():

                if notes:

                    notes += ", "

                notes += custom_note.strip()

            # ------------------------------------------------
            # TÍNH TIỀN MÓN
            # ------------------------------------------------

            preview_item = {

                "name": product["name"],

                "price": product["price"],

                "size_price": size_price,

                "quantity": quantity,

                "size": size,

                "sugar": sugar,

                "ice": ice,

                "toppings": selected_toppings,

                "notes": notes

            }

            preview_total = calculate_item_total(
                preview_item
            )

            st.info(
                f"💰 Thành tiền món này: "
                f"**{money(preview_total)}**"
            )

            # ------------------------------------------------
            # THÊM VÀO GIỎ
            # ------------------------------------------------

            if st.button(
                "➕ THÊM MÓN VÀO ĐƠN",
                type="primary",
                use_container_width=True
            ):

                item = {

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

                st.session_state.cart.append(
                    item
                )

                st.success(
                    f"Đã thêm "
                    f"{quantity} x "
                    f"{product['name']}!"
                )

                st.rerun()

    # ========================================================
    # CHI TIẾT ĐƠN
    # ========================================================

    st.divider()

    st.header("🧾 CHI TIẾT ĐƠN HÀNG")

    if not st.session_state.cart:

        st.info(
            "Chưa có món trong đơn."
        )

    else:

        for index, item in enumerate(
            st.session_state.cart
        ):

            item_total = calculate_item_total(
                item
            )

            if item["toppings"]:

                toppings_text = ", ".join(
                    topping["name"]
                    for topping in item["toppings"]
                )

            else:

                toppings_text = "Không"

            st.markdown(
                f"""
<div class="order-card">

<div class="order-title">

🧋 {index + 1}. {html.escape(item['name'])}

</div>

<div class="order-detail">

📏 <b>Size:</b>
{item['size']}
<br>

🔢 <b>Số lượng:</b>
{item['quantity']}
<br>

🍬 <b>Đường:</b>
{item['sugar']}%
<br>

🧊 <b>Đá:</b>
{item['ice']}%
<br>

🧋 <b>Topping:</b>
{html.escape(toppings_text)}
<br>

📝 <b>Ghi chú:</b>
{html.escape(item['notes'] or 'Không')}
<br>

💰 <b>Thành tiền:</b>
{money(item_total)}

</div>

</div>
""",
                unsafe_allow_html=True
            )

            delete_col1, delete_col2 = st.columns(
                [5, 1]
            )

            with delete_col2:

                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_cart_{index}"
                ):

                    st.session_state.cart.pop(
                        index
                    )

                    st.rerun()

        # ----------------------------------------------------
        # TỔNG TIỀN
        # ----------------------------------------------------

        total = calculate_cart_total()

        st.markdown(
            f"""
<div class="total-box">

<div>

👤 Khách hàng:
<b>
{html.escape(
    st.session_state.customer_name
    or "Khách lẻ"
)}
</b>

</div>

<br>

<div>

🧾 Số món:
<b>{len(st.session_state.cart)}</b>

</div>

<br>

<div class="total-money">

💰 {money(total)}

</div>

<div>

TỔNG SỐ TIỀN CẦN THANH TOÁN

</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.divider()

        # ----------------------------------------------------
        # XUẤT HÓA ĐƠN
        # ----------------------------------------------------

        st.subheader("📤 XUẤT HÓA ĐƠN")

        col1, col2, col3 = st.columns(3)

        with col1:

            txt_data = create_txt_invoice()

            st.download_button(
                "📄 Tải hóa đơn TXT",
                data=txt_data,
                file_name=(
                    f"hoa_don_"
                    f"{st.session_state.order_id}.txt"
                ),
                mime="text/plain",
                use_container_width=True
            )

        with col2:

            html_data = create_html_invoice()

            st.download_button(
                "🌐 Tải hóa đơn HTML",
                data=html_data,
                file_name=(
                    f"hoa_don_"
                    f"{st.session_state.order_id}.html"
                ),
                mime="text/html",
                use_container_width=True
            )

        with col3:

            if st.button(
                "🗑️ TẠO ĐƠN MỚI",
                use_container_width=True
            ):

                reset_order()

                st.rerun()


# ============================================================
# ============================================================
# 3. QUẢN LÝ DANH MỤC - CHỈ ADMIN
# ============================================================
# ============================================================

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
    "Order • Tính bill • Quản lý món • Admin"
)
```
