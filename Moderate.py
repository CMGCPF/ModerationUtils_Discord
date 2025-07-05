#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord Moderation Utils

A utility class for Discord moderation permission checks.

Author: CMGCPF
Version: 1.0.0
Created: 05/07/2025
Python: 3.8+
Dependencies: discord.py >= 2.0.0

Description:
    This module provides utility functions to check if a moderator has the
    necessary permissions to perform various moderation actions on Discord
    server members, channels, roles, and other guild objects.

Usage:
    # Check if a member can be kicked
    if ModerationUtils.kickable(member, moderator, guild):
        await member.kick(reason="Violation of rules")
"""

__version__ = "1.0.0"
__author__ = "CMGCPF"

import discord
from typing import Union, Optional


class ModerationUtils:
    """
    Utility class for moderator permission checks in a Discord server.
    """

    @staticmethod
    def bot_verified(user: Union[discord.User, discord.Member]) -> bool:
        """
        Checks if a bot is verified by Discord.

        Args:
            user: The user/member to check

        Returns:
            bool: True if the bot is verified, False otherwise
        """
        try:
            return user.bot and user.public_flags.verified_bot
        except AttributeError:
            return False

    @staticmethod
    def kickable(
        member: discord.Member, moderator: discord.Member, guild: discord.Guild
    ) -> bool:
        """
        Checks if a member can be kicked by the moderator.

        Args:
            member: The member to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the member can be kicked, False otherwise
        """
        try:
            if not moderator.guild_permissions.kick_members:
                return False
            if member.id in (guild.owner_id, moderator.id):
                return False
            if member.top_role >= moderator.top_role:
                return False
            if member.guild_permissions.administrator:
                return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def bannable(
        member: discord.Member, moderator: discord.Member, guild: discord.Guild
    ) -> bool:
        """
        Checks if a member can be banned.

        Args:
            member: The member to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the member can be banned, False otherwise
        """
        try:
            if not moderator.guild_permissions.ban_members:
                return False
            if member.id in (guild.owner_id, moderator.id):
                return False
            if member.top_role >= moderator.top_role:
                return False
            if member.guild_permissions.administrator:
                return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def mutable(
        member: discord.Member, moderator: discord.Member, guild: discord.Guild
    ) -> bool:
        """
        Checks if a member can be put in timeout.

        Args:
            member: The member to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the member can be timed out, False otherwise
        """
        try:
            if not moderator.guild_permissions.moderate_members:
                return False
            if member.id in (guild.owner_id, moderator.id):
                return False
            if member.top_role >= moderator.top_role:
                return False
            if member.guild_permissions.administrator:
                return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def manageable(
        member: discord.Member, moderator: discord.Member, guild: discord.Guild
    ) -> bool:
        """
        Checks if a member is manageable (e.g., nickname changes).

        Args:
            member: The member to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the member can be managed, False otherwise
        """
        try:
            if not moderator.guild_permissions.manage_nicknames:
                return False
            if member.id in (guild.owner_id, moderator.id):
                return False
            if member.top_role >= moderator.top_role:
                return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def deletable(
        channel: Union[
            discord.TextChannel,
            discord.VoiceChannel,
            discord.CategoryChannel,
            discord.Thread,
        ],
        moderator: discord.Member,
        guild: discord.Guild,
    ) -> bool:
        """
        Checks if a channel can be deleted.

        Args:
            channel: The channel to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the channel can be deleted, False otherwise
        """
        try:
            if not moderator.guild_permissions.manage_channels:
                return False
            if hasattr(channel, "permissions_for"):
                perms = channel.permissions_for(moderator)
                if not perms.manage_channels:
                    return False
            if isinstance(channel, discord.Thread):
                if not moderator.guild_permissions.manage_threads:
                    return False
                if channel.owner_id == moderator.id:
                    return True
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def editable(
        channel: Union[
            discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel
        ],
        moderator: discord.Member,
        guild: discord.Guild,
    ) -> bool:
        """
        Checks if a channel is editable (change name, permissions).

        Args:
            channel: The channel to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the channel can be edited, False otherwise
        """
        try:
            if not moderator.guild_permissions.manage_channels:
                return False
            perms = channel.permissions_for(moderator)
            return perms.manage_channels
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def message_deletable(
        message: discord.Message,
        moderator: discord.Member,
        guild: discord.Guild,
    ) -> bool:
        """
        Checks if a message can be deleted.

        Args:
            message: The message to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the message can be deleted, False otherwise
        """
        try:
            if message.author.id == moderator.id:
                return True
            if not moderator.guild_permissions.manage_messages:
                return False
            if not message.channel.permissions_for(moderator).manage_messages:
                return False
            if isinstance(message.author, discord.Member):
                if message.author.id == guild.owner_id:
                    return False
                if message.author.top_role >= moderator.top_role:
                    return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def role_deletable(
        role: discord.Role, moderator: discord.Member, guild: discord.Guild
    ) -> bool:
        """
        Checks if a role can be deleted.

        Args:
            role: The role to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the role can be deleted, False otherwise
        """
        try:
            if not moderator.guild_permissions.manage_roles:
                return False
            if role >= moderator.top_role:
                return False
            if (
                role.is_default()
                or role.is_bot_managed()
                or role.is_premium_subscriber()
            ):
                return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def role_editable(
        role: discord.Role, moderator: discord.Member, guild: discord.Guild
    ) -> bool:
        """
        Checks if a role can be edited.

        Args:
            role: The role to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the role can be edited, False otherwise
        """
        try:
            if not moderator.guild_permissions.manage_roles:
                return False
            if role >= moderator.top_role:
                return False
            if role.is_default():
                return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def role_assignable(
        role: discord.Role, moderator: discord.Member, guild: discord.Guild
    ) -> bool:
        """
        Checks if a role can be assigned.

        Args:
            role: The role to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the role can be assigned, False otherwise
        """
        try:
            if not moderator.guild_permissions.manage_roles:
                return False
            if role >= moderator.top_role:
                return False
            if (
                role.is_default()
                or role.is_bot_managed()
                or role.is_premium_subscriber()
            ):
                return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def emoji_manageable(
        emoji: discord.Emoji, moderator: discord.Member, guild: discord.Guild
    ) -> bool:
        """
        Checks if an emoji is manageable/deletable.

        Args:
            emoji: The emoji to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the emoji can be managed, False otherwise
        """
        try:
            return (
                moderator.guild_permissions.manage_emojis_and_stickers
                and emoji.guild_id == guild.id
            )
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def sticker_manageable(
        sticker: discord.GuildSticker,
        moderator: discord.Member,
        guild: discord.Guild,
    ) -> bool:
        """
        Checks if a sticker is manageable.

        Args:
            sticker: The sticker to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the sticker can be managed, False otherwise
        """
        try:
            return (
                moderator.guild_permissions.manage_emojis_and_stickers
                and sticker.guild_id == guild.id
            )
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def webhook_manageable(
        webhook: discord.Webhook,
        moderator: discord.Member,
        guild: discord.Guild,
        channel: Optional[Union[discord.TextChannel, discord.Thread]] = None,
    ) -> bool:
        """
        Checks if a webhook is manageable.

        Args:
            webhook: The webhook to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place
            channel: Optional channel to check specific permissions

        Returns:
            bool: True if the webhook can be managed, False otherwise
        """
        try:
            if not moderator.guild_permissions.manage_webhooks:
                return False
            if channel:
                if not channel.permissions_for(moderator).manage_webhooks:
                    return False
            return webhook.guild_id == guild.id
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def invite_manageable(
        invite: discord.Invite, moderator: discord.Member, guild: discord.Guild
    ) -> bool:
        """
        Checks if an invite can be deleted.

        Args:
            invite: The invite to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the invite can be deleted, False otherwise
        """
        try:
            if not moderator.guild_permissions.manage_guild:
                return False
            if invite.guild and invite.guild.id != guild.id:
                return False
            if invite.inviter and isinstance(invite.inviter, discord.Member):
                if (
                    invite.inviter.top_role >= moderator.top_role
                    and invite.inviter.id != moderator.id
                ):
                    return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def voice_manageable(
        member: discord.Member,
        moderator: discord.Member,
        guild: discord.Guild,
        voice_channel: Optional[discord.VoiceChannel] = None,
    ) -> bool:
        """
        Checks if a member can be moved in a voice channel.

        Args:
            member: The member to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place
            voice_channel: Optional voice channel to check specific permissions

        Returns:
            bool: True if the member can be moved, False otherwise
        """
        try:
            if member.id in (guild.owner_id, moderator.id):
                return False
            if member.top_role >= moderator.top_role:
                return False
            if member.guild_permissions.administrator:
                return False
            if not moderator.guild_permissions.move_members:
                return False
            if voice_channel:
                if not voice_channel.permissions_for(moderator).move_members:
                    return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def voice_mutable(
        member: discord.Member,
        moderator: discord.Member,
        guild: discord.Guild,
        voice_channel: Optional[discord.VoiceChannel] = None,
    ) -> bool:
        """
        Checks if a member can be voice muted.

        Args:
            member: The member to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place
            voice_channel: Optional voice channel to check specific permissions

        Returns:
            bool: True if the member can be voice muted, False otherwise
        """
        try:
            if member.id in (guild.owner_id, moderator.id):
                return False
            if member.top_role >= moderator.top_role:
                return False
            if member.guild_permissions.administrator:
                return False
            if not moderator.guild_permissions.mute_members:
                return False
            if voice_channel:
                if not voice_channel.permissions_for(moderator).mute_members:
                    return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def voice_deafenable(
        member: discord.Member,
        moderator: discord.Member,
        guild: discord.Guild,
        voice_channel: Optional[discord.VoiceChannel] = None,
    ) -> bool:
        """
        Checks if a member can be voice deafened.

        Args:
            member: The member to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place
            voice_channel: Optional voice channel to check specific permissions

        Returns:
            bool: True if the member can be voice deafened, False otherwise
        """
        try:
            if member.id in (guild.owner_id, moderator.id):
                return False
            if member.top_role >= moderator.top_role:
                return False
            if member.guild_permissions.administrator:
                return False
            if not moderator.guild_permissions.deafen_members:
                return False
            if voice_channel:
                if not voice_channel.permissions_for(moderator).deafen_members:
                    return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def thread_manageable(
        thread: discord.Thread, moderator: discord.Member, guild: discord.Guild
    ) -> bool:
        """
        Checks if a thread is manageable.

        Args:
            thread: The thread to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the thread can be managed, False otherwise
        """
        try:
            if thread.owner_id == moderator.id:
                return True
            if not moderator.guild_permissions.manage_threads:
                return False
            if thread.parent:
                if not thread.parent.permissions_for(moderator).manage_threads:
                    return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def event_manageable(
        event: discord.ScheduledEvent,
        moderator: discord.Member,
        guild: discord.Guild,
    ) -> bool:
        """
        Checks if a scheduled event is manageable.

        Args:
            event: The scheduled event to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the event can be managed, False otherwise
        """
        try:
            if not moderator.guild_permissions.manage_events:
                return False
            if event.creator_id == moderator.id:
                return True
            if event.creator and isinstance(event.creator, discord.Member):
                if event.creator.top_role >= moderator.top_role:
                    return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def stage_manageable(
        stage: discord.StageChannel,
        moderator: discord.Member,
        guild: discord.Guild,
    ) -> bool:
        """
        Checks if a stage channel is manageable.

        Args:
            stage: The stage channel to check
            moderator: The moderator attempting the action
            guild: The guild where the action takes place

        Returns:
            bool: True if the stage channel can be managed, False otherwise
        """
        try:
            if not moderator.guild_permissions.manage_channels:
                return False
            if not stage.permissions_for(moderator).manage_channels:
                return False
            return True
        except (AttributeError, discord.HTTPException):
            return False

    @staticmethod
    def stage_speakable(
        member: discord.Member,
        moderator: discord.Member,
        stage: discord.StageChannel,
    ) -> bool:
        """
        Checks if a member can speak in a stage channel.

        Args:
            member: The member to check
            moderator: The moderator attempting the action
            stage: The stage channel where the action takes place

        Returns:
            bool: True if the member can be allowed to speak, False otherwise
        """
        try:
            perms = stage.permissions_for(moderator)
            if not perms.mute_members:
                return False
            if member.id == moderator.id:
                return False
            if member.top_role >= moderator.top_role:
                return False
            return True
        except (AttributeError, discord.HTTPException):
            return False
