import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all('a')

    extracted_links = []
    for link in links:
        href = link.get('href')
        text = link.get_text(strip=True)
        if href:
            extracted_links.append({"Anchor Text": text, "URL": href})

    return extracted_links

def main():
    st.title("🔗 Link Extractor Tool")

    url = st.text_input("Enter a URL to extract links from", placeholder="https://example.com")

    if st.button("Extract Links"):
        if url:
            with st.spinner("Extracting links..."):
                links = extract_links(url)
            
            if links:
                df = pd.DataFrame(links)
                st.success(f"Extracted {len(links)} links!")

                st.dataframe(df)

                # Provide download button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name='extracted_links.csv',
                    mime='text/csv',
                )
            else:
                st.warning("No links found or error occurred.")
        else:
            st.error("
