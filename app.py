import streamlit as st
from supabase import create_client

# ... (инициализация supabase как раньше) ...

# Получаем параметры из URL (например, ?id=1)
params = st.query_params
product_id = params.get("id")

if product_id:
    # --- СТРАНИЦА ТОВАРА (как на Allegro) ---
    response = supabase.table("shop_products").select("*").eq("id", product_id).execute()
    if response.data:
        p = response.data[0]
        st.button("← Назад к списку", on_click=lambda: st.query_params.clear())
        st.title(p['product_name'])
        st.write(f"### Цена: {p['price']} руб.")
        st.write(f"Продавец: {p['seller_name']}")
        st.link_button("Купить сейчас", p.get('donation_url', '#'))
    else:
        st.error("Товар не найден")
else:
    # --- ГЛАВНАЯ СТРАНИЦА (список) ---
    st.title("💰 Магазин Robux")
    # ... (форма добавления как была) ...
    
    st.subheader("Список товаров")
    response = supabase.table("shop_products").select("*").execute()
    for p in response.data:
        # При клике на колонку меняем URL, и Streamlit перезагрузится на страницу товара
        if st.button(f"Посмотреть: {p['product_name']}", key=p['id']):
            st.query_params["id"] = p['id']
            st.rerun()
