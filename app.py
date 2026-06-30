import streamlit as st
from supabase import create_client

# 1. Настройка подключения (ВСТАВЬТЕ СВОИ КЛЮЧИ!)
SUPABASE_URL = "https://cfsvmuewbskyqumhkyah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNmc3ZtdWV3YnNreXF1bWhreWFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI2Mzg5MzMsImV4cCI6MjA5ODIxNDkzM30.O6gXrIDbi2J2-JYUYGIOSW6Zm2cb8Ib7YhldhF_3_Wk"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Магазин Robux", layout="centered")

# 2. Логика отображения (Параметры URL)
params = st.query_params
product_id = params.get("id")

if product_id:
    # --- СТРАНИЦА ТОВАРА ---
    response = supabase.table("shop_products").select("*").eq("id", product_id).execute()
    if response.data:
        p = response.data[0]
        if st.button("← Назад к списку"):
            st.query_params.clear()
            st.rerun()
        st.title(p['product_name'])
        st.write(f"### Цена: {p['price']} руб.")
        st.write(f"Продавец: {p['seller_name']}")
        st.link_button("Купить сейчас", p.get('donation_url', '#'))
    else:
        st.error("Товар не найден")
else:
    # --- ГЛАВНАЯ СТРАНИЦА ---
    st.title("💰 Магазин Robux")
    
    # Форма добавления
    with st.expander("➕ Добавить новый товар"):
        with st.form("add_product"):
            seller = st.text_input("Имя продавца")
            product = st.text_input("Название товара")
            price = st.number_input("Цена", min_value=0.0)
            donation_url = st.text_input("Ссылка на оплату")
            submit = st.form_submit_button("Добавить")
            if submit:
                supabase.table("shop_products").insert({
                    "seller_name": seller, "product_name": product, 
                    "price": price, "donation_url": donation_url
                }).execute()
                st.rerun()

    # Список товаров
    st.subheader("Список товаров")
    response = supabase.table("shop_products").select("*").execute()
    for p in response.data:
        if st.button(f"Посмотреть: {p['product_name']}", key=str(p['id'])):
            st.query_params["id"] = p['id']
            st.rerun()
