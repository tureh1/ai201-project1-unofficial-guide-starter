# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

My domain is unofficial student knowledge about Iowa State University dining and campus food. This knowledge is valuable because official ISU Dining pages explain menus, meal plans, hours, and dining programs, but they do not fully show what students actually think is worth eating, which places are convenient between classes, what students complain about, or how students choose between meal plans. Student opinions are scattered across Reddit threads and informal reviews, so a RAG system can make this information easier to search and summarize.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #  | Source                                | Type                         | URL or file path                             |
| -- | ------------------------------------- | ---------------------------- | -------------------------------------------- |
| 1  | Iowa State University Dining Overview | Official ISU Dining page     | `docs/01_isu_dining_overview.txt`            |
| 2  | ISU Dining Meal Plans and Rates       | Official ISU Dining page     | `docs/02_isu_meal_plans.txt`                 |
| 3  | ISU Dining Hours and Menus            | Official ISU Dining page     | `docs/03_isu_hours_menus.txt`                |
| 4  | ISU Dining GET & Go / Express Meals   | Official ISU Dining page     | `docs/04_isu_get_and_go.txt`                 |
| 5  | Best food on campus?                  | Reddit thread from r/iastate | `docs/05_reddit_best_food_on_campus.txt`     |
| 6  | Best Dining Hall / ISU food?          | Reddit thread from r/iastate | `docs/06_reddit_best_dining_hall.txt`        |
| 7  | Fave dining locations on campus?      | Reddit thread from r/iastate | `docs/07_reddit_fave_dining_locations.txt`   |
| 8  | Meal Plans                            | Reddit thread from r/iastate | `docs/08_reddit_meal_plans.txt`              |
| 9  | 5 best restaurants near campus        | Reddit thread from r/iastate | `docs/09_reddit_near_campus_restaurants.txt` |
| 10 | Dining Hall Food                      | Reddit thread from r/iastate | `docs/10_reddit_dining_hall_food.txt`        |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** Around 500 characters per chunk.

**Overlap:** One paragraph of overlap between adjacent chunks.

**Why these choices fit your documents:**

My documents are mostly short official dining descriptions and student-opinion summaries from Reddit threads. I used smaller chunks because student dining opinions are often specific and short, such as a recommendation for Clyde’s, Heaping Plato, Windows, or West Street Deli. If the chunks were too large, many unrelated food recommendations would be mixed together, making retrieval less precise.

I used paragraph-based chunking instead of blindly splitting every 500 characters. This helped keep complete ideas together. I also used one paragraph of overlap so that if an important recommendation or explanation was near the edge of a chunk, the next chunk would still include enough context.

Before chunking, my pipeline loads all `.txt` files from the `docs/` folder, removes unnecessary source headers from the chunk body, keeps the document title as a “Document topic,” removes helper/planning text, normalizes line breaks, removes extra blank lines, and stores metadata such as the source filename and chunk index.

**Final chunk count:** 61 chunks.

---

## Sample Chunks

**Sample chunk 1 — Source: `01_isu_dining_overview.txt`**

Document topic: Iowa State University Dining Overview

ISU Dining is the official dining service for Iowa State University. The official dining website describes campus dining as having many options throughout the day, from breakfast to late-night snacks. It also says online menus help students access detailed nutritional information before choosing where to eat.

**Sample chunk 2 — Source: `02_isu_meal_plans.txt`**

Document topic: ISU Dining Meal Plans and Rates

The ISU Dining meal plan page explains official meal plan options for Iowa State students. Meal plans are built around dining center meals, GET & Go or Express meals, Dining Dollars, guest meals, and sometimes Flex Meals depending on the plan.

**Sample chunk 3 — Source: `05_reddit_best_food_on_campus.txt`**

Document topic: Best food on campus?

The original Reddit post is from an incoming freshman asking what the best food places or dining halls are on campus. Student replies show that “best food” at Iowa State does not only mean dining halls. Students recommend dining halls, campus vendors, Memorial Union options, and nearby restaurants.

**Sample chunk 4 — Source: `07_reddit_fave_dining_locations.txt`**

Clyde’s is recommended by students who like burgers. One student says Clyde’s is in UDCC on the first floor and has some of the best burgers. Another student recommends Heaping Plato, Lance and Ellie’s, or Pono Poke for lunch between classes; Hawthorn for wing nights; Conversations and Windows for dining centers; and Whirlybird’s for smoothies or shakes.

