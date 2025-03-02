import os
import soundfile as sf          # noqa
import numpy as np
from kokoro import KPipeline


class AudioGenerator:
    def __init__(self, output_dir, voice='af_heart', speed=1, sample_rate=24000):
        """
        Initializes the AudioGenerator class.

        Args:
            output_dir (str): The directory where the final audio will be saved.
            voice (str, optional): The TTS voice to use. Defaults to 'af_heart'.
            speed (int, optional): The speed of speech. Defaults to 1.
            sample_rate (int, optional): The sample rate of the output audio. Defaults to 24000.
        """
        self.output_dir = output_dir
        self.voice = voice
        self.speed = speed
        self.sample_rate = sample_rate
        self.pipeline = KPipeline(lang_code='a')  # Modify language as needed
        
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_audio(self, text):
        """
        Generates and saves synthesized speech audio from text.

        Args:
            text (str): The input text to synthesize.

        Returns:
            str: The path to the final merged audio file.
        """
        generator = self.pipeline(text, voice=self.voice, speed=self.speed, split_pattern=r'\n+')
        
        audio_segments = []
        silence = np.zeros(int(self.sample_rate))  # 1 second silence

        for i, (_, _, audio) in enumerate(generator):
            audio_segments.append(audio)
            audio_segments.append(silence)  # Add a 1-second pause

        merged_audio = np.concatenate(audio_segments)
        output_path = os.path.join(self.output_dir, "final_audio.wav")
        sf.write(output_path, merged_audio, self.sample_rate)

        return output_path


if __name__ == "__main__":
    # Example usage
    text_input = """Let's solve the quadratic equation x squared minus five x plus six equals zero.  

    First, we recognize this is in standard quadratic form ax² + bx + c = zero. Here, a equals one, b equals negative five, and c equals six.  

    We need two numbers that add up to negative five and multiply to six. Let's test factor pairs of six...  

    Negative two and negative three satisfy both conditions: their sum is negative five and product is six.  

    This lets us factor the equation as (x minus two)(x minus three) equals zero.  

    Using the zero product property, either x minus two equals zero or x minus three equals zero.  

    Solving both equations gives us x equals two and x equals three.  

    Let's verify by substitution. Plugging two into the equation... and three... both satisfy the equation.  

    The final solutions are boxed two and boxed three."""

    output_directory = "media_output/videos/animation_v7/1080p60"
    audio_gen = AudioGenerator(output_directory)
    audio_file = audio_gen.generate_audio(text_input)

    print(f"Audio saved at: {audio_file}")
