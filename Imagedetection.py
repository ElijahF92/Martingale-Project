import cv2
import pytesseract

pytesseract.tesseract_cmd = "/Users/user/Desktop/Creation/Coding/Python/Martingale Project/tesseract"

import tkinter as tk
import pyautogui

class ScreenRegionSelector(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Select Screen Region")
        self.attributes("-alpha", 0.3)  # Make the window transparent
        self.overrideredirect(True)  # Remove window decorations
        self.attributes("-topmost", True)  # Keep the window on top
        self.attributes("-topmost", True)

        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas = tk.Canvas(self, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.selected_area = None

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        self.selected_area = (self.start_x, self.start_y, end_x, end_y)
        self.destroy()

def get_screen_region():
    selector = ScreenRegionSelector()
    selector.mainloop()
    return selector.selected_area

def preprocess_image(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Check if the image is loaded
    if img is None:
        print(f"Failed to load image from {image_path}")
        return None

    # Resize the image to double its original size for better OCR accuracy
    img = cv2.resize(img, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to get a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply a GaussianBlur to denoise the image
    #denoised = cv2.GaussianBlur(binary, (5, 5), 0)

    return binary

def extract_text_from_image(image_path):
    preprocessed_img = preprocess_image(image_path)
    if preprocessed_img is not None:
        # Display the preprocessed image
        cv2.imshow("Preprocessed Image", preprocessed_img)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()

        # Use pytesseract to extract text from the preprocessed image
        words_in_image = pytesseract.image_to_string(preprocessed_img)
        print("Words in image: " + words_in_image)
    else:
        print("Preprocessing failed. No text extracted.")

def main():
    region = get_screen_region()
    if region:
        print(f"Selected Region: {region}")
        x1, y1, x2, y2 = region
        screenshot = pyautogui.screenshot(region=(x1+1, y1+1, x2 - x1-1, y2 - y1-1))
        screenshot.save("selected_region_screenshot.png")
        image_path = "/Users/user/Desktop/Creation/Coding/Python/Martingale Project/selected_region_screenshot.png"
        extract_text_from_image(image_path)
        #words_in_image = pytesseract.image_to_string(img)
        #print("words in image:" + words_in_image)
        

if __name__ == "__main__":
    main()