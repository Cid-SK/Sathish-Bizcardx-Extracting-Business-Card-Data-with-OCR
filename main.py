import streamlit as st
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import sqlite3


def img2_text(path):
  sample_img=Image.open(path)

  # converting image to array format
  img_arr =np.array(sample_img)

  reader = easyocr.Reader(['en'])
  text = reader.readtext(img_arr, detail=0)
  return text,sample_img

def text2_dic(data):

  details={"NAME":[],"DESIGNATION":[],"COMPANY_NAME":[],"CONTACT":[],"E-MAIL":[],"WEBSITE":[],"ADDRESS":[],"PINCODE":[]}

  details["NAME"].append(data[0]),details["DESIGNATION"].append(data[1])

  for i in range(2,len(data)):

    if "@" in data[i]:
      details["E-MAIL"].append(data[i])

    elif "www" in data[i].lower():
      details["WEBSITE"].append(data[i])

    elif re.match(r'\+\d{3}-\d{3}-\d{4}', data[i]) or re.match(r'\+\d{2}\s\d{10}', data[i]) or re.match(r'\d{10}', data[i]):
      details["CONTACT"].append(data[i])

    elif re.match(r'\d{2,4}\s[a-zA-Z]',data[i]):
      details["ADDRESS"].append(data[i])

    elif re.match(r'^[a-zA-Z]+$',data[i]):
      details["COMPANY_NAME"].append(data[i])

    pincode = re.search(r'\b\d{6}\b', data[i])
    if pincode:
      details["PINCODE"].append(pincode.group())

  for key,value in details.items():
    if len(value)>0:
      concadenate=" ".join(value)
      details[key]=[concadenate]
    else:
      value ="NA"
      details[key]=[value]

  return details

mydb = sqlite3.connect("bizcardx.db")
cursor = mydb.cursor()

#table creation
create_table =''' CREATE TABLE IF NOT EXISTS bizcardx_details(name varchar(225),designation varchar(225),company_name varchar(225),contact varchar(225),
                                              email varchar(225) primary key ,website text,address text,pincode varchar(225),image text)'''
cursor.execute(create_table)
mydb.commit()


#streamlit part

st.set_page_config(layout="wide")
st.title(":blue[BizCardX]: Extracting Business Card Data with OCR")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>",unsafe_allow_html=True)

tab1,tab2,tab3,tab4= st.tabs(["#### ***Home***","#### ***Upload & Extract***","#### ***Modify***","#### ***Delete***"])

with tab1:

  st.subheader(":blue[Overview:]")
  st.write('''##### BizCardX is a Streamlit application designed to simplify the process of extracting and managing \
  information from business cards. By leveraging OCR technology, users can upload an image of a business card and \
  have key details extracted automatically. This includes the company name, cardholder name, designation, \
  contact details, and geographic information.''')
  st.write("")
  st.write("")

  st.subheader(":blue[Technologies Used:]")
  st.write(" * ##### :red[OCR] (Optical Character Recognition): For extracting text from images.")
  st.write(" * ##### :red[Streamlit]: For building the graphical user interface.")
  st.write(" * ##### :red[SQL] (Structured Query Language): For database management.")
  st.write(" * ##### :red[Python]: For scripting and integrating the various components.")
  st.write("")
  st.write("")

  st.subheader(":blue[Conclusion:]")
  st.write("##### BizCardX offers a comprehensive solution for extracting and managing business card information. \
  By combining OCR technology with a user-friendly interface, the application simplifies the process of \
  digitizing and organizing business card data.")

with tab2:
  st.markdown("### :blue[Upload a Business Card to Extract the Details]")
  card_img = st.file_uploader("upload here",label_visibility="collapsed",type=["png","jpeg","jpg"])

  if card_img is not None:
    col1,col2,col3 = st.columns([5,2,8])
    text_img,input_img=img2_text(card_img)
    text_dict=text2_dic(text_img)
    st.image(card_img,width=380)

    if text_dict:
      st.success("Data Extracted Successfully")

    df=pd.DataFrame(text_dict)

    #img to bytes
    image_bytes = io.BytesIO()
    input_img.save(image_bytes,format="PNG")
    img_data = image_bytes.getvalue()

    # dic creation
    data ={"IMAGE":[img_data]}
    df1=pd.DataFrame(data)
    concat_df = pd.concat([df,df1],axis=1)
    st.subheader(":blue[Preview]")
    st.dataframe(concat_df)

    button1 = st.button(":blue[***Save to Database***]",use_container_width=True)

    if button1:
      try:
        #insert data
        insert_query='''INSERT INTO bizcardx_details(name,designation,company_name,contact,email,website,address,pincode,image)
                                                values(?,?,?,?,?,?,?,?,?)'''

        datas = concat_df.values.tolist()[0]
        cursor.execute(insert_query,datas)
        mydb.commit()

        st.success("Saved !!")
      except sqlite3.IntegrityError :
        # Handle duplicate entry error
        st.error(f"This data already Exists.")