**Sample chunk 5 — Source: `09_reddit_near_campus_restaurants.txt`**

Students recommend many nearby restaurants and food spots. Common recommendations include Es Tas, Cafe Beaudelaire or Cafe B, Provisions Lot F, Stomping Grounds, and West Street Deli. These places are useful for students looking for food or hangout spots near campus.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `sentence-transformers/all-MiniLM-L6-v2`

**Production tradeoff reflection:**

I used `all-MiniLM-L6-v2` because it runs locally, is free, does not require an API key, and is recommended for this project. It works well for a small collection of student dining documents because the queries and documents are short.

If I were building this for real users and cost was not a constraint, I would compare models based on retrieval accuracy, latency, context length, multilingual support, and how well the model understands informal student language. A larger hosted embedding model might perform better with slang, vague wording, or mixed-language questions, but it would cost more and depend on an external API. A local model is cheaper and easier to run, but it may miss subtle meanings in student comments.

---

## Retrieval Test Results

### Retrieval test 1

**Query:** What do students say is the best food on campus?

**Top returned chunks:**

1. `07_reddit_fave_dining_locations.txt`, chunk 1 — A student asks for the best places to grab lunch on campus, and the chunk discusses price, Hawthorn, the Memorial Union, and packing lunch if a student does not have a meal plan.
2. `06_reddit_best_dining_hall.txt`, chunk 0 — The chunk introduces student opinions about the best ISU dining hall or campus food and explains that students compare taste, cost, convenience, reliability, and variety.
3. `09_reddit_near_campus_restaurants.txt`, chunk 1 — The chunk lists student-recommended nearby food spots such as Es Tas, Cafe B, Provisions Lot F, Stomping Grounds, and West Street Deli.
4. `07_reddit_fave_dining_locations.txt`, chunk 5 — The chunk lists Clyde’s, Heaping Plato, Lance and Ellie’s, Pono Poke, Hawthorn, Conversations, Windows, Whirlybird’s, West Street Deli, 1+1, and Joy’s Mongolian Grill.
5. `05_reddit_best_food_on_campus.txt`, chunk 0 — The chunk directly introduces the Reddit thread about “Best food on campus?” and says students recommend dining halls, vendors, Memorial Union options, and nearby restaurants.

**Why the chunks are relevant:**

These chunks are relevant because the query asks for student opinions about the best food on campus. The retrieved chunks include both general student recommendation threads and specific food locations such as Clyde’s, Heaping Plato, Hawthorn, Conversations, Windows, Whirlybird’s, West Street Deli, and 1+1. The first version of retrieval did not strongly return `05_reddit_best_food_on_campus.txt`, so I improved retrieval by keeping the document title as “Document topic” in the chunk text.

### Retrieval test 2

**Query:** Are ISU meal plans worth it?

**Top returned chunks:**

1. `08_reddit_meal_plans.txt`, chunk 1 — The chunk explains student opinions about Gold and Cardinal meal plans, including that Gold has limited swipes and Cardinal has unlimited swipes.
2. `02_isu_meal_plans.txt`, chunk 1 — The chunk describes the Cardinal Plan as having unlimited dining center access, GET & Go meals, Dining Dollars, and guest meals.
3. `06_reddit_best_dining_hall.txt`, chunk 5 — The chunk says some students feel ISU dining can be overpriced or not worth it compared with quality and suggests nearby restaurants as alternatives.
4. `04_isu_get_and_go.txt`, chunk 0 — The chunk explains that GET & Go is a quick meal option for students who do not have time to sit in a dining center.
5. `02_isu_meal_plans.txt`, chunk 0 — The chunk explains that ISU meal plans are built around dining center meals, GET & Go or Express meals, Dining Dollars, guest meals, and sometimes Flex Meals.

**Why the chunks are relevant:**

These chunks are relevant because the question asks whether meal plans are worth it, which requires both official plan information and student opinions. The official chunks explain what the plans include, while the Reddit chunks explain how students decide between Gold and Cardinal based on eating habits, cost, and swipe usage.

### Retrieval test 3

**Query:** What restaurants near campus do students recommend?

**Top returned chunks:**

