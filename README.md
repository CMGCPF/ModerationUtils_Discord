# ModerationUtils Documentation

The `ModerationUtils` class is a static utility class used to validate whether a Discord moderator can perform moderation actions on other members, channels, roles, etc. Each method performs a permission and hierarchy check and is meant to be used before attempting the actual Discord API action (like banning or moving a user).

---

## 📌 General Principles

* All methods are static and can be called directly using `ModerationUtils.method()`.
* They return a `bool`: `True` if the action is allowed, `False` otherwise.
* Methods include `try/except` safety guards against missing data (e.g., if a user has left the server).

---

## 🔐 Member-related Checks

### `bot_verified(user)`

Checks if a given user is a verified bot.

### `kickable(member, moderator, guild)`

Checks if a moderator can kick a member from the guild.

### `bannable(member, moderator, guild)`

Checks if a moderator can ban a member from the guild.

### `mutable(member, moderator, guild)`

Checks if a moderator can timeout (mute) a member.

### `manageable(member, moderator, guild)`

Checks if a moderator can manage a member (e.g., change nickname).

---

## 🧵 Thread & Channel Permissions

### `deletable(channel, moderator, guild)`

Checks if a moderator can delete a text/voice/category/thread channel.

### `editable(channel, moderator, guild)`

Checks if a moderator can edit a text/voice/category channel.

### `message_deletable(message, moderator, guild)`

Checks if a moderator can delete a specific message.

---

## 🔧 Role-related Permissions

### `role_deletable(role, moderator, guild)`

Checks if a moderator can delete a given role.

### `role_editable(role, moderator, guild)`

Checks if a moderator can edit a given role.

### `role_assignable(role, moderator, guild)`

Checks if a moderator can assign a given role.

---

## 🎨 Emoji & Sticker Permissions

### `emoji_manageable(emoji, moderator, guild)`

Checks if a moderator can manage a given emoji.

### `sticker_manageable(sticker, moderator, guild)`

Checks if a moderator can manage a given sticker.

---

## 🧷 Webhooks, Invites, and Events

### `webhook_manageable(webhook, moderator, guild, channel=None)`

Checks if a moderator can manage a webhook.

### `invite_manageable(invite, moderator, guild)`

Checks if a moderator can revoke/delete an invite.

### `event_manageable(event, moderator, guild)`

Checks if a moderator can manage a scheduled event.

---

## 🔊 Voice Channel Controls

### `voice_manageable(member, moderator, guild, voice_channel=None)`

Checks if a moderator can move a member in a voice channel.

### `voice_mutable(member, moderator, guild, voice_channel=None)`

Checks if a moderator can mute a member in a voice channel.

### `voice_deafenable(member, moderator, guild, voice_channel=None)`

Checks if a moderator can deafen a member in a voice channel.

---

## 🧵 Thread & Stage Controls

### `thread_manageable(thread, moderator, guild)`

Checks if a moderator can manage a thread.

### `stage_manageable(stage, moderator, guild)`

Checks if a moderator can manage a stage channel.

### `stage_speakable(member, moderator, stage)`

Checks if a moderator can allow/prevent a user from speaking in a stage.

---

## ✅ Usage Example

```python
if ModerationUtils.kickable(target_member, moderator, guild):
    await target_member.kick(reason="Rule violation")
else:
    await ctx.send("You do not have permission to kick this member.")
```

---

## 🔄 Suggestions

* Always call these checks before performing moderation actions.
* Handles Discord hierarchy (role comparisons) and ownership checks safely.
* Prevents exceptions when members or roles are missing or deleted.
