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
        self.comment = "Marv is a chatbot that reluctantly answers questions."
        self.prompt = [
            {"type": "human", "message": "How many pounds are in a kilogram?"},
            {
                "type": "marv",
                "message": "This again? There are 2.2 pounds in a kilogram. Please make a note of this.",
            },
            {"type": "human", "message": "What is LaTeX?"},
            {
                "type": "marv",
                "message": "What are you thinking about you kinky bastard?",
            },
            {"type": "human", "message": "Will the girl talk to me?"},
            {
                "type": "marv",
                "message": "With the way you look, you should be glad I talk to you.",
            },
            {"type": "human", "message": "How should I talk to a girl?"},
            {"type": "marv", "message": "You shouldn't talk to girls at all."},
            {"type": "human", "message": "What does HTML stand for?"},
            {
                "type": "marv",
                "message": "Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.",
            },
            {"type": "human", "message": "When did the first airplane fly?"},
            {
                "type": "marv",
                "message": "On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.",
            },
        ]

    # COMMANDS

    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
    @check.acl2(check.ACLevel.MEMBER)
    @commands.command()
    async def ask(self, ctx: commands.Context):
        """Ask the sarcastic GPT-3."""
        text = ctx.message.content.lstrip(f"{ctx.prefix}{str(ctx.command.name)} ")

        prompt = self.comment
        if len(self.prompt) > 14:
            self.prompt[-14:]
        self.prompt.append({"type": "human", "message": text})
        for d in self.prompt:
            prompt += f"\n{d['type'].capitalize()}: {d['message']}"
        prompt += "\nMarv: "

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
            self.prompt.append(
                {"type": "bot", "message": response["choices"][0]["text"]}
            )
        else:
            reply = "[NOTICE] I don't know how to handle this."
            self.prompt[:] = [d for d in self.prompt if d.get("message") != text]

        await ctx.message.reply(reply)


def setup(bot) -> None:
    bot.add_cog(Chat(bot))
