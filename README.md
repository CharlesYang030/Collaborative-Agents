# Collaborative-Agents
![image](./fig1.jpg)

### Title:
LLM-based Collaborative Agents with Pedagogy-guided Interaction Modeling for Timely Instructive Feedback Generation in Task-oriented Group Discussions

### Abstract:
Large language models (LLMs) fundamentally reshape learning and teaching models, shifting LLM-based tutoring systems from supporting individual learning to facilitating collaborative learning (CL) like task-oriented group discussions. However, existing AI tutors struggle to guide CL, as they seldom model the interactions between AI tutors and students. Neglecting such modeling affects the pedagogy adaptability of AI tutors to scaffold students to complete tasks collaboratively and impairs learning outcomes. Additionally, existing AI tutors fail to make use of CL theories to generate instructive feedback, which leads to undesirable interactions such as over-instruction and limits students' autonomy. In this paper, we propose an LLM-based collaborative agent that innovatively leverages pedagogical strategies to sense discussion stages, detect learning issues, identify the timing of intervention, and generate instructive feedback. To develop the agent, we first design a prompting strategy based on a CL theory, that is, the Community of Inquiry, to cultivate the agent to understand the discussion status.
Second, a multi-agent interaction framework is proposed to simulate the collaborative learning behavior between AI tutors and students.
Meanwhile, a synthetic task-oriented group discussion dataset, namely CLTeach, is generated, which consists of 27k manually-verified multi-party dialogues with fine-grained annotations of instructive feedback and explanations.
Lastly, we use CLTeach to fine-tune the LLM agent, ultimately enabling it to generate instructive feedback at the right time to support students in CL. Extensive experiments demonstrate that our agent achieves state-of-the-art performance in feedback generation and has the potential to mimic human teachers effectively.

### 
