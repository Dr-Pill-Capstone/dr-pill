import cv2
import pytesseract
import re
import time

class OpenCV:
    def __init__(self):
        return

    FILENAME = "dispening_schedule.csv"

    def scan_label(self):

        # C:\Program Files\Tesseract-OCR\tesseract.exe

        # For windows
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # For linux
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


        # Define the name of the output file
        output_file = 'scanned_text.txt'

        f = open(output_file, "w")

        # Set up the webcam
        cap = cv2.VideoCapture(0)

        # Define the countdown time in seconds
        COUNTDOWN_TIME = 3

        # Set up the window for displaying the video feed
        cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)

        text = ''

        # Take 5 pictures and OCR each one of them
        for i in range(5):
            # Get the current time
            start_time = time.time()

            while True:
                # Read a frame from the webcam
                ret, frame = cap.read()

                # Display the frame in the window
                cv2.imshow('Camera Feed', frame)

                # Calculate the remaining time
                elapsed_time = time.time() - start_time
                remaining_time = COUNTDOWN_TIME - elapsed_time

                # Check if the countdown has finished
                if remaining_time <= 0:
                    # Capture an image from the webcam
                    image = frame

                    # # Convert the image to grayscale
                    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    # # Apply adaptive thresholding to the image to create a binary image
                    # binary_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

                    # # Apply dilation to the binary image to make the text more visible
                    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                    # dilated_image = cv2.dilate(binary_image, kernel, iterations=3)

                    # Convert the image to grayscale
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    # Apply Gaussian Blur filter to smooth out noise
                    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

                    # Apply Otsu's thresholding to the blurred image
                    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                    # Perform morphological closing to fill small gaps in the text
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

                    # Use Pytesseract to extract the text from the image
                    ocr_text = pytesseract.image_to_string(closed)

                    # Append the OCR result to the text variable
                    text += ocr_text + '\n'

                    # Wait for 1 second before capturing the next image
                    cv2.waitKey(1000)

                    # Break out of the loop
                    break

                # Display the remaining time on the window
                text = 'Capturing in {:.0f} seconds'.format(remaining_time)
                cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Camera Feed', frame)

                # Check for user input to cancel the countdown
                key = cv2.waitKey(1)
                if key == ord('q'):
                    # Release the webcam and close the windows
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

        
        # Print the extracted text
        print(text)
        f.write(text)

        # Release the webcam and close the window
        cap.release()
        f.close()
        cv2.destroyAllWindows()
        print("Scanning Complete")
        return output_file

    def scan_label_video(self):
        print("Scanning Label")

        # C:\Program Files\Tesseract-OCR\tesseract.exe
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

        # Set up the webcam
        cap = cv2.VideoCapture(0)

        # Define the name of the output file
        output_file = 'scanned_text.txt'

        f = open(output_file, "w")

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Enhance the image using a bilateral filter
            enhanced = cv2.bilateralFilter(gray, 11, 17, 17)

            # Use Pytesseract to extract text from the image
            text = pytesseract.image_to_string(enhanced)

            # Print the resulting text to the console
            print(text)
            f.write(text)

            # Display the resulting image
            cv2.imshow('Enhanced Image', enhanced)

            # Exit the program when the 'q' key is pressed
            if cv2.waitKey(1) == ord('q'):
                break

        f.close()
        # Release the capture
        cap.release()
        cv2.destroyAllWindows()
        print("Scanning Complete")
        return output_file

    def word_to_number(self,word):
        if word.lower() == "once" or word.lower() == "one":
            return 1
        elif word.lower() == "twice" or word.lower() == "two":
            return 2
        elif word.lower() == "thrice" or word.lower() == "three":
            return 3
        elif word.lower() == "four":
            return 4
        elif word.lower() == "five":
            return 5
        elif word.lower() == "six":
            return 6
        elif word.lower() == "seven":
            return 7
        elif word.lower() == "eight":
            return 8
        elif word.lower() == "nine":
            return 9
        else:
            raise ValueError(f"Invalid interval word: {word}")

    def most_frequent(self,List):
        counter = 0
        num = List[0]
        
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num = i
    
        return num

    def parse_label(self,file_path):
        print("Parsing Label Info")

        with open(file_path, 'r') as file:
            text = file.read()

        print(text)
        # Define the regular expression patterns
        quantity_pattern = r'(\d+[- ]?\d*)\s*(tablet|tablets|tab|tabs|capsule|cap|caps|pellets|pill|pills?)'
        interval_pattern = r'(every|per)?\s*(\d+[- ]?\d*)\s*(hours|hour|hrs|minute|mins|min|days|day|times daily|doses daily)'
        # Extract medicine dosage information using regular expressions
        quantity_matches = re.findall(quantity_pattern, text, re.IGNORECASE)
        interval_matches = re.findall(interval_pattern, text, re.IGNORECASE)

        # Print the extracted information to the console
        if quantity_matches and interval_matches:
            print('Dosage information:')
            for i in range(min(len(quantity_matches), len(interval_matches))):
                quantity = quantity_matches[i][0]
                quantity_keyword = quantity_matches[i][1]
                interval = interval_matches[i][1]
                interval_keyword = interval_matches[i][2]
                print('Quantity:', quantity, quantity_keyword)
                print('Interval:', interval, interval_keyword)

            # find the quantity that was scanned the most
            qty = self.most_frequent(quantity_matches)
            itrvl = self.most_frequent(interval_matches)

            qty_list = list(qty)
            itrvl_list = list(itrvl)

            qty_list[0] = qty_list[0].strip()
            itrvl_list[1] = itrvl_list[1].strip()

            if not qty_list[0].isnumeric():
                qty_list[0] = self.word_to_number(qty_list[0])

            if not itrvl_list[1].isnumeric():
                itrvl_list[1] = self.word_to_number(itrvl_list[1])
            
            day_keys = ["days","day","dy","daily"]
            hour_keys = ["hours","hour","hr","hrs"]
            minute_keys = ["minutes", "minute","min","mins"]
            second_keys = ["seconds","second","sec","secs"]

            interval_keyword = interval_keyword.lower()

            if interval_keyword in day_keys:
                interval_keyword = "day"
            elif interval_keyword in hour_keys:
                interval_keyword = "hour"
            elif interval_keyword in minute_keys:
                interval_keyword = "minute"
            elif interval_keyword in second_keys:
                interval_keyword = "second"
            else:
                raise Exception("Keyword match not found")

            data = [qty_list[0],itrvl_list[1],interval_keyword]
            file.close()
            return data
        
        else:
            file.close()
            print("No information found")
            pass

    def execute_scan(self):
        print("Running scan")

        # scan pill bottle label
        scan_file = self.scan_label()

        # extract info from scanned text
        dosage_info = self.parse_label(scan_file)

        return dosage_info
