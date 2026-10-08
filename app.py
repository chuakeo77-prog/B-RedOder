import streamlit as st
from datetime import datetime
from io import BytesIO
import json
import os
import base64

# ============================================================
# CẤU HÌNH
# ============================================================

st.set_page_config(
    page_title="Order & Bill Trà Sữa",
    page_icon="🧋",
    layout="wide"
)

DATA_FILE = "menu_data.json"

# ============================================================
# CSS GIAO DIỆN
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #fff8f5;
}

.stApp {
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
    line-height: 1.7;
}

.total-box {
    background: #fff0e8;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #d2691e;
    text-align: center;
}

.total-money {
    font-size: 30px;
    font-weight: bold;
    color: #d35400;
}

.menu-card {
    background: white;
    border-radius: 15px;
    padding: 15px;
    border: 1px solid #ead8cf;
    margin-bottom: 12px;
}

.badge-green {
    background: #d4edda;
    color: #155724;
    padding: 5px 10px;
    border-radius: 10px;
    font-weight: bold;
}

.badge-red {
    background: #f8d7da;
    color: #721c24;
    padding: 5px 10px;
    border-radius: 10px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


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
# ĐỌC / LƯU DỮ LIỆU
# ============================================================

def load_data():

    if not os.path.exists(DATA_FILE):

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(
                DEFAULT_DATA,
                f,
                ensure_ascii=False,
                indent=4
            )

        return DEFAULT_DATA

    try:

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:

        return DEFAULT_DATA


def save_data():

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            st.session_state.data,
            f,
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
    st.session_state.order_id = datetime.now().strftime("%Y%m%d%H%M%S")


# ============================================================
# HÀM TIỆN ÍCH
# ============================================================

def money(value):

    return f"{value:,.0f} VNĐ".replace(",", ".")


def get_next_id(items):

    if not items:
        return 1

    return max(item["id"] for item in items) + 1


def calculate_item_total(item):

    product_price = item["price"]
    size_price = item["size_price"]

    topping_price = sum(
        topping["price"] for topping in item["toppings"]
    )

    return (
        product_price
        + size_price
        + topping_price
    ) * item["quantity"]


def calculate_cart_total():

    return sum(
        calculate_item_total(item)
        for item in st.session_state.cart
    )


def reset_order():

    st.session_state.cart = []
    st.session_state.customer_name = ""
    st.session_state.order_id = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )


# ============================================================
# XUẤT FILE TXT
# ============================================================

def create_txt_invoice():

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    lines = []

    lines.append("=" * 60)
    lines.append("              HÓA ĐƠN TRÀ SỮA")
    lines.append("=" * 60)
    lines.append(f"Mã đơn: {st.session_state.order_id}")
    lines.append(f"Thời gian: {now}")
    lines.append(
        f"Khách hàng: {st.session_state.customer_name or 'Khách lẻ'}"
    )
    lines.append("-" * 60)

    for i, item in enumerate(st.session_state.cart, 1):

        lines.append(
            f"{i}. {item['name']} - Size {item['size']}"
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
                t["name"] for t in item["toppings"]
            )

            lines.append(
                f"   Topping: {topping_text}"
            )

        else:

            lines.append("   Topping: Không")

        if item["notes"]:

            lines.append(
                f"   Ghi chú: {item['notes']}"
            )

        lines.append(
            f"   Đơn giá: {money(item['price'] + item['size_price'])}"
        )

        lines.append(
            f"   Thành tiền: {money(calculate_item_total(item))}"
        )

        lines.append("-" * 60)

    lines.append(
        f"TỔNG THANH TOÁN: {money(calculate_cart_total())}"
    )

    lines.append("=" * 60)
    lines.append("       Cảm ơn quý khách!")
    lines.append("=" * 60)

    return "\n".join(lines).encode("utf-8")


# ============================================================
# XUẤT FILE HTML
# ============================================================

