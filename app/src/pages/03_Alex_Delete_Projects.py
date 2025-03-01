import streamlit as st
import requests
import os
from modules.nav import SideBarLinks

# Sidebar navigation
SideBarLinks(show_home=True)

# Set BASE_URL from environment or use default
BASE_URL = os.getenv("BASE_URL", "http://web-api:4000")

# Alex's user_id (assuming you know the user_id for Alex; replace 1 with actual user_id for Alex)
ALEX_USER_ID = 1

# Page title
st.title("Manage Projects")
st.write("View and delete your projects as needed.")

# Fetch Alex's projects
response = requests.get(f"{BASE_URL}/alex/projects", params={"user_id": ALEX_USER_ID})  # Fetch projects by user_id
if response.status_code == 200:
    projects = response.json()  # Save fetched projects
    st.session_state["projects"] = projects  # Store in session state for reuse
else:
    st.error("Failed to fetch projects.")
    projects = []

# Check if projects exist
if projects:
    st.markdown(
        """
        <div style="
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            justify-content: center;
        ">
        """,
        unsafe_allow_html=True,
    )

    # Loop through each project and create cards with delete buttons
    for idx, project in enumerate(projects):
        st.markdown(
            f"""
            <div style="
                width: 300px;
                background-color: #333333;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 16px;
                margin: 8px;
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
                color: white;
                text-align: center;
                display: inline-block;
                vertical-align: top;
            ">
                <h4>{project.get('title', 'Unnamed Project')}</h4>
                <p><b>Description:</b> {project.get('description', 'No description')}</p>
                <p><b>Tags:</b> {project.get('tags', 'No tags')}</p>
                <p><b>Upload Date:</b> {project.get('upload_date', 'Unknown')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Delete button for each project
        if f"delete_id-{idx}" not in st.session_state:
            st.session_state[f"delete_id-{idx}"] = project.get("project_id")

        if st.button(f"Delete {project.get('title', 'Unnamed Project')}", key=f"delete-{idx}"):
            project_id = st.session_state[f"delete_id-{idx}"]

            # Perform DELETE request to backend
            delete_response = requests.delete(f"{BASE_URL}/alex/projects/{project_id}")

            if delete_response.status_code == 200:
                st.success(f"Deleted project: {project.get('title', 'Unnamed Project')}")
                del st.session_state[f"delete_id-{idx}"]
                # Update the session state to reflect deletion
                st.session_state["projects"] = [
                    p for p in st.session_state["projects"] if p.get("project_id") != project_id
                ]
            else:
                st.error(f"Failed to delete the project: {delete_response.status_code}")

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No projects found for Alex.")

# Back button to Alex's home page
if st.button("Back to Alex's Home"):
    st.switch_page("pages/00_Alex_Home.py")
