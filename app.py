#interface by streamlit


import streamlit as st
from story_generator import generate_story_from_images , narrate_story
from  PIL import Image
st.title("Trinity's AI Story Generator from Images")
st.markdown("Upload 1 to 10 images, choose the genre and let the AI write and narrate an story for you.")


with st.sidebar:
    st.header("Controls")


    #sidebar option to upload image
    uploaded_files = st.file_uploader(
        "Upload your images....",
        type=["png","jpg","jpeg"],
        accept_multiple_files=True
    )


    #select the genre
    story_style = st.selectbox(
        "Choose the story genre",
        ("Comedy","Thriller","Fairy Tale","Sci-F","Mystery","Adventure","Morale")
    )



    #Generate the story button
    generate_button = st.button(
        "Generate Story and Narration",
        type="primary"
    )


#main logic

if generate_button:
    if not uploaded_files:
        st.warning("Please upload atleast one image!")
    elif len(uploaded_files) > 10:
        st.warning("Please upload the images at the maximum of 10.")
    else:
        with st.spinner("The AI model is writing and narrating your story.... This may take few seconds."):
#            st.write("hello")  #checking

            try:
                pil_images = [Image.open(uploaded_file) for uploaded_file in uploaded_files]
                st.subheader ("Your visual Inspiration:")
                image_columns = st.columns(len(pil_images))

                for i , image in enumerate(pil_images):
                    with image_columns[i]:
                        st.image(image, use_container_width=True) #For expansion

                generate_story = generate_story_from_images(pil_images , story_style)
                if "Error" in generate_story or "failed" in generate_story or "API Key" in generate_story:
                    st.error(generate_story)

                else:
                    st.subheader(f"Your {story_style} story: ")
                    st.success(generate_story)



                st.subheader("Listen the narration of the story...")
                audio_file = narrate_story(generate_story)
                if audio_file:
                    st.audio(audio_file , format="audio/mp3")


            except Exception as e:
                st.error(f"An application error occured {e}")