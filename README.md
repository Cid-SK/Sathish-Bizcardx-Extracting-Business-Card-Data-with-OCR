# Project Title: BizCardX: Extracting Business Card Data with OCR

## Technologies Used
- OCR
- Streamlit GUI
- SQL
- Data Extraction

## Problem Statement
Develop a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR. The extracted information should include the company name, cardholder name, designation, mobile number, email address, website URL, area, city, state, and pin code. Users should be able to save the extracted information into a database along with the uploaded business card image, allowing for multiple entries.

## Approach
1. **Install Required Packages:** Install Python, Streamlit, easyOCR, and a database management system like SQLite or MySQL.
2. **Design User Interface:** Create a simple and intuitive user interface using Streamlit with widgets like file uploader, buttons, and text boxes.
3. **Implement Image Processing and OCR:** Use easyOCR to extract information from the uploaded image, applying image processing techniques for quality enhancement.
4. **Display Extracted Information:** Present the extracted information in a clean and organized manner in the Streamlit GUI using widgets like tables and text boxes.
5. **Implement Database Integration:** Use SQLite or MySQL to store the extracted information along with the uploaded business card image. Implement functionality to read, update, and delete data through the Streamlit UI.
6. **Test the Application:** Thoroughly test the application to ensure functionality and usability.
7. **Improve the Application:** Continuously enhance the application by adding features, optimizing code, and improving security with user authentication and authorization.

## Results
The project will result in a Streamlit application that simplifies the extraction and management of business card information. Users can upload business card images, extract information, and save it to a database with ease. The application will have a user-friendly interface and will be scalable, maintainable, and extensible.

This project requires skills in image processing, OCR, GUI development, and database management. Good documentation and code organization are crucial for its success. The application will be useful for businesses and individuals needing to manage business card information efficiently.
