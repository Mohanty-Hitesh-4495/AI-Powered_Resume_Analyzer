import streamlit as st
from io import BytesIO
import os
from batch_processing import process_resumes  

# title and description
st.title("AI-Powered Resume Analyzer")
st.write("Upload up to 4 resumes in PDF format, and get an analysis in an Excel file.")

# resume upload section
uploaded_files = st.file_uploader(
    "Upload Resumes (PDF only, max 4 files)",
    type=["pdf"],
    accept_multiple_files=True
)

# limiting the number of uploaded files
if uploaded_files and len(uploaded_files) > 4:
    st.error("⚠️ You can only upload up to 4 files at a time.")
    uploaded_files = None  

# Process button
if uploaded_files and st.button("Analyze Resumes"):
    
    # saving uploaded files temporarily
    file_paths = []
    for uploaded_file in uploaded_files:
        temp_file_path = f"sample_resumes/temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_file.read())
        file_paths.append(temp_file_path)

    # Call the process_resumes function
    output_file_path = "output_files/analyzed_resumes.xlsx"
    try:
        process_resumes(file_paths, output_file_path)
        # Convert Excel file to bytes for downloading
        with open(output_file_path, "rb") as file:
            excel_bytes = BytesIO(file.read())
        
        # Allow user to download the processed file
        st.success("✅ Resumes analyzed successfully!")
        st.download_button(
            label="📥 Download Results",
            data=excel_bytes,
            file_name="analyzed_resumes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
    finally:
        # Cleanup temporary files
        for path in file_paths:
            try:
                os.remove(path)
            except Exception:
                pass

# Footer
st.markdown("---")
st.markdown("💡 Built with Streamlit by [Mohanty Hitesh]")
