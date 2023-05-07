import torch
import discord
from discord.ext import commands
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

from pie import check, i18n, logger

_ = i18n.Translator("modules/gpt").translate
bot_log = logger.Bot.logger()
guild_log = logger.Guild.logger()


class Speak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model_path = "modules/gpt/speak/" + "models/BolGPT/"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = GPT2LMHeadModel.from_pretrained(self.model_path)
        self.tokenizer = GPT2TokenizerFast.from_pretrained(
            self.model_path, pad_token="<|endoftext|>"
        )
        self.max_length = 150
        self.min_length = 50

        self.model.eval()
        self.model.to(self.device)

    # COMMANDS

    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    @check.acl2(check.ACLevel.MEMBER)
    @commands.command()
    async def speak(self, ctx: commands.Context):
        """What should BolGPT say?"""
        async with ctx.typing():
            text = ctx.message.content.lstrip(f"{ctx.prefix}").lstrip(f"{str(ctx.command.name)} ")

            input_ids = self.tokenizer.encode("<|endoftext|>" + text, return_tensors="pt").to(self.device)
            sample_output = self.model.generate(
                input_ids,
                pad_token_id=0,
                do_sample=True,
                max_length=self.max_length,
                min_length=self.max_length,
                top_k=50,
                temperature=0.9,
            )[0]
            output: str = self.tokenizer.decode(sample_output.tolist())
            reply = "\n".join(output.split("\n")[:2]).replace('<|endoftext|>', '')
        await ctx.message.reply(discord.utils.escape_mentions(reply))


async def setup(bot) -> None:
    await bot.add_cog(Speak(bot))