def create_html_invoice():

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    rows = ""

    for i, item in enumerate(st.session_state.cart, 1):

        toppings = ", ".join(
            t["name"] for t in item["toppings"]
        ) if item["toppings"] else "Không"

        rows += f"""
        <tr>
            <td>{i}</td>
            <td>{item['name']}</td>
            <td>{item['size']}</td>
            <td>{item['quantity']}</td>
            <td>{item['sugar']}%</td>
            <td>{item['ice']}%</td>
            <td>{toppings}</td>
            <td>{item['notes']}</td>
            <td>{money(calculate_item_total(item))}</td>
        </tr>
        """

    html = f"""
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
                font-size: 22px;
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
            {st.session_state.customer_name or "Khách lẻ"}

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
            Tổng thanh toán:
            {money(calculate_cart_total())}
        </div>

        <br>

        <center>
            <b>Cảm ơn quý khách đã sử dụng dịch vụ!</b>
        </center>

    </body>
    </html>
    """

    return html.encode("utf-8")


# ============================================================
# HEADER
# ============================================================

st.title("🧋 HÓA ĐƠN TRÀ SỮA")
st.caption("Hệ thống Order – Quản lý món – Tính tiền – Xuất hóa đơn")


# ============================================================
# MENU CHÍNH
# ============================================================

menu = st.sidebar.radio(
    "📌 MENU",
    [
        "🛒 Đặt hàng",
        "📋 Quản lý danh mục",
        "🍹 Quản lý món",
        "🥤 Quản lý topping"
    ]
)


# ============================================================
# 1. ĐẶT HÀNG
# ============================================================