with tab3:
  st.markdown("### :blue[Stored Data]")

  mydb = sqlite3.connect("bizcardx.db")
  cursor = mydb.cursor()

  select_query = "SELECT * FROM bizcardx_details"
  cursor.execute(select_query)
  table = cursor.fetchall()
  mydb.commit()

  table_df = pd.DataFrame(table,columns=("Name","Designation","Company_Name","Contact","Email","Website","Address","Pincode","Image"))
  st.dataframe(table_df)

  with st.container(border=True):
      st.subheader(":blue[Alter the Data]")
      selected_name = st.selectbox("Select The Card Holder", table_df["Name"])
      try:
          df_3 = table_df[table_df["Name"] == selected_name]
          if len(df_3) == 2 and df_3.iloc[0].equals(df_3.iloc[1]):
              df_3 = df_3.iloc[[0]]
          df_4 = df_3.copy()

          c1, c2 = st.columns(2)
          with c1:
              m_name = st.text_input("Name", df_3["Name"].unique()[0])
              m_designation = st.text_input("Designation", df_3["Designation"].unique()[0])
              m_company_name = st.text_input("Company_Name", df_3["Company_Name"].unique()[0])
              m_contact = st.text_input("Contact", df_3["Contact"].unique()[0])

              df_4["Name"] = m_name
              df_4["Designation"] = m_designation
              df_4["Company_Name"] = m_company_name
              df_4["Contact"] = m_contact

          with c2:
              m_email = st.text_input("Email", df_3["Email"].unique()[0])
              m_website = st.text_input("Website", df_3["Website"].unique()[0])
              m_address = st.text_input("Address", df_3["Address"].unique()[0])
              m_pincode = st.text_input("Pincode", df_3["Pincode"].unique()[0])

              df_4["Email"] = m_email
              df_4["Website"] = m_website
              df_4["Address"] = m_address
              df_4["Pincode"] = m_pincode

          st.write("")
          st.write("")
          #st.subheader(":blue[Altered Table]")
          st.dataframe(df_4)

      except:
        pass

      col1, col2 = st.columns([2, 8])
      with col1:
          button_m = st.button(":red[***Modify***]", use_container_width=True)

      if button_m:
          mydb = sqlite3.connect("bizcardx.db")
          cursor = mydb.cursor()

          cursor.execute(f"DELETE FROM bizcardx_details WHERE NAME = '{selected_name}'")
          mydb.commit()

          insert_query = '''INSERT INTO bizcardx_details(name, designation, company_name, contact, email, website, address, pincode, image)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''

          datas = df_4.values.tolist()[0]
          cursor.execute(insert_query, datas)
          mydb.commit()

          st.success("Modified !!")

  m_db = st.button(":blue[***View Modified Database***]")

  if m_db:
    st.dataframe(table_df)

with tab4:

  with st.container(border=True):
    st.subheader(":blue[Delete The Data]")
    mydb = sqlite3.connect("bizcardx.db")
    cursor = mydb.cursor()

    col1,col2,col3 = st.columns(3)
    with col1:
      select_query = "SELECT NAME FROM bizcardx_details"

      cursor.execute(select_query)
      table1 = cursor.fetchall()
      mydb.commit()

      names = []
      for i in table1:
        names.append(i[0])

      d_name = st.selectbox("Select the Name :",names)
      st.write("")
      st.write(f" Selected Name : :red[{d_name}]")

    with col2:
      select_query = f"SELECT DESIGNATION FROM bizcardx_details WHERE NAME ='{d_name}'"

      cursor.execute(select_query)
      table2 = cursor.fetchall()
      mydb.commit()

      designations = []
      for j in table2:
        designations.append(j[0])

      d_designation = st.selectbox("Select the designations :",designations)
      st.write("")
      st.write(f" Selected Designation : :red[{d_designation}]")

    with col3:
      select_query = f"SELECT COMPANY_NAME FROM bizcardx_details WHERE NAME ='{d_name}' AND DESIGNATION = '{d_designation}'"

      cursor.execute(select_query)
      table2 = cursor.fetchall()
      mydb.commit()

      company_name = []
      for k in table2:
        company_name.append(k[0])

      d_company_name = st.selectbox("Select the Company Name :",company_name)
      st.write("")
      st.write(f" Selected Company Name : :red[{d_company_name}]")

    if  d_name and d_designation and d_company_name:

        remove = st.button(":red[***Delete***]",use_container_width=True)

        if remove:

          cursor.execute(f"DELETE FROM bizcardx_details WHERE NAME = '{d_name}' AND DESIGNATION = '{d_designation}' AND \
                            COMPANY_NAME = '{d_company_name}'")
          mydb.commit()

          st.warning("TABLE DELETED !!")

  up_db = st.button(":blue[***View Updated Database***]")

  if up_db:
    st.dataframe(table_df)

