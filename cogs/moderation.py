import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import datetime
from core.errors import construct_error_forbidden_embed, construct_error_limit_break_embed, \
    construct_error_http_exception_embed
from core.embeds import construct_basic_embed, construct_top_embed
from core.locales.getters import get_msg_from_locale_by_key
from core.parsers import parse_timeouts
import humanfriendly
from typing import Optional


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="mute", description="Mute with timeout discord's user")
    async def __mute(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True),
                     time: Optional[str] = SlashOption(required=True), *,
                     reason: Optional[str] = SlashOption(required=False)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        user: Optional[nextcord.Member]
            The discord's user, tag someone with @
        time: Optional[str]
            Type 1s/1m/1h/1d, this field is the time of mute
        reason: Optional[str]
            This parameter is optional, reason of mute
        """
        try:
            time_in_seconds = humanfriendly.parse_timespan(time)
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            if reason is None:
                reason = ' — '
            await user.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=time_in_seconds),
                            reason=reason)
            message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} {user.mention}",
                                            f"{requested} {interaction.user}\n📝 {reason}. 🕔 {time}",
                                            interaction.user.display_avatar))
        except nextcord.Forbidden:
            await interaction.response.send_message(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, 'forbidden_error'),
                    self.client.user.avatar.url)
            )

    @nextcord.slash_command(name="unmute", description="Unmute muted (timed out) discord user")
    async def __unmute(self, interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=True)):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        user: Optional[nextcord.Member]
            The discord's user, tag someone with @
        """
        try:
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            await user.edit(timeout=None)
            message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} {user.mention}",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        except nextcord.Forbidden:
            await interaction.response.send_message(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, 'forbidden_error'),
                    self.client.user.avatar.url)
            )

    @nextcord.slash_command(name="mutes", description="Show list of active mutes on this server")
    async def __mutes(self, interaction: Interaction):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        """
        requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
        mutes = parse_timeouts(interaction.guild.members)
        await interaction.response.send_message(
            embed=construct_top_embed(interaction.application_command.name, mutes,
                                      f"{requested} {interaction.user}", interaction.user.display_avatar))

    @nextcord.slash_command(name="clear", description="Deletes messages in channel, where command was used")
    async def __clear(self, interaction: Interaction,
                      messages_to_delete: Optional[int] = SlashOption(required=True),
                      *, before=None, after=None):
        """
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        messages_to_delete: Optional[int]
            How many messages i should delete, command limited to 1000 messages in one execution
        before
            ID of message, BEFORE THIS message deletion will take place
        after
            ID of message, AFTER THIS message deletion will take place
        """
        if messages_to_delete > 1000:
            return await interaction.response.send_message(
                embed=construct_error_limit_break_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, 'limit_break'),
                    self.client.user.avatar.url)
            )
        if before is None:
            before = interaction.message
        else:
            before = nextcord.Object(id=before)

        if after is not None:
            after = nextcord.Object(id=after)

        try:
            were_deleted = await interaction.channel.purge(limit=messages_to_delete, before=before, after=after)
            requested = get_msg_from_locale_by_key(interaction.guild.id, 'requested_by')
            message = get_msg_from_locale_by_key(interaction.guild.id, interaction.application_command.name)
            await interaction.response.send_message(
                embed=construct_basic_embed(interaction.application_command.name,
                                            f"{message} {len(were_deleted)}",
                                            f"{requested} {interaction.user}",
                                            interaction.user.display_avatar))
        except nextcord.Forbidden:
            return await interaction.response.send_message(
                embed=construct_error_forbidden_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, 'forbidden_error'),
                    self.client.user.avatar.url)
            )
        except nextcord.HTTPException:
            return await interaction.response.send_message(
                embed=construct_error_http_exception_embed(
                    get_msg_from_locale_by_key(interaction.guild.id, 'http_exception'),
                    self.client.user.avatar.url)
            )


def setup(client):
    client.add_cog(Moderation(client))
