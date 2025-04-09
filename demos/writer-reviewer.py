import asyncio
from common import completion

WRITER_SYSTEM_MESSAGE = "You are a very creative children book author. Keep the stories short. If revising the story, write the full story with the revisions."
REVIEWER_SYSTEM_MESSAGE = "You are a helpful AI assistant which provides constructive feedback on Kids stories to add a postive impactful ending. Respond with 'APPROVE' to when your feedbacks are addressed."


async def main(task: str) -> None:
    if not task:
        return

    # Write the story
    messages = [{
        "role": "system",
        "content": WRITER_SYSTEM_MESSAGE
    }, {
        "role": "user",
        "content": task
    }]
    story = await completion(messages=messages)
    print(f"Story:\n{story}")

    # Review the story
    messages = [{
        "role": "system",
        "content": REVIEWER_SYSTEM_MESSAGE
    }, {
        "role": "user",
        "content": story
    }]
    review = await completion(messages=messages)
    print(f"\nReview:\n{review}")

    # Rewrite the story based on the review
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
    rewrite = await completion(messages=messages)
    print(f"\nStoryRewrite:\n{rewrite}")

    # Review the rewritten story
    messages = [{
        "role": "system",
        "content": REVIEWER_SYSTEM_MESSAGE
    }, {
        "role": "user",
        "content": story
    }, {
        "role": "user",
        "content": review
    }, {
        "role": "user",
        "content": rewrite
    }]
    rewrite = await completion(messages=messages)
    print(f"\nFinal Review:\n{rewrite}")


if __name__ == "__main__":
    asyncio.run(main(task="Write a story about a dog living in the moon."))
