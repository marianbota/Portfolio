import streamlit as st


st.title("My Contact Information")

st.markdown("Feel free to reach out!")

# Email
st.subheader("Email:")
your_email = "marian.bota@proton.me"  
st.markdown(f"[{your_email}](mailto:{your_email})")

# LinkedIn
st.subheader("LinkedIn:")
linkedin_url = "www.linkedin.com/in/marian-bota-47607116a" 
st.markdown(f"[My LinkedIn Profile]({linkedin_url})")

# GitHub
st.subheader("GitHub:")
github_url = "https://github.com/marianbota"  # Replace with your GitHub username
st.markdown(f"[My GitHub Profile]({github_url})")

# Kaggle
st.subheader("Kaggle:")
kaggle_url = "https://www.kaggle.com/marianbota"  # Replace with your Kaggle username
st.markdown(f"[My Kaggle Profile]({kaggle_url})")

st.markdown("---")
st.markdown("Thank you for visiting!")