1. `09_reddit_near_campus_restaurants.txt`, chunk 1 — The chunk lists Es Tas, Cafe Beaudelaire or Cafe B, Provisions Lot F, Stomping Grounds, and West Street Deli.
2. `09_reddit_near_campus_restaurants.txt`, chunk 0 — The chunk introduces the Reddit thread asking for restaurants near campus, especially near residence halls or engineering buildings.
3. `09_reddit_near_campus_restaurants.txt`, chunk 2 — The chunk lists Pammel Grocery Deli, Mr. Burrito, The Cafe, and Macubana.
4. `09_reddit_near_campus_restaurants.txt`, chunk 6 — The chunk lists 1+1, West Street Deli, Aunt Maude’s, Cornbred, Filling Station, Ichiban, Macubana, Blaze Pizza, Pizza Pit, Freddy’s, and House of Chen.
5. `07_reddit_fave_dining_locations.txt`, chunk 0 — The chunk introduces a Reddit thread about places to grab lunch on campus between classes.

**Why the chunks are relevant:**

These chunks are strongly relevant because most of the top results come from the near-campus restaurants document. The chunks directly list restaurant names and food spots that students recommend near Iowa State, which directly answers the query.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

My system prompt tells the model to answer using only the retrieved document context. The prompt says:

“You must answer using ONLY the provided retrieved document context. Do not use outside knowledge. Do not make up facts. If the retrieved context does not contain enough information to answer the question, say exactly: ‘I don't have enough information in the collected documents to answer that.’”

This helps prevent the model from using general knowledge about Iowa State or campus dining. The retrieved chunks are passed into the prompt as the only allowed context.

**How source attribution is surfaced in the response:**

Source attribution is handled programmatically. In `query.py`, each retrieved chunk includes metadata with the source filename and chunk index. After the model generates the answer, the program creates a separate `Sources:` section using the unique source filenames from the retrieved chunks. This makes citations more reliable because the program adds them directly instead of depending only on the LLM to remember them.

---

## Example System Responses

### Example response 1

**Question:** What do students say is the best food on campus?

**System response:**

According to the students, some of the best food options on campus include Hawthorn, especially for wing nights, and Clyde’s in the UDCC for burgers. Other popular spots mentioned are Heaping Plato, Lance and Ellie’s, Pono Poke, Conversations, and Windows for dining centers, as well as Whirlybird’s for smoothies or shakes. Additionally, students recommend West Street Deli for great sandwiches with large portions and Joy’s Mongolian Grill for General Tso chicken.

**Sources:**

* `07_reddit_fave_dining_locations.txt`
* `06_reddit_best_dining_hall.txt`
* `09_reddit_near_campus_restaurants.txt`
* `05_reddit_best_food_on_campus.txt`

### Example response 2

**Question:** What restaurants near campus do students recommend?

**System response:**

Students recommend several restaurants near campus, including Es Tas, Cafe Beaudelaire or Cafe B, Provisions Lot F, Stomping Grounds, and West Street Deli. Other popular options include Pammel Grocery Deli, Mr. Burrito, The Cafe, Macubana, 1+1, Aunt Maude’s, Cornbred, Filling Station, Ichiban, Blaze Pizza, Pizza Pit, Freddy’s, and House of Chen. These places are useful for students looking for food or hangout spots near residence halls, engineering buildings, or other areas of campus.

**Sources:**

* `09_reddit_near_campus_restaurants.txt`
* `07_reddit_fave_dining_locations.txt`

### Out-of-scope example

**Question:** What do students say about parking on campus?

**System response:**

I don't have enough information in the collected documents to answer that.

**Sources:**

* `05_reddit_best_food_on_campus.txt`
* `07_reddit_fave_dining_locations.txt`
* `06_reddit_best_dining_hall.txt`
* `09_reddit_near_campus_restaurants.txt`

---

## Query Interface

I built a simple Gradio web interface in `app.py`. The interface is designed so a user can test the RAG system without using the terminal.

**Input field:**

* A text box labeled “Your question”
* The user types a natural-language question about ISU dining, meal plans, dining halls, campus food, or nearby restaurants.

**Output fields:**

* An “Answer” box that displays the LLM-generated grounded response
* A “Sources” box that displays the source document filenames retrieved for the answer

**How to run the interface:**

