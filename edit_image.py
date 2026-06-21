from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def edit_image_for_whatsapp(input_image_path, output_image_path, bot_name="KING LEO 10"):
    """
    Edit image for WhatsApp bot profile by adding bot name text
    
    Args:
        input_image_path: Path to the original image
        output_image_path: Path to save the edited image
        bot_name: Bot name to add to image (default: "KING LEO 10")
    """
    
    try:
        # Open the image
        img = Image.open(input_image_path)
        
        # Get image dimensions
        width, height = img.size
        
        # Create a copy to edit
        img_edited = img.copy()
        
        # Initialize drawing context
        draw = ImageDraw.Draw(img_edited)
        
        # Try to use a nice font, fallback to default if not available
        try:
            # Adjust font size based on image height
            font_size = int(height * 0.15)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Text to add
        text = bot_name
        
        # Get text bounding box to center it
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position (bottom center)
        x_position = (width - text_width) // 2
        y_position = height - text_height - int(height * 0.05)
        
        # Add text with outline effect for better visibility
        outline_width = 3
        outline_color = (0, 0, 0, 255)  # Black outline
        text_color = (0, 150, 255, 255)  # Blue color matching the image theme
        
        # Draw outline
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                draw.text(
                    (x_position + adj_x, y_position + adj_y),
                    text,
                    font=font,
                    fill=outline_color
                )
        
        # Draw main text
        draw.text(
            (x_position, y_position),
            text,
            font=font,
            fill=text_color
        )
        
        # Enhance the image slightly
        img_edited = img_edited.filter(ImageFilter.ENHANCE_CONTRAST)
        
        # Save the edited image
        img_edited.save(output_image_path, quality=95)
        print(f"✓ Image edited successfully!")
        print(f"✓ Saved to: {output_image_path}")
        print(f"✓ Image dimensions: {width}x{height}")
        
    except FileNotFoundError:
        print(f"✗ Error: Input image not found at {input_image_path}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def create_circular_profile(input_image_path, output_image_path, bot_name="KING LEO 10"):
    """
    Create a circular version of the image for WhatsApp profile (alternative option)
    
    Args:
        input_image_path: Path to the original image
        output_image_path: Path to save the circular image
        bot_name: Bot name to add to image
    """
    
    try:
        # Open the image
        img = Image.open(input_image_path)
        
        # Create a square version (WhatsApp profile is circular)
        size = min(img.size)
        left = (img.width - size) // 2
        top = (img.height - size) // 2
        right = left + size
        bottom = top + size
        
        img_cropped = img.crop((left, top, right, bottom))
        
        # Create circular mask
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, size, size], fill=255)
        
        # Apply mask
        output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        img_cropped = img_cropped.convert('RGBA')
        output.paste(img_cropped, (0, 0), mask)
        
        # Add bot name text
        draw = ImageDraw.Draw(output)
        
        try:
            font_size = int(size * 0.12)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        text = bot_name
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x_position = (size - text_width) // 2
        y_position = size - text_height - int(size * 0.05)
        
        # Draw text with outline
        outline_width = 2
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                draw.text(
                    (x_position + adj_x, y_position + adj_y),
                    text,
                    font=font,
                    fill=(0, 0, 0, 255)
                )
        
        draw.text(
            (x_position, y_position),
            text,
            font=font,
            fill=(0, 150, 255, 255)
        )
        
        output.save(output_image_path, quality=95)
        print(f"✓ Circular profile image created successfully!")
        print(f"✓ Saved to: {output_image_path}")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")


if __name__ == "__main__":
    # Configuration
    input_file = "messi_image.png"  # Replace with your image file name
    output_file = "king_leo_10_edited.png"
    circular_output_file = "king_leo_10_circular.png"
    bot_name = "KING LEO 10"
    
    print("=" * 50)
    print("WhatsApp Bot Image Editor")
    print("=" * 50)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"✗ Error: '{input_file}' not found!")
        print(f"Please place your image in the same directory as this script.")
        print(f"Supported formats: PNG, JPG, JPEG, GIF, BMP")
    else:
        # Edit the image (rectangular version)
        print(f"\n1. Creating edited image with '{bot_name}' text...")
        edit_image_for_whatsapp(input_file, output_file, bot_name)
        
        # Create circular version
        print(f"\n2. Creating circular profile version...")
        create_circular_profile(input_file, circular_output_file, bot_name)
        
        print("\n" + "=" * 50)
        print("Done! Check your files:")
        print(f"  - {output_file} (for posts/messages)")
        print(f"  - {circular_output_file} (for profile picture)")
        print("=" * 50)
