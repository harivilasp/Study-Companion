import img_ocr_copy as ocr
import para_summarizer as gsum
import search_results as sr

text_detected=ocr.printtest()
print("Detected Text")
print(text_detected)

if(len(text_detected)>200):
    sumtext=gsum.generate_summary(text_detected)
    sumtext=sumtext[0]
else:
    sumtext=text_detected
print("Summarized Text")
print(sumtext)

print("Web Results")
for i in sr.gsearch(sumtext):
    print(i)
print("\nVedio Results")
for i in sr.gsearch("youtube : "+sumtext):
    print(i)
