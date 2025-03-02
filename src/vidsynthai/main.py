import os
from src.vidsynthai.llm_client import LLMClient
from src.vidsynthai.utils import (
    get_prommpts,
    get_user_chat_format,
    get_model_config,
    get_python_code,
    write_code_to_file
)
from src.vidsynthai.animation.utils import compile_manim, get_video_duration
from loguru import logger

logger.add("app.log", format="{time} {level} {message}", level="INFO")


def main():
    llm_cliemt = LLMClient()
    prompts = get_prommpts()
    model_config = get_model_config()
    root_path = "experiments"
    file_name = "animation_v7.py"

    maths_expert = prompts['math_expert']
    animator = prompts['animator']
    script_prompt = prompts['script_writer']
    model_name = model_config['model_name']

    user_query = """Solve the quadratic equation: \[x^2 - 5x + 6 = 0\]"""

    get_solution = [maths_expert, get_user_chat_format(user_query)]

    response = llm_cliemt.chat_completion(get_solution, model_name)
    query_solution = response.split('</think>')[-1]
    logger.info(f"SOLUTION: {query_solution}")
    get_animation = [animator, get_user_chat_format(f"Question: {user_query}\n\nSolution: {query_solution}")]

    animation_response = llm_cliemt.chat_completion(get_animation, model_name)
    animation_code = animation_response.split('</think>')[-1]
    logger.info(f"CODE: {animation_code}")
    manim_code = get_python_code(animation_code)
    file_path = os.path.join(root_path, file_name)

    if manim_code:
        try:
            write_code_to_file(file_path, manim_code)
            print(f"Code successfully stored at: {root_path}")
        except Exception as e:
            print(f"Failed to write the file: {e}")

    # Compile manim video
    video_duration_secs = 60
    try:
        output_dir = compile_manim(file_path)
        video_duration_secs = get_video_duration([file for file in os.listdir(os.path.join(output_dir, "videos", file_name.replace(".py", ""), "1080p60")) if ".mp4" in file][0])
        # video_duration_secs = 40
    except Exception as e:
        print(f"Video compilation failed due to: {e}")

    # Get video duration

    get_transcript = [script_prompt, get_user_chat_format(f"Question: {user_query}\n\nSolution: {query_solution}\n\n Video Duration: {video_duration_secs} \n\nCode: {animation_code}")]
    response = llm_cliemt.chat_completion(get_transcript, model_name)
    transcript = response.split('</think>')[-1]

    logger.info(f"TRANSCRIPT: {transcript}")


if __name__ == "__main__":
    main()
