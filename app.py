import streamlit as st
from supabase import create_client

# 1. Настройка страницы
st.set_page_config(page_title="Магазин Robux", layout="centered")

# 2. Подключение к Supabase 
# ВАЖНО: Вставьте ваши реальные данные сюда
SUPABASE_URL = "https://cfsvmuewbskyqumhkyah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNmc3ZtdWV3YnNreXF1bWhreWFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI2Mzg5MzMsImV4cCI6MjA5ODIxNDkzM30.O6gXrIDbi2J2-JYUYGIOSW6Zm2cb8Ib7YhldhF_3_Wk"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("💰 Магазин Robux")

# 3. Форма для добавления товаров
with st.expander("➕ Добавить новый товар"):
    with st.form("add_product"):
        seller = st.text_input("Имя продавца")
        product = st.text_input("Название товара")
        price = st.number_input("Цена", min_value=0.0)
        qr_url = st.text_input("Ссылка на QR-код (URL картинки)")
        submit = st.form_submit_button("Добавить")
        
        if submit:
            if seller and product:
                data = {
                    "seller_name": seller, 
                    "product_name": product, 
                    "price": price, 
                    "qr_code_url": qr_url
                }
                supabase.table("shop_products").insert(data).execute()
                st.success("Товар успешно добавлен!")
                st.rerun() # Обновляем страницу, чтобы сразу увидеть товар
            else:
                st.error("Пожалуйста, заполните имя продавца и название товара!")

# 4. Вывод списка товаров из базы
st.subheader("Список товаров")
try:
    response = supabase.table("shop_products").select("*").execute()
    products = response.data

    if not products:
        st.write("Пока товаров нет.")
    else:
        for p in products:
            st.write(f"### {p['product_name']}")
            st.write(f"**Продавец:** {p['seller_name']} | **Цена:** {p['price']}")
            
            # Если есть ссылка на QR, показываем картинку
            if p.get('qr_code_url'):
                try:
                    st.image(p['qr_code_url'], caption="Оплатить по QR", width=200)
                except:
                    st.write("Ссылка на QR-код не работает.")
            
            st.divider()
except Exception as e:
    st.error(f"Ошибка при загрузке товаров: {e}")
