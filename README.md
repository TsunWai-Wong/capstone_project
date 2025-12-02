# Capstone project

## Track: Agents for Good (Education)

## Problem Statement
The internet has made knowledge vastly more accessible compared to traditional, institution-based learning. However, self-learners often face the opposite problem: the abundance of resources is unstructured, inconsistent, and fragmented, making it easy to wander between surface-level topics without building a coherent understanding.

## Solution Statement
This product aims to provide an intuitive and structured way for users to build deep, organized knowledge in any domain. It combines AI-generated knowledge graph to create a personalized and systematic learning experience.

Users can build a knowledge graph as a guide: Users can input the domain of knowledge that they want to master. The product can generate a network-form (or Tree in the future version) knowledge graph to showcase the keep concepts in the domain and the relation among them. This means a structure of notes that can be opened in Obisidian will be generated. Then users can establish understandings in the concepts by learning them one by one.

## Architecture

├── Root agent (Knowlege graph agent)\
│&emsp├── Roadmap Resarch agent (as tool)\
│&emsp│&emsp├── Search tool (Google search)\
│&emsp├── Write tool (Write to curricula, topics and topic links tables in database)\

## Conclusion
The software can let users to learn in followings ways:
Personalised: Users can learn at their own pace. And the difficulties of the content will be adjusted according to user’ level.
Holistic: Users can get a systematic view on the knowledge domain that they want to explore
Up-to-date: Users can learn the current knowledge, instead of pre-set knowledge that written in the textbooks