1. Activate the virtual environment.
2. Run `python app.py`.
3. Open the local Gradio URL, usually `http://127.0.0.1:7860`.
4. Type a question and click “Ask.”

**Sample interaction transcript:**

User enters:

Are ISU meal plans worth it?

System returns:

Whether ISU meal plans are worth it depends on individual student preferences and needs. Some students feel that ISU dining can be overpriced or not worth it compared to the quality, and they suggest nearby restaurants like 1+1 and West Street Deli as alternatives. On the other hand, meal plans like the Cardinal Plan offer unlimited access to dining centers, which can be beneficial for students who plan to eat in the dining halls frequently. The Cardinal Plan also includes GET & Go meals, Dining Dollars, and guest meals, which can provide flexibility and convenience. The Gold Plan, which has a limited number of swipes, may be a good option for students who do not plan to eat in the dining halls more than twice a day. Ultimately, the value of an ISU meal plan depends on how well it fits a student's lifestyle and eating habits.

Sources:

* `08_reddit_meal_plans.txt`
* `02_isu_meal_plans.txt`
* `06_reddit_best_dining_hall.txt`
* `04_isu_get_and_go.txt`

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question                                            | Expected answer                                                                                                                                                                                                                                                                                                               | System response (summarized)                                                                                                                                                                                                                                                                            | Retrieval quality  | Response accuracy |
| - | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ----------------- |
| 1 | What do students say is the best food on campus?    | The answer should mention student-recommended places such as Heaping Plato, Clyde’s, Hawthorn, Conversations, Windows, Whirlybird’s, West Street Deli, and other student food recommendations.                                                                                                                                | The system mentioned Hawthorn, Clyde’s, Heaping Plato, Lance and Ellie’s, Pono Poke, Conversations, Windows, Whirlybird’s, West Street Deli, and Joy’s Mongolian Grill.                                                                                                                                 | Relevant           | Accurate          |
| 2 | Are ISU meal plans worth it?                        | The answer should explain that value depends on eating habits. Cardinal is useful for frequent dining center users because it has unlimited access, while Gold may work for students who do not eat in dining halls more than twice per day. It should also mention Dining Dollars, GET & Go, or student concerns about cost. | The system explained that Cardinal offers unlimited dining center access and includes GET & Go, Dining Dollars, and guest meals. It also explained that Gold may work for students who do not eat in dining halls more than twice a day. It mentioned that some students feel dining can be overpriced. | Relevant           | Accurate          |
| 3 | What restaurants near campus do students recommend? | The answer should mention specific near-campus restaurants such as Es Tas, Cafe B, West Street Deli, 1+1, Macubana, Ichiban, Blaze Pizza, Pizza Pit, and others.                                                                                                                                                              | The system listed Es Tas, Cafe B, Provisions Lot F, Stomping Grounds, West Street Deli, Pammel Grocery Deli, Mr. Burrito, The Cafe, Macubana, 1+1, Aunt Maude’s, Cornbred, Filling Station, Ichiban, Blaze Pizza, Pizza Pit, Freddy’s, and House of Chen.                                               | Relevant           | Accurate          |
| 4 | What do students say about Friley Windows?          | The answer should mention that students describe Friley Windows positively, especially for variety of cuisines, healthier options, vegan or vegetarian-friendly choices, salad bar, soups, tikka masala, and a vegetarian section with variety and flavor.                                                                    | The system said students describe Friley Windows as the best dining center because of its variety of cuisines. It also said Windows is healthier and more vegan or vegetarian friendly, has a reliable salad bar and soups, and is mentioned positively for tikka masala and vegetarian variety.        | Relevant           | Accurate          |
| 5 | What do students say about parking on campus?       | The system should refuse because the collected documents are about dining and campus food, not parking.                                                                                                                                                                                                                       | The system said: “I don't have enough information in the collected documents to answer that.”                                                                                                                                                                                                           | Partially relevant | Accurate refusal  |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

What do students say about parking on campus?

**What the system returned:**

The system correctly refused to answer and said: “I don't have enough information in the collected documents to answer that.” However, the retrieval step still returned dining-related source files, such as `05_reddit_best_food_on_campus.txt`, `07_reddit_fave_dining_locations.txt`, `06_reddit_best_dining_hall.txt`, and `09_reddit_near_campus_restaurants.txt`.

