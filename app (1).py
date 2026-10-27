from datetime import datetime
import json
import os
import random
import streamlit as st

DATA_FILE = "lwandle_data.json"

DEFAULT_DATA = {
    "shops": [
        {
            "id": "mamas-kota",
            "name": "Mama's Kota & Vetkoek Corner",
            "tagline": "Legendary township kotas loaded with chips & Russian",
            "is_open": True,
            "walking_delivery_fee": 10.0,
            "walking_delivery_enabled": True,
            "password": "123",
            "menu": [
                {
                    "id": "mk1",
                    "name": "The Lwandle Beast Kota",
                    "price": 45.0,
                    "description": "Russian, polony, egg, cheese, chips, and special sauce.",
                    "is_available": True,
                },
                {
                    "id": "mk2",
                    "name": "Standard Kota",
                    "price": 25.0,
                    "description": "Chips, polony, cheese, and achar.",
                    "is_available": True,
                },
                {
                    "id": "mk3",
                    "name": "Vetkoek & Mince",
                    "price": 30.0,
                    "description": "Golden crispy vetkoek filled with savory spiced mince.",
                    "is_available": True,
                },
                {
                    "id": "mk4",
                    "name": "Snoek Fish Roll",
                    "price": 35.0,
                    "description": "Freshly fried snoek chunk in a warm roll with lettuce.",
                    "is_available": False,
                },
            ],
        },
        {
            "id": "mzansi-grill",
            "name": "Mzansi Braai & Chips",
            "tagline": "Hot chips, wors rolls, and flame-grilled goodness",
            "is_open": True,
            "walking_delivery_fee": 15.0,
            "walking_delivery_enabled": True,
            "password": "123",
            "menu": [
                {
                    "id": "mg1",
                    "name": "Boerewors Roll Deluxe",
                    "price": 35.0,
                    "description": "Juicy boerewors in a fresh roll with chakalaka & onions.",
                    "is_available": True,
                },
                {
                    "id": "mg2",
                    "name": "Large Slap Chips (Medium)",
                    "price": 20.0,
                    "description": "Golden township slap chips with vinegar and salt.",
                    "is_available": True,
                },
                {
                    "id": "mg3",
                    "name": "Chicken Wing Basket (6 pcs)",
                    "price": 50.0,
                    "description": "Spicy peri-peri wings served with chips.",
                    "is_available": True,
                },
            ],
        },
        {
            "id": "zola-kitchen",
            "name": "Zola's Fast Food & Sphatlo",
            "tagline": "Quick meals and cold drinks right in the hood",
            "is_open": False,
            "walking_delivery_fee": 10.0,
            "walking_delivery_enabled": True,
            "password": "123",
            "menu": [
                {
                    "id": "zk1",
                    "name": "Cheese & Egg Sphatlo",
                    "price": 30.0,
                    "description": "Half-loaf hollowed out and packed with chips, egg, and cheese.",
                    "is_available": True,
                },
                {
                    "id": "zk2",
                    "name": "Vienna & Chips Parcel",
                    "price": 28.0,
                    "description": "Sliced viennas and chips wrapped in paper.",
                    "is_available": True,
                },
            ],
        },
        {
            "id": "khaya-burger",
            "name": "Khaya Burger & Kota Bar",
            "tagline": "Juicy patties, double cheese, and township vibes",
            "is_open": True,
            "walking_delivery_fee": 0.0,
            "walking_delivery_enabled": False,
            "password": "123",
            "menu": [
                {
                    "id": "kb1",
                    "name": "Double Cheese Burger",
                    "price": 40.0,
                    "description": "Two beef patties, cheddar cheese, lettuce, burger sauce.",
                    "is_available": True,
                },
                {
                    "id": "kb2",
                    "name": "Chicken Burger & Chips",
                    "price": 45.0,
                    "description": "Crispy chicken fillet with mayo and regular chips.",
                    "is_available": True,
                },
            ],
        },
    ],
    "orders": [],
}


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


st.set_page_config(
    page_title="LwandleFastfood Orders",
    page_icon="🍔",
    layout="centered",
)

# Initialize session state data
if "db" not in st.session_state:
    st.session_state["db"] = load_data()

# App header
st.title("🍔 LwandleFastfood Orders")
st.caption(
    "Order pickup or short walking delivery from local township fast-food spots in Lwandle."
)

# Navigation mode
mode = st.sidebar.radio(
    "Select Mode",
    ["🛒 Customer: Order Food", "🔐 Shop Owner Portal"],
)
st.sidebar.divider()

db = st.session_state["db"]

