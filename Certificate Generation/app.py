import os
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import zipfile

def main():
    st.title("Certificate Generator")
    st.write("Upload a certificate template image and a CSV file with participant names to generate certificates.")

    # File uploads
    st.subheader("1. Upload Files")
    template_file = st.file_uploader("Upload Certificate Template (JPG, PNG)", type=["jpg", "jpeg", "png"])
    csv_file = st.file_uploader("Upload Participants CSV File", type=["csv"])
    
    # Font options
    st.subheader("2. Customize Settings")
    
    font_options = ["Arial", "Times New Roman", "Courier", "Verdana", "DejaVuSans"]
    selected_font = st.selectbox("Select Font", font_options, index=4)
    
    font_size = st.slider("Font Size", min_value=20, max_value=200, value=100, step=5)
    font_color = st.color_picker("Font Color", "#E1E1E1")
    
    # Preview and positioning
    if template_file and csv_file:
        # Load the data
        df = pd.read_csv(csv_file)
        
        # Display column selection
        st.subheader("3. Select Name Column")
        name_column = st.selectbox("Select the column containing participant names", df.columns)
        
        # Show template preview
        st.subheader("4. Preview & Position Text")
        template_img = Image.open(template_file)
        
        # Get image dimensions
        img_width, img_height = template_img.size
        
        # Position controls
        col1, col2 = st.columns(2)
        with col1:
            x_pos = st.slider("X Position", 0, img_width, img_width // 2)
        with col2:
            y_pos = st.slider("Y Position", 0, img_height, img_height // 2)
        
        # Preview with sample text
        preview_img = template_img.copy()
        draw = ImageDraw.Draw(preview_img)
        
        # Try loading font
        try:
            font = ImageFont.truetype(f"{selected_font}.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
            st.warning(f"Could not load font {selected_font}. Using default font instead.")
        
        # Convert hex color to RGB
        rgb_color = tuple(int(font_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        sample_name = "Sample Name"
        draw.text((x_pos, y_pos), sample_name, font=font, fill=rgb_color)
        
        # Display the preview
        st.image(preview_img, caption="Certificate Preview", use_column_width=True)
        
        # Generate certificates
        if st.button("Generate Certificates"):
            certificates_zip = generate_certificates(
                df, 
                name_column,
                template_img,
                selected_font,
                font_size,
                rgb_color,
                (x_pos, y_pos)
            )
            
            # Provide download link
            st.download_button(
                label="Download Certificates (ZIP)",
                data=certificates_zip,
                file_name="certificates.zip",
                mime="application/zip"
            )

def generate_certificates(df, name_column, template_img, font_name, font_size, font_color, text_position):
    # Create a buffer for ZIP file
    zip_buffer = BytesIO()
    
    # Create a ZIP file
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Try loading font
        try:
            font = ImageFont.truetype(f"{font_name}.ttf", font_size)
        except IOError:
            # Use default font if specified font can't be loaded
            font = ImageFont.load_default()
        
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, row in df.iterrows():
            # Update progress
            progress = int((i + 1) / len(df) * 100)
            progress_bar.progress(progress)
            
            participant_name = row[name_column]
            status_text.text(f"Generating certificate for {participant_name}...")
            
            # Create certificate
            cert_img = template_img.copy()
            draw = ImageDraw.Draw(cert_img)
            draw.text(text_position, participant_name, font=font, fill=font_color)
            
            # Save to bytes
            img_byte_arr = BytesIO()
            cert_img.save(img_byte_arr, format='PDF')
            img_byte_arr.seek(0)
            
            # Add to ZIP
            zip_file.writestr(f"{participant_name}_certificate.pdf", img_byte_arr.getvalue())
        
        status_text.text("All certificates generated!")
    
    # Reset buffer position and return
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

if __name__ == "__main__":
    main()