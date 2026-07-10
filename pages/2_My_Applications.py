import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from db.database import init_db, list_applications, update_status, delete_application

st.set_page_config(page_title="My Applications", page_icon="📋", layout="wide")
init_db()

st.title("📋 My Applications")
st.caption("Track every job you've applied to.")

STATUS_OPTIONS = ["applied", "interview", "offer", "rejected", "saved"]
STATUS_EMOJI = {
    "applied": "📨",
    "interview": "🎤",
    "offer": "🎉",
    "rejected": "❌",
    "saved": "🔖",
}

apps = list_applications()

if not apps:
    st.info("No applications saved yet. Head back to the main page to analyse a job and save it.")
    st.stop()

st.write(f"**{len(apps)} application(s)** on record.")
st.divider()

for app in apps:
    emoji = STATUS_EMOJI.get(app["status"], "📨")
    with st.expander(f"{emoji} {app['job_title']} — {app['company']}  |  {app['status'].upper()}"):
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.markdown(f"**Company:** {app['company']}")
            if app["job_url"]:
                st.markdown(f"**URL:** [{app['job_url']}]({app['job_url']})")
            st.markdown(f"**Deadline:** {app['deadline'] or '—'}")
            st.markdown(f"**Saved on:** {app['created_at'][:10]}")

        with col2:
            new_status = st.selectbox(
                "Update status",
                STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(app["status"]) if app["status"] in STATUS_OPTIONS else 0,
                key=f"status_{app['id']}",
            )
            if new_status != app["status"]:
                if st.button("Save status", key=f"save_{app['id']}"):
                    update_status(app["id"], new_status)
                    st.success("Status updated.")
                    st.rerun()

        with col3:
            if st.button("🗑️ Delete", key=f"del_{app['id']}", type="secondary"):
                delete_application(app["id"])
                st.warning(f"Deleted application for {app['job_title']}.")
                st.rerun()

        if app.get("cover_letter"):
            with st.container():
                st.markdown("**Cover Letter:**")
                st.markdown(app["cover_letter"])
