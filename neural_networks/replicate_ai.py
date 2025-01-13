import replicate


def generate(prompt: str):
    input = {
        "prompt": prompt,
        "aspect_ratio": "3:2"
    }

    output = replicate.run(
        "black-forest-labs/flux-1.1-pro-ultra",
        input=input
    )

    return output
