# A Practical Approach to Deploying LLM Chatbots for Human-AI Interaction Research

This tutorial addresses the growing need for accessible methods to conduct studies involving user interactions with AI chatbots. While existing research has often focused on evaluating large language models (LLMs) based on static text input, interactive applications such as conversational agents and collaborative problem-solving remain relatively underexplored due to technical barriers associated with chatbot development and deployment. In response to this challenge, the present paper presents a simple wrapper method for launching AI chatbots into interactive web applications using Flask and Google App Engine. Our approach provides a basic chat interface and data collection capabilities, allowing researchers from various disciplines to deploy customizable chatbots and run large-scale online experiments without requiring extensive technical expertise.

Disclaimer: This software is work in progress and is provided "as-is" without warranties or guarantees. The authors are not liable for its use or misuse. Users must ensure compliance with all applicable laws and regulations. The software may contain bugs or limitations, and users should test and validate it for their specific needs before relying on it for critical applications. If you encounter any issues or have feedback, please feel free to reach out.


## Technical Background
The current tutorial enables users to deploy API-powered LLM chatbots into Google App Engine using Flask. Flask is a lightweight and flexible web framework for Python, allowing developers to create web applications without requiring extensive configuration. Google App Engine is a fully managed platform-as-a-service (PaaS) that allows developers to build and run applications on Google Cloud Platform (GCP) infrastructure while managing the hardware, networking, and scaling automatically. This offers significant advantages in the context of the current LLM-chatbot application, as it reduces the need for technical expertise and cloud infrastructure management.

The source code of the LLM-chatbot app contains several key components that can be adjusted to enable different types of chatbot applications and act as a wrapper for an LLM API (e.g., OpenAI’s ChatGPT API). Below is the directory structure of a basic wrapper app, along with a description of the main components. 

```
llm_webapp/\
├── app.yaml\
├── bot.py\
├── main.py\
├── requirements.txt\
├── static/\
│     ├── script.js\
│     └── style.css\
└── templates/\
      └── index.html\
```

The app.yaml file specifies the runtime Python version, handlers, service name, and environment variables. By specifying service names, multiple apps can be run in the same GCP project in parallel as distinct services (please note that the first service needs to be set to “default”). Environment variables are used to specify LLM API keys (by default OPENAI_API_KEY), a GCP project ID (GCP_PROJECT_ID), and a Firestore database name (FIRESTORE_DB). These variables need to be specified with valid IDs for the app to work. 

This bot.py file contains the ChatBot class along with the methods needed to facilitate user interactions. While the current example is based on the ChatGPT API, users can swap in other LLMs as long as the behavior of the ChatBot class remains unchanged. The ChatBot class allows to set system prompts, process user input, set the message history, make calls to the underlying LLM’s API, and return the bot’s response. 

The main.py This file creates the Flask app instance and runs the application. It contains the logic for message processing (i.e., user input is fed to the bot, the bot processes the message history, the response is returned to the user) and data collection (message histories are saved to a Firestore database). It also contains condition statements to stop the application after a certain number of turns or when a specific keyword appears in the input. Additional modifications can be made to guide the behavior of the chatbot. 

The prompts.py file contains prompts that are passed to the ChatBot class in order to guide the behavior of the chatbot. The prompts can easily be swapped out for different research applications. 

The requirements.txt file specifies dependencies and library versions. It can be changed according to an application's requirements.

The script.js file contains JavaScript code, which controls the web app's interactive elements. It handles events (like button clicks) and communicates with the server asynchronously using AJAX. 

The style.css file contains the CSS code to define the visual appearance of the web app, including layout, colors, fonts, spacing, and overall design. It can be adjusted to change the design of the chat interface.

The index.html file provides the basic structure for the chatbot interface. It features a user ID input section to unlock chat functionality, a chat history display with an initial bot message, and a form for sending messages. Aside from the initial message, the file should not be altered unless fundamental changes in the user interface are desired.

Researchers are encouraged to change the prompts in the prompts.py file and the control logic in the main.py file to adapt the current code base for different applications. For example, researchers could prompt the bot to adopt a certain persona by changing a system prompt, or they could integrate a condition statement where the bot reacts in a predetermined way to a specific user input. Similarly, the stopping criterion or the closing message can easily be changed. However, the code template also lends itself to more fundamental changes as long as the overarching logic is preserved.

## Step-By-Step Guide: How to Launch a Chatbot on Google App Engine
To deploy a Flask app in Google App Engine, researchers need to follow a series of steps that involve setting up cloud resources in GCP, changing the web app's source code, and deploying the app into the cloud using the Google Cloud Command Line Interface (gcloud CLI). Below, we provide an overview of the most important steps needed to set up the chatbot app in Google App Engine. Please refer to the official Google App Engine documentation, after which the section below is modeled, for more extensive tutorials and additional information.

Set up Google App Engine
- Begin by creating a GCP account
- Create a new project in the GCP console
- Enable billing for your Google Cloud project
- Create a new Firestore Database in “Native Mode”
- Create a composite index in Firestore with the following specifications:
    * Collection ID: messages
    * Field path 1: session_id (ASC)
    * Field path 2: timestamp (DESC)
    * Field path 3: __name__ (DESC)
- Query scope: Collection
- Install the Google Cloud Command Line Interface (gcloud CLI)
- Initialize the gcloud CLI by running “gcloud init” in the command line
- Run “gcloud app create” command to enable App Engine in your project

Prepare App Source Code
- Download the source files or clone the GitHub repository https://github.com/hp2500/llm_web_app/ 
- Adjust prompts (prompts.py) and control statements (main.py) to determine the behavior of the chatbot
- Fill in API credentials, GCP project name, and Firestore database name as environment variables in the app.yaml file

Launch Web App
- Navigate to the directory containing the prepared app source files
- Run “gcloud app deploy” to deploy an app with the current specifications
- If deployed successfully check the URL to ensure the app works as expected

## Example Application: Chatbots for Personality Inference 
The example source files are loosely based on software developed by the author for a study on the capacity of chatbots to collect information about users' personality traits (Peters et al., 2024). The chatbots were programmed using specific system prompts and logic statements that guided their responses and behaviors. Throughout the interaction, user inputs and chatbot responses were recorded and later analyzed to evaluate the accuracy of personality inferences across different chatbots. 

Users were directed to the web app from a Qualtrics survey, where they had responded to extensive questionnaire measures. Depending on a randomly assigned experimental condition they were directed to one of three different URLs associated with three different chatbots. Users had to submit a previously established user ID to activate the chatbot. This requirement ensured that users could be tracked across data collection platforms. The interaction ended after a predefined number of turns, and the chatbot returned a confirmation code allowing users to redeem a monetary reward. Using this procedure the authors collected data from almost 1000 participants within less than two days. 

This example demonstrates that the proposed method can easily be integrated with standard data collection methods in the behavioral and social sciences. Similar studies can be set up using the provided example code with limited effort.

