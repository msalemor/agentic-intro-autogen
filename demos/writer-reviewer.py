import asyncio
import click
from common import REVIEWER_SYSTEM_MESSAGE, WRITER_SYSTEM_MESSAGE, completion


async def document_writer(task: str) -> str:
    messages = [{
        "role": "system",
        "content": WRITER_SYSTEM_MESSAGE
    }, {
        "role": "user",
        "content": task
    }]
    return await completion(messages=messages)


async def document_reviewer(story: str, previous_review=None, rewrite=None) -> str:
    messages = [{
        "role": "system",
        "content": REVIEWER_SYSTEM_MESSAGE
    }, {
        "role": "user",
        "content": story
    }]

    if previous_review:
        messages.append({
            "role": "user",
            "content": previous_review
        })

    if rewrite:
        messages.append({
            "role": "user",
            "content": rewrite
        })

    return await completion(messages=messages)


async def rewrite_document(story: str, review: str) -> str:
    messages = [{
        "role": "system",
        "content": WRITER_SYSTEM_MESSAGE
    }, {
        "role": "user",
        "content": story
    }, {
        "role": "user",
        "content": review
    }]
    return await completion(messages=messages)


async def main(task: str) -> None:
    if not task:
        return

    # Write the document
    document = await document_writer(task)
    click.echo(click.style(f"Document:\n{document}", fg="yellow"))
    # print(f"Story:\n{story}")

    # Review the document
    document_review = await document_reviewer(document)
    click.echo(click.style(f"\nReview:\n{document_review}", fg="green"))
    # print(f"\nReview:\n{review}")

    # Rewrite the document based on the review
    document_rewrite = await rewrite_document(document, document_review)
    click.echo(click.style(
        f"\Document Rewrite:\n{document_rewrite}", fg="yellow"))
    # print(f"\nStory Rewrite:\n{rewrite}")

    # Review the document story
    document_final_review = await document_reviewer(document, document_review, document_rewrite)
    print(f"\nFinal Review:\n{document_final_review}")


if __name__ == "__main__":
    asyncio.run(main(task="Write about prompt engineering."))
