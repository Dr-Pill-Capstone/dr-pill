import cv2
import pytesseract
import re
import csv

class OpenCV:
    def __init__(self):
        return

    FILENAME = "dispening_schedule.csv"

    def scan_label(self):
        print("Scanning Label")

        # C:\Program Files\Tesseract-OCR\tesseract.exe
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

    def interval_to_number(self,interval_word):
        if interval_word.lower() == "once":
            return 1
        elif interval_word.lower() == "twice":
            return 2
        elif interval_word.lower() == "thrice":
            return 3
        else:
            raise ValueError("Invalid interval word: " + interval_word)

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
        quantity_pattern = r'(\d+[- ]?\d*)\s*(tablet|tablets|tab|tabs|pills?)'
        interval_pattern = r'(every|per)?\s*(\d+[- ]?\d*)\s*(hours|hour|hrs|minute|mins|min|days|day|daily|times|doses)'
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
            itrvl_list = list(itrvl)
            itrvl_list[1] = itrvl_list[1].strip()
            if not itrvl_list[1].isnumeric():
                itrvl_list[1] = self.interval_to_number(itrvl_list[1])
            
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

            data = [qty[0],itrvl_list[1],interval_keyword]
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
