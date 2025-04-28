# DELTA : **D**eepSeek for **E**vent-based **L**ocation **T**racking and **A**nalysis
==============================================================

**DELTA** is an advanced framework designed for real-time geolocation extraction and event-based analysis from social media data, specifically focusing on natural disasters such as earthquakes, wildfires, and hurricanes. Leveraging the DeepSeek R1 model with 1.5B parameters, DELTA utilizes cutting-edge techniques to provide information extracted from Twitter and YouTube in the form of text, video, and audio.

🔍 Project Overview
-------------------

DELTA aims to provide a robust solution for:
    
*   **Location Extraction**: Extracting geolocation information from unstructured text.
    
*   **Multi-aspect Support**: Analysing data from multiple countries, events, and social-media platforms (Twitter and YouTube).

*   **Summarisation Webapp**: Fetching relevant YouTube videos from user query, providing a summary of the video and audio file of the summary. 
    
*   **Data Privacy**: Running the model locally without relying on external APIs.
    

📁 Folder Structure
-------------------

The repository is organized into the following directories:

*   app/: Contains the web application code for user interaction.
    
*   coredata/: Stores initial data files imported from previous work and data imported from HumAID dataset.
    
*   img/: Holds images and visual assets.
    
*   llm/: Includes the preprocessed tweets, DeepSeek model testing for NER and related fine-tuning scripts.
    
*   README.md: This file.
