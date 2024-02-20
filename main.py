from OcrToTableTool import OcrToTableTool
from TableExtractor import TableExtractor
from TableLinesRemover import TableLinesRemover
import cv2

path_to_image = "./images/OCR.jpg"
table_extractor = TableExtractor(path_to_image)
perspective_corrected_image = table_extractor.execute()
cv2.imshow("perspective_corrected_image", perspective_corrected_image)

lines_remover = TableLinesRemover(perspective_corrected_image)
image_without_lines = lines_remover.execute()
cv2.imshow("image_without_lines", image_without_lines)

ocr_tool = OcrToTableTool(image_without_lines, perspective_corrected_image)
ocr_tool.execute()

cv2.waitKey(0)
cv2.destroyAllWindows()