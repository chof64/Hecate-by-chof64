# """
# Called by the `core/error/handler` when a critical error is encountered.
# """

# from components.embeds import GlobalEmbed


# class CriticalLoggers:
#     """
#     Contains all the critical exception loggers responsible
#     for informing the message author and developers.
#     """

#     def __init__(self, bot):
#         self.bot = bot
#         self.color = 0xF43F5E  # Tailwind CSS Rose 500

#     async def extension_not_found(self, ctx, error):
#         """
#         Called when an extension is not found.
#         """
#         embed = await GlobalEmbed.base_global(
#             self,
#             ctx,
#             title="Extension not found",
#             description=f"Extension `{ctx.invoked_with}` not found.",
#             color=self.color,
#         )
#         await ctx.send(embed=embed)

#     async def command_not_found(self, ctx, error):
#         """
#         Called when a command is not found.
#         """
#         embed = await GlobalEmbed.base_global(
#             self,
#             ctx,
#             title="Command not found",
#             description=f"Command `{ctx.invoked_with}` not found.",
#             color=self.color,
#         )
#         await ctx.send(embed=embed)
