import streamlit as st
from dataclasses import asdict
import pandas as pd
from db_query import get_conversations, get_stats

st.title("Course Assistant Dashboard")

stats = get_stats()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Conversations", stats.total)
col2.metric("Avg Response Time", f"{stats.avg_response_time:.2f}s")
col3.metric("Total Cost", f"{stats.total_cost:.4f}")
col4.metric("Avg Tokens", f"{stats.avg_tokens:.0f}")

records = get_conversations(limit=100)
df = pd.DataFrame([asdict(r) for r in records])

st.subheader("Cost over time")
st.line_chart(df, x="timestamp", y="cost")

st.subheader("Response time over time")
st.line_chart(df, x="timestamp", y="response_time")

st.subheader("Recent conversations")
records = get_conversations(limit=20)

for record in records:
    st.write(f"**{record.prompt[:80]}...**")
    st.write(f"{record.answer[:200]}...")
    st.write(f"Time: {record.response_time:.2f}s | Cost: ${record.cost:.4f}")
    st.divider()

