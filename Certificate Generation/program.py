import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# Load the CSV file containing participant names
csv_file = 'participants.csv'
data = pd.read_csv(csv_file)

# Folder where the certificates will be saved
output_folder = 'Generated Certificate'
os.makedirs(output_folder, exist_ok=True)

# Path to the certificate template
template_path = 'certificate.jpg'

# Load the font
font_path = 'DejaVuSans.ttf'  # Make sure the font is in the same directory or provide the full path
font_size = 100
font = ImageFont.truetype(font_path, font_size)

# Certificate generation function
def generate_certificate(participant_name):
    # Open the certificate template
    template = Image.open(template_path)
    draw = ImageDraw.Draw(template)
    
    # Define the position where the name should be written (above the line in the middle)
    # Customize the coordinates based on the specific template layout
    text_position = (480,660)  # Change these values as necessary
    

    # Draw the participant's name on the certificate
    draw.text(text_position, participant_name, font=font, fill=(225, 225, 225))
    
    # Save the generated certificate
    output_path = os.path.join(output_folder, f'{participant_name}_certificate.pdf')
    template.save(output_path)
    print(f'Certificate saved for {participant_name}')

# Iterate through the CSV and generate certificates for each participant
for index, row in data.iterrows():
    participant_name = row['Name']  # Assuming the CSV has a column 'Name'
    generate_certificate(participant_name)

print("All certificates have been generated and saved.")
