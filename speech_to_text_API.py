import io

import requests
import asyncio

# Source: https://speechtext.ai/

# retrieve transcription results for the task
async def get_results(config):
    # endpoint to check status of the transcription task
    endpoint = "https://api.speechtext.ai/results?"
    # use a loop to check if the task is finished
    while True:
        results = requests.get(endpoint, params=config).json()
        if "status" not in results:
            break
        print("Task status: {}".format(results["status"]))
        if results["status"] == 'failed':
            print("The task is failed: {}".format(results))
            break
        if results["status"] == 'finished':
            break
        # sleep for 15 seconds if the task has the status - 'processing'
        await asyncio.sleep(15)
    return results


async def speech_to_text_pipeline(voice: io.BytesIO, key: str):

    endpoint = "https://api.speechtext.ai/recognize?"
    header = {'Content-Type': "application/octet-stream"}
    post_config = {
        "key": key,
        "language": "ru-RU",  # Expect to get voice messages in russian
        "punctuation": True,
        "format": "m4a"
    }

    r = requests.post(endpoint, headers=header, params=post_config, data=voice).json()

    get_config = {
        "key": key,
        "task": r['id'],
        "summary": True,
        "summary_size": 15,
        "highlights": False,
        "max_keywords": 10
    }

    transcription = await get_results(get_config)
    print("Transcription: {}".format(transcription))
    return transcription
