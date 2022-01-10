import os

import openai
from nextcord.ext import commands

from pie import i18n, logger


_ = i18n.Translator("modules/gpt3").translate
bot_log = logger.Bot.logger()
guild_log = logger.Guild.logger()

openai.api_key = os.getenv("OPENAI_API_KEY")


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conversations = {}

    # COMMANDS

    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
    @commands.command()
    async def ask(self, ctx: commands.Context):
        """Ask the sarcastic GPT-3."""
        text = ctx.message.content.lstrip(f"{ctx.prefix}{str(ctx.command.name)} ")

        prompt = f"Marv is a chatbot that reluctantly answers questions.\nYou: How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What is LaTeX?\nMarv: What are you thinking about you kinky bastard?\nYou: Will I get a girlfriend?\nMarv: With the way you look, you should be glad you can talk to me.\nYou: How should I talk to a girl?\nMarv: You shouldn't talk to girls at all.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: {text}\nMarv: "

        response = openai.Completion.create(
            engine="curie",
            prompt=prompt,
            temperature=0.3,
            max_tokens=150,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0,
            stop=["\n", "Marv: ", "You: "],
        )
        if response["choices"][0]["text"] != "":
            reply = response["choices"][0]["text"]
        else:
            reply = "[NOTICE] I don't know how to handle this."

        await ctx.message.reply(reply)


def setup(bot) -> None:
    bot.add_cog(Chat(bot))
