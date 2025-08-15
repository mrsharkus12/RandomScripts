from PIL import Image
import argparse

def count_colored_opaque_pixels(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGBA')
            
            pixels = img.getdata()
            
            color_counts = {}
            total_opaque_pixels = 0
            
            for pixel in pixels:
                r, g, b, a = pixel
                
                if a > 0:
                    total_opaque_pixels += 1
                    
                    if pixel in color_counts:
                        color_counts[pixel] += 1
                    else:
                        color_counts[pixel] = 1
            
            return {
                'total_opaque_pixels': total_opaque_pixels,
                'unique_colors': len(color_counts),
                'color_counts': color_counts
            }
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Count colored opaque pixels in a PNG image.')
    parser.add_argument('image_path', help='Path to the PNG image file')
    parser.add_argument('--verbose', action='store_true', help='Show detailed color information')
    
    args = parser.parse_args()
    
    result = count_colored_opaque_pixels(args.image_path)
    
    if result:
        print(f"total opaque pixels: {result['total_opaque_pixels']}")
        print(f"unique colors: {result['unique_colors']}")
        
        if args.verbose and result['color_counts']:
            print("\nColor breakdown:")
            for color, count in sorted(result['color_counts'].items(), key=lambda x: x[1], reverse=True):
                print(f"RGB: {color[:3]}, Alpha: {color[3]}, Count: {count}")

if __name__ == "__main__":
    main()