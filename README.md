# EquiGo
EquiGo is an interactive, smart and considerate route planner.

# Introduction
Estimating based on the global average, India likely has around 22.4 million disabled individuals. According to a United Nations report, more than 46 per cent of older persons–those aged 60 years and over—have disabilities and more than 250 million older people experience moderate to severe disability. 

# Problem Statement
- Barriers hinder effective navigation, especially for individuals with varying abilities and linguistic backgrounds.
- Our app addresses the lack of awareness regarding the environmental impact of transportation choices.
- EquiGo aims to establish an inclusive and accessible urban navigation experience in smart cities.
- The overarching problem is the need for a transformative solution, turning urban navigation into an inclusive, accessible, and sustainable experience.
- EquiGo strives to be the answer to this multifaceted urban navigation challenge.

# Ideation Process
EquiGo is an interactive, smart and considerate route planner.
It addresses language translation challenges and goes beyond by offering various modes to meet specific needs including:
- Wheelchair-friendly navigation
- Voice assistance for visual impairment
- Text and visual assistance for the hearing-impaired

The app's user interface (UI) is designed to be dyslexia-friendly, enhancing accessibility.
The collected data is utilized to set the context for sessions with the RAG (Retrieval-augmented generation) LLM.
EquiGo offers valuable insights regarding the navigation route:
- Air quality index information for individuals with breathing difficulties.
- Daily push notifications with general travel advisories, such as reminders to carry an umbrella.

EquiGo enhances cost saving by providing fuel pricing information for selected routes.

To enhance sustainability in smart cities, EquiGo incorporates
- EV-based extended routing, allowing drivers access to facilities for charging their electric vehicles along the way.
- A comparison of different public transportation modes using data sourced from APIs to recommend the most suitable solution based on the individuals abilities.
- Analytics on CO2 emissions for a selected route.


# Constraints and Considerations

The main concerns in this application are:
- Reliability of Data - There is a lack of available information regarding the facilities and safety ratings of regions in India.-
- Adaptation to regional variances - In a diverse domain space like our country catering to different geographical and cultural differences is challenging.
- Privacy and Security - Dealing with sensitive information like health details and travel information requires a safe environment and data policy.

To address this we propose to devise:
- Feedback by community engagement- The community feedback system ensures a continuous inflow of diverse and real-time data, enriching the app's information on wheelchair accessibility and safety.
- Enhanced RAG Model - User-generated data feeds into the RAG model, improving its accuracy over time.

# References

Idea:

https://indianexpress.com/article/et-al-express-insight/the-invisible-travellers-struggles-of-exploring-the-world-with-a-disability-8916145

https://www.outlookindia.com/international/worldwide-efforts-to-improve-quality-of-life-for-disabled-people-see-a-great-leap-forward-news-284536

https://planetabled.com

RAG:

https://gathnex.medium.com/build-your-own-production-ready-retrival-augmented-genration-system-at-zero-cost-b619c26c10c1

https://huggingface.co/docs/transformers/model_doc/rag

https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation

APIs:

https://github.com/AI4Bharat/IndicTrans2

https://www.w3.org/WAI/WCAG21/Understanding/intro#understanding-the-four-principles-of-accessibility

https://developer.tomtom.com/products/traffic-api

https://wiki.openstreetmap.org/wiki/List_of_OSM-based_services

https://data.gov.in/catalog/real-time-air-quality-index - Real time Air Quality Index

https://openweathermap.org/api/uvi

https://models.ai4bharat.org/#/nmt/v2

https://developer.tomtom.com/routing-api/api-explorer