# ==================== CUSTOMER VIEW ====================
if mode == "🛒 Customer: Order Food":
    st.subheader("Explore Local Shops")

    search_query = st.text_input(
        "🔍 Search shops or food...",
        placeholder="e.g. Kota, Chips, Burger",
    )

    shops = db["shops"]
    if search_query:
        filtered_shops = []
        for s in shops:
            match = (
                search_query.lower() in s["name"].lower()
                or search_query.lower() in s["tagline"].lower()
            )
            for m in s["menu"]:
                if search_query.lower() in m["name"].lower():
                    match = True
            if match:
                filtered_shops.append(s)
        shops = filtered_shops

    if not shops:
        st.info("No shops found matching your search.")
        st.stop()

    shop_options = {s["name"]: s for s in shops}
    selected_shop_name = st.selectbox(
        "Choose a Shop to View Menu",
        list(shop_options.keys()),
    )

    if selected_shop_name:
        shop = shop_options[selected_shop_name]
        st.divider()

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {shop['name']}")
            st.write(shop["tagline"])
        with col2:
            if shop["is_open"]:
                st.success("🟢 OPEN")
            else:
                st.error("🔴 CLOSED")

        if shop["walking_delivery_enabled"] and shop["walking_delivery_fee"] > 0:
            st.info(
                f"🚶 Walking delivery available for R{shop['walking_delivery_fee']:.2f} (Pickup is also free)"
            )
        else:
            st.info("📦 Pickup only from shop")

        st.markdown("#### Menu")

        if not shop["is_open"]:
            st.warning(
                "⚠️ This shop is currently closed. You can view the menu, but orders cannot be placed right now."
            )

        # Order form
        with st.form(key=f"order_form_{shop['id']}"):
            cart_quantities = {}
            for item in shop["menu"]:
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    availability_badge = "✅" if item["is_available"] else "❌ *[Sold Out]*"
                    st.markdown(f"**{item['name']}** {availability_badge}")
                    st.caption(f"{item['description']} — **R{item['price']:.2f}**")
                with c2:
                    qty = st.number_input(
                        "Qty",
                        min_value=0,
                        max_value=10,
                        value=0,
                        key=f"item_{shop['id']}_{item['id']}",
                        disabled=not (shop["is_open"] and item["is_available"]),
                        label_visibility="collapsed",
                    )
                    cart_quantities[item["id"]] = {
                        "name": item["name"],
                        "price": item["price"],
                        "qty": qty,
                    }
                with c3:
                    st.write(
                        f"**R{item['price'] * qty:.2f}**" if qty > 0 else "R0.00"
                    )
                st.divider()

            st.markdown("#### Checkout Details")
            cust_name = st.text_input(
                "Your Name",
                placeholder="e.g. Sibusiso Dlamini",
            )
            cust_phone = st.text_input(
                "Phone Number",
                placeholder="e.g. 072 123 4567",
            )
            cust_notes = st.text_area(
                "Special Instructions / Notes",
                placeholder="e.g. Extra chilli sauce, ring doorbell",
            )

            request_delivery = False
            if shop["walking_delivery_enabled"] and shop["walking_delivery_fee"] > 0:
                request_delivery = st.checkbox(
                    f"Request walking delivery (+R{shop['walking_delivery_fee']:.2f})"
                )

            submitted = st.form_submit_button(
                "🚀 Place Order",
                disabled=not shop["is_open"],
            )

            if submitted:
                ordered_items = [
                    item for item in cart_quantities.values() if item["qty"] > 0
                ]
                if not ordered_items:
                    st.error("⚠️ Please select at least one item to order.")
                elif not cust_name.strip() or not cust_phone.strip():
                    st.error("⚠️ Please provide your name and phone number.")
                else:
                    subtotal = sum(item["price"] * item["qty"] for item in ordered_items)
                    delivery_fee = shop["walking_delivery_fee"] if request_delivery else 0.0
                    total = subtotal + delivery_fee

                    order_id = f"LW-{random.randint(1000, 9999)}"
                    new_order = {
                        "order_id": order_id,
                        "shop_id": shop["id"],
                        "customer_name": cust_name.strip(),
                        "customer_phone": cust_phone.strip(),
                        "items": ordered_items,
                        "subtotal": subtotal,
                        "request_delivery": request_delivery,
                        "delivery_fee": delivery_fee,
                        "total": total,
                        "notes": cust_notes.strip(),
                        "status": "Pending",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }

                    db["orders"].append(new_order)
                    save_data(db)

                    st.success(
                        f"🎉 Order successfully placed! Reference: **{order_id}**"
                    )
                    st.balloons()
                    st.info(
                        f"Total to pay: **R{total:.2f}** ({'Walking Delivery' if request_delivery else 'Pickup'}). Pay at shop or upon delivery."
                    )