**Root cause (tied to a specific pipeline stage):**

This is a retrieval-stage limitation. ChromaDB always returns the top-k closest chunks, even if none of the chunks are truly relevant to the question. Since my document collection only covers dining and campus food, the retriever still returned the “closest” dining-related chunks for a parking question. The generation stage handled the issue correctly by refusing to answer, but the retrieval stage did not have a confidence threshold to filter out weak matches.

**What you would change to fix it:**

I would add a distance threshold to the retrieval function. If the best retrieved chunks have weak similarity scores, the system should return no context and immediately say that the collected documents do not contain enough information. I could also add metadata filtering or a domain check that detects whether a question is outside the ISU dining and campus food topic.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The spec helped me make important design choices before writing the code. For example, I already knew my system would use local `.txt` documents, paragraph-based chunking, `all-MiniLM-L6-v2` embeddings, ChromaDB, and Groq for generation. This made the coding process easier because each file had a clear purpose: `ingest.py` for document processing, `retriever.py` for vector search, `query.py` for grounded generation, and `app.py` for the interface.

The spec also helped me test the system in the right order. Instead of building the whole app first, I tested ingestion, then retrieval, then generation. This made debugging easier because I could see whether a problem came from bad chunks, bad retrieval, or the LLM response.

**One way your implementation diverged from the spec, and why:**

My original plan used chunks around 700 characters, but I changed the chunk size to around 500 characters after testing. The first chunks were readable, but they were sometimes too broad and mixed multiple ideas together. Because my documents were short student-opinion summaries, smaller paragraph-based chunks worked better.

I also changed the preprocessing step so the document title stayed in the chunk as “Document topic.” At first, I removed the title completely, but retrieval for “best food on campus” did not return `05_reddit_best_food_on_campus.txt` as strongly as I wanted. Keeping the title improved retrieval because it gave the embedding model more useful topic keywords.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

* *What I gave the AI:* I mainly used Claude for planning support. I gave Claude the project instructions, my chosen domain about Iowa State dining, and my list of official ISU Dining and Reddit sources.
* *What it produced:* Claude helped me organize the project idea into a clearer domain, document list, chunking strategy, retrieval approach, evaluation questions, and AI tool plan for `planning.md`.
* *What I changed or overrode:* I narrowed the project to Iowa State dining and campus food instead of a broader student-life guide. I also revised the chunking strategy after testing real chunk output instead of accepting the first plan unchanged.

**Instance 2**

* *What I gave the AI:* I gave Claude my Chunking Strategy section from `planning.md` and asked it to help implement an ingestion pipeline that loads `.txt` files, cleans them, and creates readable chunks.
* *What it produced:* Claude helped draft an `ingest.py` script that loads files from the `docs/` folder, cleans the text, creates paragraph-based chunks, adds source metadata, and prints sample chunks.
* *What I changed or overrode:* I changed the chunk size from about 700 characters to about 500 characters after inspecting the chunks. I also kept one paragraph of overlap and adjusted the cleaning function so the document title stays in the chunk as “Document topic,” which improved retrieval.

**Instance 3**

* *What I gave the AI:* I gave Claude my Retrieval Approach section and asked for help using `sentence-transformers/all-MiniLM-L6-v2` with ChromaDB.
* *What it produced:* Claude helped generate `retriever.py`, which embeds chunks, stores them in ChromaDB, and retrieves top-k chunks with source filenames and distance scores.
* *What I changed or overrode:* I tested retrieval before adding generation and noticed that the “best food on campus” query did not strongly retrieve the best food Reddit thread at first. I changed the chunk text to include the document topic, reran retrieval, and confirmed that `05_reddit_best_food_on_campus.txt` appeared in the top results.

**Instance 4**

* *What I gave the AI:* I used ChatGPT for smaller debugging and wording help after most of the implementation was already planned with Claude. I gave ChatGPT my terminal outputs and asked whether the retrieval and generation results looked grounded enough for the rubric.
* *What it produced:* ChatGPT helped me interpret the output, improve README wording, and make the evaluation and failure-case explanation more specific.
* *What I changed or overrode:* I did not accept the AI output blindly. I used my own terminal results, such as the actual Friley Windows response and the parking refusal response, to make the README reflect what my system actually returned.
