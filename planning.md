# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

My domain is unofficial student knowledge about Iowa State University dining and campus food. This knowledge is valuable because official ISU Dining pages explain menus, meal plans, hours, and dining programs, but they do not fully show what students actually think is worth eating, which places are convenient between classes, what students complain about, or how students choose between meal plans. Student opinions are scattered across Reddit threads and informal reviews, so a RAG system can make this information easier to search and summarize.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | ISU Dining homepage | Official overview of ISU Dining options and resources | `docs/01_isu_dining_overview.txt` |
| 2 | ISU Dining Meal Plans and Rates | Official meal plan details, dining dollars, meal swipes, and plan structure | `docs/02_isu_meal_plans.txt` |
| 3 | ISU Dining Hours & Menus | Official hours, menus, and campus dining location information | `docs/03_isu_hours_menus.txt` |
| 4 | ISU Dining GET & Go | Official information about using meal swipes for quick GET & Go meals | `docs/04_isu_get_and_go.txt` |
| 5 | r/iastate: Best food on campus? | Student recommendations about campus food and dining halls | `docs/05_reddit_best_food_on_campus.txt` |
| 6 | r/iastate: Best Dining Hall / ISU food? | Student discussion about dining halls and campus food quality | `docs/06_reddit_best_dining_hall.txt` |
| 7 | r/iastate: Fave dining locations on campus? | Student discussion about lunch spots and food between classes | `docs/07_reddit_fave_dining_locations.txt` |
| 8 | r/iastate: Meal Plans | Student advice about meal plans, swipes, Dining Dollars, and cost efficiency | `docs/08_reddit_meal_plans.txt` |
| 9 | r/iastate: 5 best restaurants near campus | Student recommendations for restaurants near campus | `docs/09_reddit_near_campus_restaurants.txt` |
| 10 | r/iastate: Dining Hall Food | Student opinions comparing dining halls such as UDCC and Windows | `docs/10_reddit_dining_hall_food.txt` |


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** Around 700 characters

**Overlap:** Around 100 characters

**Reasoning:**

My documents are a mix of short student comments and longer official dining information. I will use paragraph-based chunking instead of blindly splitting every fixed number of characters. The chunker will group nearby paragraphs until the chunk is around 700 characters, with about 100 characters of overlap.

This fits my documents because one student comment or a small group of related comments usually forms a complete thought. If chunks are too small, a phrase like “Windows is the best” may not include enough context to know that “Windows” means Friley Windows dining center. If chunks are too large, unrelated opinions about meal plans, restaurants, dining halls, and GET & Go may get mixed together and make retrieval less precise. The overlap helps preserve context when a useful detail appears near a chunk boundary.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`

**Top-k:** 5 chunks per query

**Production tradeoff reflection:**

I will use `all-MiniLM-L6-v2` because it runs locally, is free, and is fast enough for this project. I will use ChromaDB as the local vector store and retrieve the top 5 chunks for each user question.

For a production system, I would compare embedding models based on accuracy, latency, cost, context length, multilingual support, and how well they handle informal student language. A larger API-hosted embedding model might understand slang, vague student comments, or mixed-language comments better, but it would cost more and depend on an external service. A local model is easier for this course project because it avoids API costs for embeddings.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say is the best food on campus? | The system should summarize specific student recommendations from the collected Reddit documents, such as campus food spots, dining halls, vendors, or nearby restaurants mentioned in the sources. |
| 2 | What do students say about Friley Windows? | The system should mention student opinions about Windows, including whether students describe it positively, compare it with UDCC, or mention vegetarian or healthier options. |
| 3 | Are ISU meal plans worth it? | The system should combine official meal plan information with student advice about swipes, Dining Dollars, plan choice, and cost efficiency. |
| 4 | What are quick food options for students between classes? | The system should mention GET & Go from the official source and student-recommended lunch spots from the dining location thread if those chunks are retrieved. |
| 5 | What restaurants near campus do students recommend? | The system should answer using the near-campus restaurant discussion and mention specific restaurants that students recommend. |


---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Reddit threads may contain noisy text such as jokes, usernames, repeated reply labels, or comments that do not actually answer the dining question. If I include too much noise, retrieval may return irrelevant chunks. I will reduce this risk by manually copying only useful post text and relevant comments into the `.txt` files.

2. Student opinions may conflict. One student may say a dining hall is great while another says it is bad. The system should summarize disagreement instead of pretending there is one correct opinion.

3. Some user questions may be too vague, such as “What is good?” A vague query may retrieve mixed chunks about dining halls, restaurants, and meal plans. I will evaluate this by testing specific questions first and documenting at least one failure case if retrieval is too broad.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     flowchart LR
    A[Raw .txt documents in docs/] --> B[Document ingestion and cleaning with Python]
    B --> C[Paragraph-based chunking: 700 characters, 100 overlap]
    C --> D[Embeddings with all-MiniLM-L6-v2]
    D --> E[ChromaDB vector store]
    F[User question] --> G[Semantic retrieval: top-k = 5]
    E --> G
    G --> H[Groq Llama 3.3 grounded generation]
    H --> I[Answer with source filenames]

     

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

I plan to use Claude and ChatGPT to help implement ingest.py. I will give the AI my Documents section, Chunking Strategy section, and Architecture diagram. I expect it to produce functions that load .txt files from docs/, clean repeated whitespace and boilerplate, and split text into paragraph-based chunks around 700 characters with 100 characters of overlap. I will verify the output by printing 5 sample chunks and checking that they are readable, substantive, and labeled with the correct source file.

**Milestone 4 — Embedding and retrieval:**

I plan to use Claude or ChatGPT to help implement retriever.py. I will give it my Retrieval Approach section and ask for ChromaDB code that embeds chunks with all-MiniLM-L6-v2, stores source metadata, and retrieves the top 5 chunks for a query. I will verify the code by printing retrieved chunks and distance scores for at least 3 evaluation questions.

**Milestone 5 — Generation and interface:**

I plan to use Claude and ChatGPT to help implement generator.py, query.py, and a Gradio app.py. I will give the AI my grounding requirement: answers must use only retrieved chunks, cite source filenames, and refuse when the documents do not contain enough information. I will verify the output by asking one answerable question and one out-of-scope question, then checking whether the response cites sources and avoids guessing.