if menu == "🛒 Đặt hàng":

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
    # CHỌN MÓN
    # --------------------------------------------------------

    st.subheader("🥤 Thêm món vào đơn")

    visible_categories = [
        c["name"]
        for c in st.session_state.data["categories"]
        if c["visible"]
    ]

    if not visible_categories:

        st.warning("Chưa có danh mục món đang hiển thị.")

    else:

        selected_category = st.selectbox(
            "📂 Danh mục",
            visible_categories
        )

        available_products = [
            p for p in st.session_state.data["products"]
            if p["category"] == selected_category
            and p["status"] == "Còn hàng"
        ]

        if not available_products:

            st.warning("Danh mục này hiện chưa có món còn hàng.")

        else:

            product_names = [
                p["name"]
                for p in available_products
            ]

            selected_product_name = st.selectbox(
                "🧋 Chọn món",
                product_names
            )

            product = next(
                p for p in available_products
                if p["name"] == selected_product_name
            )

            col1, col2 = st.columns([1, 2])

            with col1:

                if product["image"]:

                    try:
                        st.image(
                            product["image"],
                            use_container_width=True
                        )
                    except:
                        pass

            with col2:

                st.write(
                    f"**{product['name']}**"
                )

                st.write(
                    product["description"]
                )

                st.write(
                    f"Giá cơ bản: **{money(product['price'])}**"
                )

            # ------------------------------------------------
            # SIZE
            # ------------------------------------------------

            size = st.radio(
                "📏 Size",
                ["S", "M", "L"],
                horizontal=True
            )

            size_price = product["sizes"].get(size, 0)

            st.info(
                f"Giá Size {size}: "
                f"{money(product['price'] + size_price)}"
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
                format_func=lambda x: f"{x}%"
            )

            # ------------------------------------------------
            # ĐÁ
            # ------------------------------------------------

            ice = st.selectbox(
                "🧊 Lượng đá",
                [100, 70, 50, 30, 10, 0],
                format_func=lambda x: f"{x}%"
            )

            # ------------------------------------------------
            # TOPPING
            # ------------------------------------------------

            available_toppings = [
                t
                for t in st.session_state.data["toppings"]
                if t["visible"]
                and t["status"] == "Còn hàng"
            ]

            topping_options = {
                f"{t['name']} (+{money(t['price'])})": t
                for t in available_toppings
            }

            selected_topping_labels = st.multiselect(
                "🧋 Topping – có thể chọn nhiều",
                list(topping_options.keys())
            )

            selected_toppings = [
                topping_options[x]
                for x in selected_topping_labels
            ]

            # ------------------------------------------------
            # GHI CHÚ
            # ------------------------------------------------

            st.markdown("### 📝 Ghi chú riêng")

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
                "Ghi chú thêm",
                placeholder="Ví dụ: Ít ngọt hơn, để riêng topping..."
            )

            notes = ", ".join(selected_notes)

            if custom_note.strip():

                if notes:
                    notes += ", "

                notes += custom_note.strip()

            # ------------------------------------------------
            # GIÁ MÓN
            # ------------------------------------------------

            temp_item = {
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

            preview_total = calculate_item_total(temp_item)

            st.info(
                f"💰 Thành tiền món này: "
                f"**{money(preview_total)}**"
            )

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

                st.session_state.cart.append(item)

                st.success(
                    f"Đã thêm {quantity} x {product['name']} vào đơn!"
                )

                st.rerun()

    # ========================================================
    # ĐƠN HÀNG HIỆN TẠI
    # ========================================================

    st.divider()

    st.header("🧾 CHI TIẾT ĐƠN HÀNG")

    if not st.session_state.cart:

        st.info(
            "Chưa có món nào trong đơn. "
            "Hãy chọn món phía trên và bấm 'THÊM MÓN VÀO ĐƠN'."
        )

    else:

        for index, item in enumerate(
            st.session_state.cart
        ):

            item_total = calculate_item_total(item)

            toppings_text = (
                ", ".join(
                    topping["name"]
                    for topping in item["toppings"]
                )
                if item["toppings"]
                else "Không"
            )

            st.markdown(
                f"""
                <div class="order-card">

                    <div class="order-title">
                        🧋 {index + 1}. {item['name']}
                    </div>

                    <div class="order-detail">

                        📏 <b>Size:</b> {item['size']}<br>

                        🔢 <b>Số lượng:</b>
                        {item['quantity']}<br>

                        🍬 <b>Đường:</b>
                        {item['sugar']}%<br>

                        🧊 <b>Đá:</b>
                        {item['ice']}%<br>

                        🧋 <b>Topping:</b>
                        {toppings_text}<br>

                        📝 <b>Ghi chú:</b>
                        {item['notes'] or 'Không'}<br>

                        💰 <b>Thành tiền:</b>
                        {money(item_total)}

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2 = st.columns([5, 1])

            with col2:

                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_{index}"
                ):

                    st.session_state.cart.pop(index)

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
                    {st.session_state.customer_name or "Khách lẻ"}
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

        st.subheader("📤 Xuất hóa đơn")

        col1, col2, col3 = st.columns(3)

        with col1:

            txt_data = create_txt_invoice()

            st.download_button(
                "📄 Tải hóa đơn TXT",
                data=txt_data,
                file_name=f"hoa_don_{st.session_state.order_id}.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col2:

            html_data = create_html_invoice()

            st.download_button(
                "🌐 Tải hóa đơn HTML",
                data=html_data,
                file_name=f"hoa_don_{st.session_state.order_id}.html",
                mime="text/html",
                use_container_width=True
            )

        with col3:

            if st.button(
                "🗑️ Tạo đơn mới",
                use_container_width=True
            ):

                reset_order()

                st.rerun()


# ============================================================
# 2. QUẢN LÝ DANH MỤC
# ============================================================

elif menu == "📋 Quản lý danh mục":

    st.header("📋 QUẢN LÝ DANH MỤC")

    st.subheader("➕ Tạo danh mục mới")

    new_category = st.text_input(
        "Tên danh mục mới",
        placeholder="Ví dụ: Cà phê, Đá xay..."
    )

    if st.button(
        "➕ Tạo danh mục",
        type="primary"
    ):

        if not new_category.strip():

            st.error("Vui lòng nhập tên danh mục.")

        elif any(
            c["name"].lower() == new_category.strip().lower()
            for c in st.session_state.data["categories"]
        ):

            st.error("Danh mục này đã tồn tại.")

        else:

            st.session_state.data["categories"].append(
                {
                    "id": get_next_id(
                        st.session_state.data["categories"]
                    ),
                    "name": new_category.strip(),
                    "visible": True
                }
            )

            save_data()

            st.success("Đã tạo danh mục.")

            st.rerun()

    st.divider()

    st.subheader("📂 Danh sách danh mục")

    for category in st.session_state.data["categories"]:

        col1, col2, col3, col4 = st.columns(
            [3, 2, 1, 1]
        )

        with col1:

            st.write(
                f"**{category['name']}**"
            )

        with col2:

            if category["visible"]:

                st.success("Đang hiển thị")

            else:

                st.warning("Đang ẩn")

        with col3:

            button_text = (
                "🙈 Ẩn"
                if category["visible"]
                else "👁️ Hiện"
            )

            if st.button(
                button_text,
                key=f"cat_visible_{category['id']}"
            ):

                category["visible"] = not category["visible"]

                save_data()

                st.rerun()

        with col4:

            if st.button(
                "🗑️ Xóa",
                key=f"cat_delete_{category['id']}"
            ):

                # Không cho xóa nếu đang có món thuộc danh mục
                used = any(
                    p["category"] == category["name"]
                    for p in st.session_state.data["products"]
                )

                if used:

                    st.error(
                        "Không thể xóa vì danh mục đang có món."
                    )

                else:

                    st.session_state.data["categories"].remove(
                        category
                    )

                    save_data()

                    st.rerun()

        edit_name = st.text_input(
            "Sửa tên danh mục",
            value=category["name"],
            key=f"cat_edit_{category['id']}"
        )

        if st.button(
            "💾 Lưu tên",
            key=f"cat_save_{category['id']}"
        ):

            old_name = category["name"]

            category["name"] = edit_name.strip()

            # cập nhật category cho sản phẩm
            for product in st.session_state.data["products"]:

                if product["category"] == old_name:

                    product["category"] = edit_name.strip()

            save_data()

            st.success("Đã cập nhật.")

            st.rerun()


# ============================================================
# 3. QUẢN LÝ MÓN
# ============================================================

elif menu == "🍹 Quản lý món":

    st.header("🍹 QUẢN LÝ MÓN")

    categories = [
        c["name"]
        for c in st.session_state.data["categories"]
    ]

    if not categories:

        st.warning("Hãy tạo danh mục trước.")

    else:

        st.subheader("➕ Thêm món mới")

        with st.form("add_product_form"):

            col1, col2 = st.columns(2)

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
                    "Mô tả"
                )

            with col2:

                image_url = st.text_input(
                    "URL hình ảnh",
                    placeholder="https://..."
                )

                status = st.selectbox(
                    "Trạng thái món",
                    ["Còn hàng", "Hết hàng"]
                )

                st.write("Chênh lệch giá theo Size")

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

            if not product_name.strip():

                st.error("Vui lòng nhập tên món.")

            else:

                new_product = {

                    "id": get_next_id(
                        st.session_state.data["products"]
                    ),

                    "category": category,

                    "name": product_name.strip(),

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

                st.session_state.data["products"].append(
                    new_product
                )

                save_data()

                st.success("Đã thêm món.")

                st.rerun()

    st.divider()

    st.subheader("📋 Danh sách món")

    for product in st.session_state.data["products"]:

        with st.expander(
            f"{product['name']} – {money(product['price'])}"
        ):

            col1, col2 = st.columns([1, 3])

            with col1:

                if product["image"]:

                    try:
                        st.image(
                            product["image"],
                            use_container_width=True
                        )
                    except:
                        pass

            with col2:

                st.write(
                    f"**Danh mục:** {product['category']}"
                )

                st.write(
                    f"**Giá cơ bản:** {money(product['price'])}"
                )

                st.write(
                    f"**Size S:** +{money(product['sizes']['S'])}"
                )

                st.write(
                    f"**Size M:** +{money(product['sizes']['M'])}"
                )

                st.write(
                    f"**Size L:** +{money(product['sizes']['L'])}"
                )

                st.write(
                    f"**Trạng thái:** {product['status']}"
                )

                st.write(
                    product["description"]
                )

            st.markdown("---")

            # ------------------------------------------------
            # SỬA MÓN
            # ------------------------------------------------

            st.markdown("### ✏️ Chỉnh sửa món")

            edit_col1, edit_col2 = st.columns(2)

            with edit_col1:

                edit_name = st.text_input(
                    "Tên món",
                    value=product["name"],
                    key=f"edit_name_{product['id']}"
                )

                edit_category = st.selectbox(
                    "Danh mục",
                    categories,
                    index=(
                        categories.index(product["category"])
                        if product["category"] in categories
                        else 0
                    ),
                    key=f"edit_category_{product['id']}"
                )

                edit_price = st.number_input(
                    "Giá cơ bản",
                    min_value=0,
                    value=int(product["price"]),
                    step=1000,
                    key=f"edit_price_{product['id']}"
                )

            with edit_col2:

                edit_image = st.text_input(
                    "URL hình ảnh",
                    value=product["image"],
                    key=f"edit_image_{product['id']}"
                )

                edit_status = st.selectbox(
                    "Trạng thái",
                    ["Còn hàng", "Hết hàng"],
                    index=(
                        0
                        if product["status"] == "Còn hàng"
                        else 1
                    ),
                    key=f"edit_status_{product['id']}"
                )

                edit_description = st.text_area(
                    "Mô tả",
                    value=product["description"],
                    key=f"edit_description_{product['id']}"
                )

            size_col1, size_col2, size_col3 = st.columns(3)

            with size_col1:

                edit_s = st.number_input(
                    "Size S +",
                    min_value=0,
                    value=int(product["sizes"]["S"]),
                    step=1000,
                    key=f"edit_s_{product['id']}"
                )

            with size_col2:

                edit_m = st.number_input(
                    "Size M +",
                    min_value=0,
                    value=int(product["sizes"]["M"]),
                    step=1000,
                    key=f"edit_m_{product['id']}"
                )

            with size_col3:

                edit_l = st.number_input(
                    "Size L +",
                    min_value=0,
                    value=int(product["sizes"]["L"]),
                    step=1000,
                    key=f"edit_l_{product['id']}"
                )

            button_col1, button_col2 = st.columns(2)

            with button_col1:

                if st.button(
                    "💾 LƯU THAY ĐỔI",
                    key=f"save_product_{product['id']}",
                    type="primary"
                ):

                    product["name"] = edit_name.strip()

                    product["category"] = edit_category

                    product["price"] = edit_price

                    product["image"] = edit_image.strip()

                    product["status"] = edit_status

                    product["description"] = edit_description.strip()

                    product["sizes"] = {
                        "S": edit_s,
                        "M": edit_m,
                        "L": edit_l
                    }

                    save_data()

                    st.success("Đã cập nhật món.")

                    st.rerun()

            with button_col2:

                if st.button(
                    "🗑️ XÓA MÓN",
                    key=f"delete_product_{product['id']}"
                ):

                    st.session_state.data["products"].remove(
                        product
                    )

                    save_data()

                    st.success("Đã xóa món.")

                    st.rerun()


# ============================================================
# 4. QUẢN LÝ TOPPING
# ============================================================

elif menu == "🥤 Quản lý topping":

    st.header("🥤 QUẢN LÝ TOPPING")

    st.subheader("➕ Thêm topping")

    with st.form("add_topping_form"):

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
            ["Còn hàng", "Hết hàng"]
        )

        topping_submit = st.form_submit_button(
            "➕ THÊM TOPPING",
            type="primary"
        )

    if topping_submit:

        if not topping_name.strip():

            st.error("Vui lòng nhập tên topping.")

        else:

            new_topping = {

                "id": get_next_id(
                    st.session_state.data["toppings"]
                ),

                "name": topping_name.strip(),

                "price": topping_price,

                "status": topping_status,

                "visible": True
            }

            st.session_state.data["toppings"].append(
                new_topping
            )

            save_data()

            st.success("Đã thêm topping.")

            st.rerun()

    st.divider()

    st.subheader("📋 Danh sách topping")

    for topping in st.session_state.data["toppings"]:

        with st.expander(
            f"{topping['name']} – {money(topping['price'])}"
        ):

            edit_name = st.text_input(
                "Tên topping",
                value=topping["name"],
                key=f"top_name_{topping['id']}"
            )

            edit_price = st.number_input(
                "Giá",
                min_value=0,
                value=int(topping["price"]),
                step=1000,
                key=f"top_price_{topping['id']}"
            )

            edit_status = st.selectbox(
                "Trạng thái",
                ["Còn hàng", "Hết hàng"],
                index=(
                    0
                    if topping["status"] == "Còn hàng"
                    else 1
                ),
                key=f"top_status_{topping['id']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                if st.button(
                    "💾 Lưu",
                    key=f"save_top_{topping['id']}"
                ):

                    topping["name"] = edit_name.strip()

                    topping["price"] = edit_price

                    topping["status"] = edit_status

                    save_data()

                    st.success("Đã cập nhật.")

                    st.rerun()

            with col2:

                visible_text = (
                    "🙈 Ẩn"
                    if topping["visible"]
                    else "👁️ Hiện"
                )

                if st.button(
                    visible_text,
                    key=f"visible_top_{topping['id']}"
                ):

                    topping["visible"] = not topping["visible"]

                    save_data()

                    st.rerun()

            with col3:

                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_top_{topping['id']}"
                ):

                    st.session_state.data["toppings"].remove(
                        topping
                    )

                    save_data()

                    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "🧋 Milk Tea Order & Billing"
)

st.sidebar.caption(
    "Quản lý món • Order • Tính bill • Xuất hóa đơn"
)
```