# ==================== SHOP OWNER PORTAL ====================
else:
    st.subheader("🔐 Shop Owner Dashboard")
    st.caption("Manage your shop status, menu items, and incoming orders.")

    if not db["shops"]:
        st.warning("No shops have been configured yet.")
        st.stop()

    shop_options = {s["name"]: s for s in db["shops"]}
    owner_shop_name = st.selectbox("Select Your Shop", list(shop_options.keys()))
    shop = shop_options[owner_shop_name]

    password_input = st.text_input("Enter Owner Password", type="password")

    if password_input == shop["password"]:
        st.success(f"Access granted for {shop['name']}!")
        st.divider()

        tab1, tab2, tab3 = st.tabs(
            ["📦 Manage Orders", "⚙️ Shop Settings", "🍔 Menu Items"]
        )

        # TAB 1: ORDERS
        with tab1:
            st.markdown("### Incoming & Active Orders")
            shop_orders = [o for o in db["orders"] if o["shop_id"] == shop["id"]]

            if not shop_orders:
                st.info("No orders yet for your shop.")
            else:
                for idx, order in enumerate(reversed(shop_orders)):
                    with st.expander(
                        f"Order #{order['order_id']} — {order['customer_name']} ({order['status']}) — R{order['total']:.2f}"
                    ):
                        st.write(f"**Phone:** {order['customer_phone']}")
                        st.write(f"**Time:** {order['timestamp']}")
                        st.write(
                            f"**Type:** {'Walking Delivery (R' + str(order['delivery_fee']) + ')' if order['request_delivery'] else 'Pickup'}"
                        )
                        if order["notes"]:
                            st.write(f"**Notes:** {order['notes']}")

                        st.markdown("**Items:**")
                        for itm in order["items"]:
                            st.text(
                                f"- {itm['qty']}x {itm['name']} @ R{itm['price']:.2f} each"
                            )

                        st.write(f"**Total Amount:** R{order['total']:.2f}")

                        status_options = [
                            "Pending",
                            "Preparing",
                            "Ready for Pickup / Delivery",
                            "Completed",
                        ]
                        current_status_idx = (
                            status_options.index(order["status"])
                            if order["status"] in status_options
                            else 0
                        )
                        new_status = st.selectbox(
                            "Update Order Status",
                            status_options,
                            index=current_status_idx,
                            key=f"status_{order['order_id']}_{idx}",
                        )

                        if new_status != order["status"]:
                            for db_ord in db["orders"]:
                                if db_ord["order_id"] == order["order_id"]:
                                    db_ord["status"] = new_status
                                    save_data(db)
                                    st.success(f"Order status updated to: {new_status}")
                                    st.rerun()

        # TAB 2: SETTINGS
        with tab2:
            st.markdown("### Shop Operation Settings")

            new_open_status = st.toggle(
                "Shop is Open for Orders",
                value=shop["is_open"],
            )
            if new_open_status != shop["is_open"]:
                shop["is_open"] = new_open_status
                save_data(db)
                st.success(
                    f"Shop status updated to: {'Open 🟢' if new_open_status else 'Closed 🔴'}"
                )
                st.rerun()

            st.divider()

            st.markdown("#### Walking Delivery Settings")
            new_delivery_enabled = st.checkbox(
                "Enable Walking Delivery Option for Customers",
                value=shop["walking_delivery_enabled"],
            )
            new_delivery_fee = st.number_input(
                "Walking Delivery Fee (R)",
                min_value=0.0,
                step=5.0,
                value=float(shop["walking_delivery_fee"]),
            )

            if st.button("Save Delivery Settings"):
                shop["walking_delivery_enabled"] = new_delivery_enabled
                shop["walking_delivery_fee"] = new_delivery_fee
                save_data(db)
                st.success("Delivery settings saved successfully!")
                st.rerun()

        # TAB 3: MENU ITEMS
        with tab3:
            st.markdown("### Manage Menu Item Availability")

            for item in shop["menu"]:
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**{item['name']}** (R{item['price']:.2f})")
                    st.caption(item["description"])
                with c2:
                    item_avail = st.toggle(
                        "Available",
                        value=item["is_available"],
                        key=f"avail_{shop['id']}_{item['id']}",
                    )
                    if item_avail != item["is_available"]:
                        item["is_available"] = item_avail
                        save_data(db)
                        st.rerun()
                st.divider()

            st.markdown("#### Add New Menu Item")
            with st.form(key=f"add_item_form_{shop['id']}"):
                new_item_name = st.text_input("Item Name", placeholder="e.g. Dagwood Burger")
                new_item_price = st.number_input(
                    "Price (R)",
                    min_value=1.0,
                    step=5.0,
                    value=35.0,
                )
                new_item_desc = st.text_area(
                    "Description",
                    placeholder="Ingredients & details",
                )
                add_submitted = st.form_submit_button("Add Item to Menu")

                if add_submitted:
                    if not new_item_name.strip():
                        st.error("Please enter an item name.")
                    else:
                        new_item_id = f"{shop['id']}_{random.randint(100, 999)}"
                        new_menu_item = {
                            "id": new_item_id,
                            "name": new_item_name.strip(),
                            "price": new_item_price,
                            "description": new_item_desc.strip(),
                            "is_available": True,
                        }
                        shop["menu"].append(new_menu_item)
                        save_data(db)
                        st.success(f"Added '{new_item_name}' to menu!")
                        st.rerun()

    elif password_input:
        st.error(
            "❌ Incorrect password. (Hint: default password for demo shops is '123')"
        )
    else:
        st.info("💡 Please enter your owner password to access management tools.")