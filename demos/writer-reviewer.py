import asyncio
from common import completion

WRITER_SYSTEM_MESSAGE = "You are a very creative children book author. Keep the stories short. If revising the story, write the full story with the revisions."
REVIEWER_SYSTEM_MESSAGE = "You are a helpful AI assistant which provides constructive feedback on Kids stories to add a postive impactful ending. Respond with 'APPROVE' to when your feedbacks are addressed."


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
    print(f"Story:\n{story}")

    # Review the story
    review = await review_story(story)
    print(f"\nReview:\n{review}")

    # Rewrite the story based on the review
    rewrite = await rewrite_story(story, review)
    print(f"\nStoryRewrite:\n{rewrite}")

    # Review the rewritten story
    final_review = await review_story(story, review, rewrite)
    print(f"\nFinal Review:\n{final_review}")


if __name__ == "__main__":
    asyncio.run(main(task="Write a story about a dog living in the moon."))
