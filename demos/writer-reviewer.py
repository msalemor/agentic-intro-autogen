import asyncio
import click
from common import completion

WRITER_SYSTEM_MESSAGE = "You are a AI techical document author. Write a concise document. If revising the document, write the full document with the revisions."
REVIEWER_SYSTEM_MESSAGE = "You are a reviewer AI assistant who can review technical documents. Make sure that the reviesion include an edge if approprite for the subject. Respond with 'APPROVE' to when your feedbacks are addressed."


async def write_story(task: str) -> str:
    messages = [{
        "role": "system",
        "content": WRITER_SYSTEM_MESSAGE
    }, {
        "role": "user",
        "content": task
    }]
    return await completion(messages=messages)


async def review_story(story: str, previous_review=None, rewrite=None) -> str:
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


async def rewrite_story(story: str, review: str) -> str:
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

    # Write the story
    story = await write_story(task)
    click.echo(click.style(f"Document:\n{story}", fg="yellow"))
    # print(f"Story:\n{story}")

    # Review the story
    review = await review_story(story)
    click.echo(click.style(f"\nReview:\n{review}", fg="green"))
    # print(f"\nReview:\n{review}")

    # Rewrite the story based on the review
    rewrite = await rewrite_story(story, review)
    click.echo(click.style(f"\Document Rewrite:\n{rewrite}", fg="yellow"))
    # print(f"\nStory Rewrite:\n{rewrite}")

    # Review the rewritten story
    final_review = await review_story(story, review, rewrite)
    print(f"\nFinal Review:\n{final_review}")


if __name__ == "__main__":
    asyncio.run(main(task="Write about prompt engineering."))
