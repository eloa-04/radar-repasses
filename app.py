import streamlit as st
import pandas as pd

st.title("Radar de Repasses")
df = pd.read_csv("pedidos.csv", parse_dates=["data"])
divs = pd.read_csv("divergencias.csv", parse_dates=["data"])

c1, c2, c3 = st.columns(3)
c1.metric("Valor bruto", f"R$ {df.valor_bruto.sum():,.2f}")
c2.metric("Líquido esperado", f"R$ {df.valor_esperado.sum():,.2f}")
c3.metric("Divergências", len(divs))

st.subheader("Esperado vs repassado por dia")
diario = df.groupby("data")[["valor_esperado", "valor_repassado"]].sum()
st.line_chart(diario)

st.subheader("Divergências")
st.dataframe(divs)

st.subheader("Resumo com IA")
if st.button("Gerar resumo"):
    from google import genai
    client = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    prompt = "Resuma em português, em até 5 linhas, as divergências de repasse abaixo e sugira ações:\n" + divs.head(30).to_string()
    resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    st.write(resp.text)
