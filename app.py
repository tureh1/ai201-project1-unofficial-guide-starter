import gradio as gr

from query import ask


def handle_query(question):
    """
    Run the full RAG pipeline for a user question.
    """
    if not question or not question.strip():
        return "Please enter a question.", ""

    result = ask(question)

    answer = result["answer"]
    sources = "\n".join(f"- {source}" for source in result["sources"])

    return answer, sources


with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown("# The Unofficial Guide: ISU Dining")
    gr.Markdown(
        "Ask a question about Iowa State University dining, meal plans, dining halls, "
        "campus food, or nearby restaurants. Answers are grounded in the collected documents."
    )

    question = gr.Textbox(
        label="Your question",
        placeholder="Example: What do students say is the best food on campus?",
        lines=2,
    )

    ask_button = gr.Button("Ask")

    answer = gr.Textbox(
        label="Answer",
        lines=10,
    )

    sources = gr.Textbox(
        label="Sources",
        lines=5,
    )

    ask_button.click(
        fn=handle_query,
        inputs=question,
        outputs=[answer, sources],
    )

    question.submit(
        fn=handle_query,
        inputs=question,
        outputs=[answer, sources],
    )


if __name__ == "__main__":
    demo.launch()