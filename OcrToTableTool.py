import cv2
import numpy as np
import subprocess
import easyocr

class OcrToTableTool:

    def __init__(self, thresholded_image, original_image):
        self.thresholded_image = thresholded_image
        self.original_image = original_image

    def execute(self):
        self.dilate_image()
        self.store_process_image('0_dilated_image.jpg', self.dilated_image)
        self.find_contours()
        self.store_process_image('1_contours.jpg', self.image_with_contours_drawn)
        self.convert_contours_to_bounding_boxes()
        self.store_process_image('2_bounding_boxes.jpg', self.image_with_all_bounding_boxes)
        self.mean_height = self.get_mean_height_of_bounding_boxes()# correct
        self.sort_bounding_boxes_by_y_coordinate()# correct
        self.club_all_bounding_boxes_by_similar_y_coordinates_into_rows()
        self.sort_all_rows_by_x_coordinate()
        self.crop_each_bounding_box_and_ocr()
        self.generate_output_file()

    def threshold_image(self):
        return cv2.threshold(self.grey_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    def convert_image_to_grayscale(self):
        return cv2.cvtColor(self.image, self.dilated_image)

    def dilate_image(self):
        kernel_to_remove_gaps_between_words = np.array([
                [1,1,1,1,1,1,1,1,1,1],
               [1,1,1,1,1,1,1,1,1,1]
        ]) 
        self.dilated_image = cv2.dilate(self.thresholded_image, kernel_to_remove_gaps_between_words, iterations=3) #from 3 to 1
        simple_kernel = np.ones((5,5), np.uint8)
        self.dilated_image = cv2.dilate(self.dilated_image, simple_kernel, iterations=1)
    
    def find_contours(self):
        result = cv2.findContours(self.dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = result[0]
        self.image_with_contours_drawn = self.original_image.copy()
        cv2.drawContours(self.image_with_contours_drawn, self.contours, -1, (0, 255, 0), 5)
    
    def approximate_contours(self):
        self.approximated_contours = []
        for contour in self.contours:
            approx = cv2.approxPolyDP(contour, 3, True)
            self.approximated_contours.append(approx)

    def draw_contours(self):
        self.image_with_contours = self.original_image.copy()
        cv2.drawContours(self.image_with_contours, self.approximated_contours, -1, (0, 255, 0), 5)

    def convert_contours_to_bounding_boxes(self):
        self.bounding_boxes = []
        self.image_with_all_bounding_boxes = self.original_image.copy()
        for contour in self.contours:
            x, y, w, h = cv2.boundingRect(contour)
            self.bounding_boxes.append((x, y, w, h))
            self.image_with_all_bounding_boxes = cv2.rectangle(self.image_with_all_bounding_boxes, (x, y), (x + w, y + h), (0, 255, 0), 5)#(x + w, y + h) => (x + w, y + h+2)

    def get_mean_height_of_bounding_boxes(self):
        heights = []
        for bounding_box in self.bounding_boxes:
            x, y, w, h = bounding_box
            heights.append(h) #change from 'h' to 'h+2' to 'h+4' to 'h+10'
        return np.mean(heights)

    def sort_bounding_boxes_by_y_coordinate(self):
        self.bounding_boxes = sorted(self.bounding_boxes, key=lambda x: x[1])

    def club_all_bounding_boxes_by_similar_y_coordinates_into_rows(self):
        self.rows = []
        half_of_mean_height = self.mean_height / 2
        current_row = [ self.bounding_boxes[0] ]
        for bounding_box in self.bounding_boxes[1:]:
            current_bounding_box_y = bounding_box[1]
            previous_bounding_box_y = current_row[-1][1]
            distance_between_bounding_boxes = abs(current_bounding_box_y - previous_bounding_box_y)
            if distance_between_bounding_boxes <= half_of_mean_height:
                current_row.append(bounding_box)
            else:
                self.rows.append(current_row)
                current_row = [ bounding_box ]
        self.rows.append(current_row)

    def sort_all_rows_by_x_coordinate(self):
        for row in self.rows:
            row.sort(key=lambda x: x[0])

    def crop_each_bounding_box_and_ocr(self):
        self.results = []
        image_number = 0
        # number_of_rows=len(self.rows)
        # number_of_contours=len(self.contours)
        # if number_of_contours%number_of_rows!=0:
        #     raise('This is not the format of table')
        # number_of_title=number_of_contours//number_of_rows
        for row in self.rows:
            is_title=True if self.rows.index(row)==0 else False
            for bounding_box in row:
                x, y, w, h = bounding_box
                y = y - 5 # -5 => -3 
                # print("x:")
                # print(x)
                # print("y:")
                # print(y)
                # print("w:")
                # print(w)
                # print("h:")
                # print(h)
                cropped_image = self.original_image[y:y+h, x+10:x+w-10] #change x:x+w to x+15:x+w-15
                image_slice_path = "./ocr_slices/img_" + str(image_number) + ".jpg"
                cv2.imwrite(image_slice_path, cropped_image)
                results_from_ocr = self.OCR(image_slice_path,is_title)
                image_number += 1
                self.results.append(results_from_ocr)


    def OCR(self, image_path,is_title:bool):
        reader = easyocr.Reader(['en']) if is_title else easyocr.Reader(['vi'])
        print(image_path)
        output = reader.readtext(image_path,detail=0) #Doi ti le mag_ratio =2 neu can thiet
  
        if len(output)==0:
            blured_image=cv2.blur(cv2.imread(image_path),(5,5))
            print("Cannot use readtext")
            output = reader.recognize(blured_image,detail=0,contrast_ths =0.3)
        print(output[0] if len(output)>0 else "")
        result=output[0] if len(output)>0 else ""
        result=result.title().replace(" ","") if is_title else result
        return result

    def generate_output_file(self):
        # This is format just for specific image that i use so maybe it will cause exeption when use with other
        with open("output.txt", "w", encoding="utf-8") as f:
            number_of_rows=len(self.rows)
            number_of_cells=len(self.results)
            if number_of_cells%number_of_rows!=0:
                raise('This is not the format of table')
            number_of_columns=number_of_cells//number_of_rows
            output=[]
            for r in range(number_of_rows):
                if r==0:
                    continue
                record={}
                for c in range(number_of_columns):
                    key=str(self.results[c])
                    value=str(self.results[number_of_columns*(r)+c])
                    record[key]=value
                output.append(record)
            f.write(str(output))

    def store_process_image(self, image_file_name, image):
        path = "./process_images/ocr_table_tool/" + image_file_name
        cv2.imwrite(path, image)