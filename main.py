import qrcode
import qrcode.image.svg
import os
import base64

def generate_svg_qr(data, logo_path, output_filename):
    if not output_filename.lower().endswith('.svg'):
        output_filename += '.svg'

    # Level H allows 30% error correction
    qr = qrcode.QRCode(
        version=5, 
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    base_svg_str = img.to_string().decode('utf-8')

    if logo_path and os.path.exists(logo_path):
        qr_size = 450 
        logo_size = 100 
        offset = (qr_size - logo_size) // 2
        
        # Read the external file and convert to Base64
        with open(logo_path, "rb") as f:
            encoded_data = base64.b64encode(f.read()).decode("utf-8")
        
        # Determine the correct image type for the SVG tag
        ext = logo_path.lower().split('.')[-1]
        if ext == 'svg':
            mime_type = "image/svg+xml"
        elif ext == 'png':
            mime_type = "image/png"
        elif ext == 'webp':
            mime_type = "image/webp"
        elif ext in ['jpg', 'jpeg']:
            mime_type = "image/jpeg"
        else:
            mime_type = "image/png" # Default fallback
        
        # Create a white background box
        bg_rect = f'<rect x="{offset - 5}" y="{offset - 5}" width="{logo_size + 10}" height="{logo_size + 10}" fill="white" rx="10"/>'
        
        # Embed the image using the correct mime_type
        href = f"data:{mime_type};base64,{encoded_data}"
        image_tag = f'<image x="{offset}" y="{offset}" width="{logo_size}" height="{logo_size}" href="{href}"/>'
        
        # Inject our background and logo right before the closing </svg> tag
        injected_content = f'{bg_rect}\n{image_tag}\n</svg>'
        final_svg_str = base_svg_str.replace('</svg>', injected_content)
        
        print(f"\n[+] Successfully injected logo from: {logo_path}")
    else:
        final_svg_str = base_svg_str
        print("\n[+] Generating standard SVG QR without a logo.")

    with open(output_filename, 'w') as f:
        f.write(final_svg_str)
        
    print(f"[+] QR code saved successfully as: {output_filename}\n")


def main():
    print("========================================")
    print("   HYBRID QR GENERATOR (TERMUX)         ")
    print("========================================")
    
    logo_dir = "logos"
    if not os.path.exists(logo_dir):
        os.makedirs(logo_dir)

    data = input("Enter the URL or text for the QR code: ")
    output_filename = input("Enter output filename (e.g., my_qr.svg): ")

    # Now scans for SVG, PNG, WEBP, and JPG
    allowed_extensions = ('.svg', '.png', '.webp', '.jpg', '.jpeg')
    available_logos = [f for f in os.listdir(logo_dir) if f.lower().endswith(allowed_extensions)]
    
    print("\nSelect a logo from your 'logos' folder:")
    
    for i, logo in enumerate(available_logos, start=1):
        print(f"{i}. {logo}")
    
    no_logo_option = len(available_logos) + 1
    print(f"{no_logo_option}. No Logo (Standard QR)")
    
    try:
        choice = int(input(f"\nEnter your choice (1-{no_logo_option}): "))
        if 1 <= choice <= len(available_logos):
            selected_logo_path = os.path.join(logo_dir, available_logos[choice - 1])
        elif choice == no_logo_option:
            selected_logo_path = None
        else:
            print("Invalid choice. Generating without a logo.")
            selected_logo_path = None
    except ValueError:
        print("Invalid input. Generating without a logo.")
        selected_logo_path = None

    generate_svg_qr(data, selected_logo_path, output_filename)

if __name__ == "__main__":
    main()
      
